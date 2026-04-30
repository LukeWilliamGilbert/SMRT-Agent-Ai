# SMRT Prompt-System Forensic Audit

Author: **Manus AI**  
Date: **2026-04-30**  
Primary audience: **SMRT development team, workflow owner, and prompt-system maintainers**

## Executive Assessment

The current evidence supports the working hypothesis that SMRT’s response failures are **not primarily a prose-level prompt problem yet**. The wording of the communicating prompt can be improved, but the higher-leverage issue is architectural: the customer-facing AI Agent is being asked to act as conversation writer, state interpreter, tool router, scheduler, CRM updater, memory updater, compliance checker, and recovery handler at the same time. That design makes every response turn carry too much cognitive and operational weight.

The most important finding is that the communicating agent appears to have **fifteen connected tools**, whose recovered descriptions total approximately **12,774 characters** before schemas and runtime context are considered. This is not automatically invalid, but it means the responding model must repeatedly digest a substantial tool surface while also producing the customer-facing message. The n8n Tools Agent documentation describes the agent as using external tools and APIs, understanding tool capabilities, and determining which tool to use depending on the task.[1] OpenAI’s function-calling documentation similarly describes tools as definitions supplied to the model with names, descriptions, and schemas, and notes that function definitions are injected into model context and count against the context limit.[2] Therefore, the user’s instinct is directionally correct: **the communication agent is likely spending too much per-turn attention on tool selection and operational policy**.

The second major finding is that SMRT already has a viable memory-compression foothold. The `Analyze Conversation` summary node has a hardwired system prompt that asks for an accumulative **250–350 word summary**, preserves prior facts and pivots, classifies lead intent and timeline, tracks appointment and newsletter signals, and detects forbidden internal-reasoning leak phrases. The workflow also persists summary fields into the `conversation_context` table. This means the next step should not be “inject all historical conversation strips into the responder.” The better move is to **tighten the summary node and the table it populates**, then feed the final responder a compact state packet rather than full verbatim history except during explicit recovery, QA, or audit flows.

| Core Question | Forensic Answer | Practical Implication |
|---|---|---|
| Is the prompt itself the main issue? | **Not proven.** The prompt may need refinement, but tool burden and context assembly are stronger suspects. | Do not perform a large prose rewrite until the system can prove what context and tools were presented per turn. |
| Is the single-agent design too broad? | **Yes.** The communicating agent is exposed to too many operational responsibilities and tool choices. | Split routing, memory, tool execution, and final response composition into clearer layers. |
| Should full conversation history be injected? | **No, not by default.** Existing summary infrastructure should be upgraded and trusted. | Use summary plus recent-turn window, with verbatim retrieval only when needed. |
| Is the summary node strategically important? | **Yes.** It is the natural memory-augmentation layer. | Treat the summary prompt and `conversation_context` schema as first-class production components. |
| Should tool descriptions remain attached to the responder? | **Only in a smaller allowlisted set.** | Use deterministic routing or a watcher/router step to expose only relevant tools for the current intent. |

## Evidence Base Reviewed

This audit is grounded in the repository’s current final focus document, prior memory and prompt-hardening notes, recovered raw workflow evidence, the generated prompt-system forensic digest, and external documentation for n8n and model tool calling. The raw workflow extraction used defensive redaction and was limited to non-credential prompt, summary, and tool-description surfaces.

| Evidence Artifact | Relevance |
|---|---|
| `docs/system/SMRT_FINAL_CORE_FOCUS_DOCUMENT.md` | Establishes the prior infrastructure-first diagnosis and handoff sequence. |
| `docs/system/prompt_system_forensic_digest.md` | Summarizes recovered Brain Engine prompt assembly, connected tool descriptions, summary nodes, and history-query surfaces. |
| `data/workflows/raw_prompt_summary_surfaces_redacted.json` | Preserves redacted raw non-secret evidence for prompt, summary, table, and tool surfaces. |
| `/home/ubuntu/smrt_analysis/smrt_live_prompt_evidence_summary.md` | Captures live Supabase prompt rows, static prompt sections, active defaults, and agent character configuration. |
| `/home/ubuntu/smrt_analysis/smrt_memory_architecture_note.md` | Provides continuity with the earlier memory architecture diagnosis. |
| `/home/ubuntu/smrt_analysis/smrt_prompt_hardening_and_replay_plan.md` | Provides continuity with prior prompt hardening and replay recommendations. |
| `data/workflows/external_tool_calling_findings.md` | Captures external documentation facts used for citations in this report. |

