# HANDOFF 006 — Prompt System Forensics and Memory Routing

Author: **Manus AI**  
Date: **2026-04-30**  
Status: **Ready for developer intake**  
Primary report: [`docs/system/SMRT_PROMPT_SYSTEM_FORENSIC_AUDIT.md`](../system/SMRT_PROMPT_SYSTEM_FORENSIC_AUDIT.md)

## Purpose

This handoff converts the prompt-system forensic audit into an implementation packet. The core objective is not to rewrite SMRT’s communication prompt first. The core objective is to make the prompt system observable, reduce the final responder’s tool burden, and promote the existing summary node into a reliable structured memory interface.

The audit found that the communicating AI Agent is carrying too many simultaneous responsibilities. It appears to be exposed to fifteen connected tools, whose recovered descriptions total approximately **12,774 characters** before schemas and runtime context. It also receives layered personality, static policy, channel, guardrail, memory, and recent-history instructions. This creates a high-risk architecture where poor behavior can be caused by routing, stale memory, excessive tool load, missing state, or prompt wording, but the system does not yet reliably separate those failure causes.

## Developer Scope

| Workstream | Required Change | Reason |
|---|---|---|
| Prompt observability | Add per-run prompt assembly manifest logging. | Failed turns must show which prompt blocks, conditionals, context fields, and tools were present. |
| Tool routing | Add route-specific tool allowlists before the final responder. | The responder should not digest the full toolbox every turn. |
| Memory architecture | Upgrade `conversation_context` into a structured state packet. | The final responder should rely on summary and structured facts, not full conversation strips. |
| Summary cadence | Add event-triggered summary refresh. | Important facts should not wait until every tenth turn. |
| Responder context | Feed compact state packet plus last 3–5 turns. | Full verbatim history should be reserved for summarizer, recovery, QA, or replay. |
| Replay QA | Add tests for repeated-question, appointment, newsletter, and internal-leak failures. | Prompt tuning should become evidence-based. |

## Implementation Requirements

### 1. Prompt Assembly Manifest

Every AI Agent run should write a metadata-only manifest. The manifest does not need to store the full prompt body if privacy or storage cost is a concern. It should store enough information to reproduce the architecture of the prompt.

| Manifest Field | Description |
|---|---|
| `run_id` | Unique workflow execution or message-run identifier. |
| `contact_id` | GHL/Supabase contact identifier. |
| `direction` | Inbound, outbound, replay, or test. |
| `channel` | SMS, email, social DM, or other. |
| `prompt_sections_included` | Ordered list of static sections included. |
| `conditional_blocks_included` | Ordered list of conditional prompt blocks included. |
| `summary_present` | Boolean showing whether `conversation_summary` was present. |
| `summary_age_seconds` | Age of persisted summary at assembly time. |
| `recent_turn_count` | Number of verbatim turns included. |
| `tool_names_exposed` | Tool names available to the model for this run. |
| `tool_description_chars` | Total characters in exposed tool descriptions. |
| `system_prompt_chars` | Character count of assembled system prompt. |
| `user_prompt_chars` | Character count of user/content prompt. |
| `fallback_flags` | Any missing-data or fallback branches used during prompt assembly. |

### 2. Route-Specific Tool Allowlists

Introduce a watcher/router step before the final response composer. The router should classify the current turn and expose only the tools that route requires. For simple response routes, no write tools should be available to the final responder.

| Route | Tool Allowlist |
|---|---|
| `simple_answer` | No tools; response composer only. |
| `qualification` | No write tools; ask one next question from state packet. |
| `scheduling_offer` | Availability lookup only until the lead selects a time. |
| `book_appointment` | Booking tool only after required preconditions are present. |
| `reschedule_or_cancel` | Reschedule/cancel only after appointment identity is known. |
| `newsletter_consent` | Newsletter subscription only after affirmative consent. |
| `memory_update` | No final-responder tool; extractor/summarizer writes state. |
| `escalation_or_stop` | Escalation marker or silence behavior only. |

### 3. Conversation Context State Packet

The current summary path is valuable and should be expanded. The responder should receive structured memory, not long conversation strips. The table or assembled payload should include the following fields, even if some are initially stored as JSON.

| Field | Required Behavior |
|---|---|
| `conversation_summary` | Durable 250–350 word accumulative summary. |
| `lead_intent` | Buy, sell, both, unknown. |
| `lead_timeline` | Now, three months, six months, one year, unknown. |
| `known_facts` | Structured facts such as area, budget, property type, address, constraints, financing, motivation. |
| `answered_questions` | Normalized answers already supplied by the lead. |
| `last_asked_question` | Most recent question SMRT asked. |
| `open_loops` | Unresolved questions, promised follow-ups, pending appointments, pending newsletter offers. |
| `appointment_state` | None, offered, accepted, booked, rejected, rescheduled, canceled, unknown. |
| `newsletter_state` | Not offered, offered, accepted, declined, subscribed. |
| `summary_source_turn_ids` | Message IDs included in the latest summary. |
| `summary_confidence` | High, medium, low, or numeric confidence. |
| `last_summarized_at` | Timestamp for freshness logic. |

### 4. Event-Triggered Summary Refresh

Keep the existing accumulative summary prompt, but change refresh conditions. Summary should update on high-signal turns, not only at early turns or every tenth turn.

| Trigger | Reason |
|---|---|
| Lead provides or changes buy/sell intent. | Prevents stale qualification state. |
| Lead provides or changes timeline. | Prevents repeated or wrong timeline questions. |
| Lead provides area, budget, property type, address, or financing detail. | Preserves concrete lead facts. |
| Appointment is offered, accepted, rejected, rescheduled, or canceled. | Keeps scheduling state accurate. |
| Newsletter is offered, accepted, or declined. | Prevents repeated newsletter asks. |
| Lead says “I already told you” or equivalent. | Forces memory repair. |
| Internal-reasoning leak is detected. | Creates QA event and hardening signal. |

## Acceptance Criteria

The work is complete only when the team can inspect a failed turn and answer four questions without guessing: what prompt blocks were included, what memory was included, what tools were exposed, and what state writes succeeded or failed.

| Acceptance Criterion | Pass Condition |
|---|---|
| Manifest exists for every AI run. | Logs include prompt sections, conditionals, summary age, recent-turn count, and exposed tools. |
| Tool exposure is route-scoped. | Simple answer and qualification routes do not expose broad CRM/calendar write tools. |
| Summary refresh is event-triggered. | High-signal turns update `conversation_context` even when the turn counter is not divisible by ten. |
| Responder context is compact. | Final responder receives structured memory plus last 3–5 turns, not default last 15+ strips. |
| Repeated-question prevention is explicit. | `last_asked_question` and `answered_questions` are persisted and visible in context packet. |
| Write failures are observable. | Supabase, GHL, and calendar write outcomes are logged with success/failure status. |
| Prompt tuning can be replayed. | Known failed turns can be replayed against captured manifest and state packet. |

## Non-Goals

This handoff should not be interpreted as a request to rewrite all prompt prose immediately. Prompt wording should be tuned after observability and routing changes are in place. This handoff also does not require injecting full historical transcripts into the final responder. Full transcripts should remain available for summarization, replay, recovery, and audit, but they should not be the default response-composition substrate.

## Final Developer Note

Treat the summary node as a first-class memory subsystem. The existing hardwired summary prompt is a useful foundation, but its output needs stronger structure, fresher update triggers, and a cleaner contract with the final response composer. Once the model sees a compact state packet and a narrow route-specific tool set, prompt tuning will become a much more controlled and testable exercise.
