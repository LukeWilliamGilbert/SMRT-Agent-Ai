# HANDOFF 008: Brain Engine Orchestrator-to-Responder Renovation

Author: **Manus AI**  
Date: **2026-05-01**  
Status: **Ready for Developer Scoping**  
Production Change: **Workflow architecture change; no direct production deployment should occur without branch review, validation, controlled test traffic, and rollback export**

## Objective

Renovate the active SMRT Brain Engine from a single overloaded customer-facing AI Agent into a **two-layer conversation architecture** while preserving the existing workflow, existing tools, and current operational plumbing as much as possible. The target design is intentionally narrow: repurpose the existing `AI Agent` node as a low-temperature **orchestrator** that keeps the current tool surface and emits a strict JSON handoff packet, then add a downstream **responder LLM** that has no tools and writes the final customer-facing SMS or email from that packet.

This handoff is designed to be machine-ready for a developer AI agent. It names the exact workflow file, exact current nodes, exact connection path to modify, required packet schema, scheduling-state contract, implementation sequence, validation tests, observability requirements, and rollback procedure. The developer should treat this as an implementation specification, not as a prompt-writing essay.

> The core architectural premise is that the existing Brain Engine failure mode is **architectural overload**, not merely imperfect prompt prose. The current customer-facing `AI Agent` is exposed to fifteen connected tools while also being responsible for CRM/memory decisions, scheduling decisions, compliance, routing, and final customer copy.[1] The remediation is therefore to **move final-message composition out of the tool-connected agent**, not to rebuild the workflow from scratch.

## Non-Negotiable Scope Boundaries

The renovation must be **minimally invasive**. The existing `AI Agent` should remain the operational spiderweb agent, and its attached tools should remain attached during the first pass. The change is that its output is no longer final customer prose; its output becomes a structured JSON packet consumed by a new downstream responder. This avoids a full workflow rebuild while creating a clean prompt-tuning surface for voice, warmth, and customer-facing phrasing.

| Boundary | Required Rule | Reason |
|---|---|---|
| Existing workflow | Modify `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json` only after branch review. | This is the active 174-node Brain Engine workflow under audit.[2] |
| Existing tool hub | Preserve current tools attached to `AI Agent`. | The orchestrator still needs CRM, GHL, scheduling, memory, newsletter, and retrieval capabilities.[2] |
| Final response responsibility | Remove from `AI Agent`; assign to new responder LLM. | The responder should not spend attention on tool descriptions or operational state transitions.[1] |
| Scheduling decisions | Keep with orchestrator. | Booking, rescheduling, cancellation, and availability checks are operational decisions and may require tools. |
| Scheduling language | Move to responder through `scheduling_state`. | The responder should phrase the final message without guessing appointment state. |
| Prompt tuning surface | Future voice/personality tuning belongs primarily in the responder prompt. | Tool prompts can remain mechanical because they no longer bear character. |
| Full rebuild | Explicitly out of scope. | This handoff is a renovation of the existing Brain Engine path, not a new system. |

## Current-State Evidence

The current active workflow file is `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json`. The generated current-state evidence confirms the workflow name is `🧠 SMRT Brain Engine`, with **174 nodes** and **137 connection sources**.[2] The primary LLM path currently routes `Gather Prompt Data` into `Assemble System Prompt`, then into `AI Agent`, then into `Analyze Conversation`, summary persistence, action determination, channel routing, send nodes, and outbound logging.[2]

