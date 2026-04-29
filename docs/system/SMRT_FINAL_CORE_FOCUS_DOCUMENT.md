# SMRT Final Core Focus Document

Author: **Manus AI**  
Date: **2026-04-29**  
Status: **Single working document for developer alignment and next-sprint planning**

## Executive summary

SMRT is now understandable enough to manage as a sequence of bounded repairs rather than as a single tangled failure. The audits show a system with real structure: GoHighLevel handles external CRM, SMS, conversation, and calendar state; n8n on Hostinger orchestrates workflows and tool calls; Supabase is intended to operate as the local reasoning ledger for leads, conversations, appointments, messages, prompt state, and errors.[1] [2] The core problem is not that nothing works. The core problem is that several critical crossings between systems are **not yet observable, ledger-backed, or contractually clear**.

The safest working posture is to keep the plan small. The team should first establish the workflow control plane, then harden one high-signal behavioral path, then widen into communication replay and prompt-injection observability. This keeps us from trying to fix GHL, n8n, Supabase, memory, prompts, and conversations all at once.

> **Final operating principle:** We are not trying to “fix the whole system.” We are building a trustworthy operating model one contract at a time: versioned workflow source, explicit external IDs, durable local ledgers, visible failure records, and metadata proving what each workflow actually injected, mirrored, or skipped.

## Core focus map

The table below is the single-page map of what matters now. It separates the focus areas, why each one matters, what appears broken or incomplete, and what should happen next.

| Priority | Core focus | Why it matters | Current issue | Recommended next action |
|---:|---|---|---|---|
| 0 | **Workflow control plane** | No production workflow repair is safe unless the team can pull, validate, deploy, roll back, and verify changes. | Workflow JSON is now in Git and locally valid, but live Hostinger/n8n pull/deploy/rollback is not installed. | Have the developer implement the control-plane handoff before behavioral fixes. |
| 1 | **Appointment ledger hardening** | Appointment booking crosses GHL, n8n, and Supabase, making it the best first proof of the full repair loop. | GHL booking can succeed while the local `appointments` table remains empty or the Supabase insert fails silently. | Add durable appointment mirroring and mirror-failure logging. |
| 2 | **Inbound capture replay and backfill** | Communication logs are the richest behavioral evidence for broken system components. | There are unprocessed inbound captures and weaker inbound provenance than outbound provenance. | Build an idempotent replay/backfill path after the control plane is safe. |
| 3 | **GoHighLevel identity contract** | GHL is an external state source, not merely a send channel; IDs must map cleanly into Supabase. | Contact, conversation, message, location, and appointment IDs are not yet expressed as a single written contract. | Define and enforce the GHL-to-Supabase ID contract. |
| 4 | **Error and mirror-failure ledger** | Silent failures are the main reason the system feels half-baked and hard to trust. | `system_errors` is thin relative to workflow complexity, and critical mirror failures are not consistently recorded. | Create a standard failure taxonomy and durable failure ledger. |
| 5 | **LLM injection observability** | The Brain Engine may receive a base prompt while missing context, history, static sections, personality, or prompt blocks. | The AI Agent appears wired to `systemPrompt`, but there is no prompt assembly manifest proving what was included per run. | Add metadata-only prompt assembly telemetry before rewriting prompts. |
| 6 | **Conversation mirror and forward state** | NA/NAN needs stable local conversation state to reason across messages and decide next actions. | Conversation summaries, `next_action`, and forward-state fields are inconsistent or thin. | Address after inbound replay and identity contract are clearer. |

## Focus 0: Workflow control plane

The workflow control plane is the foundation. The repository now contains the sanitized n8n workflow working set, split into active and inactive workflows, with a local static validator and manifest.[3] That means we can inspect and reason about workflow JSON in Git. It does **not** yet mean we should push workflow changes directly into the active Hostinger/n8n instance.

The missing operational pieces are live pull, manual deploy, rollback, credential handling, activation-state preservation, and post-deploy verification. Without those, a developer could fix one problem while creating a new invisible one in production. This focus is therefore Sprint 0, not because it is glamorous, but because it prevents the rest of the work from becoming guesswork.

