#!/usr/bin/env python3
"""Extract non-credential prompt/tool/summary surfaces from raw n8n export with defensive redaction."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
RAW = Path('/home/ubuntu/smrt_analysis/raw_export/root/smrt_n8n_export_20260428_194357/workflows/smrt_workflows_all.json')
OUT = ROOT / 'data/workflows/raw_prompt_summary_surfaces_redacted.json'
OUT.parent.mkdir(parents=True, exist_ok=True)

TARGET_ID = 'mlR5dZuzXxP_JYGaqrqpu'
TARGET_NAME = 'SMRT Brain Engine'

SENSITIVE_PATTERNS = [
    (re.compile(r'Bearer\s+[A-Za-z0-9._\-]+', re.I), 'Bearer [REDACTED]'),
    (re.compile(r'(api[_-]?key|token|secret|password|authorization)(\s*[:=]\s*)([^\s,}]+)', re.I), r'\1\2[REDACTED]'),
    (re.compile(r'sk-[A-Za-z0-9_\-]{16,}'), 'sk-[REDACTED]'),
    (re.compile(r'eyJ[A-Za-z0-9_\-.]{30,}'), '[JWT_REDACTED]'),
]

INTERESTING_NODES = {
    'AI Agent', 'Assemble System Prompt', 'Gather Prompt Data', 'Get Prompt Blocks (SMRT)',
    'Get Static Prompt Sections', 'Get Conversation Summary', 'Get Outbound Conversation Summary',
    'Get Message History', 'Get Outbound Message History', 'Analyze Conversation',
    'Update Conversation Context', 'Insert Conversation Context', 'Summary Exists?',
    'KB Tool', 'getContact', 'getAppointments', 'getNotes', 'searchPastMessages',
    'checkQualificationStatus', 'saveQualifyingAnswer', 'updateContactMemory', 'switchChannel',
    'subscribeToNewsletter', 'getAvailableSlots', 'bookAppointment', 'rescheduleAppointment',
    'deleteAppointment', 'addAppointmentNotes'
}

INTERESTING_PATH_WORDS = [
    'description', 'toolDescription', 'prompt', 'systemMessage', 'text', 'message', 'content',
    'query', 'jsCode', 'schemaExample', 'operation', 'tableId', 'fieldsUi', 'columns'
]


def redact(s: str) -> str:
    for pat, repl in SENSITIVE_PATTERNS:
        s = pat.sub(repl, s)
    return s


def safe_value(v: Any) -> Any:
    if isinstance(v, str):
        return redact(v)
    if isinstance(v, (int, float, bool)) or v is None:
        return v
    return redact(json.dumps(v, ensure_ascii=False))


def flatten(obj: Any, prefix: str = ''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in {'credentials', 'credential', 'authentication'}:
                continue
            yield from flatten(v, f'{prefix}.{k}' if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f'{prefix}[{i}]')
    else:
        yield prefix, obj


def load_workflow():
    data = json.loads(RAW.read_text())
    workflows = data if isinstance(data, list) else data.get('workflows') or data.get('data') or []
    for wf in workflows:
        if wf.get('id') == TARGET_ID or wf.get('name') == TARGET_NAME or 'Brain Engine' in wf.get('name', ''):
            if wf.get('id') == TARGET_ID or 'SMRT' in wf.get('name', ''):
                return wf
    raise SystemExit('target workflow not found')


def main():
    wf = load_workflow()
    nodes = wf.get('nodes', [])
    node_map = {n.get('name'): n for n in nodes}
    result = {
        'source': str(RAW),
        'workflow': {'id': wf.get('id'), 'name': wf.get('name'), 'active': wf.get('active'), 'node_count': len(nodes)},
        'nodes': [],
        'connections_ai_tool_to_agent': [],
    }

    conns = wf.get('connections', {})
    for src, ports in conns.items():
        for channel, groups in (ports or {}).items():
            if channel == 'ai_tool':
                for group in groups or []:
                    for edge in group or []:
                        if edge.get('node') == 'AI Agent':
                            result['connections_ai_tool_to_agent'].append(src)

    for n in nodes:
        name = n.get('name') or ''
        params = n.get('parameters') or {}
        params_text = json.dumps(params, ensure_ascii=False)
        if name not in INTERESTING_NODES and not re.search(r'summary|conversation_context|prompt|message history|AI Agent', name, re.I) and not re.search(r'summary|conversation_context|prompt', params_text, re.I):
            continue
        fields = []
        for path, value in flatten(params):
            low = path.lower()
            if any(word.lower() in low for word in INTERESTING_PATH_WORDS):
                fields.append({'path': path, 'length': len(str(value)), 'value': safe_value(value)})
        result['nodes'].append({
            'name': name,
            'type': n.get('type'),
            'position': n.get('position'),
            'fields': fields,
        })

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({
        'workflow': result['workflow'],
        'ai_tools_to_agent': len(result['connections_ai_tool_to_agent']),
        'interesting_nodes': len(result['nodes']),
        'output': str(OUT),
    }, indent=2))

if __name__ == '__main__':
    main()
