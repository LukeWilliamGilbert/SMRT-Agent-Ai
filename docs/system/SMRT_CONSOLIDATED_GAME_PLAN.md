# SMRT Consolidated Game Plan

Author: **Manus AI**  
Date: **2026-04-29**  
Status: **Developer-meeting working document**

## Executive position

SMRT is no longer an unknowable rat’s nest. The current evidence points to a system that has **real working pieces**, especially around outbound message logging and send-error classification, but it does not yet have a reliable enough control plane to make live workflow changes casually. The right move before the developer meeting is to align on a small, disciplined repair sequence: first make the workflow-development loop safe, then use appointment booking as the first bounded production repair, then move into inbound replay/backfill and identity-contract cleanup.[1] [2] [3]

The main planning risk is trying to solve “GHL,” “Supabase,” “n8n,” “conversation memory,” and “appointment booking” as one giant problem. They are connected, but they should not be fixed as one unit. The strongest implementation path is to turn the system into a series of **ledger-backed contracts**: when something important happens in GoHighLevel or n8n, Supabase should record the event, the external IDs, the local state transition, and any mirror failure that prevents the local model from staying truthful.[2] [4]

> **Working principle:** We do not hand the developer a vague mandate to “fix GHL” or “fix the workflows.” We hand him tightly scoped tickets with acceptance tests, while we keep ownership of the system model, priority order, verification evidence, and change log.

![SMRT System Flow](./smrt_system_flow.png)

## What we know now

The system is operating across three main zones. **GoHighLevel** is the external source for contacts, conversations, SMS delivery, calendars, and booked appointment events. **n8n** is the workflow/orchestration layer that receives webhooks, calls tools, routes messages, and performs persistence. **Supabase** is the local operating ledger that should allow NA/NAN and the workflow layer to reason across conversations, leads, appointments, errors, and state without repeatedly rediscovering the same facts.[1] [2]

| Zone | Current role | Evidence-based status | Planning implication |
| --- | --- | --- | --- |
| GoHighLevel | External CRM, SMS, contact, conversation, and calendar system. | Observed workflow calls and API boundaries show that GHL is not merely a delivery channel; it is a source of external state that must be mirrored carefully.[2] | Treat GHL as an external system of record for selected objects, not as a black box. |
| n8n / Hostinger | Active workflow runtime and orchestration layer. | Sanitized workflow JSON is now versioned in Git, but live pull/deploy/rollback automation is not yet installed.[3] | Do not push behavioral fixes until the control-plane runbook and credentials path are agreed. |
| Supabase | Local ledger for leads, messages, conversation context, appointments, errors, and audit state. | Leads and messages are populated; appointments remain empty; system-error logging is thin.[1] [4] | Use Supabase as the truth surface for verification, but harden missing ledgers first. |

## The communication logs changed the picture

The communication-log deep dive makes the system look less broken and more uneven. There are **378 `message_log` rows**, **179 `inbound_capture` rows**, **313 leads**, and **8 send-error rows**, so the system is capturing meaningful communication activity. The problem is that the capture, replay, and forward-state layers are not consistently complete. Inbound messages can remain unprocessed, inbound provenance is weaker than outbound provenance, and global system-error logging is too sparse to trust as a complete failure surface.[4]

| Communication evidence | Current count or pattern | What it means |
| --- | ---: | --- |
| `message_log` rows | 378 | There is enough data to reason from real communication behavior. |
| `inbound_capture` rows | 179 | Webhook capture is active and useful as a raw queue. |
| Unprocessed inbound captures | 31 | There is a real replay/backfill hygiene issue that should become a near-term sprint. |
| `message_send_errors` rows | 8 | Outbound send failures are being classified, which is a good model for future mirror-failure ledgers. |
| `system_errors` rows | 2 | Global workflow-error observability is underdeveloped relative to system complexity. |
| `appointments` rows | 0 | The appointment ledger is still not reflecting booked appointment behavior. |
| `conversation_context.next_action` populated | 0 audited contexts | Forward orchestration state is thin even where summaries and intents exist. |

The most important nuance is that outbound message observability is ahead of inbound observability. Sent and delivered outbound messages generally carry GHL IDs, while audited inbound `message_log` rows do not carry GHL message or conversation IDs. That does not necessarily mean inbound processing is failing completely, but it does mean replay, deduplication, and provenance are weaker than they need to be.[4]