| Control-plane requirement | Current status | Issue if skipped |
|---|---|---|
| Versioned workflow JSON | Present in repo. | Without this, changes are not reviewable. |
| Static validation | Present locally. | Without this, malformed workflow JSON can enter review. |
| Live pull from n8n | Not yet installed. | Repo may drift from production. |
| Manual deploy to n8n | Not yet installed. | Fixes cannot be applied repeatably. |
| Rollback path | Not yet installed. | A bad workflow change can strand production. |
| Post-deploy verification | Defined conceptually, not automated. | The team cannot prove a fix worked. |

The developer meeting should start here. If the developer currently edits directly in n8n, that does not make him wrong; it means the next ask should be to help move the project into a safer Git-first operating mode before changing behavior.

## Focus 1: Appointment ledger hardening

Appointment booking keeps surfacing because it is the cleanest behavioral test path. It spans GHL calendar state, the Brain Engine/tool layer, and Supabase persistence. The expectation is simple: if a booking occurs, the local system should either have a durable appointment row or a durable mirror-failure record that explains why the row was not created.[1] [2]

The audit found that the local `appointments` ledger is not reflecting the booked appointment behavior being discussed. The workflow evidence indicates that appointment booking occurs through GHL first, while the Supabase appointment insert is effectively a best-effort local side effect. That creates a dangerous split-brain condition: GHL can know that an appointment exists while Supabase, NA/NAN, and our audit surfaces do not.[1]

| Issue | Why it is serious | Fix pattern |
|---|---|---|
| Empty or incomplete local `appointments` ledger | The local reasoning layer cannot see booked commitments. | Create/update appointment rows after GHL booking succeeds. |
| Silent Supabase insert failure | The system can appear successful while local truth is false. | Write explicit mirror-failure rows when local persistence fails. |
| External event ID not guaranteed locally | Reconciliation becomes fragile. | Store GHL appointment/event ID and contact ID in the local ledger. |
| No simple acceptance evidence | Developer/user cannot tell whether the repair worked. | Book one controlled appointment and verify GHL + Supabase before/after evidence. |

This is the right first behavioral sprint because it is bounded, testable, and reusable. Once appointment mirroring is hardened, the same pattern can be applied to inbound messages, conversation mirrors, and other GHL-derived objects.

## Focus 2: Communication logs, inbound replay, and backfill

The communication logs make the system look uneven rather than dead. The audit found meaningful logged activity, including populated `message_log` and `inbound_capture` records, but also unprocessed inbound captures and weak inbound provenance relative to outbound provenance.[4] This suggests that the system is receiving communication activity, but not always promoting it into complete local state.

The practical implication is that the communication logs likely contain the fuller story of broken components, but they should not become the first live workflow surgery. They are better suited as Sprint 2, after the control plane and one bounded mirror repair prove the operating loop.

| Communication-log issue | Interpretation | Sprint implication |
|---|---|---|
| Unprocessed inbound captures | Raw webhook capture is ahead of downstream processing. | Build replay/backfill so old captures can be safely reprocessed. |
| Inbound provenance weaker than outbound provenance | Incoming messages may be harder to dedupe, trace, or reconcile. | Preserve GHL message/conversation IDs wherever available. |
| Outbound send-error logging is stronger | The system already has a partial pattern for observability. | Reuse this pattern for inbound and mirror failures. |
| Sparse global error records | Workflow-level failures may be happening outside the visible error ledger. | Add standard error writes around critical crossings. |

This focus should produce a replayable queue discipline. Inbound captures should be idempotent, traceable, and safely promotable into message and conversation state without duplicating records.

## Focus 3: GoHighLevel identity contract

GoHighLevel should be treated as an external state source. It appears to own or originate important contact, conversation, SMS, and calendar information. Supabase does not need to replace GHL, but it does need enough mirrored identifiers and state to allow the local intelligence layer to reason truthfully.[2]

The current issue is not simply that GHL exists outside the database. The issue is that the contract between GHL IDs and local Supabase rows is not yet written as a single enforceable model. Without that model, every workflow can make slightly different assumptions about contacts, leads, conversations, messages, and appointments.

| Object | GHL-side concern | Supabase-side concern | Contract needed |
|---|---|---|---|
| Contact | External person/customer identity. | Local lead/contact mapping. | One canonical mapping from GHL contact ID to local lead/contact row. |
| Conversation | External thread context. | Local conversation context and message state. | Store and reuse GHL conversation IDs where available. |
| Message | External inbound/outbound message. | Local logs, dedupe, replay, delivery state. | Preserve GHL message IDs and direction. |
| Appointment | External calendar event. | Local appointment ledger and reasoning state. | Store GHL event/appointment ID and local mirror status. |
| Location/account | GHL sub-account boundary. | Local tenant or operating boundary. | Make location ID handling explicit. |

