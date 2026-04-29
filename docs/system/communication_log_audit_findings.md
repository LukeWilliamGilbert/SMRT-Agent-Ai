# SMRT Communication Log Audit Findings

Author: **Manus AI**  
Date: **2026-04-29**

## Executive finding

The communication logs do not suggest that everything is broken. They show a system with **partially mature observability**: outbound delivery status and send-error tracking are materially better developed than appointment mirroring, while inbound capture and replay remain the biggest unresolved communication-control gap. The highest-signal problem is not duplicate messages or orphaned identities; it is that inbound events can sit unprocessed and the recovery workflows that would backfill or replay them are currently inactive.

| Metric | Current evidence | Planning interpretation |
| --- | ---: | --- |
| Leads | 313 | Identity base exists and should be preserved as the contact/location anchor. |
| Message log rows | 378 | Sufficient live evidence to reason from communication behavior. |
| Inbound capture rows | 179 | Raw inbound queue exists and is being populated. |
| Unprocessed inbound captures | 31 | Active backlog/replay hygiene problem. |
| Message send error rows | 8 | Error ledger exists and is useful. |
| System error rows | 2 | Global execution errors are underpopulated compared with expected workflow complexity. |
| Appointment rows | 0 | Confirms appointment ledger remains empty while communication tables are active. |

## Communication-status pattern

| Direction | Delivery status | Rows | Missing GHL message ID | Missing GHL conversation ID | Latest timestamp |
| --- | --- | ---: | ---: | ---: | --- |
| inbound | queued | 187 | 187 | 187 | 2026-04-29T20:58:15.115+00:00 |
| outbound | sent | 95 | 0 | 0 | 2026-04-29T22:00:36.685+00:00 |
| outbound | queued | 75 | 74 | 74 | 2026-04-27T19:25:14.257+00:00 |
| outbound | delivered | 17 | 0 | 0 | 2026-04-29T21:00:10.356+00:00 |
| outbound | failed | 4 | 0 | 0 | 2026-04-26T04:12:10.229+00:00 |

The key communication-log asymmetry is that inbound `message_log` rows currently lack GHL message and conversation IDs (187 inbound rows), while sent and delivered outbound rows generally carry GHL identifiers. This means outbound delivery observability is stronger than inbound provenance. There are also 74 queued outbound rows missing a GHL message ID, which should be separated into expected pre-send queue rows versus failed/abandoned send attempts before any broad fix is attempted.

## Inbound-capture pattern

| Source | Processed | Rows | Missing identity | Missing GHL message ID | Oldest | Newest |
| --- | --- | ---: | ---: | ---: | --- | --- |
| webhook | True | 147 | 0 | 147 | 2026-04-25T17:50:20.019422+00:00 | 2026-04-26T23:47:17.426248+00:00 |
| webhook | False | 31 | 0 | 31 | 2026-04-26T01:00:59.532923+00:00 | 2026-04-29T20:58:14.764997+00:00 |
| replay | True | 1 | 0 | 1 | 2026-04-27T19:23:27.693286+00:00 | 2026-04-27T19:23:27.693286+00:00 |

The raw capture table has no orphaned contact/location identities in this audit, which is good. The risk is operational: 31 captures remain unprocessed, and both the backfill and replay workflows are inactive. Processed captures also lack stored GHL message IDs in the audited rows, so replay/backfill idempotency depends on payload content rather than a clean top-level ID.

## Error pattern

| Classification | HTTP status | GHL error code | Rows | Latest |
| --- | --- | --- | ---: | --- |
| cap_hit | null |  | 5 | 2026-04-26T04:12:16.392007+00:00 |
| invalid_number | null | 30005 | 2 | 2026-04-25T21:23:43+00:00 |
| unreachable | null | 30003 | 1 | 2026-04-25T21:07:41.854+00:00 |

The current send-error ledger points first to **SMS cap governance** (5 rows) and then terminal/invalid phone handling (3 rows). This is actually a positive sign: communication failure modes are being classified and can be turned into product rules. The more concerning issue is that `system_errors` contains only 2 rows, both resolved warnings/tests, which suggests the global error surface may not be receiving all production failures or has not been exercised enough to trust as a complete control plane.

## Conversation-context pattern

| Context metric | Count |
| --- | ---: |
| total_contexts | 25 |
| has_last_intent | 23 |
| has_conversation_summary | 23 |
| has_next_action | 0 |
| appointment_offered | 3 |
| appointment_booked | 0 |
| appointment_pending_slot | 0 |

Conversation context has summaries and last intents for most rows, but `next_action` is empty across the audited set. That matters because a working assistant/orchestrator needs not only memory of what happened, but an explicit forward state: what should happen next, when, and why. This does not need to be fixed before appointment-ledger hardening, but it belongs in the second-wave planning backlog because it affects orchestration quality.

## Sprint implications

| Sprint implication | Evidence | Recommended sequencing |
| --- | --- | --- |
| Appointment ledger is still a first repair candidate. | Appointment table is empty while communication ledgers are populated and observable. | Keep as Sprint 1 or Sprint 1B after control-plane setup. |
| Inbound replay/backfill deserves a near-term sprint. | 31 unprocessed inbound captures; inactive replay/backfill workflows; inbound message IDs not promoted cleanly. | Sprint 2 after appointment ledger or immediately after workflow control plane if developer wants a communications sprint. |
| Outbound send-error handling is a reusable pattern. | Cap-hit and carrier failures are classified in `message_send_errors`; status workflows update `message_log`. | Reuse this architecture for appointment mirror failures. |
| Global execution error logging may be incomplete. | Only two `system_errors` rows, both resolved warnings/tests. | Add to control-plane/hardening sprint, not as a standalone first fix. |
| Forward orchestration state is thin. | `conversation_context.next_action` is empty across audited contexts. | Later sprint after transport ledgers are reliable. |

## Files generated

| File | Purpose |
| --- | --- |
| `data/supabase/communication_log_audit_clean.json` | Clean structured evidence from the read-only communication-log query. |
| `data/supabase/communication_log_audit_raw.json` | Raw MCP query result retained for traceability. |
| `data/supabase/comm_schema_columns.txt` | Exact table-column reference used to write the query safely. |

