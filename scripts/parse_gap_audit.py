#!/usr/bin/env python3
import json, re
from pathlib import Path
ROOT=Path('/home/ubuntu/SMRT-Agent-Ai')
raw_path=ROOT/'data/supabase/gap_audit_raw.json'
out_json=ROOT/'data/supabase/gap_audit_clean.json'
out_md=ROOT/'docs/system/supabase_gap_audit_findings.md'
raw=raw_path.read_text()
outer=json.loads(raw.split('Tool execution result:\n',1)[1]) if 'Tool execution result:\n' in raw else json.loads(raw)
result=outer.get('result','')
starts=list(re.finditer(r'<untrusted-data-[^>]+>', result))
payload_text=None
for marker in reversed(starts):
    tail=result[marker.end():]
    if not tail.lstrip().startswith('['):
        continue
    close=re.search(r'</untrusted-data-[^>]+>', tail, re.S)
    if close:
        payload_text=tail[:close.start()].strip(); break
if payload_text is None:
    # fallback for direct JSON result
    m=re.search(r'(\[\{.*\}\])', result, re.S)
    if m: payload_text=m.group(1)
if payload_text is None:
    raise SystemExit('Could not isolate gap audit JSON payload')
rows=json.loads(payload_text)
if not rows or 'gap_audit' not in rows[0]:
    raise SystemExit(f'Unexpected payload keys: {rows[0].keys() if rows else None}')
audit=rows[0]['gap_audit']
out_json.write_text(json.dumps(audit, indent=2, default=str)+'\n')

lines=[]
lines.append('# SMRT Supabase Gap Audit Findings')
lines.append('')
lines.append('This document summarizes a read-only data-integrity query focused on the live SMRT appointment, identity, memory, message, inbound capture, and agent configuration surfaces. It is intended to support a ranked hardening plan rather than to make direct production changes.')
lines.append('')
lines.append('> **Read-only audit note:** The query used only `SELECT` statements through the configured Supabase connector. No rows, schema, workflows, prompts, credentials, or runtime configuration were modified.')
lines.append('')
lines.append(f'Generated at: `{audit.get("audit_generated_at")}`')
lines.append('')
lines.append('## Row Counts')
lines.append('')
lines.append('| Surface | Count |')
lines.append('| --- | ---: |')
for k,v in audit.get('counts',{}).items():
    lines.append(f'| `{k}` | {v} |')
lines.append('')
lines.append('## Appointment Health')
lines.append('')
lines.append('| Check | Count / Value |')
lines.append('| --- | ---: |')
for k,v in audit.get('appointment_health',{}).items():
    if isinstance(v, dict):
        lines.append(f'| `{k}` | `{json.dumps(v, sort_keys=True)}` |')
    else:
        lines.append(f'| `{k}` | {v} |')
lines.append('')
lines.append('The critical visibility signal is whether conversation contexts have `appointment_booked = true` while no matching row exists in `appointments` for the same contact/location pair.')
lines.append('')
cb=audit.get('contexts_booked',{})
lines.append('| Context Booking Check | Count |')
lines.append('| --- | ---: |')
lines.append(f'| `total_contexts_booked_true` | {cb.get("total_contexts_booked_true")} |')
lines.append(f'| `booked_contexts_without_appointment_row` | {cb.get("booked_contexts_without_appointment_row")} |')
lines.append('')
lines.append('## Recent Appointment Rows')
lines.append('')
lines.append('| Created At | Contact ID | Location ID | Status | Lead ID Exists | Contact/Location Lead Exists | Agent ID Exists | Location Agent Exists |')
lines.append('| --- | --- | --- | --- | --- | --- | --- | --- |')
for r in audit.get('recent_appointments',[])[:20]:
    lines.append(f'| `{r.get("created_at")}` | `{r.get("contact_id")}` | `{r.get("location_id")}` | `{r.get("status")}` | {r.get("lead_id_exists")} | {r.get("contact_location_lead_exists")} | {r.get("agent_id_exists")} | {r.get("location_agent_exists")} |')
lines.append('')
lines.append('## Booked Context Sample')
lines.append('')
lines.append('| Updated At | Contact ID | Location ID | Appointment Rows | Pending Slot | Summary Excerpt |')
lines.append('| --- | --- | --- | ---: | --- | --- |')
for r in audit.get('contexts_booked',{}).get('sample',[])[:20]:
    summary=(r.get('conversation_summary') or '').replace('|','\\|').replace('\n',' ')[:240]
    lines.append(f'| `{r.get("updated_at")}` | `{r.get("contact_id")}` | `{r.get("location_id")}` | {r.get("appointment_rows")} | `{r.get("appointment_pending_slot")}` | {summary} |')
lines.append('')
lines.append('## Orphan Summary')
lines.append('')
lines.append('| Check | Count |')
lines.append('| --- | ---: |')
for k,v in audit.get('orphan_summary',{}).items():
    if not isinstance(v, list):
        lines.append(f'| `{k}` | {v} |')
lines.append('')
lines.append('## Agent State')
lines.append('')
lines.append('| Agent | Location ID | Active | Custom Personality Enabled | Has Personality Prompt | Has Agent Notes | Has Calendar ID | Has Calendar Link | Has GHL User ID |')
lines.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- |')
for r in audit.get('agent_state',[]):
    lines.append(f'| {r.get("agent_name")} | `{r.get("location_id")}` | {r.get("active")} | {r.get("use_custom_personality")} | {r.get("has_personality_prompt")} | {r.get("has_agent_notes")} | {r.get("has_calendar_id")} | {r.get("has_calendar_link")} | {r.get("has_ghl_user_id")} |')

out_md.write_text('\n'.join(lines)+'\n')
print('Wrote', out_json)
print('Wrote', out_md)
