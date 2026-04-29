#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF_DIR = Path('/home/ubuntu/smrt_analysis/sanitized_workflows')
SCHEMA_PATH = ROOT / 'data/supabase/schema_inventory_clean.json'
OUT_JSON = ROOT / 'data/supabase/workflow_db_interactions.json'
OUT_MD = ROOT / 'docs/system/workflow_schema_relationship_map.md'

schema = json.loads(SCHEMA_PATH.read_text())
tables = sorted({item['table'] for item in schema}, key=len, reverse=True)
canonical_tables = sorted({item['table'] for item in schema})

def flatten(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f'{path}.{k}' if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f'{path}[{i}]')
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        yield path, '' if obj is None else str(obj)

sql_kw = re.compile(r'\b(select|insert|update|delete|upsert|from|join|into|set|where|rpc|rest/v1)\b', re.I)
crud_patterns = {
    'read': re.compile(r'\b(select|from|join|get|fetch|lookup|search|retrieve|list)\b', re.I),
    'create': re.compile(r'\b(insert|create|post|upsert|add|log|capture|enqueue)\b', re.I),
    'update': re.compile(r'\b(update|patch|put|set|sync|mark|increment)\b', re.I),
    'delete': re.compile(r'\b(delete|remove|archive)\b', re.I),
}

records = []
table_to_workflows = defaultdict(set)
table_ops = defaultdict(Counter)
workflow_summaries = []

for wf_path in sorted(WF_DIR.glob('*.json')):
    wf = json.loads(wf_path.read_text())
    wf_name = wf.get('name') or wf_path.stem
    wf_id = wf.get('id') or ''
    active = wf.get('active')
    nodes = wf.get('nodes', [])
    wf_tables = Counter()
    wf_ops = Counter()
    for node in nodes:
        node_name = node.get('name', '')
        node_type = node.get('type', '')
        node_text_parts = [node_name, node_type]
        for p, val in flatten(node.get('parameters', {})):
            if val and (sql_kw.search(val) or any(re.search(rf'(?<![A-Za-z0-9_]){re.escape(t)}(?![A-Za-z0-9_])', val) for t in tables)):
                node_text_parts.append(f'{p}: {val}')
        text = '\n'.join(node_text_parts)
        mentioned = []
        for table in tables:
            if re.search(rf'(?<![A-Za-z0-9_]){re.escape(table)}(?![A-Za-z0-9_])', text):
                mentioned.append(table)
        if not mentioned and not sql_kw.search(text) and 'supabase' not in node_type.lower():
            continue
        ops = []
        for op, pat in crud_patterns.items():
            if pat.search(text):
                ops.append(op)
        if not ops and mentioned:
            ops = ['reference']
        excerpts = []
        for p, val in flatten(node.get('parameters', {})):
            if not val:
                continue
            if sql_kw.search(val) or any(t in val for t in mentioned):
                clean = re.sub(r'\s+', ' ', val).strip()
                if len(clean) > 500:
                    clean = clean[:500] + '…'
                excerpts.append({'path': p, 'text': clean})
        rec = {
            'workflow_file': str(wf_path),
            'workflow_name': wf_name,
            'workflow_id': wf_id,
            'workflow_active': active,
            'node_name': node_name,
            'node_id': node.get('id',''),
            'node_type': node_type,
            'tables': sorted(set(mentioned)),
            'operations': sorted(set(ops)),
            'excerpts': excerpts[:8],
        }
        records.append(rec)
        for t in rec['tables']:
            table_to_workflows[t].add(wf_name)
            wf_tables[t] += 1
            for op in rec['operations']:
                table_ops[t][op] += 1
        for op in rec['operations']:
            wf_ops[op] += 1
    workflow_summaries.append({
        'workflow_name': wf_name,
        'workflow_id': wf_id,
        'active': active,
        'node_count': len(nodes),
        'db_interaction_nodes': sum(1 for r in records if r['workflow_name'] == wf_name),
        'tables': dict(wf_tables),
        'operations': dict(wf_ops),
    })

