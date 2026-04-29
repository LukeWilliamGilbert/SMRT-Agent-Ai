# HANDOFF 003 — GoHighLevel Conversation and Inbound Mirror

**Prepared by:** Manus AI  
**Date:** 2026-04-29  
**Target implementer:** SMRT developer using Claude or equivalent coding agent  
**Dependency:** Do this after appointment ledger hardening and the GHL identity contract unless a production incident requires immediate message recovery.

## Problem statement

Conversation state appears distributed across GoHighLevel conversations/messages, Supabase `message_log`, Supabase `inbound_capture`, and Supabase `conversation_context`. The exported workflow set also includes inactive `GHL Conversation Backfill` and `Inbound Replay` workflows. The system needs a canonical local message ledger so the Brain Engine has reliable context and operators can inspect what happened without reading raw GHL threads manually.

## Workflows in scope

| Workflow | Role |
| --- | --- |
| `🧠 SMRT Brain Engine` | Sends outbound messages, updates context, and may write message logs. |
| `📬 GHL Delivery Status Handler` | Handles message delivery events and error state. |
| `🔍 GHL Send Status Checker` | Checks GHL message status and updates local logs/errors. |
| `🔍 GHL Conversation Backfill` | Inactive recovery path for historical GHL conversation import. |
| `🔁 Inbound Replay` | Inactive replay surface for inbound capture recovery. |

## Required decision

Before implementing changes, decide and document whether `message_log` is the canonical local message ledger. If it is not, identify the canonical table. If it is, then every inbound, outbound, delivery, failed, replayed, or backfilled GHL message should have an idempotent local representation.

## Required implementation properties

| Requirement | Detail |
| --- | --- |
| Idempotent local messages | Use GHL `messageId`, `conversationId`, `contactId`, and timestamp as dedupe/correlation fields where available. |
| Direction clarity | Distinguish inbound, outbound, delivery-status update, system note, reminder, and replay/backfill records. |
| Error visibility | Failed GHL sends or missing IDs must produce durable errors rather than silent fallbacks. |
| Brain context compatibility | The Brain Engine must be able to retrieve the relevant local message/context history without depending solely on live GHL reads. |
| Backfill safety | Historical imports must not duplicate existing local messages. |

## Acceptance tests

| Test | Expected result |
| --- | --- |
| A new inbound GHL message arrives. | Exactly one canonical local message record is created or updated. |
| The Brain Engine sends an outbound SMS. | Local message state records accepted/sent/failed lifecycle data and GHL IDs where available. |
| A delivery status webhook arrives. | Existing local message row is updated rather than duplicated. |
| Conversation backfill runs for a known contact. | Missing messages are inserted and existing messages are skipped or updated idempotently. |
| A malformed webhook payload arrives. | The workflow records an error/triage event without corrupting local conversation state. |

## Out of scope

Do not redesign the full Brain Engine prompt, add new marketing campaign logic, change appointment booking behavior, or rework onboarding. This ticket is solely about message/conversation mirroring and recovery.

## Completion evidence to return

Return the canonical ledger decision, workflow/node diff or export, sample local rows with sensitive data redacted, and a replay/backfill test proving that duplicate messages are not created.