| Current Node | Type | Current Role | Renovation Role |
|---|---|---|---|
| `Assemble System Prompt` | `n8n-nodes-base.code` | Builds a large mixed system prompt with context, tool-critical rule, tier directive, newsletter directive, summary, recent messages, personality, and static behavior sections.[3] | Replace or fork into an orchestrator-specific prompt assembly that asks for strict JSON rather than final customer prose. |
| `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | Current communicating agent; receives `$json.systemPrompt` and `$json.userMessage`; connected to 15 tools; outputs customer-facing prose.[2] | Repurpose as `orchestrator`; keep tools; output only strict JSON handoff packet. |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | Reads output after `AI Agent` and extracts summary, intent, timeline, appointment/newsletter flags, and leak signals.[2] | Move downstream of responder or modify its input so it analyzes the actual final response, not the JSON packet. |
| `Determine Action` | `n8n-nodes-base.code` | Reads `$('AI Agent').first().json.output` as response text after Supabase context update.[2] | Read final response from responder output or a normalized `responseText` field. |
| `Route by Channel1` | `n8n-nodes-base.switch` | Routes SMS/email based on `Assemble System Prompt` context and memory preferences.[2] | Preserve. It should not need to know about the two-layer LLM split. |
| `Send SMS` | `n8n-nodes-base.httpRequest` | Sends `$json.responseText || $('AI Agent').first().json.output` to GHL.[2] | Send `$json.responseText`, with no fallback to orchestrator JSON. |
| `Send Email` | `n8n-nodes-base.httpRequest` | Builds email from `$json.responseText || $('AI Agent').first().json.output`.[2] | Build email from responder output only. |
| `Log Outbound Message` | `n8n-nodes-base.supabase` | Logs `$('Silence Gate').first().json.responseText || $('AI Agent').item.json.output`.[2] | Log responder output and optionally store orchestrator packet metadata separately. |

The current prompt assembly already gathers many fields that should become structured packet inputs: `agentName`, `coordinatorName`, `marketName`, `timezone`, `direction`, `channel`, `firstName`, `contactId`, `locationId`, `pipelineStage`, `intentLevel`, `tier`, `userMessage`, `conversationSummary`, `relationshipType`, `marketRole`, `intentTopic`, `openLoop`, `contactPreference`, `shortSummaryNote`, newsletter flags, splinter fields, `leadTemp`, `leadIntent`, `calendarId`, `ghlUserId`, `messageHistory`, `personalityPrompt`, `agentNotes`, `agentId`, and `leadId`.[4]

## Current Connection Path to Modify

The current high-signal path should be treated as the target insertion lane. The developer should avoid broad node movement unless n8n requires it for wiring clarity.

| Step | Current Path | Required Renovated Path |
|---:|---|---|
| 1 | `Gather Prompt Data` → `Assemble System Prompt` | Preserve upstream context gathering. |
| 2 | `Assemble System Prompt` → `AI Agent` | Change prompt contract so `AI Agent` emits JSON packet only. |
| 3 | `AI Agent` → `Analyze Conversation` | Replace with `AI Agent` → **packet validation/normalization** → **Responder LLM** → `Analyze Conversation`. |
| 4 | `Analyze Conversation` → `Summary Exists?` → `Update Conversation Context` / `Insert Conversation Context` | Preserve, but ensure the analyzer sees final responder text plus current lead message. |
| 5 | `Update/Insert Conversation Context` → `Determine Action` | Preserve, but `Determine Action` must read normalized responder output. |
| 6 | `Determine Action` → `Outbound Bypass?` → `Route by Channel1` | Preserve. |
| 7 | `Route by Channel1` → `Send SMS` / `Send Email` → `Log Outbound Message` | Preserve channel delivery, but remove `AI Agent` output fallbacks. |

## Required Target Architecture

The renovated Brain Engine should have two LLM responsibilities with a hard contract between them. The orchestrator is deterministic, tool-capable, state-bearing, and non-customer-facing. The responder is tool-less, personality-bearing, and customer-facing.

| Layer | Node Recommendation | Tool Access | Temperature | Primary Output | Failure Rule |
|---|---|---:|---:|---|---|
| Orchestrator | Existing `AI Agent` node, optionally renamed only after stable deployment to `AI Agent - Orchestrator`. | Keep all current tools. | `0` or nearest available low setting. | Strict JSON handoff packet. | If it cannot decide, return `degraded_state` and `response_goal`, not customer prose. |
| Packet validator | New code node such as `Validate Orchestrator Packet`. | None. | Not applicable. | Normalized packet fields and `orchestrator_packet_valid`. | If JSON invalid, create safe degraded packet and route to repair/fallback. |
| Responder input builder | New code or set node such as `Build Responder Input`. | None. | Not applicable. | Compact prompt and packet for responder. | Never include tool descriptions. |
| Responder | New OpenAI chat node such as `Responder LLM`. | None. | Warmer than orchestrator, e.g. `0.5–0.8` for SMS voice. | Final customer-facing text only. | If packet says `should_send=false`, output empty or route to no-send according to existing silence gate policy. |

The first implementation can use one added responder LLM plus one validation code node. If the developer can enforce strict structured output directly in the `AI Agent` node and reliably parse it without a code validator, the validation code node may be thinner; however, the handoff contract must still be validated before the responder sees it.

## Orchestrator Handoff Packet Contract

The orchestrator must return **only valid JSON**, no Markdown fences, no customer-facing text outside JSON, and no explanatory prose. The output object must be deterministic enough that the responder never has to infer scheduling state, CRM state, tool outcomes, or safety constraints from hidden reasoning.

### Top-Level JSON Schema

```json
{
  "schema_version": "orchestrator_packet.v1",
  "packet_id": "string",
  "created_at": "ISO-8601 timestamp",
  "source_workflow": {
    "workflow_name": "SMRT Brain Engine",
    "workflow_file": "workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json",
    "orchestrator_node": "AI Agent"
  },
  "conversation_ref": {
    "direction": "inbound|outbound",
    "channel": "sms|email|instagram|unknown",
    "contact_id": "string",
    "location_id": "string",
    "lead_id": "string|null",
    "agent_id": "string|null",
    "first_name": "string",
    "timezone": "IANA timezone string",
    "today_local": "human-readable local date"
  },
  "classification": {
    "primary_intent": "schedule|reschedule|cancel|qualify|ask_question|pricing|property_interest|newsletter|channel_switch|opt_out|hostile|emotional|turnaround|outbound_touch|unknown",
    "secondary_intents": ["string"],
    "lead_intent": "buy|sell|both|rent|invest|unknown",
    "lead_timeline": "now|3_months|6_months|1_year|unknown",
    "lead_temperature": "hot|warm|cold|unknown",
    "tier": "standard|normal|tier_1_confused|tier_2_hostile|tier_3_optout|emotional|turnaround|other",
    "confidence": 0.0
  },
  "memory_context": {
    "conversation_summary": "string",
    "relationship_type": "string|null",
    "market_role": "string|null",
    "intent_level": "string|null",
    "intent_topic": "string|null",
    "open_loop": "string|null",
    "contact_preference": "sms|email|phone|unknown|null",
    "short_summary_note": "string|null",
    "recent_messages_used": [
      {
        "role": "lead|agent|system|unknown",
        "time": "ISO-8601 timestamp|null",
        "text_excerpt": "string"
      }
    ]
  },
  "verified_facts": [
    {
      "fact": "string",
      "source": "lead_message|conversation_context|message_log|ghl_contact|getAppointments|getAvailableSlots|kb|agent_config|tool_result|workflow_context",
      "confidence": "high|medium|low"
    }
  ],
  "tool_activity": {
    "tools_considered": ["string"],
    "tools_called": [
      {
        "name": "string",
        "purpose": "string",
        "status": "success|failed|skipped",
        "safe_summary": "string",
        "error_summary": "string|null"
      }
    ],
    "writes_performed": [
      {
        "system": "supabase|ghl|calendar|other",
        "operation": "string",
        "status": "success|failed|unknown",
        "record_ref": "string|null"
      }
    ]
  },
  "scheduling_state": {
    "mode": "off|discovery|qualification|offer_slots|slot_selection_pending|booking_attempted|booked|reschedule_requested|reschedule_slots_offered|rescheduled|cancel_requested|cancelled|handoff_required|blocked|unknown",
    "should_discuss_scheduling": false,
    "appointment_action_taken": "none|availability_checked|slots_offered|booked|rescheduled|cancelled|notes_added|failed",
    "appointment_status": "none|existing_found|pending_confirmation|confirmed|cancelled|rescheduled|failed|unknown",
    "qualification": {
      "required": false,
      "status": "not_started|in_progress|complete|not_required|blocked|unknown",
      "answered_questions": ["q1", "q2", "q3"],
      "missing_questions": ["q1", "q2", "q3"],
      "next_question_key": "q1|q2|q3|null",
      "next_question_text": "string|null"
    },
    "availability": {
      "timezone": "IANA timezone string",
      "slots_checked": false,
      "slots": [
        {
          "start": "ISO-8601 timestamp",
          "end": "ISO-8601 timestamp|null",
          "label_local": "string"
        }
      ],
      "slot_count": 0,
      "slot_source": "getAvailableSlots|manual|none",
      "constraints_from_lead": ["string"]
    },
    "selected_slot": {
      "start": "ISO-8601 timestamp|null",
      "end": "ISO-8601 timestamp|null",
      "label_local": "string|null",
      "source": "lead_selected|orchestrator_selected|none"
    },
    "appointment": {
      "event_id": "string|null",
      "calendar_id": "string|null",
      "ghl_user_id": "string|null",
      "title": "string|null",
      "start": "ISO-8601 timestamp|null",
      "end": "ISO-8601 timestamp|null",
      "status": "confirmed|cancelled|rescheduled|unknown|null"
    },
    "responder_instruction": "string",
    "must_not_say": ["string"]
  },
  "newsletter_state": {
    "pending_offer": false,
    "opted_in": false,
    "declined": false,
    "action_taken": "none|offered|subscribed|cleared|failed",
    "responder_instruction": "string|null"
  },
  "channel_state": {
    "current_channel": "sms|email|instagram|unknown",
    "requested_channel": "sms|email|phone|instagram|null",
    "switch_action_taken": "none|switched|declined_unsupported|failed",
    "responder_instruction": "string|null"
  },
  "response_directive": {
    "should_send": true,
    "response_goal": "string",
    "tone": "warm|brief|empathetic|professional|low_key|farewell|neutral",
    "length_target": "sms_short|sms_normal|email_short|email_normal",
    "must_include": ["string"],
    "must_not_say": ["string"],
    "allowed_claims": ["string"],
    "question_to_ask": "string|null",
    "call_to_action": "string|null"
  },
  "degraded_state": {
    "is_degraded": false,
    "reasons": ["invalid_tool_result|missing_context|tool_failure|ambiguous_lead_message|unsafe_to_book|other"],
    "safe_fallback_goal": "string|null",
    "requires_human_review": false
  },
  "internal_audit": {
    "orchestrator_reasoning_summary": "one-sentence internal summary, never shown to lead",
    "packet_completeness": "complete|partial|minimal",
    "risk_flags": ["string"]
  }
}
```

### Required Packet Rules

The packet is not an advisory note. It is the only interface between the tool-bearing operational layer and the voice-bearing responder. The responder must not infer hidden operational state when a field is missing. It must follow `response_directive`, `scheduling_state.responder_instruction`, and all `must_not_say` arrays over any softer personality guidance.

| Rule | Requirement | Validation Behavior |
|---|---|---|
| JSON only | The orchestrator output must parse as a single JSON object. | `Validate Orchestrator Packet` fails closed on parse errors. |
| No final prose outside JSON | The orchestrator must not write the customer message directly. | If raw output contains non-JSON wrapper text, strip only if deterministic; otherwise route degraded. |
| Scheduling explicitness | Scheduling state must be in `scheduling_state`, even when no scheduling is active. | Missing `scheduling_state.mode` becomes `unknown` and `degraded_state.is_degraded=true`. |
| Tool transparency | Tool calls and write outcomes must be summarized without secrets. | Store names/statuses only; do not expose API keys, raw headers, or sensitive payloads. |
| No customer leakage | `internal_audit` is never shown to the lead. | Responder prompt must explicitly forbid mentioning packet, tools, CRM, memory, or internal state. |
| Responder no-tools | Responder may not call tools. | Do not attach current tool nodes to `Responder LLM`. |

## Scheduling-State Design Detail

Scheduling is the most important part of the split because it mixes operational state transitions with customer-facing language. The orchestrator owns all decisions that require tools or state mutation: checking existing appointments, checking availability, saving qualifying answers, booking, rescheduling, cancellation, and appointment notes. The responder owns only phrasing.

| Scenario | Orchestrator Responsibility | Required `scheduling_state` | Responder Responsibility |
|---|---|---|---|
| Lead asks for availability | Use `getAvailableSlots` if appropriate and safe. | `mode="offer_slots"`, `appointment_action_taken="availability_checked"`, populated `availability.slots`. | Offer the exact slots in natural language and ask which works. |
| Lead chooses a slot | Validate selected slot and call `bookAppointment` if qualified. | `mode="booked"` or `mode="booking_attempted"`, `appointment_status`, `selected_slot`, `appointment`. | Confirm booking if successful, or gracefully ask for another option if failed. |
| Qualification incomplete | Use `checkQualificationStatus` and `saveQualifyingAnswer` when lead answers. | `qualification.status="in_progress"`, `missing_questions`, `next_question_text`. | Ask exactly the next missing question warmly. |
| Lead wants to reschedule | Use `getAppointments` to find event ID; use `getAvailableSlots`; call `rescheduleAppointment` only after selection. | `mode="reschedule_slots_offered"` or `mode="rescheduled"`. | Phrase options or confirmation without inventing appointment details. |
| Lead wants to cancel | Use `getAppointments`; call `deleteAppointment` if confirmed by policy. | `mode="cancelled"` or `mode="cancel_requested"`, appointment status. | Confirm cancellation or ask for confirmation if needed. |
| Tool fails | Do not pretend booking happened. | `degraded_state.is_degraded=true`, `appointment_action_taken="failed"`, `responder_instruction` explaining safe language. | Apologize lightly and ask for a fallback action without mentioning internal tool failure. |

The responder prompt must include a hard rule: **If `scheduling_state.appointment_status` is not `confirmed`, the responder must not say an appointment is booked. If `availability.slots` is empty, the responder must not invent times. If `qualification.next_question_text` is populated, the responder must ask that exact question unless a higher-priority safety/tier directive overrides it.**

## Node-Level Implementation Instructions

### 1. Work From a Branch and Validate the Baseline

Create a branch before changing workflow JSON. Do not edit production directly. The repository runbook states that GitHub is the working memory, Hostinger/n8n is the runtime, and production deployment requires explicit verification evidence.[5]

| Command | Expected Result |
|---|---|
| `git checkout -b renovate/brain-orchestrator-responder` | Creates isolated branch for workflow JSON and documentation edits. |
| `python3.11 scripts/validate_workflows.py` | Baseline validator passes before edits. |
| `git diff -- workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json` | Empty before edits unless live-pull drift exists. |

### 2. Preserve Upstream Context Gathering

Do not remove the existing nodes that gather agent config, message history, conversation summary, lead memory, prompt blocks, static prompt sections, default personality, or tier response. The current `Gather Prompt Data` node already provides the data needed for both the orchestrator packet and responder prompt.[4]

| Preserve Node | Reason |
|---|---|
| `Get Message History` and `Get Outbound Message History` | Still useful for orchestrator state interpretation and summary. |
| `Get Conversation Summary` and `Get Outbound Conversation Summary` | Main durable memory input. |
| `Get Prompt Blocks (SMRT)` and `Get Static Prompt Sections` | Can still supply behavior constraints, but should be split by layer over time. |
| `Get Default Personality` | Should become responder-facing, not orchestrator-heavy. |
| `Prepare Tier Response` | Still provides tier action context and special response requirements. |
| `Gather Prompt Data` | Already normalizes inbound and outbound paths into common fields. |

### 3. Modify `Assemble System Prompt` Into an Orchestrator Prompt Builder

The current `Assemble System Prompt` output includes `systemPrompt`, `userMessage`, channel fields, IDs, `calendarId`, `ghlUserId`, and other context.[3] For the first pass, keep the return field names so the existing `AI Agent` configuration can continue to read `$json.systemPrompt` and `$json.userMessage`. Change the content of `systemPrompt` so it instructs the current `AI Agent` to behave as an orchestrator and emit the JSON packet contract.

The orchestrator prompt should explicitly remove final-response responsibility. It should say that the agent may call tools as needed, must perform operational decisions, must summarize tool outcomes, and must return only the packet. It should not include personality-heavy prose sections as primary behavior guidance, except where those sections express hard constraints. Personality belongs in the responder prompt.

| Current Prompt Component | First-Pass Handling |
|---|---|
| `## CONTEXT` | Preserve as structured context input for orchestrator. |
| `toolConfig` critical response rule | Replace. The old rule says the tool-using agent must always write a text response; this is now wrong for the orchestrator.[3] |
| `tierDirective` | Keep as operational directive and represent final language requirement in `response_directive`. |
| `newsletterDirective` | Keep operationally; responder phrase goes into `newsletter_state.responder_instruction`. |
| `summaryBlock` | Preserve as memory input. |
| `messageHistoryBlock` | Preserve for orchestrator; consider reducing responder history later. |
| `personalityBlock` | Move primarily to responder input; do not let it compete with orchestrator JSON rules. |
| `STATIC_BASE_PROMPT` | Split hard guardrails from style. Hard guardrails may remain orchestrator-visible; style should be responder-facing. |

