#!/usr/bin/env python3
"""Extract full non-secret node details for the SMRT newsletter audit."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
OUT = ROOT / 'docs' / 'system' / 'newsletter_workflow_node_details.md'
FILES = {
    'Data Source & Newsletter Creation': ROOT / 'workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json',
    'Newsletter Dispatch': ROOT / 'workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json',
    'SMRT Brain Engine': ROOT / 'workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json',
}
TARGET_NODES = {
    'Data Source & Newsletter Creation': [
        'Weekly Schedule', 'Get Newsletter Agents', 'Get Altos Hash', 'Altos Get Stats', 'Condense Altos Data',
        'Grok National Context', 'Prep Data for AI', 'Get Previous Newsletters', 'Generate Newsletter',
        'Extract Splinters', 'Prepare Storage Data', 'Store Newsletter', 'Store Splinter', 'Store Weekly Stats',
        'Generate Embedding', 'Store Embedded Doc', 'Create Newsletter Doc', 'Upload to Supabase Storage',
        'Delete Old Splinters', 'Check Newsletter For Week', 'Check Week Stats Exist'
    ],
    'Newsletter Dispatch': [
        'Weekly Schedule', 'Fetch Active Agents', 'Get Newest Newsletter', 'Fetch Eligible Leads',
        'Build HTML Email', 'Send Email via GHL', 'Log Delivery', 'Update Send Counts',
        'Has Eligible Leads?', 'Newsletter Found?'
    ],
    'SMRT Brain Engine': [
        'Schedule Outbound Check', 'Fetch Outbound Candidates', 'Set Outbound Context', 'Merge Outbound Context',
        'Get Outbound Agent Config', 'Get Outbound Message History', 'Get Outbound Conversation Summary',
        'Get Outbound Lead Memory', 'Assemble System Prompt', 'AI Agent', 'Log Outbound Message',
        'Send SMS', 'Send Email', 'Record Splinter Usage', 'Update Next Outbound Due'
    ],
}

SECRET_PATTERNS = [
    (re.compile(r'Bearer\s+[A-Za-z0-9._\-]+'), 'Bearer [REDACTED]'),
    (re.compile(r'(?i)(api[_-]?key|authorization|token|secret|supabaseKey|ghlApiKey)\s*[:=]\s*["\']?[^"\'\s,}]+'), r'\1=[REDACTED]'),
    (re.compile(r'https://altos\.re/api/v2/[^\s"\'`]+'), 'https://altos.re/api/v2/[REDACTED_QUERY]'),
    (re.compile(r'eyJ[A-Za-z0-9._\-]+'), '[JWT_REDACTED]'),
]


def redact(text: Any) -> str:
    if not isinstance(text, str):
        text = json.dumps(text, indent=2, ensure_ascii=False, default=str)
    for pat, repl in SECRET_PATTERNS:
        text = pat.sub(repl, text)
    return text


def flatten(obj: Any, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f'{path}[{i}]')
    else:
        if isinstance(obj, str) and (len(obj) > 15 or re.search(r'(?i)(newsletter|splinter|altos|grok|macro|market|email|sms|lead|select|insert|update|fetch|message|prompt|system|json|content|conversation)', obj)):
            yield path, obj


def node_by_name(path: Path):
    wf = json.loads(path.read_text())
    return wf, {n.get('name'): n for n in wf.get('nodes', [])}


def main():
    lines = ['# SMRT Newsletter Workflow Node Details', '', 'This is targeted local evidence for the newsletter forensic audit. Secrets and credential-like values are defensively redacted. The file intentionally preserves prompt, code, SQL, and API-body surfaces needed to map actual behavior.', '']
    for label, path in FILES.items():
        wf, nodes = node_by_name(path)
        lines += [f'## {label}', '', f'Workflow file: `{path.relative_to(ROOT)}`', '', f'Node count: `{len(wf.get("nodes", []))}`', '']
        for name in TARGET_NODES[label]:
            n = nodes.get(name)
            if not n:
                lines += [f'### {name}', '', '**Status:** Not found in export.', '']
                continue
            lines += [f'### {name}', '', '| Field | Value |', '| --- | --- |', f'| Type | `{n.get("type")}` |', f'| Disabled | `{n.get("disabled", False)}` |', f'| Retry on fail | `{n.get("retryOnFail")}` |', f'| On error | `{n.get("onError")}` |', '']
            params = n.get('parameters', {})
            selected = []
            for p, v in flatten(params):
                selected.append((p, redact(v)))
            if not selected:
                selected = [('parameters', redact(params))]
            for p, v in selected:
                lang = 'javascript' if 'jsCode' in p else ('sql' if 'query' in p.lower() else 'text')
                lines += [f'#### `{p}`', '', f'```{lang}', v.strip(), '```', '']
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
