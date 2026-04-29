# SMRT Sprint Priority Matrix

Author: **Manus AI**  
Date: **2026-04-29**

This matrix consolidates the current schema, workflow, GoHighLevel boundary, workflow-operations, and communication-log audit evidence into an implementation sequence for the developer meeting. Scores use a simple 1–5 scale, where **5** means higher user/business impact, higher risk reduction, lower dependency burden, or higher testability. The resulting recommendation favors repairs that create durable observability before broad behavior changes.

| Rank | Sprint candidate | Impact | Risk reduction | Dependency readiness | Testability | Why it belongs here | Primary evidence |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 0 | Workflow control plane hardening | 5 | 5 | 5 | 4 | This is the prerequisite for safe change. The repository now has sanitized workflow JSON and local validation, but it still lacks live pull, manual deploy, rollback, and post-deploy verification against Hostinger/n8n. | `SMRT_WORKFLOW_OPERATIONS_READINESS.md`; `HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md` |
| 1 | Appointment ledger hardening | 5 | 5 | 4 | 5 | This is the cleanest first production behavior fix because it crosses GHL, n8n, and Supabase while remaining bounded and easy to acceptance-test. A booked GHL appointment should produce a durable local ledger row or explicit mirror failure. | `SMRT_SCHEMA_WORKFLOW_AUDIT.md`; `GHL_BOUNDARY_AND_HANDOFF_PLAN.md`; `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` |
| 2 | Inbound capture replay and backfill | 5 | 4 | 3 | 4 | Communication logs show 31 unprocessed inbound captures, inactive replay/backfill workflows, and weak top-level GHL message ID promotion. This likely explains broader “conversation state feels incomplete” symptoms. | `communication_log_audit_findings.md`; workflow manifest |
| 3 | GHL-to-Supabase identity contract | 4 | 5 | 3 | 4 | The system needs one written contract for `contact_id`, `location_id`, `lead_id`, `ghl_conversation_id`, `ghl_message_id`, and `ghl_event_id` before deeper automation is safe. This should follow the first ledger repair so it is grounded in an actual production path. | `HANDOFF_002_GHL_IDENTITY_CONTRACT.md`; `GHL_BOUNDARY_AND_HANDOFF_PLAN.md` |
| 4 | Global system-error and mirror-failure ledger | 4 | 5 | 3 | 4 | `message_send_errors` is useful, but `system_errors` has only two resolved warnings/tests. Critical mirror failures should land in a unified error surface. This belongs with or immediately after the ledger work. | `communication_log_audit_findings.md`; `supabase_gap_audit_findings.md` |
| 5 | Conversation mirror and inbound provenance cleanup | 4 | 4 | 2 | 3 | Inbound `message_log` rows lack GHL message/conversation IDs, even though outbound sent/delivered messages are well linked. This should be handled after replay/backfill and identity rules are clarified. | `communication_log_audit_findings.md`; `HANDOFF_003_GHL_CONVERSATION_MIRROR.md` |
| 6 | Forward orchestration state and `next_action` discipline | 3 | 3 | 2 | 3 | Conversation summaries and last intents exist for most contexts, but `next_action` is empty across the audited set. This affects NA/NAN orchestration quality but should not precede transport/ledger reliability. | `communication_log_audit_findings.md`; `SMRT_SCHEMA_WORKFLOW_AUDIT.md` |
| 7 | Prompt/agent state simplification | 3 | 3 | 2 | 2 | Prompt and agent state may matter, but it is less testable until the event ledgers and communication state are trustworthy. This is a later architecture sprint, not a first repair. | `SMRT_SCHEMA_WORKFLOW_AUDIT.md` |

## Recommended first developer meeting framing

The developer should not be asked to “fix GHL” or “fix the workflows.” The correct handoff is narrower: **install the missing control-plane pieces, then harden the appointment ledger as the first bounded production repair**. If the developer pushes back that communication logs show a broader problem, the response is that the broader communication issue is real, but it becomes Sprint 2 because it depends on replay/backfill discipline and a clearer identity contract.

| Meeting decision | Recommended answer |
| --- | --- |
| Do we change live workflows before the meeting? | No. Keep the current work as audit, planning, and repository preparation. |
| Do we have enough evidence to start implementation? | Yes, for control-plane setup and appointment-ledger hardening. |
| Should we chase every log issue at once? | No. Use appointment booking to prove the safe find → fix → verify loop, then move to inbound replay/backfill. |
| What should the developer receive first? | `HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md` and `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md`. |
| What should we keep owning? | System map, priority order, acceptance criteria, verification results, and change-log discipline. |