## Finding 1: The Communication Agent Is Carrying Too Much Tool Burden

The recovered evidence shows a connected tool surface that includes calendar availability, appointment booking, appointment deletion, appointment updates, GHL notes, contact lookup, timezone detection, mailing-list subscription, GHL contact tag operations, contact memory updates, CRM field updates, prompt memory helpers, OpenAI helper access, and other workflow-level capabilities. Several descriptions are not trivial routing labels; they contain operational instructions, ordering constraints, required JSON shapes, and behavioral obligations.

This matters because the final AI Agent is not simply choosing a phrase. It is simultaneously deciding whether to answer, ask, book, reschedule, update memory, tag CRM records, update custom fields, subscribe someone to a newsletter, or post notes. The recovered connected-tool descriptions alone total about **12,774 characters**, and this excludes schemas, input examples, current conversation context, the assembled system prompt, recent history, summary fields, and any model/runtime wrappers.

> OpenAI’s function-calling guidance says function definitions include descriptions explaining when and how to use the function, recommends keeping initially available functions small for higher accuracy, and states that function definitions are injected into model context and count against the context limit.[2]

The issue is not that fifteen tools is above a hard universal limit. In fact, OpenAI’s cited soft suggestion is fewer than twenty initially available functions.[2] The issue is that SMRT’s tool surface is attached to a **high-stakes customer-facing responder** that also has relationship, brand, memory, appointment, and compliance obligations. Fifteen tools may be survivable in a narrow automation agent. It is much riskier in a conversational agent that must sound human, avoid internal-state leakage, preserve prior relationship context, and take real CRM actions.

| Tool-Burden Symptom | Risk Created | Recommended Correction |
|---|---|---|
| Many tools exposed to final responder | Model must route actions while writing customer copy. | Introduce an upstream watcher/router that produces an intent and tool allowlist. |
| Long tool descriptions with behavioral rules | Operational instructions compete with voice and memory instructions. | Move deterministic requirements into workflow code and shorten tool descriptions. |
| Tools mix read, write, booking, and messaging support | Sensitive writes can be selected by the same model writing the SMS. | Separate read-only enrichment, sensitive writes, and final response generation. |
| Tool selection happens inside communication turn | Debugging failures becomes opaque. | Log selected tool set, tool-call rationale category, and tool outputs in metadata. |
| Prompt must teach the model all tool policies every turn | Repeated token burden and instruction dilution. | Use route-specific agent profiles or route-specific subworkflows. |

## Finding 2: The Summary Node Is Already the Correct Memory-Augmentation Focal Point

The workflow already contains an `Analyze Conversation` node with a structured, hardwired prompt. It asks the model to return JSON containing `summary`, `lead_intent`, `lead_timeline`, appointment flags, newsletter flags, and internal-reasoning leak detection. Its summary instructions are specifically accumulative: preserve concrete facts from previous summaries, layer in new facts, preserve pivot history, focus on customer statements and commitments, and build from scratch only when no prior summary exists.

That design is directionally sound. It means SMRT does not need to solve memory by passing entire conversation strands to the final responder. The stronger architecture is to make the summary node and persistence table reliable enough that the responder receives **a compact durable-memory packet** plus a small recent-turn window.

The current persistence logic, however, appears to regenerate or replace the stored `conversation_summary` only when `turnCounter <= 2` or `turnCounter % 10 === 0`. When the condition is false, the workflow keeps the previous summary. This creates a gap: the summary prompt is sophisticated, but updates may be intentionally sparse. That cadence may reduce cost, but it can also cause stale memory during turns three through nine, especially if a lead changes intent, provides scheduling constraints, rejects an appointment, supplies a new address, or corrects an earlier assumption.