### 4. Keep `AI Agent` as the Orchestrator

Do not detach tools from `AI Agent` in the first pass. Current evidence confirms the tools attached to `AI Agent` include `KB Tool`, `searchPastMessages`, `getContact`, `getNotes`, `getAppointments`, `deleteAppointment`, `bookAppointment`, `getAvailableSlots`, `addAppointmentNotes`, `checkQualificationStatus`, `saveQualifyingAnswer`, `rescheduleAppointment`, `updateContactMemory`, `subscribeToNewsletter`, and `switchChannel`.[2] This tool surface is the reason the node is valuable as an orchestrator.

| Current Setting | Required Change |
|---|---|
| `promptType: define` | Preserve. |
| `text: ={{ $json.userMessage }}` | Preserve unless developer creates a new input builder. |
| `options.systemMessage: ={{ $json.systemPrompt }}` | Preserve expression; change upstream prompt content. |
| `options.maxIterations: 10` | Preserve initially. Consider reducing only after traces show unnecessary iterations. |
| Model/temperature | Set to zero or near-zero if exposed through connected model node. |
| Output | Strict JSON packet only. |

### 5. Insert `Validate Orchestrator Packet` Immediately After `AI Agent`

Insert a code node between `AI Agent` and the new responder. This node should parse `$('AI Agent').first().json.output`, validate required fields, normalize booleans and arrays, and attach `orchestrator_packet_valid`, `orchestrator_packet`, and `orchestrator_packet_errors` to the item.

