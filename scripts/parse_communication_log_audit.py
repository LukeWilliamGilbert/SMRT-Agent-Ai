#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import Counter

repo = Path('/home/ubuntu/SMRT-Agent-Ai')
raw_path = repo / 'data/supabase/communication_log_audit_raw.json'
clean_path = repo / 'data/supabase/communication_log_audit_clean.json'
md_path = repo / 'docs/system/communication_log_audit_findings.md'

raw = raw_path.read_text()
outer_start = raw.find('{')
if outer_start == -1:
    raise SystemExit('Could not locate outer JSON object in raw audit output')
outer = json.loads(raw[outer_start:])
result_text = outer.get('result', '')
payload_text = None
for open_match in re.finditer(r'<untrusted-data-[^>]+>', result_text):
    remainder = result_text[open_match.end():]
    if remainder.lstrip().startswith('['):
        close_match = re.search(r'</untrusted-data-[^>]+>', remainder)
        if close_match:
            payload_text = remainder[:close_match.start()].strip()
            break
if not payload_text:
    raise SystemExit('Could not locate JSON-bearing untrusted-data payload in raw audit output')
rows = json.loads(payload_text)
if not rows or 'communication_log_audit' not in rows[0]:
    raise SystemExit('Unexpected communication audit payload shape')
audit = rows[0]['communication_log_audit']
clean_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + '\n')

counts = audit.get('counts', {})
msg_status = audit.get('message_status', [])
inbound_status = audit.get('inbound_status', [])
error_summary = audit.get('error_summary', [])
system_error_summary = audit.get('system_error_summary', [])
context_health = audit.get('context_health', {}) or {}

# Derived metrics.
total_msgs = counts.get('message_log', 0) or 0
total_inbound_capture = counts.get('inbound_capture', 0) or 0
unprocessed_inbound = sum(row.get('ct', 0) for row in inbound_status if not row.get('processed'))
processed_missing_ghl = sum(row.get('missing_ghl_message_id', 0) for row in inbound_status if row.get('processed'))
inbound_msg_missing_ghl = sum(row.get('missing_ghl_message_id', 0) for row in msg_status if row.get('direction') == 'inbound')
outbound_queued_missing_ghl = sum(row.get('missing_ghl_message_id', 0) for row in msg_status if row.get('direction') == 'outbound' and row.get('delivery_status') == 'queued')
cap_hit_errors = sum(row.get('ct', 0) for row in error_summary if row.get('classification') == 'cap_hit')
invalid_or_terminal = sum(row.get('ct', 0) for row in error_summary if row.get('classification') in {'invalid_number','unreachable'})

lines = []
lines.append('# SMRT Communication Log Audit Findings')
lines.append('')
lines.append('Author: **Manus AI**  ')
lines.append('Date: **2026-04-29**')
lines.append('')
lines.append('## Executive finding')
lines.append('')
lines.append('The communication logs do not suggest that everything is broken. They show a system with **partially mature observability**: outbound delivery status and send-error tracking are materially better developed than appointment mirroring, while inbound capture and replay remain the biggest unresolved communication-control gap. The highest-signal problem is not duplicate messages or orphaned identities; it is that inbound events can sit unprocessed and the recovery workflows that would backfill or replay them are currently inactive.')
lines.append('')
lines.append('| Metric | Current evidence | Planning interpretation |')
lines.append('| --- | ---: | --- |')
lines.append(f"| Leads | {counts.get('leads', 0)} | Identity base exists and should be preserved as the contact/location anchor. |")
lines.append(f"| Message log rows | {total_msgs} | Sufficient live evidence to reason from communication behavior. |")
lines.append(f"| Inbound capture rows | {total_inbound_capture} | Raw inbound queue exists and is being populated. |")
lines.append(f"| Unprocessed inbound captures | {unprocessed_inbound} | Active backlog/replay hygiene problem. |")
lines.append(f"| Message send error rows | {counts.get('message_send_errors', 0)} | Error ledger exists and is useful. |")
lines.append(f"| System error rows | {counts.get('system_errors', 0)} | Global execution errors are underpopulated compared with expected workflow complexity. |")
lines.append(f"| Appointment rows | {counts.get('appointments', 0)} | Confirms appointment ledger remains empty while communication tables are active. |")
lines.append('')
lines.append('## Communication-status pattern')
lines.append('')
lines.append('| Direction | Delivery status | Rows | Missing GHL message ID | Missing GHL conversation ID | Latest timestamp |')
lines.append('| --- | --- | ---: | ---: | ---: | --- |')
for row in msg_status:
    lines.append(f"| {row.get('direction')} | {row.get('delivery_status')} | {row.get('ct')} | {row.get('missing_ghl_message_id')} | {row.get('missing_ghl_conversation_id')} | {row.get('latest_at')} |")
