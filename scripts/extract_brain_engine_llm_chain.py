#!/usr/bin/env python3.11
from __future__ import annotations

import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF = ROOT / 'workflows' / 'active' / 'SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json'
OUT_JSON = ROOT / 'data' / 'workflows' / 'brain_engine_llm_chain.json'
OUT_MD = ROOT / 'docs' / 'system' / 'brain_engine_llm_chain.md'

FOCUS_NAMES = {
    'AI Agent', 'Anthropic Chat Model', 'AI Sentiment Analysis', 'Analyze Conversation',
    'Assemble System Prompt', 'Prepare Tier Response', 'Determine Action', 'Parse Sentiment',
    'Get Message History', 'Get Conversation Summary', 'Get Outbound Conversation Summary',
    'Get Agent Config', 'Get Agent Config (RAG)', 'Get Outbound Agent Config', 'LeadDetails',
    'Search Relevant Messages', 'Docs Store', 'RAG LLM', 'Embeddings', 'Update Conversation Context',
    'Update Last Agent Message', 'Log Outbound Message'
}
KEYWORDS = re.compile(r'prompt|system|message|context|history|summary|agent|memory|model|temperature|tool|output|json|lead|conversation|sentiment|tier|behavioral|persona|rag|document|knowledge', re.I)


def flatten(obj: Any, prefix='') -> list[tuple[str, Any]]:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{prefix}.{k}' if prefix else str(k)
            out.extend(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(flatten(v, f'{prefix}[{i}]'))
    else:
        out.append((prefix, obj))
    return out


def clean(v: Any, n=2500) -> str:
    s = str(v)
    s = s.replace('\r', '')
    if len(s) > n:
        return s[:n] + f'… [truncated, total {len(s)} chars]'
    return s


def edges(conns: dict[str, Any]) -> list[tuple[str, str, str]]:
    out = []
    for src, channels in (conns or {}).items():
        if not isinstance(channels, dict):
            continue
        for ch, groups in channels.items():
            if not isinstance(groups, list):
                continue
            for group in groups:
                if not isinstance(group, list):
                    continue
                for item in group:
                    if isinstance(item, dict) and item.get('node'):
                        out.append((src, item['node'], ch))
    return out


def neighborhood(start: str, incoming: dict[str, list[tuple[str,str]]], outgoing: dict[str, list[tuple[str,str]]], depth=2) -> set[str]:
    seen = {start}
    q = deque([(start, 0)])
    while q:
        cur, d = q.popleft()
        if d >= depth:
            continue
        for src, _ in incoming.get(cur, []):
            if src not in seen:
                seen.add(src); q.append((src, d+1))
        for dst, _ in outgoing.get(cur, []):
            if dst not in seen:
                seen.add(dst); q.append((dst, d+1))
    return seen


def main():
    wf = json.loads(WF.read_text())
    nodes = wf.get('nodes') or []
    node_by_name = {n.get('name'): n for n in nodes if isinstance(n, dict)}
    inc = defaultdict(list); out = defaultdict(list)
    for src, dst, ch in edges(wf.get('connections') or {}):
        out[src].append((dst, ch)); inc[dst].append((src, ch))

    focus = set(FOCUS_NAMES)
    for anchor in ['AI Agent', 'AI Sentiment Analysis', 'Analyze Conversation']:
        focus |= neighborhood(anchor, inc, out, depth=2)
    # Include any node whose name/params look prompt-critical.
    for n in nodes:
        name = n.get('name')
        combined = name + '\n' + json.dumps(n.get('parameters', {}), ensure_ascii=False)
        if name and KEYWORDS.search(combined) and ('prompt' in combined.lower() or 'conversation' in combined.lower() or 'message history' in combined.lower()):
            focus.add(name)

    records = []
    for name in sorted(focus):
        n = node_by_name.get(name)
        if not n:
            continue
        params = n.get('parameters', {})
        all_fields = flatten(params)
        relevant_fields = []
        for path, val in all_fields:
            sval = str(val)
            if KEYWORDS.search(path) or KEYWORDS.search(sval) or len(sval) > 700:
                relevant_fields.append({'path': path, 'value': clean(val, 4000), 'length': len(sval)})
        records.append({
            'name': name,
            'type': n.get('type'),
            'disabled': bool(n.get('disabled')),
            'incoming': [{'node': s, 'channel': ch} for s, ch in inc.get(name, [])],
            'outgoing': [{'node': d, 'channel': ch} for d, ch in out.get(name, [])],
            'relevant_fields': relevant_fields,
            'all_parameter_keys': [p for p, _ in all_fields],
        })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({'workflow': wf.get('name'), 'file': str(WF.relative_to(ROOT)), 'nodes': records}, indent=2, ensure_ascii=False))

    lines = ['# Brain Engine LLM Injection Chain Evidence', '', 'Author: **Manus AI**', 'Date: **2026-04-29**', '', 'This file captures static evidence from the active Brain Engine workflow export. It does not modify production.', '']
    lines.append('## Focus-node connection table')
    lines.append('')
    lines.append('| Node | Type | Incoming | Outgoing | Relevant fields |')
    lines.append('| --- | --- | --- | --- | ---: |')
    for r in records:
        incoming = ', '.join(f"{x['node']} ({x['channel']})" for x in r['incoming']) or '—'
        outgoing = ', '.join(f"{x['node']} ({x['channel']})" for x in r['outgoing']) or '—'
        lines.append(f"| `{r['name']}` | `{r['type']}` | {incoming} | {outgoing} | {len(r['relevant_fields'])} |")
    lines.append('')
    lines.append('## Relevant prompt/context fields')
    for r in records:
        if not r['relevant_fields']:
            continue
        lines.append('')
        lines.append(f"### {r['name']}")
        lines.append('')
        lines.append(f"Type: `{r['type']}`")
        lines.append('')
        for f in r['relevant_fields'][:35]:
            lines.append(f"#### `{f['path']}` ({f['length']} chars)")
            lines.append('')
            lines.append('```text')
            lines.append(f['value'])
            lines.append('```')
            lines.append('')
    OUT_MD.write_text('\n'.join(lines) + '\n')
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')
    print(f'Focus nodes: {len(records)}')

if __name__ == '__main__':
    main()