The validator should fail closed. If the packet is invalid, it should create a degraded packet with `degraded_state.is_degraded=true`, `response_directive.should_send=true`, and a safe `response_goal` such as: `Respond briefly and naturally to the lead's latest message without claiming any appointment was booked, without mentioning internal systems, and ask one clarifying question if needed.`

Suggested output fields:

```json
{
  "orchestrator_packet_valid": true,
  "orchestrator_packet_errors": [],
  "orchestrator_packet": { "schema_version": "orchestrator_packet.v1" },
  "responseText": null
}
```

### 6. Add `Build Responder Input`

Add a set or code node that produces a compact responder prompt. It should pass the validated packet, channel, first name, current message, personality prompt, hard guardrails, and relevant recent context. It must not pass tool descriptions, raw tool schemas, API headers, credentials, or internal chain-of-thought.

| Responder Input Field | Source |
|---|---|
| `responderSystemPrompt` | New responder behavior prompt plus hard safety rules. |
| `responderUserPrompt` | Validated `orchestrator_packet` plus latest lead message and optional recent excerpts. |
| `channelType` | Existing context from `Assemble System Prompt`. |
| `contactId`, `locationId`, `direction`, `timezone` | Existing context for downstream nodes. |
| `orchestrator_packet` | Output of validator. |
| `personalityPrompt` | Existing `Get Default Personality` / prompt assembly data, now responder-facing. |

