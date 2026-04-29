# SMRT LLM Injection Audit

Author: **Manus AI**  
Date: **2026-04-29**  
Repository: `LukeWilliamGilbert/SMRT-Agent-Ai`  
Status: **Read-only audit; no production workflow or database changes made**

## Executive summary

This audit surfaced the LLM injection path as a **real but bounded system risk**. The main AI Agent does appear to be connected to the assembled system prompt: the Brain Engine `AI Agent` node reads `options.systemMessage` from `{{ $json.systemPrompt }}`, and the upstream `Assemble System Prompt` code node returns `systemPrompt` directly into that path.[^brain-chain] The strongest concern is therefore not that the LLM node is completely disconnected. The stronger concern is that the assembled prompt can be **partial, stale, silently starved of runtime context, or misunderstood by operators** because several prompt-feeding surfaces coexist without a durable prompt manifest.[^assembly-code] [^db-findings]

The audit supports your intuition that “some of the prompt is being delivered and some is not,” but with a sharper framing: **the base prompt likely reaches the model, while individual prompt fragments, prompt-source expectations, message history, memory/context, and personality controls may fail or be inactive without obvious runtime evidence**. That is the gap to fix first.

| Bottom line | Assessment |
|---|---|
| Is the AI Agent wired to a system prompt? | **Yes.** The AI Agent reads `systemPrompt` from the previous assembly node. |
| Is the prompt-source contract clear? | **No.** Static sections, prompt blocks, defaults, agent notes, agent personality, message history, and conversation summaries overlap. |
| Is the prompt library empty? | **No.** The database-side audit found 18 active prompt blocks and 7 active static sections. |
| Is there evidence of partial injection risk? | **Yes.** Nineteen static sections are inactive, conversation summaries are inconsistent, agent personality is disabled, and message-history parsing can fail silently. |
| Should we rewrite prompts now? | **No.** First add observability so we can prove what reached the LLM before editing behavior. |

## Working model of the injection path

The current Brain Engine prompt flow has six layers. The workflow gathers lead/contact state, merges prompt-related data, assembles a `systemPrompt`, injects that prompt into the AI Agent, then sends/logs the model output through GoHighLevel and Supabase surfaces. This is a workable architecture, but it currently lacks a reliable trace that says, “for this exact response, these prompt sections and context inputs were included.”

| Layer | Component | Current role | Audit interpretation |
|---|---|---|---|
| Context capture | Lead/context/message nodes | Pulls contact ID, current message, channel, memory, summaries, and recent messages. | This is where runtime context starvation can begin. |
| Prompt library | `prompt_blocks` and `static_prompt_sections` | Stores reusable prompt fragments and base sections. | Present, but active/inactive contract is unclear. |
| Agent config | `agents`, `system_defaults`, agent notes | Supplies agent identity, notes, calendar/GHL fields, and possible personality controls. | Custom personality is not currently live for the active agent. |
| Assembly | `Assemble System Prompt` code node | Builds the final `systemPrompt` string from context, directives, memory, history, personality, notes, and static sections. | Core injection point; needs observability. |
| LLM execution | `AI Agent` + Anthropic chat model | Receives `systemPrompt` and produces the reply. | Wiring appears sound. |
| Post-output handling | Analyze/leak/send/log nodes | Classifies output, detects leaks, sends through GHL, logs results. | Does not yet prove prompt-fragment inclusion. |

The `Assemble System Prompt` node explicitly builds the final system prompt as `context + toolConfig + tierDirective + starvationDirective + agentNotesBlock + newsletterDirective + summaryBlock + messageHistoryBlock + personalityBlock + '## BEHAVIOR' + STATIC_BASE_PROMPT`.[^assembly-code] This is a useful construction because it keeps runtime context and static behavior in one final string. It is also a risk concentration point because a missing upstream value can quietly remove an entire block without generating an operational error.

## Confirmed and likely failure surfaces

The current evidence points to **upstream assembly integrity** as the main risk class. The following defects are ranked by operational impact, testability, and likelihood of explaining observed “partial prompt injection” behavior.