lines.append('')
lines.append(f"The key communication-log asymmetry is that inbound `message_log` rows currently lack GHL message and conversation IDs ({inbound_msg_missing_ghl} inbound rows), while sent and delivered outbound rows generally carry GHL identifiers. This means outbound delivery observability is stronger than inbound provenance. There are also {outbound_queued_missing_ghl} queued outbound rows missing a GHL message ID, which should be separated into expected pre-send queue rows versus failed/abandoned send attempts before any broad fix is attempted.")
lines.append('')
lines.append('## Inbound-capture pattern')
lines.append('')
lines.append('| Source | Processed | Rows | Missing identity | Missing GHL message ID | Oldest | Newest |')
lines.append('| --- | --- | ---: | ---: | ---: | --- | --- |')
for row in inbound_status:
    lines.append(f"| {row.get('source')} | {row.get('processed')} | {row.get('ct')} | {row.get('missing_identity')} | {row.get('missing_ghl_message_id')} | {row.get('oldest_at')} | {row.get('newest_at')} |")
lines.append('')
lines.append(f"The raw capture table has no orphaned contact/location identities in this audit, which is good. The risk is operational: {unprocessed_inbound} captures remain unprocessed, and both the backfill and replay workflows are inactive. Processed captures also lack stored GHL message IDs in the audited rows, so replay/backfill idempotency depends on payload content rather than a clean top-level ID.")
lines.append('')
lines.append('## Error pattern')
lines.append('')
lines.append('| Classification | HTTP status | GHL error code | Rows | Latest |')
lines.append('| --- | --- | --- | ---: | --- |')
for row in error_summary:
    lines.append(f"| {row.get('classification')} | {row.get('http_status')} | {row.get('ghl_error_code')} | {row.get('ct')} | {row.get('latest_at')} |")
lines.append('')
lines.append(f"The current send-error ledger points first to **SMS cap governance** ({cap_hit_errors} rows) and then terminal/invalid phone handling ({invalid_or_terminal} rows). This is actually a positive sign: communication failure modes are being classified and can be turned into product rules. The more concerning issue is that `system_errors` contains only {counts.get('system_errors', 0)} rows, both resolved warnings/tests, which suggests the global error surface may not be receiving all production failures or has not been exercised enough to trust as a complete control plane.")
lines.append('')
lines.append('## Conversation-context pattern')
lines.append('')
lines.append('| Context metric | Count |')
lines.append('| --- | ---: |')
for key in ['total_contexts','has_last_intent','has_conversation_summary','has_next_action','appointment_offered','appointment_booked','appointment_pending_slot']:
    lines.append(f"| {key} | {context_health.get(key, 0)} |")
lines.append('')
lines.append('Conversation context has summaries and last intents for most rows, but `next_action` is empty across the audited set. That matters because a working assistant/orchestrator needs not only memory of what happened, but an explicit forward state: what should happen next, when, and why. This does not need to be fixed before appointment-ledger hardening, but it belongs in the second-wave planning backlog because it affects orchestration quality.')
lines.append('')
lines.append('## Sprint implications')
lines.append('')
lines.append('| Sprint implication | Evidence | Recommended sequencing |')
lines.append('| --- | --- | --- |')
lines.append('| Appointment ledger is still a first repair candidate. | Appointment table is empty while communication ledgers are populated and observable. | Keep as Sprint 1 or Sprint 1B after control-plane setup. |')
lines.append('| Inbound replay/backfill deserves a near-term sprint. | 31 unprocessed inbound captures; inactive replay/backfill workflows; inbound message IDs not promoted cleanly. | Sprint 2 after appointment ledger or immediately after workflow control plane if developer wants a communications sprint. |')
lines.append('| Outbound send-error handling is a reusable pattern. | Cap-hit and carrier failures are classified in `message_send_errors`; status workflows update `message_log`. | Reuse this architecture for appointment mirror failures. |')
lines.append('| Global execution error logging may be incomplete. | Only two `system_errors` rows, both resolved warnings/tests. | Add to control-plane/hardening sprint, not as a standalone first fix. |')
lines.append('| Forward orchestration state is thin. | `conversation_context.next_action` is empty across audited contexts. | Later sprint after transport ledgers are reliable. |')
lines.append('')
lines.append('## Files generated')
lines.append('')
lines.append('| File | Purpose |')
lines.append('| --- | --- |')
lines.append('| `data/supabase/communication_log_audit_clean.json` | Clean structured evidence from the read-only communication-log query. |')
lines.append('| `data/supabase/communication_log_audit_raw.json` | Raw MCP query result retained for traceability. |')
lines.append('| `data/supabase/comm_schema_columns.txt` | Exact table-column reference used to write the query safely. |')
lines.append('')
md_path.write_text('\n'.join(lines) + '\n')
print(f'Wrote {clean_path}')
print(f'Wrote {md_path}')
