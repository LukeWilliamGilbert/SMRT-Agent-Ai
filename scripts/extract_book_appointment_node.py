#!/usr/bin/env python3
import json
from pathlib import Path
RAW=Path('/home/ubuntu/smrt_analysis/raw_export/root/smrt_n8n_export_20260428_194357/workflows/smrt_workflows_all.json')
OUT=Path('/home/ubuntu/SMRT-Agent-Ai/docs/system/book_appointment_node_full.md')
workflows=json.loads(RAW.read_text(encoding='utf-8'))
lines=['# Full `bookAppointment` Node Evidence','']
for wf in workflows:
    for n in wf.get('nodes') or []:
        if n.get('name')=='bookAppointment':
            lines += [f"Workflow: **{wf.get('name')}** (`{wf.get('id')}`)", '', f"Type: `{n.get('type')}`", '', '## Description', '', '```text', n.get('parameters',{}).get('description',''), '```', '', '## JavaScript', '', '```javascript', n.get('parameters',{}).get('jsCode',''), '```', '']
OUT.write_text('\n'.join(lines),encoding='utf-8')
print(OUT)