| Rank | ID | Failure surface | What can fail | Evidence | Severity |
|---:|---|---|---|---|---|
| 1 | LLM-001 | Static prompt section contract | Only the newer active section set may be injected while older sections remain inactive; operators may expect inactive content to apply. | 7 active of 26 static sections; 19 inactive sections coexist in the same location.[^db-findings] | High |
| 2 | LLM-002 | Missing prompt manifest | The system cannot prove which sections, blocks, history, summaries, and fallback paths were included in a specific run. | Assembly returns `systemPrompt`, but no durable inclusion metadata is logged.[^defect-map] | High |
| 3 | LLM-003 | Runtime context and summary starvation | The model can receive the base prompt but lack recent or summarized conversation context. | Recent `conversation_context` sample includes empty and near-empty summaries.[^db-findings] | High |
| 4 | LLM-004 | Message-history parsing mismatch | If upstream passes newline text instead of a JSON array string, recent message history is silently dropped. | Assembly parses `d.messageHistory` using `JSON.parse`; catch block sets message history to empty.[^assembly-code] | High |
| 5 | LLM-005 | Agent personality confusion | The active agent row is not currently a live custom personality source. | `use_custom_personality=false`; `personality_prompt_length=0`; a default personality row exists.[^db-findings] | Medium |
| 6 | LLM-006 | Prompt blocks may be present but not visibly included | Active prompt blocks exist, but the final assembly code primarily consumes input items with `section_key` and `content`. | Prompt-block retrieval exists; assembly filters static section-shaped items.[^brain-chain] [^assembly-code] | Medium |
| 7 | LLM-007 | Agent notes as hidden directive surface | Agent notes are treated as followable instructions and truncated at 2,000 characters. | Assembly emits `## AGENT NOTES ... follow these instructions` and truncates long notes.[^assembly-code] | Medium |
| 8 | LLM-008 | Scheduling instruction/tool mismatch | Prompt context says `SCHEDULING_MODE: OFF` while appointment tools remain connected. | Assembly hard-codes scheduling mode off; AI Agent has appointment tools connected.[^brain-chain] [^assembly-code] | Medium |

## What should not be done first

The wrong first move would be to rewrite large prompt sections because the system “feels off.” That would add more moving parts before we can observe the current ones. The better first move is to make prompt injection measurable without exposing private prompt text or lead data.

| Avoid | Better next step |
|---|---|
| Rewriting the whole base prompt | Add non-sensitive prompt assembly telemetry first. |
| Asking the developer to “fix prompt injection” generally | Hand off a scoped prompt-manifest ticket with acceptance tests. |
| Treating the agent personality row as the obvious fix | Decide the canonical prompt ownership model first. |
| Debugging from model behavior alone | Compare runtime prompt manifest against expected prompt registry. |

## Recommended Sprint 1B: prompt assembly observability

The next bounded implementation should be **Prompt Assembly Observability v1**. This should not change the model’s behavior. It should add a safe, redacted manifest that proves which prompt sources were assembled for each response. This belongs after, or alongside, the workflow control-plane work because it touches the active Brain Engine workflow and should be deployed with rollback discipline.

| Required manifest field | Why it matters |
|---|---|
| `static_section_keys_included` | Proves which static sections reached the final prompt. |
| `static_section_count` | Detects missing or unexpectedly inactive base sections. |
| `prompt_block_ids_included` | Proves whether prompt blocks are actually incorporated. |
| `conversation_summary_length` | Detects context-starved runs. |
| `message_history_count` | Detects message-history parsing failures. |
| `message_history_parse_ok` | Makes silent history drops visible. |
| `personality_source` | Distinguishes static/default/agent personality sources. |
| `agent_notes_length` and `agent_notes_truncated` | Detects hidden directive and truncation behavior. |
| `final_prompt_length` | Helps catch unexpectedly short or oversized prompts. |
| `fallback_flags` | Records defaults such as missing summary, missing history, default personality, or missing static sections. |

The manifest should not store raw lead messages, raw summaries, API keys, or full prompt text. It should store **metadata only** so production behavior can be diagnosed without creating a privacy or prompt-leak problem.

## Developer-ready acceptance tests

| Test | Setup | Pass condition |
|---|---|---|
| Static section proof | Run one controlled Brain Engine execution. | Manifest lists the exact active static section keys included in the final prompt. |
| History parse proof | Run one contact with recent message history. | `message_history_parse_ok=true` and `message_history_count > 0`. |
| Context starvation proof | Run or replay a contact with empty summary/history. | Manifest records starvation fallback without exposing private content. |
| Personality source proof | Run current active agent config. | Manifest states whether personality came from agent row, default, static sections, or none. |
| Prompt-block proof | Run with active prompt blocks. | Manifest proves whether prompt blocks were incorporated or flags them as retrieved-but-unused. |
| Scheduling contract proof | Ask a controlled scheduling-related prompt. | Manifest and system context agree on whether scheduling is enabled or disabled. |

## Meeting recommendation

For tomorrow’s developer meeting, the best framing is: **the LLM node appears wired, but the prompt injection contract is not observable enough to trust.** The developer should not be asked to overhaul prompts. He should be asked to implement a narrow observability layer that proves what the Brain Engine injected for each response.

This gives us a safe decision tree. If the manifest shows all intended prompt sources are present, then behavior problems are prompt-design/model-behavior problems. If the manifest shows missing sections, empty history, missing summaries, or unused prompt blocks, then we have concrete workflow defects to fix. Either way, we stop guessing.

## References

[^brain-chain]: [`docs/system/brain_engine_llm_chain.md`](brain_engine_llm_chain.md), focused Brain Engine LLM chain evidence.
[^assembly-code]: [`docs/system/assemble_system_prompt_code.md`](assemble_system_prompt_code.md), extracted `Assemble System Prompt` code with secret redaction.
[^db-findings]: [`docs/system/llm_injection_audit_findings.md`](llm_injection_audit_findings.md), read-only Supabase prompt-feeding audit findings.
[^defect-map]: [`docs/system/llm_injection_defect_map.md`](llm_injection_defect_map.md), ranked injection defect map and validation sequence.
