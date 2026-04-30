#!/usr/bin/env python3
"""Local-only forensic inventory for SMRT newsletter workflows.

Reads sanitized n8n workflow exports from the repository and writes Markdown/JSON
summaries of newsletter generation, dispatch, and splinter-delivery surfaces.
No external services are called and no workflow state is modified.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WORKFLOWS = ROOT / 'workflows' / 'active'
OUT_DIR = ROOT / 'docs' / 'system'
DATA_DIR = ROOT / 'data' / 'workflows'
OUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    WORKFLOWS / 'Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json',
    WORKFLOWS / 'Newsletter_Dispatch__XDcom3gft8yqwa5O.json',
    WORKFLOWS / 'SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json',
]

SECRET_PATTERNS = [
    (re.compile(r'Bearer\s+[A-Za-z0-9._\-]+'), 'Bearer [REDACTED]'),
    (re.compile(r'(?i)(api[_-]?key|authorization|token|secret)\s*[:=]\s*["\']?[^"\'\s,}]+'), r'\1=[REDACTED]'),
    (re.compile(r'https://altos\.re/api/v2/[^\s"\']+'), 'https://altos.re/api/v2/[REDACTED_QUERY]'),
]

KEY_TERMS = re.compile(
    r'(?i)(newsletter|splinter|altos|grok|xai|x-ai|perplexity|macro|housing|market|leadconnector|ghl|email|sms|content_splinters|newsletter_deliveries|newsletters|altos_weekly_stats|documents|storage|conversation|messages)'
)


def redact(s: Any) -> str:
    text = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False, default=str)
    for pat, repl in SECRET_PATTERNS:
        text = pat.sub(repl, text)
    return text


def flatten_params(obj: Any, prefix: str = ''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten_params(v, f'{prefix}.{k}' if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten_params(v, f'{prefix}[{i}]')
    else:
        if isinstance(obj, str) and KEY_TERMS.search(obj):
            yield prefix, redact(obj)


def node_summary(node: dict[str, Any]) -> dict[str, Any]:
    params = node.get('parameters', {})
    matched = []
    for path, value in flatten_params(params):
        if len(value) > 2500:
            value = value[:2500] + '…[TRUNCATED]'
        matched.append({'path': path, 'value': value})
    return {
        'name': node.get('name'),
        'type': node.get('type'),
        'disabled': node.get('disabled', False),
        'matched_parameters': matched,
        'on_error': node.get('onError'),
        'retry_on_fail': node.get('retryOnFail'),
    }


def extract_edges(workflow: dict[str, Any]):
    edges = []
    conns = workflow.get('connections', {})
    for src, by_type in conns.items():
        for conn_type, outs in by_type.items():
            if not isinstance(outs, list):
                continue
            for out_idx, out in enumerate(outs):
                for entry in out or []:
                    edges.append({
                        'source': src,
                        'output_index': out_idx,
                        'type': conn_type,
                        'target': entry.get('node'),
                        'target_type': entry.get('type'),
                        'target_index': entry.get('index'),
                    })
    return edges


def adjacency(edges):
    adj = defaultdict(list)
    indeg = Counter()
    nodes = set()
    for e in edges:
        s, t = e['source'], e['target']
        nodes.add(s); nodes.add(t)
        adj[s].append(t)
        indeg[t] += 1
        indeg.setdefault(s, 0)
    return adj, indeg, nodes


def topo_like(edges):
    adj, indeg, nodes = adjacency(edges)
    q = deque(sorted([n for n in nodes if indeg[n] == 0]))
    order = []
    seen = set()
    while q:
        n = q.popleft()
        if n in seen:
            continue
        seen.add(n); order.append(n)
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    for n in sorted(nodes - seen):
        order.append(n)
    return order


def load(path: Path):
    with path.open() as f:
        wf = json.load(f)
    nodes = wf.get('nodes', [])
    edges = extract_edges(wf)
    by_name = {n.get('name'): n for n in nodes}
    relevant = [node_summary(n) for n in nodes if KEY_TERMS.search(json.dumps(n, ensure_ascii=False, default=str)) or 'Newsletter' in (n.get('name') or '') or 'Splinter' in (n.get('name') or '')]
    type_counts = Counter(n.get('type') for n in nodes)
    table_refs = Counter()
    api_refs = Counter()
    prompt_nodes = []
    for n in nodes:
        raw = json.dumps(n.get('parameters', {}), ensure_ascii=False, default=str)
        for table in ['newsletters','newsletter_deliveries','content_splinters','splinter_usage','altos_weekly_stats','documents','agents','leads','message_log','message_send_errors']:
            if re.search(rf'\b{re.escape(table)}\b', raw):
                table_refs[table] += 1
        for api in ['leadconnectorhq.com/conversations/messages','altos.re/api/v2','api.x.ai','grok','perplexity','openai']:
            if api.lower() in raw.lower():
                api_refs[api] += 1
        if n.get('type','').endswith('openAi') or 'messages' in raw or 'system' in raw:
            if KEY_TERMS.search(raw):
                prompt_nodes.append(node_summary(n))
    return {
        'file': str(path),
        'workflow_name': wf.get('name'),
        'workflow_id': wf.get('id'),
        'active': wf.get('active'),
        'node_count': len(nodes),
        'edge_count': len(edges),
        'type_counts': dict(type_counts),
        'table_refs': dict(table_refs),
        'api_refs': dict(api_refs),
        'topo_order': topo_like(edges),
        'relevant_nodes': relevant,
        'prompt_nodes': prompt_nodes,
        'edges': edges,
    }


def md_escape_cell(text: Any) -> str:
    s = redact(text)
    s = s.replace('\n', '<br>').replace('|', '\\|')
    if len(s) > 1400:
        s = s[:1400] + '…[TRUNCATED]'
    return s


def write_markdown(inventory):
    lines = []
    lines.append('# SMRT Newsletter Workflow Forensic Inventory')
    lines.append('')
    lines.append('This document is a local-only evidence inventory generated from the sanitized workflow exports. It extracts newsletter, macro-context, Altos, GoHighLevel, email, SMS, and splinter-related surfaces for audit synthesis.')
    lines.append('')
    for wf in inventory:
        lines.append(f"## {wf['workflow_name']}")
        lines.append('')
        lines.append('| Field | Value |')
        lines.append('| --- | --- |')
        lines.append(f"| File | `{wf['file'].replace(str(ROOT) + '/', '')}` |")
        lines.append(f"| Active | `{wf['active']}` |")
        lines.append(f"| Nodes | `{wf['node_count']}` |")
        lines.append(f"| Edges | `{wf['edge_count']}` |")
        lines.append(f"| Table refs | `{json.dumps(wf['table_refs'], sort_keys=True)}` |")
        lines.append(f"| API refs | `{json.dumps(wf['api_refs'], sort_keys=True)}` |")
        lines.append('')
        lines.append('### Approximate execution order')
        lines.append('')
        lines.append('`' + ' → '.join(wf['topo_order'][:80]) + ('`' if len(wf['topo_order']) <= 80 else ' → …`'))
        lines.append('')
        lines.append('### Relevant nodes and parameters')
        lines.append('')
        lines.append('| Node | Type | Parameter | Evidence |')
        lines.append('| --- | --- | --- | --- |')
        for n in wf['relevant_nodes']:
            params = n['matched_parameters'] or [{'path':'name/type only', 'value':''}]
            for p in params[:12]:
                lines.append(f"| {md_escape_cell(n['name'])} | `{md_escape_cell(n['type'])}` | `{md_escape_cell(p['path'])}` | {md_escape_cell(p['value'])} |")
        lines.append('')
        lines.append('### Prompt-like nodes')
        lines.append('')
        lines.append('| Node | Parameter | Prompt Evidence |')
        lines.append('| --- | --- | --- |')
        for n in wf['prompt_nodes']:
            for p in (n['matched_parameters'] or [])[:10]:
                lines.append(f"| {md_escape_cell(n['name'])} | `{md_escape_cell(p['path'])}` | {md_escape_cell(p['value'])} |")
        lines.append('')
    return '\n'.join(lines) + '\n'


def main():
    inventory = [load(path) for path in TARGETS]
    json_path = DATA_DIR / 'newsletter_workflow_forensics.json'
    md_path = OUT_DIR / 'newsletter_workflow_forensic_inventory.md'
    json_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding='utf-8')
    md_path.write_text(write_markdown(inventory), encoding='utf-8')
    print(f'Wrote {json_path}')
    print(f'Wrote {md_path}')


if __name__ == '__main__':
    main()