| Summary-System Component | Current Evidence | Audit Interpretation |
|---|---|---|
| Summary prompt | Strong 250–350 word accumulative summary instructions. | Keep this layer; it is a core asset. |
| Structured extraction | Intent, timeline, appointment, newsletter, and leak flags are extracted. | Expand this into a richer state packet rather than relying on prose alone. |
| Persistence target | `conversation_context` stores `conversation_summary`, `last_intent`, `lead_intent`, and `lead_timeline`. | Table should become the main responder memory interface. |
| Regeneration cadence | Summary updates at early turns and every tenth turn. | Too coarse for high-signal turns; add event-triggered regeneration. |
| Recent history query | `message_log` is queried in descending timestamp order with `LIMIT 15`. | Useful for summarizer, but not ideal as default responder input. |

The best route is not to remove conversation history from the system entirely. Rather, the default responder context should be **summary-first, recent-turn-second, verbatim-on-demand**. The summarizer can read the larger history window and latest exchange. The responder should usually read a concise state packet containing durable facts, unresolved open loops, last asked question, current lead state, current channel, current allowed next move, and only a very small recent-turn excerpt.

## Finding 3: Full Conversation Strips Are a Poor Default for the Final Responder

The existing workflow queries the last fifteen `message_log` rows for both inbound and outbound paths. That data is useful for summary generation and debugging, but it should not be treated as the default memory substrate for the final communicating agent. Long verbatim history forces the model to re-derive state from noisy turns, increases the chance of recency bias, and can bury the true durable facts behind informal language, duplicates, and historical pivots.

The stronger division of labor is to let the summarizer read more and let the responder read less. The responder’s job should be to produce the next message from a clean state packet, not reconstruct the whole relationship every turn. When the responder needs a missing fact, it should request a narrow retrieval or receive a precomputed field, not scan a large strand.

| Context Type | Recommended Default Use | Reason |
|---|---|---|
| Durable summary | Always include. | Gives stable relationship memory without rereading the whole thread. |
| Structured lead facts | Always include when populated. | Prevents repeated qualification questions and preserves concrete facts. |
| Open loops and commitments | Always include. | Ensures the agent follows through on promised next steps. |
| Last asked question | Always include. | Prevents asking the same question twice. |
| Last 3–5 turns | Include by default. | Preserves immediate conversational continuity. |
| Last 15+ verbatim messages | Summarizer/recovery only. | Too much noise for normal response composition. |
| Full conversation transcript | Audit/replay only. | Useful for forensic analysis, not routine customer response. |

## Finding 4: The Prompt Stack Has Multiple Instruction Layers That Can Compete

The live prompt evidence shows a layered prompt stack: a default personality prompt, active static prompt sections, conditional prompt blocks, agent notes, memory/context inserts, and tool descriptions. Active static sections include `core_identity`, `decision_framework`, `hard_guardrails`, `execution_rules`, `channel_config`, `style_rules`, and `silence_protocol`. These are generally valuable, but their accumulation creates an instruction-density problem.

For example, the static sections include high-level identity and voice rules, decision frameworks, legal guardrails, execution rules, scheduling protocol content, memory update directives, conversation awareness logic, channel behavior, and silence behavior. This is a large amount of policy for the same agent that also sees a large operational tool surface. The risk is not only token volume. The risk is **priority ambiguity**: when a lead says something that touches scheduling, newsletter fallback, contact preference, prior memory, and tone, the model has to reconcile too many rule sources inside one generation step.

| Prompt Layer | Value | Risk |
|---|---|---|
| Default personality | Preserves Luke’s tone and human communication style. | Can be diluted by operational tool instructions and merged static sections. |
| Active static sections | Provide behavior, safety, channel, style, and silence policy. | May be too broad for a single responder turn without route-specific pruning. |
| Conditional blocks | Enable situational behavior. | Need manifest logging to prove when they are included. |
| Tool descriptions | Teach tool use. | Consume attention and introduce operational obligations into copy generation. |
| Recent conversation/history | Provides continuity. | Can compete with summary and cause model to re-infer state inconsistently. |

The correct next step is not to delete these layers. It is to **instrument and modularize them**. The team should add a prompt assembly manifest that records which blocks were included, which conditionals fired, how many characters or tokens each layer contributed, which memory fields were present, how many recent turns were included, and which tools were exposed. This does not require storing full sensitive prompt content in logs; metadata-only manifests are sufficient for diagnosis.

## Recommended Target Architecture

