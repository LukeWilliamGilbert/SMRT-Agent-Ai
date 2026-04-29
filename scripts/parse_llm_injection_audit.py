#!/usr/bin/env python3.11
"""Parse raw MCP/Supabase LLM injection audit output into clean JSON and Markdown findings."""
from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
RAW = ROOT / 'data/supabase/llm_injection_audit_raw.json'
CLEAN = ROOT / 'data/supabase/llm_injection_audit_clean.json'
MD = ROOT / 'docs/system/llm_injection_audit_findings.md'


def extract_payload(raw_text: str):
    outer = raw_text.strip()
    try:
        outer_obj = json.loads(outer.split('Tool execution result:', 1)[-1].strip())
        result = outer_obj.get('result', outer)
    except Exception:
        result = outer
    # Choose the marker whose opening tag is followed by JSON payload.
    matches = list(re.finditer(r'<untrusted-data-[^>]+>', result))
    for m in matches:
        after = result[m.end():].lstrip()
        if after.startswith('[') or after.startswith('{'):
            close = result.find('</untrusted-data-', m.end())
            if close != -1:
                payload_text = result[m.end():close].strip()
                payload = json.loads(payload_text)
                if isinstance(payload, list) and payload and 'llm_injection_audit' in payload[0]:
                    return payload[0]['llm_injection_audit']
                return payload
    raise ValueError('Could not locate JSON payload inside untrusted-data markers')


def bullet_rows(rows, fields, limit=10):
    out = []
    for row in rows[:limit]:
        parts = []
        for f in fields:
            val = row.get(f)
            if isinstance(val, str):
                val = val.replace('\n', ' ')[:180]
            parts.append(f"{f}={val}")
        out.append('- ' + '; '.join(parts))
    if len(rows) > limit:
        out.append(f'- … {len(rows) - limit} additional rows omitted from Markdown; see clean JSON evidence.')
    return '\n'.join(out) if out else '- None found.'