out = {
    'source_workflow_dir': str(WF_DIR),
    'workflow_count': len(workflow_summaries),
    'interaction_node_count': len(records),
    'tables_seen_in_workflows': sorted(table_to_workflows),
    'tables_not_seen_in_workflows': [t for t in canonical_tables if t not in table_to_workflows],
    'table_workflow_map': {t: sorted(wfs) for t, wfs in sorted(table_to_workflows.items())},
    'table_operation_counts': {t: dict(table_ops[t]) for t in sorted(table_ops)},
    'workflow_summaries': workflow_summaries,
    'records': records,
}
OUT_JSON.write_text(json.dumps(out, indent=2) + '\n')

lines = []
lines.append('# SMRT Workflow–Schema Relationship Map')
lines.append('')
lines.append('This map is generated from a static, read-only scan of the sanitized n8n workflow exports and the live Supabase schema inventory. It identifies where workflow nodes reference database tables, SQL-like operations, Supabase REST endpoints, or persistence concepts. Because n8n expressions can construct URLs and SQL dynamically, this document should be treated as a **high-confidence static map**, not a replacement for runtime tracing.')
lines.append('')
lines.append('> **Read-only audit note:** This extraction inspected exported workflow JSON only. It did not change workflows, credentials, database rows, schema, prompt configuration, or production routing.')
lines.append('')
lines.append('## Coverage Summary')
lines.append('')
lines.append(f'The scan covered **{len(workflow_summaries)} workflows** and found **{len(records)} workflow nodes** with database or schema-relevant references.')
lines.append('')
lines.append('| Metric | Count |')
lines.append('| --- | ---: |')
lines.append(f'| Public schema relations inventoried | {len(canonical_tables)} |')
lines.append(f'| Relations referenced by workflows | {len(table_to_workflows)} |')
lines.append(f'| Relations not directly observed in workflow exports | {len(out["tables_not_seen_in_workflows"])} |')
lines.append(f'| Database-relevant workflow nodes | {len(records)} |')
lines.append('')
lines.append('## Table-to-Workflow Map')
lines.append('')
lines.append('| Table | Workflow References | Operation Signals |')
lines.append('| --- | --- | --- |')
for table in canonical_tables:
    wfs = sorted(table_to_workflows.get(table, []))
    ops = table_ops.get(table, Counter())
    ops_str = ', '.join(f'{op}: {count}' for op, count in sorted(ops.items())) if ops else 'not observed'
    lines.append(f'| `{table}` | {"<br>".join(wfs) if wfs else "not observed"} | {ops_str} |')
lines.append('')
lines.append('## Workflow Persistence Summary')
lines.append('')
lines.append('| Workflow | Active | Nodes | DB-Relevant Nodes | Tables Referenced |')
lines.append('| --- | --- | ---: | ---: | --- |')
for wf in sorted(workflow_summaries, key=lambda x: x['workflow_name']):
    tables_str = ', '.join(f'`{t}` ({c})' for t, c in sorted(wf['tables'].items())) if wf['tables'] else 'none observed'
    lines.append(f'| {wf["workflow_name"]} | {wf["active"]} | {wf["node_count"]} | {wf["db_interaction_nodes"]} | {tables_str} |')
lines.append('')
lines.append('## Node-Level Evidence')
for rec in records:
    lines.append('')
    lines.append(f'### {rec["workflow_name"]} / {rec["node_name"]}')
    lines.append('')
    lines.append(f'- **Node type:** `{rec["node_type"]}`')
    lines.append(f'- **Tables:** {", ".join(f"`{t}`" for t in rec["tables"]) if rec["tables"] else "none explicitly matched"}')
    lines.append(f'- **Operation signals:** {", ".join(rec["operations"]) if rec["operations"] else "none"}')
    if rec['excerpts']:
        lines.append('')
        lines.append('| Parameter Path | Evidence Excerpt |')
        lines.append('| --- | --- |')
        for ex in rec['excerpts'][:4]:
            val = ex['text'].replace('|', '\\|')
            lines.append(f'| `{ex["path"]}` | `{val}` |')
OUT_MD.write_text('\n'.join(lines) + '\n')
print(f'Parsed {len(workflow_summaries)} workflows; found {len(records)} database-relevant nodes')
print(OUT_JSON)
print(OUT_MD)