## Why appointment booking is still the right first behavioral repair

The appointment workflow keeps coming up because it is a **high-signal test path**, not because it is the only problem. Appointment booking crosses all three zones: GHL calendar state, n8n tool execution, and Supabase persistence. It also has a clear acceptance test: if an appointment is booked in GHL, the local `appointments` table should show either a durable booking row or a clear mirror-failure record explaining why the row does not exist.[1] [2] [5]

| Reason appointment ledger is first | Explanation |
| --- | --- |
| It is bounded. | The scope can be limited to one tool path and one local ledger. |
| It is testable. | A booked test appointment should result in a known Supabase state. |
| It proves the full loop. | The repair exercises Git, workflow JSON, deployment, GHL, Supabase, and verification. |
| It exposes mirror failures. | If GHL succeeds and Supabase fails silently, the system becomes untruthful. |
| It creates a reusable pattern. | The same mirror-failure pattern can later be applied to inbound replay and conversation mirroring. |

This does not mean the communication logs are less important. The communication logs suggest the **second major repair area** should be inbound replay/backfill, because 31 captured inbound events are unprocessed and the replay/backfill workflows appear inactive. But appointment-ledger hardening is a cleaner first proof that the team can safely change, deploy, and verify a production workflow before taking on a broader communications repair.[3] [4]

## Recommended sprint sequence

The sequence below is intentionally small. It is designed to keep you from trying to fix too many things at once while still giving the developer enough specificity to act. Sprint 0 is the operational prerequisite. Sprint 1 is the first bounded production behavior repair. Sprint 2 is the communication-log repair that likely reveals the fuller story of broken components.

| Sprint | Name | Owner model | Outcome | Primary handoff |
| ---: | --- | --- | --- | --- |
| 0 | Workflow control plane | Developer implements; we verify. | Live pull, manual deploy, rollback, and post-deploy verification are installed before production edits. | `HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md` |
| 1 | Appointment ledger hardening | Developer implements bounded workflow change; we define acceptance tests and verify. | Booked GHL appointments create local `appointments` rows or explicit mirror-failure records. | `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` |
| 2 | Inbound capture replay/backfill | Developer implements after Sprint 0/1; we inspect evidence and prioritize edge cases. | Unprocessed inbound captures are replayable, idempotent, and promoted into message/conversation state. | New handoff to be drafted after the developer meeting. |
| 3 | GHL identity contract | Shared design; developer codifies. | One written contract maps contact, location, lead, conversation, message, and event IDs across GHL and Supabase. | `HANDOFF_002_GHL_IDENTITY_CONTRACT.md` |
| 4 | Error and mirror-failure ledger | Developer implements; we define failure taxonomy. | Workflow and mirror failures are visible in a durable local control surface. | Extend Sprint 1 pattern after appointment repair. |
| 5 | Conversation mirror and forward state | Later shared design sprint. | Conversation state becomes useful for NA/NAN orchestration, including `next_action`. | `HANDOFF_003_GHL_CONVERSATION_MIRROR.md` plus new forward-state spec. |

## Developer meeting agenda

The developer meeting should focus on getting agreement around the operating model rather than debating every defect. The core question is not whether the system has issues; it does. The question is whether the developer can help us establish a safe path for changing live n8n workflows without losing the thread.

| Meeting topic | Question to ask | Desired answer |
| --- | --- | --- |
| Repository workflow JSON | “Can we agree that Git is now the working review surface for sanitized workflow JSON?” | Yes; fixes should be proposed against versioned workflow JSON, not improvised directly in production. |
| n8n/Hostinger control plane | “What are the exact API base URL, credential, import/export method, and rollback path?” | A documented pull/deploy/rollback process before behavior changes. |
| Workflow ownership | “Will you implement from scoped handoff tickets rather than broad system directives?” | Yes; first ticket is control plane, second is appointment ledger. |
| GHL boundary | “Do you agree GHL is an external state source and Supabase needs durable mirrored ledger rows for critical events?” | Yes; no silent side-effect persistence for critical events. |
| Verification | “Can every deployed change include before/after database evidence?” | Yes; verification is part of the definition of done. |