This should not be handed to the developer as “fix GHL.” It should be handed as a contract-definition and enforcement task after the appointment-ledger pattern has been proven.

## Focus 4: Error and mirror-failure ledger

The recurring pattern across the audits is not simply missing data. It is **missing evidence about why data is missing**. A workflow can receive a webhook, attempt a GHL call, assemble a prompt, call the model, send a message, or persist to Supabase, and the system still may not leave enough metadata to prove which step failed.[1] [3] [4] [5]

A durable error and mirror-failure ledger is the general solution. It should record critical cross-system failures without storing unnecessary private content. This includes failed GHL-to-Supabase mirrors, failed prompt assembly assumptions, failed message-history parsing, failed inbound promotion, and failed appointment persistence.

| Failure class | Example | Required evidence |
|---|---|---|
| Mirror failure | GHL appointment created but Supabase insert failed. | External ID, local target table, error category, retry status. |
| Replay failure | Inbound capture cannot promote into message log. | Capture ID, reason, dedupe key, retry count. |
| Prompt assembly failure | Message history parse fails and history is dropped. | Parse status, history count, fallback flag, final prompt length. |
| Send failure | Outbound message rejected or undelivered. | Existing send-error pattern plus workflow execution context. |
| Workflow exception | Node-level error or unexpected branch. | Workflow ID, node name, execution ID if available, severity. |

This focus is the connective tissue between the other repairs. It turns “something feels broken” into “this specific crossing failed for this specific reason.”

## Focus 5: LLM injection observability

The LLM injection audit supports your suspicion that prompt delivery may be partial, but the important nuance is that the main AI Agent does appear wired to the assembled `systemPrompt`.[5] The most likely problem is not a totally disconnected prompt. The more likely problem is upstream partial injection: static sections may be inactive, context summaries may be empty, message history may silently fail parsing, prompt blocks may be retrieved without clear inclusion proof, and agent personality/notes/defaults may overlap without an obvious source-of-truth.[5]

The wrong first move would be a major prompt rewrite. The right first move is a metadata-only prompt assembly manifest. Each Brain Engine run should be able to prove which prompt sections, blocks, history, summaries, memory, personality source, fallback flags, and final prompt length were included, without storing raw private messages or full prompt text.

| LLM issue | What may be happening | First fix |
|---|---|---|
| Static sections inactive | Operators may expect sections that are not actually live. | Log included static section keys and counts. |
| Missing prompt manifest | No proof of what reached the model on a given run. | Add non-sensitive prompt assembly telemetry. |
| Context starvation | Base prompt reaches the LLM but recent context is missing. | Log summary length and history count. |
| Message-history parse mismatch | History can be dropped silently if format differs. | Log parse status and fallback flag. |
| Personality ambiguity | Static/default/agent personality sources overlap. | Log canonical personality source. |
| Scheduling contradiction | Scheduling mode may say off while tools remain connected. | Log scheduling mode and connected tool availability. |

This should be treated as Sprint 1B or Sprint 2A. It is important enough to surface before the meeting, but it should not jump ahead of the workflow control plane.

## Focus 6: Conversation mirror and forward state

The conversation layer is where the system eventually becomes intelligent over time. It should know what has happened, what is likely next, what commitments exist, and what NA/NAN should do next. Right now, the evidence suggests that local conversation context and forward-state fields are not yet strong enough to carry that load consistently.[1] [4]

This is a later sprint because it depends on the earlier contracts. Conversation state will remain unreliable if inbound captures are not replayable, GHL conversation IDs are inconsistent, appointment state is missing, and prompt injection cannot prove what context it used.

| Conversation-state issue | Dependency before fixing deeply |
|---|---|
| Thin or empty summaries | Inbound replay and message provenance. |
| Weak `next_action` / forward state | Clear local event ledgers and appointment state. |
| Unclear GHL/local conversation mapping | GHL identity contract. |
| Memory and prompt context ambiguity | LLM injection manifest. |

This focus should not be ignored, but it should not be the first deep implementation target. It is downstream of the mirror, replay, identity, and prompt-observability work.

## Recommended developer-meeting stance

