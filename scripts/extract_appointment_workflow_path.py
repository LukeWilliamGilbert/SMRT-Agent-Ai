#!/usr/bin/env python3
import json
from pathlib import Path

RAW = Path('/home/ubuntu/smrt_analysis/raw_export/root/smrt_n8n_export_20260428_194357/workflows/smrt_workflows_all.json')
OUT_JSON = Path('/home/ubuntu/SMRT-Agent-Ai/data/workflows/appointment_workflow_path.json')
OUT_MD = Path('/home/ubuntu/SMRT-Agent-Ai/docs/system/appointment_workflow_path.md')

KEYWORDS = ['appointment', 'book', 'calendar', 'slot', 'qualif']

def compact(v, max_len=2400):
    s = json.dumps(v, ensure_ascii=False, indent=2) if not isinstance(v, str) else v
    if len(s) > max_len:
        return s[:max_len] + '\n...[truncated]'
    return s

with RAW.open('r', encoding='utf-8') as f:
    workflows = json.load(f)

records = []
for wf in workflows:
    wf_name = wf.get('name','')
    wf_id = wf.get('id','')
    if 'Brain Engine' not in wf_name and not any(k in wf_name.lower() for k in KEYWORDS):
        # Still keep appointment reminder separately via keyword in workflow name.
        pass
    nodes = wf.get('nodes') or []
    conns = wf.get('connections') or {}
    matched_nodes = []
    for n in nodes:
        blob = json.dumps(n, ensure_ascii=False).lower()
        if any(k in blob for k in KEYWORDS):
            matched_nodes.append({
                'workflow_id': wf_id,
                'workflow_name': wf_name,
                'node_id': n.get('id'),
                'node_name': n.get('name'),
                'node_type': n.get('type'),
                'parameters': n.get('parameters', {}),
                'outgoing': conns.get(n.get('name'), {})
            })
    if matched_nodes:
        records.append({
            'workflow_id': wf_id,
            'workflow_name': wf_name,
            'active': wf.get('active'),
            'archived': wf.get('isArchived'),
            'matched_node_count': len(matched_nodes),
            'nodes': matched_nodes
        })

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_MD.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

lines = ['# Appointment Workflow Path Evidence', '', 'This file is generated from the raw n8n workflow export and focuses on nodes that mention appointments, booking, calendar, slots, or qualification. It is read-only evidence for the missing-appointment audit.', '']
for wf in records:
    lines.append(f"## {wf['workflow_name']} (`{wf['workflow_id']}`)")
    lines.append('')
    lines.append(f"Active: **{wf['active']}**. Archived: **{wf['archived']}**. Matched nodes: **{wf['matched_node_count']}**.")
    lines.append('')
    lines.append('| Node | Type | Outgoing connection summary |')
    lines.append('|---|---|---|')
    for n in wf['nodes']:
        outgoing_keys = ', '.join((n.get('outgoing') or {}).keys()) or 'none'
        lines.append(f"| `{n['node_name']}` | `{n['node_type']}` | {outgoing_keys} |")
    lines.append('')
    for n in wf['nodes']:
        lines.append(f"### {n['node_name']}")
        lines.append('')
        lines.append(f"Type: `{n['node_type']}`. Node ID: `{n['node_id']}`.")
        lines.append('')
        lines.append('```json')
        lines.append(compact(n['parameters']))
        lines.append('```')
        lines.append('')

OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'Wrote {OUT_JSON}')
print(f'Wrote {OUT_MD}')
print(f'Workflows with appointment evidence: {len(records)}')
for wf in records:
    print(f"- {wf['workflow_name']}: {wf['matched_node_count']} nodes")