## What to hand the developer tomorrow

The most useful handoff packet is small. The developer should receive the control-plane ticket first because it enables safe work. The appointment-ledger ticket should be framed as the first behavior change, not the entire project. The GHL boundary document provides context but should not be treated as a mandate to redesign everything.

| Give him | Purpose | How to frame it |
| --- | --- | --- |
| `HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md` | Establishes the safe find → fix → push loop. | “Before we change live workflows, we need pull/deploy/rollback and validation.” |
| `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` | Defines the first bounded production repair. | “After control-plane setup, prove the loop on appointment mirroring.” |
| `GHL_BOUNDARY_AND_HANDOFF_PLAN.md` | Explains the GHL/Supabase responsibility boundary. | “This is context for why we are not saying ‘just fix GHL.’” |
| `communication_log_audit_findings.md` | Shows the next likely sprint area. | “The logs point to inbound replay/backfill as the next problem after appointment ledger.” |
| `SMRT_WORKFLOW_OPERATIONS_READINESS.md` | Shows current readiness and missing deployment pieces. | “We are close, but not safe for automatic push-to-n8n yet.” |

## What we should keep owning

You and I should keep ownership of the **working invisible model**. That means we should maintain the system map, the ranked backlog, the evidence ledger, the change log, and the acceptance-test definitions. The developer can absolutely implement, but the system needs product/architecture control so that every fix improves traceability rather than burying another workaround.

| We own | Developer owns |
| --- | --- |
| System narrative and priority order. | Implementation mechanics inside workflow JSON and scripts. |
| Acceptance criteria and verification evidence. | Pull/deploy/rollback tooling and production-safe changes. |
| Cross-system contracts and documentation discipline. | Code-level or workflow-level implementation details. |
| Deciding what not to fix yet. | Estimating effort and exposing technical constraints. |

## Decision tree for tomorrow

If the developer agrees to a Git-first workflow control plane, the next move is straightforward: have him implement or confirm live pull, manual deploy, rollback, and verification. Once that is in place, the appointment-ledger hardening ticket becomes the first behavioral sprint.

If the developer does not agree to the control-plane approach, then we should not ask him to patch production workflows immediately. Instead, we should ask for a fresh export of the live n8n instance, confirmation of the deployment method currently used on Hostinger, and a walkthrough of how GHL credentials, webhook URLs, and workflow activation are managed.

| Developer response | Our next move |
| --- | --- |
| “Yes, I can set up pull/deploy/rollback.” | Proceed with Sprint 0 and schedule appointment-ledger Sprint 1. |
| “I usually edit directly in n8n.” | Pause production fixes and require a documented export/rollback process first. |
| “GHL owns appointments, Supabase does not need them.” | Clarify that Supabase does not need to replace GHL, but it does need a local ledger for NA/NAN reasoning and verification. |
| “The bigger issue is communication logs.” | Agree, then point to Sprint 2; explain that appointment-ledger repair proves the safe deployment loop first. |
| “The repo workflow JSON is stale.” | Request a live pull/export as the first control-plane task before judging any workflow defect. |

## Current bottom line

We are close enough to have a productive developer meeting, but not close enough to push live production fixes blindly. The repo now has workflow JSON, local validation, durable audit docs, GHL boundary mapping, and developer handoff tickets. What is still missing is the production bridge: confirmed Hostinger/n8n API access, live pull, manual deploy, rollback, and post-deploy verification.[3]

My recommendation is to go into tomorrow with one sentence: **“We are building a safe workflow control plane first, then proving it on appointment-ledger hardening, then moving into inbound replay/backfill based on the communication logs.”** That keeps the plan small, concrete, and defensible.

## References

[1]: ./SMRT_SCHEMA_WORKFLOW_AUDIT.md "SMRT Schema-Workflow Audit"
[2]: ./GHL_BOUNDARY_AND_HANDOFF_PLAN.md "GoHighLevel Boundary and Handoff Plan"
[3]: ./SMRT_WORKFLOW_OPERATIONS_READINESS.md "SMRT Workflow Operations Readiness"
[4]: ./communication_log_audit_findings.md "SMRT Communication Log Audit Findings"
[5]: ../handoffs/HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md "Handoff 001: Appointment Ledger Hardening"