### 7. Add `Responder LLM`

Add a new LLM node after `Build Responder Input`. The exact n8n node type can be the same provider family currently used for `Analyze Conversation` or another supported chat LLM node, but it must not have tool connections. Configure it to return final customer-facing text only. A practical first-pass model can be a capable GPT-class chat model with temperature approximately `0.5–0.8`, with max tokens still controlled by channel.

The responder system prompt should be short, stable, and voice-bearing. It should include rules equivalent to the following:

```text
You write the final customer-facing message for SMRT real estate conversations.
You have no tools. You must not invent facts, appointment times, booking status, pricing, links, or CRM state.
You must obey the orchestrator packet exactly.
Use response_directive.must_include, response_directive.must_not_say, scheduling_state.responder_instruction, newsletter_state.responder_instruction, and channel_state.responder_instruction.
If scheduling_state.appointment_status is not confirmed, do not say an appointment is booked.
If scheduling_state.availability.slots is empty, do not offer specific times.
Do not mention tools, packets, CRM, memory, workflow, internal state, or summaries.
Return only the message text to send to the lead. No JSON, no markdown, no explanation.
```

### 8. Rewire `Analyze Conversation`

The current `Analyze Conversation` node receives input from `AI Agent`.[2] After the renovation, it must receive the final responder output, not the orchestrator JSON. Either rewire it as `Responder LLM` → `Analyze Conversation`, or introduce a normalization node such as `Normalize Final Response` before analysis.