SMRT should move from a single broad communicating agent to a **routed multi-stage response pipeline**. This does not require a large multi-agent science project. It can be implemented pragmatically in n8n as deterministic routing plus smaller specialized model calls.

| Stage | Responsibility | Model Required? | Output |
|---|---|---:|---|
| Intake normalizer | Normalize inbound/outbound event, contact identity, channel, and direction. | No | Clean event packet. |
| Watcher/router | Classify current intent, risk, and required capabilities. | Sometimes | Route label and allowed tool group. |
| Memory summarizer | Update durable summary and structured state when new facts or commitments appear. | Yes | `conversation_context` update. |
| Tool executor | Perform deterministic CRM, calendar, newsletter, and memory operations. | Mostly no | Tool result packet. |
| Response composer | Write only the customer-facing message from compact state and tool results. | Yes | Final message text. |
| Observer/logger | Record prompt manifest, route, tool results, errors, and state changes. | No | Audit trail. |

In this model, the final responder is no longer responsible for deciding among every tool. It receives a **compact context packet** and a small allowed action space. Most write operations are handled upstream or downstream by deterministic nodes with explicit preconditions. This preserves the human feel of the response while reducing the chance that the same model is both deciding infrastructure actions and producing customer copy.

## Proposed Context Packet for the Final Responder

The final responder should usually receive a compact packet like the following. The exact field names can be adapted to the existing table schema, but the principle should remain stable: **structured facts first, short narrative summary second, recent turns third, tool outputs last**.

| Field | Purpose |
|---|---|
| `lead_identity` | Contact name, channel, location, agent, coordinator, and CRM identifiers needed for wording only. |
| `conversation_summary` | 250–350 word durable accumulative summary generated by the summary node. |
| `known_facts` | Budget, area, property type, buy/sell intent, timeline, financing status, address, constraints, and preferences. |
| `open_loops` | Promises, pending questions, pending scheduling actions, pending newsletter offer, or unresolved customer requests. |
| `last_asked_question` | The most recent question SMRT asked so it does not repeat itself. |
| `last_customer_answer` | The latest customer-provided answer or correction. |
| `conversation_state` | Early, qualifying, ready, nurture, rejection, sensitive, stop, or escalation. |
| `allowed_next_move` | One primary move selected upstream: answer, ask, guide, schedule, newsletter, escalate, or stop. |
| `recent_turns` | Last 3–5 turns only, preferably chronological and trimmed. |
| `tool_results_this_turn` | Only results from tools actually executed for this turn. |
| `do_not_say` | Internal-state phrases and leak-prone wording that must not appear. |

This packet should be produced by code or a dedicated assembly node, not improvised inside the final responder prompt. It should also be logged through a manifest so failed responses can be replayed against the exact same state conditions.

## Summary Node Upgrade Plan

The existing summary prompt is good enough to become the foundation of memory augmentation, but the table and update conditions need to be strengthened. The current summary should not remain a single prose blob plus a few intent fields. It should become a durable state object with both narrative and structured components.

| Upgrade | Implementation Detail | Benefit |
|---|---|---|
| Add event-triggered summarization | Regenerate summary when lead provides new facts, changes intent, discusses appointments, rejects scheduling, supplies contact preferences, or says “I already told you.” | Prevents stale memory between tenth-turn updates. |
| Preserve chronological pivot history | Keep prior-to-current transitions explicit in summary and structured fields. | Avoids losing important reversals like buyer to seller or now to six months. |
| Add `last_asked_question` | Store exact or normalized latest question SMRT asked. | Reduces repetitive qualification. |
| Add `answered_questions` | Store known answers by category such as intent, timeline, area, budget, and appointment preference. | Lets responder skip already-answered prompts. |
| Add `open_commitments` | Store promises SMRT made, including appointment offers and follow-up commitments. | Prevents customer-facing inconsistency. |
| Add confidence and freshness fields | Store `summary_confidence`, `last_summarized_at`, and `summary_source_turn_ids`. | Makes memory quality observable. |
| Add leak signal handling | Keep existing leak detector but route positive detections to QA/observability, not only storage. | Converts prompt failure into measurable incidents. |

## Tool-Surface Rerouting Recommendation