def main() -> None:
    audit = extract_payload(RAW.read_text())
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    CLEAN.write_text(json.dumps(audit, indent=2, sort_keys=True) + '\n')

    counts = audit.get('counts', {})
    prompt_blocks = audit.get('prompt_block_summary', []) or []
    static_summary = audit.get('static_section_summary', []) or []
    static_samples = audit.get('static_sections_sample', []) or []
    defaults = audit.get('system_default_prompt_state', []) or []
    agents = audit.get('agent_prompt_state', []) or []
    agent_static = audit.get('agent_location_static_health', []) or []
    context_rows = audit.get('recent_context_health', []) or []
    dupes = audit.get('duplicate_prompt_blocks', []) or []
    errors = audit.get('ai_error_summary', {}) or {}

    active_static = counts.get('active_static_prompt_sections', 0)
    total_static = counts.get('static_prompt_sections', 0)
    inactive_static = max(total_static - active_static, 0) if isinstance(total_static, int) and isinstance(active_static, int) else 'unknown'
    zero_summary_contexts = [r for r in context_rows if (r.get('conversation_summary_length') or 0) == 0 and (r.get('summary_length') or 0) == 0]
    tiny_summary_contexts = [r for r in context_rows if (r.get('conversation_summary_length') or 0) <= 4 and (r.get('summary_length') or 0) == 0]
    custom_personality_disabled = [a for a in agents if not a.get('use_custom_personality') and (a.get('personality_prompt_length') or 0) == 0]
    default_lengths = [d.get('value_length') for d in defaults if isinstance(d.get('value_length'), int)]
    context_lengths = [r.get('conversation_summary_length') for r in context_rows if isinstance(r.get('conversation_summary_length'), int)]

    lines = []
    lines.append('# LLM Injection Audit Findings')
    lines.append('')
    lines.append('This document summarizes a read-only audit of the SMRT LLM injection path, focusing on prompt-feeding records, static prompt sections, agent prompt state, conversation context availability, and output-error evidence. It does not modify production data or workflow behavior.')
    lines.append('')
    lines.append('## Executive Findings')
    lines.append('')
    lines.append('| Finding | Evidence | Impact |')
    lines.append('|---|---:|---|')
    lines.append(f"| Prompt block library is present and active | {counts.get('active_prompt_blocks')} active of {counts.get('prompt_blocks')} prompt blocks | The dynamic prompt-block layer appears populated rather than empty. |")
    lines.append(f"| Static prompt library is partly disabled | {active_static} active of {total_static} static sections; {inactive_static} inactive | If workflow expects all old sections, only a subset is being injected. If the new 7-section design is intentional, this is a configuration contract that needs to be documented. |")
    lines.append(f"| Agent-level custom personality is not feeding injection | {len(custom_personality_disabled)} active agent row(s) have custom personality disabled and empty personality_prompt | The workflow may rely on static prompt sections/defaults instead of agent.personality_prompt; this can look like partial injection if people expect the agent row to drive voice. |")
    lines.append(f"| Conversation context is inconsistent | {len(zero_summary_contexts)} of {len(context_rows)} sampled recent contexts have no summary fields; {len(tiny_summary_contexts)} have near-empty summaries | The LLM may receive thin or missing memory/context even when the base prompt is intact. |")
    lines.append(f"| Prompt/output error surface exists but is small | {errors.get('total_errors')} ai_output_errors; {errors.get('likely_prompt_leaks')} likely prompt leaks | Error logging exists, but it probably does not yet prove whether individual prompt fragments reached the model. |")
    lines.append('')
    lines.append('## Prompt Block Health')
    lines.append('')
    lines.append('| Category | Total | Active | Inactive | Empty Content | Priority Range |')
    lines.append('|---|---:|---:|---:|---:|---|')
    for r in prompt_blocks:
        lines.append(f"| {r.get('category')} | {r.get('total')} | {r.get('active')} | {r.get('inactive')} | {r.get('empty_content')} | {r.get('min_priority')}–{r.get('max_priority')} |")
    lines.append('')
    lines.append('Duplicate/ambiguous prompt-block IDs:')
    lines.append('')
    lines.append(bullet_rows(dupes, ['block_id', 'row_count', 'active_count'], limit=12))
    lines.append('')
    lines.append('## Static Prompt Section Health')
    lines.append('')
    lines.append('| Location ID | Total | Active | Inactive | Empty Content | Sort Range |')
    lines.append('|---|---:|---:|---:|---:|---|')
    for r in static_summary:
        lines.append(f"| {r.get('location_id')} | {r.get('total')} | {r.get('active')} | {r.get('inactive')} | {r.get('empty_content')} | {r.get('min_sort_order')}–{r.get('max_sort_order')} |")
    lines.append('')
    lines.append('Active/inactive static-section samples show both a newer all-caps prompt set and older markdown-headed sections in the same location. This is not automatically wrong, but it is a likely source of confusion about which prompt surface is live.')
    lines.append('')
    lines.append(bullet_rows(static_samples, ['section_key', 'heading', 'is_active', 'sort_order', 'content_length'], limit=20))
    lines.append('')
    lines.append('## System Defaults and Agent Prompt State')
    lines.append('')
    lines.append(f"System-default prompt-like rows found: {len(defaults)}. Mean default value length: {round(mean(default_lengths), 1) if default_lengths else 'n/a'} characters.")
    lines.append('')
    lines.append(bullet_rows(defaults, ['key', 'value_length', 'description'], limit=20))
    lines.append('')
    lines.append('Agent prompt state:')
    lines.append('')
    lines.append(bullet_rows(agents, ['location_id', 'agent_name', 'active', 'use_custom_personality', 'personality_prompt_length', 'agent_notes_length', 'coordinator_name', 'has_calendar_id', 'has_ghl_user_id'], limit=20))
    lines.append('')
    lines.append('Agent-to-static-section health:')
    lines.append('')
    lines.append(bullet_rows(agent_static, ['location_id', 'agent_name', 'active', 'active_static_sections', 'empty_static_sections'], limit=20))
    lines.append('')
    lines.append('## Conversation Context Injection Risk')
    lines.append('')
    lines.append(f"The sampled recent conversation contexts have an average conversation_summary length of {round(mean(context_lengths), 1) if context_lengths else 'n/a'} characters, but several records have empty or near-empty summary fields. This points to a context/memory injection risk rather than only a base-prompt risk.")
    lines.append('')
    lines.append(bullet_rows(context_rows, ['contact_id', 'lead_intent', 'lead_timeline', 'appointment_offered', 'appointment_booked', 'conversation_summary_length', 'summary_length', 'updated_at'], limit=20))
    lines.append('')
    lines.append('## Preliminary Defect Hypotheses')
    lines.append('')
    lines.append('| ID | Hypothesis | Evidence | Severity | Next Validation |')
    lines.append('|---|---|---|---|---|')
    lines.append('| LLM-001 | The live system prompt may be assembled from static_prompt_sections and prompt_blocks, while agent.personality_prompt is not used. | Active agent has use_custom_personality=false and personality_prompt_length=0. | Medium | Confirm exact workflow expression mapping into the AI Agent systemMessage and test with a known marker in a non-production prompt section. |')
    lines.append('| LLM-002 | Prompt injection may be partially intentional because only 7 of 26 static sections are active, but this contract is undocumented. | 19 inactive static sections coexist with 7 active sections. | High | Define the canonical active prompt-section set and remove/deprecate or label inactive historical sections. |')
    lines.append('| LLM-003 | Context injection is unreliable for some conversations because memory summaries are empty or near-empty. | Recent context sample includes empty and 4-character summaries. | High | Trace the context builder and context update nodes against message_log/inbound_capture for those contact IDs. |')
    lines.append('| LLM-004 | Current error logging does not capture prompt-fragment inclusion/exclusion. | ai_output_errors has only 4 rows and no prompt-leak markers. | Medium | Add non-sensitive prompt assembly telemetry: section keys included, block IDs included, context length, model input length, and fallback flags. |')
    lines.append('| LLM-005 | Duplicate or overlapping prompt surfaces may make the developer and operators misdiagnose behavior. | Static prompt samples include old markdown section headings and newer canonical headings in one location. | Medium | Create a prompt registry document and enforce status labels: live, deprecated, experimental. |')
    lines.append('')
    lines.append('## Evidence Files')
    lines.append('')
    lines.append('- Clean structured evidence: `data/supabase/llm_injection_audit_clean.json`')
    lines.append('- Raw read-only query result: `data/supabase/llm_injection_audit_raw.json`')
    lines.append('- Prompt schema columns: `data/supabase/prompt_schema_columns.txt`')
    lines.append('- Workflow-side map: `docs/system/llm_injection_workflow_map.md`')
    lines.append('- Focused Brain Engine chain: `docs/system/brain_engine_llm_chain.md`')
    lines.append('- Full prompt assembly evidence: `docs/system/brain_engine_prompt_assembly_full.md`')
    lines.append('')

    MD.parent.mkdir(parents=True, exist_ok=True)
    MD.write_text('\n'.join(lines) + '\n')
    print(CLEAN)
    print(MD)


if __name__ == '__main__':
    main()
