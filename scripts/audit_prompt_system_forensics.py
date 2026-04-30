#!/usr/bin/env python3
"""Static, read-only forensic audit of SMRT Brain Engine prompt, tool, and summary surfaces."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF = ROOT / 'workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json'
OUT_DIR = ROOT / 'data/workflows'
DOC_DIR = ROOT / 'docs/system'
OUT_DIR.mkdir(parents=True, exist_ok=True)
DOC_DIR.mkdir(parents=True, exist_ok=True)

TOOL_TYPES = {
    '@n8n/n8n-nodes-langchain.toolCode',
    '@n8n/n8n-nodes-langchain.toolHttpRequest',
    '@n8n/n8n-nodes-langchain.toolVectorStore',
    'n8n-nodes-base.supabaseTool',
}
LLM_TYPES = {
    '@n8n/n8n-nodes-langchain.agent',
    '@n8n/n8n-nodes-langchain.openAi',
    '@n8n/n8n-nodes-langchain.anthropic',
    '@n8n/n8n-nodes-langchain.lmChatAnthropic',
    '@n8n/n8n-nodes-langchain.lmChatOpenAi',
}


def flatten(obj: Any, prefix: str = ''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f'{prefix}.{k}' if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f'{prefix}[{i}]')
    else:
        yield prefix, obj


def text_len(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    return len(json.dumps(value, ensure_ascii=False))


def trunc(s: Any, n: int = 500) -> str:
    if s is None:
        return ''
    s = str(s).replace('\n', ' ').strip()
    return s[:n] + ('…' if len(s) > n else '')


def extract_textish(params: dict) -> list[tuple[str, str]]:
    out = []
    for path, value in flatten(params):
        if isinstance(value, str) and any(k in path.lower() for k in ['description', 'prompt', 'message', 'content', 'query', 'jscode', 'schemaexample']):
            out.append((path, value))
    return out


def main():
    wf = json.loads(WF.read_text())
    nodes = {n.get('name'): n for n in wf.get('nodes', [])}
    conns = wf.get('connections', {})

    ai_agent = nodes.get('AI Agent')
    ai_agent_connected_tools = []
    for src, ports in conns.items():
        for channel, groups in (ports or {}).items():
            if channel != 'ai_tool':
                continue
            for group in groups or []:
                for edge in group or []:
                    if edge.get('node') == 'AI Agent':
                        node = nodes.get(src, {})
                        params = node.get('parameters', {})
                        tool_desc = params.get('toolDescription') or params.get('description') or ''
                        ai_agent_connected_tools.append({
                            'name': src,
                            'type': node.get('type'),
                            'description_length': len(tool_desc),
                            'description_excerpt': trunc(tool_desc, 900),
                            'has_when_to_use': 'WHEN TO USE' in tool_desc.upper(),
                            'has_when_not_to_use': 'WHEN NOT TO USE' in tool_desc.upper(),
                            'has_mandatory_language': bool(re.search(r'\bMUST\b|\bMANDATORY\b|\bALWAYS\b|\bCRITICAL\b', tool_desc, re.I)),
                        })

    tool_nodes = []
    for n in wf.get('nodes', []):
        if n.get('type') in TOOL_TYPES:
            params = n.get('parameters', {})
            desc = params.get('toolDescription') or params.get('description') or ''
            tool_nodes.append({
                'name': n.get('name'),
                'type': n.get('type'),
                'connected_to_ai_agent': any(t['name'] == n.get('name') for t in ai_agent_connected_tools),
                'description_length': len(desc),
                'description_excerpt': trunc(desc, 700),
            })

    summary_nodes = []
    summary_pat = re.compile(r'summary|summar|conversation_context|conversation summary|Analyze Conversation|Update Conversation Context|Summary Exists', re.I)
    for n in wf.get('nodes', []):
        params = n.get('parameters', {})
        params_text = json.dumps(params, ensure_ascii=False)
        if summary_pat.search(n.get('name', '')) or summary_pat.search(params_text):
            textish = extract_textish(params)
            summary_nodes.append({
                'name': n.get('name'),
                'type': n.get('type'),
                'textish_fields': [
                    {'path': p, 'length': len(v), 'excerpt': trunc(v, 600)} for p, v in textish[:12]
                ],
                'total_textish_length': sum(len(v) for _, v in textish),
                'mentions_conversation_context': 'conversation_context' in params_text,
                'mentions_conversation_summary': 'conversation_summary' in params_text,
            })

    ai_agent_params = ai_agent.get('parameters', {}) if ai_agent else {}
    prompt_surfaces = []
    prompt_names = ['Assemble System Prompt', 'Gather Prompt Data', 'Get Prompt Blocks (SMRT)', 'Get Static Prompt Sections', 'Get Conversation Summary', 'Get Outbound Conversation Summary', 'Get Message History', 'Get Outbound Message History', 'Analyze Conversation', 'Update Conversation Context', 'Insert Conversation Context']
    for name in prompt_names:
        n = nodes.get(name)
        if not n:
            continue
        textish = extract_textish(n.get('parameters', {}))
        prompt_surfaces.append({
            'name': name,
            'type': n.get('type'),
            'textish_total_length': sum(len(v) for _, v in textish),
            'key_fields': [{'path': p, 'length': len(v), 'excerpt': trunc(v, 700)} for p, v in textish[:10]],
        })

    # Estimate per-turn instruction burden from static tool descriptions and the system prompt pointer.
    total_connected_tool_desc_len = sum(t['description_length'] for t in ai_agent_connected_tools)
    mandatory_tool_count = sum(1 for t in ai_agent_connected_tools if t['has_mandatory_language'])
    tool_type_counts = Counter(t['type'] for t in ai_agent_connected_tools)

    result = {
        'workflow': {'name': wf.get('name'), 'active': wf.get('active'), 'node_count': len(wf.get('nodes', []))},
        'ai_agent': {
            'present': ai_agent is not None,
            'type': ai_agent.get('type') if ai_agent else None,
            'system_message': ai_agent_params.get('options', {}).get('systemMessage') if ai_agent else None,
            'text_expression': ai_agent_params.get('text') if ai_agent else None,
            'max_iterations': ai_agent_params.get('options', {}).get('maxIterations') if ai_agent else None,
        },
        'summary': {
            'tool_nodes_total': len(tool_nodes),
            'ai_agent_connected_tool_count': len(ai_agent_connected_tools),
            'connected_tool_description_chars': total_connected_tool_desc_len,
            'connected_tool_description_est_tokens': round(total_connected_tool_desc_len / 4),
            'mandatory_or_critical_connected_tools': mandatory_tool_count,
            'summary_related_node_count': len(summary_nodes),
            'tool_type_counts': dict(tool_type_counts),
        },
        'ai_agent_connected_tools': sorted(ai_agent_connected_tools, key=lambda x: x['name'].lower()),
        'all_tool_nodes': sorted(tool_nodes, key=lambda x: x['name'].lower()),
        'summary_nodes': sorted(summary_nodes, key=lambda x: x['name'].lower()),
        'prompt_surfaces': prompt_surfaces,
    }

    out_json = OUT_DIR / 'prompt_system_forensics.json'
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')

    lines = []
    lines.append('# SMRT Prompt System Forensics — Raw Static Evidence')
    lines.append('')
    lines.append('Author: **Manus AI**')
    lines.append('')
    lines.append('Status: **Static, read-only workflow evidence. No production changes were made.**')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append('| Metric | Value |')
    lines.append('|---|---:|')
    for k, v in result['summary'].items():
        lines.append(f'| `{k}` | {v} |')
    lines.append('')
    lines.append('## AI Agent Wiring')
    lines.append('')
    lines.append('| Field | Value |')
    lines.append('|---|---|')
    for k, v in result['ai_agent'].items():
        safe_v = str(v).replace('|', '\\|')
        lines.append(f'| `{k}` | `{safe_v}` |')
    lines.append('')
    lines.append('## Tools Connected Directly To AI Agent')
    lines.append('')
    lines.append('| Tool | Type | Description chars | Mandatory/critical language | When-to-use | When-not-to-use |')
    lines.append('|---|---|---:|---|---|---|')
    for t in result['ai_agent_connected_tools']:
        lines.append(f"| `{t['name']}` | `{t['type']}` | {t['description_length']} | {t['has_mandatory_language']} | {t['has_when_to_use']} | {t['has_when_not_to_use']} |")
    lines.append('')
    lines.append('## Connected Tool Description Excerpts')
    lines.append('')
    for t in result['ai_agent_connected_tools']:
        lines.append(f"### `{t['name']}`")
        lines.append('')
        lines.append(f"Type: `{t['type']}`. Description chars: **{t['description_length']}**.")
        lines.append('')
        lines.append('> ' + (t['description_excerpt'] or '(no description)').replace('\n', '\n> '))
        lines.append('')
    lines.append('## Summary and Memory Related Nodes')
    lines.append('')
    lines.append('| Node | Type | Text-like chars | Mentions `conversation_context` | Mentions `conversation_summary` |')
    lines.append('|---|---|---:|---|---|')
    for n in result['summary_nodes']:
        lines.append(f"| `{n['name']}` | `{n['type']}` | {n['total_textish_length']} | {n['mentions_conversation_context']} | {n['mentions_conversation_summary']} |")
    lines.append('')
    lines.append('## Prompt Surface Nodes')
    lines.append('')
    lines.append('| Node | Type | Text-like chars | High-signal fields |')
    lines.append('|---|---|---:|---|')
    for n in result['prompt_surfaces']:
        fields = '<br>'.join(f"`{f['path']}` ({f['length']})" for f in n['key_fields'][:6])
        lines.append(f"| `{n['name']}` | `{n['type']}` | {n['textish_total_length']} | {fields} |")
    lines.append('')

    out_md = DOC_DIR / 'prompt_system_forensics_raw_evidence.md'
    out_md.write_text('\n'.join(lines) + '\n')
    print(json.dumps(result['summary'], indent=2))
    print(out_json)
    print(out_md)


if __name__ == '__main__':
    main()