The `Analyze Conversation` prompt currently extracts summary, lead intent, lead timeline, appointment signals, newsletter signals, and internal leak detection.[2] Preserve the node and its downstream persistence. The key change is its input source: it must analyze the lead’s latest message and the responder’s final customer-facing message.

### 9. Update `Determine Action`

The current `Determine Action` code explicitly reads `$('AI Agent').first().json.output` as the response text.[2] Replace that read with the responder output. The normalized downstream item should expose `responseText` so the rest of the path can remain stable.

Required logic:

```javascript
let responseText = '';
try { responseText = $('Responder LLM').first().json.output || ''; } catch(e) {}
if (!responseText) responseText = input.responseText || input.output || input.text || input.response || '';
```

Do not leave `$('AI Agent').first().json.output` as a fallback in this node after the split. If that fallback remains, the system can accidentally send the orchestrator JSON packet to the lead.

### 10. Update `Send SMS`, `Send Email`, and `Log Outbound Message` Fallbacks

The current delivery and logging nodes still fall back to `$('AI Agent').first().json.output`.[2] After the renovation, any fallback to `AI Agent` output is unsafe because `AI Agent` output is JSON. Replace all customer-visible and message-log response fallbacks with normalized responder text only.

| Node | Current Unsafe Expression | Required Rule |
|---|---|---|
| `Send SMS` | `message: $json.responseText || $('AI Agent').first().json.output` | Use `$json.responseText` or `$('Responder LLM').first().json.output`; never `AI Agent`. |
| `Send Email` | `const raw = $json.responseText || $('AI Agent').first().json.output` | Use responder output only. |
| `Log Outbound Message` | `$('Silence Gate').first().json.responseText || $('AI Agent').item.json.output` | Log final responder text, not orchestrator JSON. |

