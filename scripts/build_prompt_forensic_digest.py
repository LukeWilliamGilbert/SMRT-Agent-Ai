#!/usr/bin/env python3
"""Build concise forensic digest of prompt assembly, summary node, and tool load from redacted raw extract."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
SRC = ROOT / 'data/workflows/raw_prompt_summary_surfaces_redacted.json'
OUT = ROOT / 'docs/system/prompt_system_forensic_digest.md'


def one_line(s: str, n: int = 220) -> str:
    s = re.sub(r'\s+', ' ', str(s)).strip()
    return s[:n] + ('…' if len(s) > n else '')


def find_node(data, name):
    for node in data['nodes']:
        if node['name'] == name:
            return node
    return None


def field(node, contains):
    if not node:
        return None
    for f in node['fields']:
        if contains.lower() in f['path'].lower():
            return f
    return None


def fields_matching(node, pattern):
    rx = re.compile(pattern, re.I)
    return [f for f in (node or {}).get('fields', []) if rx.search(f['path']) or rx.search(str(f.get('value', '')))]


def extract_code_facts(js: str):
    facts = []
    order_match = re.search(r'const systemPrompt = ([^;]+);', js)
    if order_match:
        facts.append(('Final assembly order', order_match.group(1)))
    for term in ['messageHistoryBlock', 'summaryBlock', 'personalityBlock', 'agentNotesBlock', 'starvationDirective', 'toolConfig']:
        m = re.search(r'const ' + re.escape(term) + r'\s*=\s*([^;]+);', js)
        if m:
            facts.append((term, m.group(1)))
    m = re.search(r'LIMIT\s+15', js)
    return facts


def main():
    data = json.loads(SRC.read_text())
    tool_names = data.get('connections_ai_tool_to_agent', [])
    tool_nodes = [find_node(data, name) for name in tool_names]
    desc_rows = []
    for n in tool_nodes:
        if not n:
            continue
        desc = next((f for f in n['fields'] if 'description' in f['path'].lower()), None)
        desc_rows.append({
            'name': n['name'],
            'type': n['type'],
            'chars': desc['length'] if desc else 0,
            'mandatory': bool(desc and re.search(r'\b(MUST|MANDATORY|ALWAYS|CRITICAL)\b', str(desc['value']), re.I)),
            'when_to_use': bool(desc and re.search(r'WHEN TO USE', str(desc['value']), re.I)),
            'when_not_to_use': bool(desc and re.search(r'WHEN NOT TO USE', str(desc['value']), re.I)),
            'excerpt': one_line(desc['value'] if desc else '', 260),
        })
    desc_rows.sort(key=lambda r: r['name'].lower())

    assemble = find_node(data, 'Assemble System Prompt')
    js = field(assemble, 'jsCode')['value']
    analyze = find_node(data, 'Analyze Conversation')
    analyze_fields = [f for f in analyze['fields'] if 'content' in f['path'].lower()] if analyze else []
    get_hist = find_node(data, 'Get Message History')
    get_out_hist = find_node(data, 'Get Outbound Message History')
    get_summary = find_node(data, 'Get Conversation Summary')
    update_ctx = find_node(data, 'Update Conversation Context')
    insert_ctx = find_node(data, 'Insert Conversation Context')

    lines = []
    lines.append('# SMRT Prompt-System Forensic Digest')
    lines.append('')
    lines.append('Author: **Manus AI**')
    lines.append('')
    lines.append('Status: **Static, read-only forensic digest from redacted workflow export. No production changes were made.**')
    lines.append('')
    lines.append('## High-Signal Mechanical Facts')
    lines.append('')
    lines.append('| Finding | Evidence |')
    lines.append('|---|---|')
    lines.append(f"| Workflow size | `{data['workflow']['node_count']}` nodes in active `SMRT Brain Engine`. |")
    lines.append(f"| Direct tool fan-out | `{len(tool_names)}` tools connected directly into the final `AI Agent`. |")
    lines.append("| Final agent input | `AI Agent` reads `systemPrompt` as system message and `userMessage` as text input. |")
    lines.append("| Recent verbatim history | Inbound path queries `message_log` ordered descending with `LIMIT 15`. |")
    lines.append("| Summary source | `Get Conversation Summary` reads `conversation_context`; summary text is assembled as evidence in `summaryBlock`. |")
    lines.append("| Summary writer | `Analyze Conversation` creates JSON for `conversation_summary`, `lead_intent`, `key_topics`, `detected_intents`, `appointment_state`, and `qualifying_answers`; `Update/Insert Conversation Context` persists it. |")
    lines.append('')
    lines.append('## Final Prompt Assembly Order')
    lines.append('')
    for label, val in extract_code_facts(js):
        lines.append(f'| {label} | `{one_line(val, 500)}` |')
    lines.append('')
    lines.append('The notable ordering is that **summary and recent messages are injected before personality, while static behavior sections are appended last after `## BEHAVIOR`**. That does not prove failure by itself, but it means later static sections may carry disproportionate authority relative to earlier personality or memory material.')
    lines.append('')
    lines.append('## Tool Load Attached To Communicating Agent')
    lines.append('')
    lines.append('| Tool | Type | Description chars | Mandatory language | When-to-use | When-not-to-use |')
    lines.append('|---|---|---:|---|---|---|')
    for r in desc_rows:
        lines.append(f"| `{r['name']}` | `{r['type']}` | {r['chars']} | {r['mandatory']} | {r['when_to_use']} | {r['when_not_to_use']} |")
    lines.append('')
    lines.append('## Tool Description Excerpts')
    lines.append('')
    for r in desc_rows:
        lines.append(f"### `{r['name']}`")
        lines.append('')
        lines.append(f"> {r['excerpt'] or '(none found)'}")
        lines.append('')
    lines.append('## Summary Node Prompt Surface')
    lines.append('')
    if analyze_fields:
        lines.append('| Analyze Conversation field | Chars | Excerpt |')
        lines.append('|---|---:|---|')
        for f in analyze_fields:
            lines.append(f"| `{f['path']}` | {f['length']} | {one_line(f['value'], 420)} |")
    lines.append('')
    lines.append('## Summary Persistence Surfaces')
    lines.append('')
    for node in [get_summary, update_ctx, insert_ctx, get_hist, get_out_hist]:
        if not node:
            continue
        lines.append(f"### `{node['name']}`")
        lines.append('')
        lines.append('| Field | Chars | Value |')
        lines.append('|---|---:|---|')
        for f in node['fields'][:18]:
            lines.append(f"| `{f['path']}` | {f['length']} | `{one_line(f['value'], 360)}` |")
        lines.append('')
    lines.append('## Preliminary Interpretation')
    lines.append('')
    lines.append('The evidence supports the user’s concern: this is not simply a “bad prompt wording” problem. The communicating agent is expected to simultaneously decide conversational tone, remember relationship context, select among many operational tools, obey several mandatory tool directives, preserve appointment and CRM state, and produce the customer-facing response. That creates a high per-turn instruction burden and exposes the final response model to many operational choices that could be routed before the final communicating step.')
    lines.append('')
    lines.append('The existing `conversation_context` summary path is valuable and should be treated as a focal point rather than bypassed. If the summary node and table are tightened, the final communicating agent should not need full conversation-strand strips except on explicit retrieval. A better architecture would feed the final responder a compact state packet containing durable lead facts, current summary, open loops, unresolved commitments, recent turns, and only the tool outputs needed for this turn.')
    lines.append('')
    OUT.write_text('\n'.join(lines) + '\n')
    print(OUT)

if __name__ == '__main__':
    main()
