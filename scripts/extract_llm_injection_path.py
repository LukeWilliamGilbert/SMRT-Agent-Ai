#!/usr/bin/env python3.11
"""Extract LLM injection surfaces from SMRT n8n workflow JSON.

This is read-only. It scans versioned workflow exports and writes durable evidence
for prompt/LLM audit work.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF_DIRS = [ROOT / 'workflows' / 'active', ROOT / 'workflows' / 'inactive']
OUT_JSON = ROOT / 'data' / 'workflows' / 'llm_injection_inventory.json'
OUT_MD = ROOT / 'docs' / 'system' / 'llm_injection_workflow_map.md'

LLM_PAT = re.compile(r'(openai|anthropic|gemini|gpt|llm|language\s*model|chat\s*model|ai\s*agent|agent)', re.I)
PROMPT_PAT = re.compile(r'(prompt|system\s*message|systemPrompt|instruction|persona|personality|container|template)', re.I)
MEMORY_PAT = re.compile(r'(memory|context|conversation_context|summary|history|lead|appointment|message_log|inbound_capture|agent_config|bio|embedding)', re.I)
SUPABASE_PAT = re.compile(r'(supabase|postgres|select\s+|insert\s+into|update\s+|from\s+)', re.I)
EXPR_PAT = re.compile(r'={{.*?}}|\$\([^)]+\)|\$json|\$node|\$items|\$now', re.S)
TABLE_PAT = re.compile(r'\b(?:from|into|update|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', re.I)


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        return {'_parse_error': str(exc)}


def flatten_strings(obj: Any, prefix: str = '') -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f'{prefix}.{k}' if prefix else str(k)
            out.extend(flatten_strings(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f'{prefix}[{i}]'
            out.extend(flatten_strings(v, key))
    elif isinstance(obj, str):
        out.append((prefix, obj))
    return out


def preview(text: str, n: int = 700) -> str:
    clean = re.sub(r'\s+', ' ', text).strip()
    if len(clean) > n:
        return clean[: n - 1] + '…'
    return clean


def extract_node_refs(text: str) -> list[str]:
    refs = set(re.findall(r"\$\(['\"]([^'\"]+)['\"]\)", text))
    refs.update(re.findall(r"\$node\[['\"]([^'\"]+)['\"]\]", text))
    return sorted(refs)


def connection_edges(connections: dict[str, Any]) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for src, outs in (connections or {}).items():
        if not isinstance(outs, dict):
            continue
        for channel, groups in outs.items():
            if not isinstance(groups, list):
                continue
            for group in groups:
                if not isinstance(group, list):
                    continue
                for item in group:
                    if isinstance(item, dict) and item.get('node'):
                        edges.append((src, item['node'], channel))
    return edges


def main() -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    workflows = []
    all_tables = Counter()
    issue_counter = Counter()

    for wf_dir in WF_DIRS:
        status = wf_dir.name
        for path in sorted(wf_dir.glob('*.json')):
            wf = load_json(path)
            if not isinstance(wf, dict) or wf.get('_parse_error'):
                workflows.append({'file': str(path.relative_to(ROOT)), 'status': status, 'parse_error': wf.get('_parse_error') if isinstance(wf, dict) else 'unknown'})
                continue
            nodes = wf.get('nodes') or []
            edges = connection_edges(wf.get('connections') or {})
            incoming = defaultdict(list)
            outgoing = defaultdict(list)
            for src, dst, channel in edges:
                outgoing[src].append({'node': dst, 'channel': channel})
                incoming[dst].append({'node': src, 'channel': channel})

            node_index = {n.get('name', f'unnamed_{i}'): n for i, n in enumerate(nodes) if isinstance(n, dict)}
            wf_record = {
                'file': str(path.relative_to(ROOT)),
                'workflow_name': wf.get('name') or path.stem,
                'workflow_id': wf.get('id'),
                'active': wf.get('active'),
                'status_dir': status,
                'llm_nodes': [],
                'prompt_related_nodes': [],
                'memory_context_nodes': [],
                'supabase_prompt_feed_nodes': [],
                'possible_issues': [],
            }

            for i, node in enumerate(nodes):
                if not isinstance(node, dict):
                    continue
                name = str(node.get('name') or f'unnamed_{i}')
                ntype = str(node.get('type') or '')
                params = node.get('parameters') or {}
                strings = flatten_strings(params)
                combined = '\n'.join([name, ntype] + [f'{k}: {v}' for k, v in strings])
                tables = sorted(set(m.group(1).lower() for m in TABLE_PAT.finditer(combined)))
                for t in tables:
                    all_tables[t] += 1
                exprs = [(k, v) for k, v in strings if EXPR_PAT.search(v)]
                refs = sorted(set(r for _, v in strings for r in extract_node_refs(v)))
                base = {
                    'name': name,
                    'type': ntype,
                    'disabled': bool(node.get('disabled')),
                    'incoming': incoming.get(name, []),
                    'outgoing': outgoing.get(name, []),
                    'referenced_nodes_in_expressions': refs,
                    'tables_referenced': tables,
                    'expression_fields': [{'path': k, 'preview': preview(v, 350)} for k, v in exprs[:25]],
                }

                node_is_llm = bool(LLM_PAT.search(name) or LLM_PAT.search(ntype))
                node_is_prompt = bool(PROMPT_PAT.search(combined))
                node_is_memory = bool(MEMORY_PAT.search(combined))
                node_is_supabase_prompt = bool(SUPABASE_PAT.search(combined) and (PROMPT_PAT.search(combined) or MEMORY_PAT.search(combined)))

                if node_is_llm:
                    long_prompt_fields = []
                    for k, v in strings:
                        if PROMPT_PAT.search(k) or PROMPT_PAT.search(v) or len(v) > 1500:
                            long_prompt_fields.append({'path': k, 'length': len(v), 'preview': preview(v, 900)})
                    rec = dict(base)
                    rec['prompt_like_fields'] = long_prompt_fields[:30]
                    rec['has_expression_inputs'] = bool(exprs)
                    rec['has_incoming_connection'] = bool(incoming.get(name))
                    rec['has_model_hint'] = bool(re.search(r'(model|gpt|openai|gemini|anthropic)', combined, re.I))
                    wf_record['llm_nodes'].append(rec)
                    if not exprs and not incoming.get(name):
                        wf_record['possible_issues'].append({'severity': 'high', 'node': name, 'issue': 'LLM/agent node has neither expression fields nor incoming connection evidence in export.'})
                        issue_counter['llm_without_inputs'] += 1
                    if not long_prompt_fields:
                        wf_record['possible_issues'].append({'severity': 'medium', 'node': name, 'issue': 'LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only.'})
                        issue_counter['llm_without_prompt_fields'] += 1

                if node_is_prompt and not node_is_llm:
                    prompt_strings = [{'path': k, 'length': len(v), 'preview': preview(v, 500)} for k, v in strings if PROMPT_PAT.search(k) or PROMPT_PAT.search(v) or 'prompt' in v.lower()]
                    rec = dict(base)
                    rec['prompt_strings'] = prompt_strings[:20]
                    wf_record['prompt_related_nodes'].append(rec)

                if node_is_memory and not node_is_llm:
                    rec = dict(base)
                    rec['memory_context_strings'] = [{'path': k, 'length': len(v), 'preview': preview(v, 450)} for k, v in strings if MEMORY_PAT.search(k) or MEMORY_PAT.search(v)][:20]
                    wf_record['memory_context_nodes'].append(rec)

                if node_is_supabase_prompt:
                    rec = dict(base)
                    rec['query_or_payload_fields'] = [{'path': k, 'length': len(v), 'preview': preview(v, 650)} for k, v in strings if SUPABASE_PAT.search(v) or SUPABASE_PAT.search(k)][:25]
                    wf_record['supabase_prompt_feed_nodes'].append(rec)

                # Generic expression hygiene checks on all nodes.
                for k, v in exprs:
                    for ref in extract_node_refs(v):
                        if ref not in node_index:
                            wf_record['possible_issues'].append({'severity': 'high', 'node': name, 'field': k, 'issue': f'Expression references missing node {ref!r}.'})
                            issue_counter['missing_node_reference'] += 1
                    if re.search(r'prompt|context|memory|history|conversation', k + ' ' + v, re.I) and len(v) > 12000:
                        wf_record['possible_issues'].append({'severity': 'medium', 'node': name, 'field': k, 'issue': f'Prompt/context expression is very large ({len(v)} chars), raising truncation/maintainability risk.'})
                        issue_counter['large_prompt_expression'] += 1

            workflows.append(wf_record)

    summary = {
        'workflow_count': len(workflows),
        'active_count': sum(1 for w in workflows if w.get('status_dir') == 'active'),
        'llm_node_count': sum(len(w.get('llm_nodes', [])) for w in workflows),
        'prompt_related_node_count': sum(len(w.get('prompt_related_nodes', [])) for w in workflows),
        'memory_context_node_count': sum(len(w.get('memory_context_nodes', [])) for w in workflows),
        'supabase_prompt_feed_node_count': sum(len(w.get('supabase_prompt_feed_nodes', [])) for w in workflows),
        'issue_counts': dict(issue_counter),
        'top_tables_referenced': all_tables.most_common(40),
    }

    payload = {'summary': summary, 'workflows': workflows}
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    lines = []
    lines.append('# SMRT LLM Injection Workflow Map')
    lines.append('')
    lines.append('Author: **Manus AI**')
    lines.append('Date: **2026-04-29**')
    lines.append('Status: **Static workflow evidence; no production changes**')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append('| Metric | Count |')
    lines.append('| --- | ---: |')
    for key in ['workflow_count','active_count','llm_node_count','prompt_related_node_count','memory_context_node_count','supabase_prompt_feed_node_count']:
        lines.append(f'| `{key}` | {summary[key]} |')
    lines.append('')
    lines.append('## Static issue counters')
    lines.append('')
    lines.append('| Issue | Count |')
    lines.append('| --- | ---: |')
    for issue, count in sorted(summary['issue_counts'].items()):
        lines.append(f'| `{issue}` | {count} |')
    lines.append('')
    lines.append('## Workflow-level LLM surfaces')
    lines.append('')
    for w in workflows:
        if not (w.get('llm_nodes') or w.get('prompt_related_nodes') or w.get('supabase_prompt_feed_nodes') or w.get('possible_issues')):
            continue
        lines.append(f"### {w.get('workflow_name')} — `{w.get('file')}`")
        lines.append('')
        lines.append(f"Active flag: `{w.get('active')}`; directory: `{w.get('status_dir')}`")
        lines.append('')
        if w.get('llm_nodes'):
            lines.append('| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |')
            lines.append('| --- | --- | ---: | ---: | ---: | ---: | --- |')
            for n in w['llm_nodes']:
                refs = ', '.join(n.get('referenced_nodes_in_expressions') or [])[:180]
                lines.append(f"| `{n['name']}` | `{n['type']}` | {len(n.get('incoming', []))} | {len(n.get('outgoing', []))} | {len(n.get('expression_fields', []))} | {len(n.get('prompt_like_fields', []))} | {refs or '—'} |")
            lines.append('')
        if w.get('supabase_prompt_feed_nodes'):
            lines.append('| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |')
            lines.append('| --- | --- | --- |')
            for n in w['supabase_prompt_feed_nodes'][:20]:
                examples = '<br>'.join([f"`{x['path']}`: {x['preview'][:180]}" for x in n.get('query_or_payload_fields', [])[:3]])
                lines.append(f"| `{n['name']}` | {', '.join(n.get('tables_referenced') or []) or '—'} | {examples or '—'} |")
            lines.append('')
        if w.get('possible_issues'):
            lines.append('| Severity | Node | Issue |')
            lines.append('| --- | --- | --- |')
            for issue in w['possible_issues'][:30]:
                lines.append(f"| {issue.get('severity')} | `{issue.get('node')}` | {issue.get('issue')} |")
            lines.append('')
    OUT_MD.write_text('\n'.join(lines) + '\n')
    print(json.dumps(summary, indent=2))
    print(f'Wrote {OUT_JSON}')
    print(f'Wrote {OUT_MD}')


if __name__ == '__main__':
    main()