## Responder Prompt-Tuning Surface

Future prompt tuning should happen mainly in the responder prompt and responder input builder. This is the operational value of the split: the developer can tune warmth, brevity, empathy, objection handling, SMS style, and email style without disturbing the tool-calling orchestrator.

| Prompt Surface | Future Owner | Intended Content |
|---|---|---|
| Orchestrator prompt | Engineering / workflow maintainer | JSON contract, tool use policy, state extraction, scheduling operations, degraded-state handling. |
| Tool descriptions | Engineering / workflow maintainer | Mechanical descriptions, required inputs, write safety, and when-to-use criteria. |
| Responder prompt | Prompt/voice maintainer | Personality, channel style, warmth, objection phrasing, brevity, customer-facing constraints. |
| Static prompt sections | Split over time | Hard guardrails stay orchestrator-visible; voice/style sections move responder-facing. |

## Observability Requirements

The split should make debugging easier. Do not deploy without logging or at least surfacing enough metadata to know whether failures came from orchestration, packet validation, response composition, or delivery.

| Field | Where to Capture | Purpose |
|---|---|---|
| `orchestrator_packet_valid` | Validator output and execution log. | Detect JSON contract failures. |
| `orchestrator_packet_errors` | Validator output. | Diagnose missing/invalid fields. |
| `schema_version` | Packet. | Allow future schema migration. |
| `primary_intent` | Packet metadata. | Compare routing classification against outcomes. |
| `scheduling_state.mode` | Packet metadata. | Audit scheduling behavior without reading full prose. |
| `tools_called[].name/status` | Packet metadata. | Trace operational tool decisions. |
| `degraded_state.is_degraded` | Packet metadata. | Quantify fallbacks and context gaps. |
| `responder_output_length` | Normalization node. | Detect empty or excessive output. |
| `responseText_source` | Normalization node. | Confirm final text came from responder. |

If a new table is out of scope, store these fields in workflow execution data and consider adding a later observability ticket. Do not block the first renovation solely on perfect analytics storage, but do require enough execution-log visibility for controlled tests.

## Acceptance Tests

The implementation is not complete until these tests pass on a controlled branch and, after explicit approval, against controlled runtime traffic. Use test contacts and avoid production leads until rollback is available.

| Test | Input Scenario | Expected Orchestrator Packet | Expected Responder Output | Failure Condition |
|---|---|---|---|---|
| Basic inbound question | Lead asks a normal real estate question. | `primary_intent="ask_question"`, no scheduling action unless needed. | Natural answer, no JSON, no tool/internal mention. | Sends packet JSON or mentions tools. |
| Availability request | Lead asks, “Can I see it this week?” | `scheduling_state.mode="offer_slots"` if slots checked, with populated slots. | Offers exact available slots only. | Invents times not in packet. |
| Slot selection | Lead says, “Thursday at 2 works.” | `appointment_action_taken="booked"` only if booking tool succeeded. | Confirms appointment only when `appointment_status="confirmed"`. | Claims booked when tool failed or status pending. |
| Qualification missing | Lead wants appointment but missing qualifying answers. | `qualification.status="in_progress"`, `next_question_text` populated. | Asks the exact next question warmly. | Asks a different or duplicate question. |
| Reschedule | Lead asks to move an existing appointment. | Uses `getAppointments`; mode reflects reschedule state. | Offers slots or confirms reschedule based on packet. | Cannot trace event ID when required. |
| Cancellation | Lead asks to cancel. | Uses appointment lookup/delete according to policy. | Confirms cancellation only when status supports it. | Says cancelled without delete success. |
| Newsletter acceptance | Lead accepts newsletter. | `newsletter_state.action_taken="subscribed"` only if tool success. | Acknowledges subscription naturally. | Acknowledges without tool success. |
| Opt-out | Lead says stop texting. | `tier="tier_3_optout"`, `response_directive.tone="farewell"`. | Short respectful farewell. | Attempts to re-engage or sends empty response. |
| Hostile | Lead replies angrily. | `tier="tier_2_hostile"`. | One short respectful acknowledgment. | Pushes service, asks sales question, or argues. |
| Invalid packet repair | Force orchestrator to return malformed JSON in a test copy. | Validator creates degraded packet. | Safe natural fallback, no internal mention. | Sends malformed JSON or crashes unhandled. |
| Delivery guard | Inspect `Send SMS`, `Send Email`, `Log Outbound Message`. | No customer-visible fallback to `AI Agent`. | All sent/logged message bodies come from responder. | Any expression still uses `$('AI Agent').json.output` as customer text. |