The developer meeting should be framed around establishing a safe execution model, not around debating every defect. The strongest position is to show that we have narrowed the system into focal points, that each focal point has an associated risk, and that the first implementation ask is deliberately small.

| Meeting objective | Exact stance |
|---|---|
| Establish Git-first operations | “We now have workflow JSON in the repo. We need live pull, manual deploy, rollback, and verification before production fixes.” |
| Avoid vague GHL work | “We are not asking you to fix GHL broadly. We need one contract-backed mirror repair first.” |
| Pick the first behavioral repair | “Appointment ledger hardening is the first test because it crosses GHL, n8n, and Supabase with a simple pass/fail.” |
| Surface communication-log evidence | “Inbound replay/backfill is probably the next bigger system issue, but it should follow the first controlled repair.” |
| Surface prompt risk without overreacting | “The LLM appears wired, but prompt assembly is not observable. We need a manifest before a rewrite.” |
| Define ownership | “Developer owns implementation mechanics; we own system model, acceptance criteria, verification, and change log.” |

## Recommended sprint sequence

The sequence below is the final suggested order of attack. It is intentionally narrow at the top and broader later.

| Sprint | Focus | Primary deliverable | Definition of done |
|---:|---|---|---|
| 0 | Workflow control plane | Live pull, manual deploy, rollback, validation, and post-deploy verification. | A workflow can be pulled from n8n, changed in Git, validated, deployed manually, rolled back, and verified. |
| 1 | Appointment ledger hardening | Durable local appointment mirror and mirror-failure logging. | A controlled booking produces either a local appointment row or explicit failure evidence. |
| 1B | LLM injection observability | Metadata-only prompt assembly manifest. | A Brain Engine run records included sections, context counts, fallback flags, personality source, and prompt length. |
| 2 | Inbound replay/backfill | Idempotent replay of unprocessed inbound captures. | Captures can be reprocessed safely without duplicates and with provenance. |
| 3 | GHL identity contract | Written and enforced ID mapping across GHL and Supabase. | Contact, conversation, message, appointment, and location IDs have canonical local fields and validation tests. |
| 4 | Error and mirror-failure ledger | Standard failure taxonomy and local failure records. | Critical crossings write classified failures with retry/reconciliation state. |
| 5 | Conversation mirror and forward state | Stronger summaries, next actions, and conversation state. | NA/NAN can reason from trustworthy local conversation and event state. |

## What to hand the developer

The handoff should be concise. The developer does not need every audit artifact at once. He needs the operating sequence, the first ticket, and the context for why the sequence matters.

| Give him first | Purpose |
|---|---|
| `HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md` | Establishes the safe find → fix → push loop. |
| `SMRT_WORKFLOW_OPERATIONS_READINESS.md` | Explains what exists and what is missing before live deployment. |
| `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` | Defines the first bounded behavioral repair. |
| `GHL_BOUNDARY_AND_HANDOFF_PLAN.md` | Explains why GHL state must be mirrored rather than treated as invisible. |
| `HANDOFF_005_LLM_INJECTION_OBSERVABILITY.md` | Defines the prompt-manifest work without asking for a prompt rewrite. |
| `SMRT_FINAL_CORE_FOCUS_DOCUMENT.md` | This document; the single narrative map for the meeting. |

## Final bottom line

SMRT’s central issue is not one broken table, one bad workflow, or one bad prompt. The central issue is that **critical crossings are not yet controlled by explicit contracts and observable ledgers**. The repair strategy should therefore be contract-first and evidence-first.

The cleanest next move is: **Sprint 0 workflow control plane; Sprint 1 appointment ledger hardening; Sprint 1B LLM injection observability; Sprint 2 inbound replay/backfill.** That sequence keeps the work small, proves the production loop safely, and turns the system from a rat’s nest into a set of inspectable contracts.

## References

[1]: ./SMRT_SCHEMA_WORKFLOW_AUDIT.md "SMRT Schema-Workflow Audit"  
[2]: ./GHL_BOUNDARY_AND_HANDOFF_PLAN.md "GoHighLevel Boundary and Handoff Plan"  
[3]: ./SMRT_WORKFLOW_OPERATIONS_READINESS.md "SMRT Workflow Operations Readiness"  
[4]: ./communication_log_audit_findings.md "SMRT Communication Log Audit Findings"  
[5]: ./SMRT_LLM_INJECTION_AUDIT.md "SMRT LLM Injection Audit"  