The final responder should not be exposed to all tools all the time. The development team should create route-specific tool groups. If the route is simple conversational answer, the responder should have **no write tools**. If the route is scheduling, only the minimal scheduling tools should be available. If the route is memory update, memory writes should be deterministic based on extracted state, not a free-form responder choice.

| Route | Tools Exposed to Final Responder | Preferred Execution Pattern |
|---|---|---|
| Simple answer or nurture | None, or read-only context already preloaded. | Compose response only. |
| Qualification | None by default. | Ask one next question from state packet. |
| Scheduling intent | Availability and booking only after upstream preconditions. | Deterministic appointment ledger plus GHL/Supabase writes. |
| Reschedule/cancel | Only reschedule/cancel tools after appointment identity is known. | Pre-validated appointment operation. |
| Newsletter fallback | No broad CRM tools; explicit subscribe/update operation after consent. | Deterministic subscription step. |
| Memory update | No final-responder tool call. | Summary/extractor writes structured fields. |
| Escalation/sensitive | No tools except escalation marker if needed. | Human handoff or silence policy. |

This approach aligns with the external guidance that initially available tools should be kept small for higher accuracy and that burden should be offloaded from the model into code where possible.[2]

## Developer Acceptance Criteria

The following criteria can be used to determine whether the prompt-system remediation is working. They intentionally avoid subjective prompt-quality judgments and focus on observable architecture.

| Acceptance Criterion | Required Evidence |
|---|---|
| Prompt assembly is observable. | Each run stores a metadata manifest listing prompt blocks, conditional blocks, context fields, recent-turn count, tool names exposed, and character/token estimates. |
| Final responder tool load is route-scoped. | Logs show simple-answer routes expose zero write tools and scheduling routes expose only scheduling-relevant tools. |
| Summary is event-refreshed. | Summary updates occur on high-signal turns even when the turn counter is not `<= 2` or divisible by ten. |
| Full history is not default responder context. | Final responder receives summary plus small recent-turn window except in explicit recovery/debug paths. |
| Repeated-question failures are measurable. | `last_asked_question` and `answered_questions` are stored and included in responder context. |
| Tool write failures are not swallowed. | CRM/calendar/memory write outcomes are logged with success/failure status and surfaced to observer layer. |
| Internal-reasoning leak incidents are trackable. | Leak detector positives create structured QA events for review. |

## Recommended Immediate Developer Handoff

The next developer handoff should be framed as **Prompt System Forensics and Memory-Routing Refactor**, not as “rewrite the prompt.” The core work is to open the prompt system, reduce the communicating agent’s tool burden, and promote the summary node into a durable memory interface.

| Priority | Work Item | Outcome |
|---:|---|---|
| 1 | Add prompt assembly manifest logging. | The team can prove what the model saw on every failed run. |
| 2 | Add route-specific tool allowlists. | The responder stops seeing irrelevant write tools. |
| 3 | Upgrade `conversation_context` schema or payload. | Summary becomes structured memory, not just a prose blob. |
| 4 | Add event-triggered summary refresh. | High-signal facts are not delayed until every tenth turn. |
| 5 | Change responder input to compact context packet. | Full conversation strips become exception paths, not default context. |
| 6 | Shorten and externalize tool descriptions. | Tool usage policy moves into deterministic workflow code where possible. |
| 7 | Add replay tests for known prompt failures. | Prompt tuning becomes evidence-based after plumbing is observable. |

## Final Opinion

The user’s concern is well-founded: a single communicating agent connected to a broad tool surface is likely an architectural weakness. The final responder should not have to repeatedly digest the full operational toolbox while also sounding human and preserving relationship memory. The system already has the beginning of the right memory strategy through the summary node and `conversation_context` table. The most important next move is to **make that memory path reliable, structured, and observable**, then reduce the final responder to its proper job: write the next message from a clean state packet and a narrow, route-specific action space.

Prompt tuning should come after this. Once the team can inspect the prompt manifest, summary freshness, exposed tools, and state packet for a failed turn, they can identify whether the remaining issue is voice, policy wording, memory extraction, routing, or infrastructure. Until then, a prose rewrite would risk masking the real failure mode.

## References

[1]: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/tools-agent/ "n8n Docs — Tools AI Agent node documentation"

[2]: https://developers.openai.com/api/docs/guides/function-calling "OpenAI API Docs — Function calling"