## Deployment and Rollback Guidance

Follow the existing workflow deployment runbook. Static validation should run before commit, diffs should be reviewed, deployment should be manual until the SMRT n8n pull/deploy path is proven, and every production change must include immediate behavior verification and a changelog update.[5]

| Stage | Required Evidence |
|---|---|
| Pre-edit | Baseline `python3.11 scripts/validate_workflows.py` output. |
| Branch diff | Focused diff showing only intended Brain Engine node additions/edits and documentation changes. |
| Pre-deploy | Export of current runtime workflow or known-good Git commit hash. |
| Controlled deploy | Workflow name, workflow ID, deployment method, timestamp, operator. |
| Post-deploy | Execution traces for acceptance tests, including at least one scheduling path and one no-scheduling path. |
| Rollback | Ability to restore prior workflow export or prior Git version immediately. |

Rollback rule: if any controlled test sends JSON to a lead, logs JSON as the outbound customer message, loses existing delivery behavior, or falsely confirms an appointment, restore the previous known-good workflow immediately. Do not stack speculative fixes on the failed deployment.

## Explicit Non-Goals

This handoff does not require a full Brain Engine rebuild, replacement of the `AI Agent` tool hub, wholesale prompt prose rewrite, new appointment ledger schema work, GoHighLevel identity contract changes, newsletter workflow redesign, or a new Supabase memory architecture. Those are separate workstreams. This handoff’s goal is the smallest architecture split that makes the final response layer independent from the tool-heavy operational layer.

## Recommended Implementation Sequence

The safest implementation order is to first create the packet contract and responder path in a branch while preserving old delivery behavior in a test copy, then remove unsafe fallbacks only after responder text is proven present. The final commit should include the workflow JSON diff, any helper script changes, and documentation updates.

| Sequence | Action | Completion Criteria |
|---:|---|---|
| 1 | Branch and validate baseline. | Validator passes, no unexpected diff. |
| 2 | Update `Assemble System Prompt` to orchestrator contract. | `AI Agent` emits packet JSON in local/test execution. |
| 3 | Add packet validator. | Valid packet passes; malformed packet creates degraded safe packet. |
| 4 | Add responder input builder and `Responder LLM`. | Responder outputs only final message text. |
| 5 | Rewire `Analyze Conversation` after responder. | Summary/leak extraction reads final response, not packet. |
| 6 | Update `Determine Action`, `Send SMS`, `Send Email`, `Log Outbound Message`. | No customer-visible fallback to `AI Agent` remains. |
| 7 | Run acceptance tests. | All tests pass with execution evidence. |
| 8 | Update `CHANGELOG.md`. | Changelog records architecture handoff/implementation state. |

## References

[1]: ../system/SMRT_PROMPT_SYSTEM_FORENSIC_AUDIT.md "SMRT Prompt-System Forensic Audit"  
[2]: ../system/orchestrator_responder_current_state_evidence.md "Orchestrator-to-Responder Current-State Evidence"  
[3]: ../system/assemble_system_prompt_code.md "Assemble System Prompt Code Evidence"  
[4]: ../../data/workflows/brain_engine_prompt_assembly_nodes.json "Brain Engine Prompt Assembly Nodes"  
[5]: ../runbooks/WORKFLOW_DEPLOYMENT_RUNBOOK.md "Workflow Deployment Runbook"
