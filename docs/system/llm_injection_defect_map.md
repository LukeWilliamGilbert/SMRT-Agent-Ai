# SMRT LLM Injection Defect Map

Author: **Manus AI**  
Date: **2026-04-29**  
Scope: **read-only audit of workflow-side prompt assembly and Supabase-side prompt-feeding state**

This defect map consolidates the workflow evidence from the Brain Engine prompt chain with the read-only Supabase prompt audit. It is designed to answer one question: **where can the system appear to be partially injecting the prompt, or fail to inject expected prompt/context components, without making that failure obvious to an operator?**

## Current injection path model

| Layer | Component | Current role | Primary evidence |
|---|---|---|---|
| Workflow trigger/context layer | Brain Engine inbound/outbound context builders | Collects contact identity, channel, message, agent config, lead memory, conversation summary, recent messages, and tier/sentiment routing. | `docs/system/brain_engine_llm_chain.md` |
| Database prompt library | `prompt_blocks` | Active dynamic prompt-block library; all 18 audited blocks are active. | `docs/system/llm_injection_audit_findings.md` |
| Database static library | `static_prompt_sections` | Main base-prompt library; only 7 of 26 sections are active for the audited location. | `docs/system/llm_injection_audit_findings.md` |
| Agent config | `agents` row for Luke Gilbert | Provides agent metadata, notes, GHL calendar/user fields, website/funnel toggles, but custom personality is disabled and empty. | `docs/system/llm_injection_audit_findings.md` |
| Assembly node | `Assemble System Prompt` | Builds `systemPrompt` from context, tool rules, tier directives, starvation directive, agent notes, newsletter directive, conversation summary, message history, optional personality, and active static sections. | `docs/system/assemble_system_prompt_code.md` |
| LLM node | `AI Agent` | Receives `options.systemMessage = {{ $json.systemPrompt }}` and model connection from Anthropic chat model. | `docs/system/brain_engine_llm_chain.md` |
| Post-response layer | Analyze Conversation, leak detection, outbound send/logging | Extracts structured signals, checks leaks, sends through GHL, and logs outbound messages. | `docs/system/brain_engine_llm_chain.md` |

> The central workflow-side finding is that the **AI Agent is wired to the assembled `systemPrompt`**. The injection concern is less likely to be a totally disconnected LLM node and more likely to be a **partial, stale, empty, fallback, or undocumented prompt-source problem upstream of `systemPrompt`**.

## Ranked defect candidates

| Rank | ID | Defect candidate | Why it matters | Evidence | Severity | First validation test |
|---:|---|---|---|---|---|---|
| 1 | LLM-001 | Static prompt contract is ambiguous: only 7 of 26 static sections are active. | Operators/developer may expect older markdown-headed sections to feed the model when they are inactive. This can look exactly like “some of the prompt is delivered and some is not.” | `static_prompt_sections`: 7 active, 19 inactive; mixed old and new section styles in one location. | High | Create a canonical prompt registry marking each section as `live`, `deprecated`, or `experimental`; compare live 7-section output against intended product behavior. |
| 2 | LLM-002 | Prompt assembly has no explicit telemetry for included sections/blocks/fallbacks. | Even if `systemPrompt` is assembled correctly, there is no durable non-sensitive trace proving which prompt sections, context fields, and fallbacks were included for a given message. | Assembly returns `systemPrompt` but not a prompt manifest; error logs do not capture section inclusion/exclusion. | High | Add non-sensitive prompt assembly manifest: section keys, prompt block IDs/categories, context lengths, history count, personality source, fallback flags, final character count. |
| 3 | LLM-003 | Conversation context injection is inconsistent. | Some conversations have empty or near-empty summaries, so the LLM can receive the base prompt but poor runtime memory. This produces behavior that feels like failed prompt injection even if base instructions are present. | Recent `conversation_context` sample includes 0-length and 4-character summaries; several rows have empty `summary` fields. | High | For the sampled contact IDs, trace inbound capture → message log → conversation summary update → Assemble System Prompt fields. |
| 4 | LLM-004 | Agent-level personality is not a live control surface right now. | If the team expects `agents.personality_prompt` to drive voice, the current active agent has `use_custom_personality=false` and `personality_prompt_length=0`; voice is likely coming from default/static sections instead. | Active Luke Gilbert agent has disabled custom personality and empty personality prompt; default personality exists in `system_defaults`. | Medium | Decide whether personality should be controlled by static sections, system default, or agent row; document one canonical owner. |
| 5 | LLM-005 | Message history can silently disappear if the format is not JSON array-compatible. | `Assemble System Prompt` parses `d.messageHistory` as JSON; if upstream delivers newline text rather than JSON, the catch block silently removes the entire recent-message block. | Code: `JSON.parse(d.messageHistory || '[]')`; catch sets `messageHistoryBlock = ''`. Some upstream evidence shows `messageHistory` may be built as joined text in at least one path. | High | Execute a controlled non-production/manual workflow test and inspect whether `messageHistory` entering the assembly node is a JSON array string or plain text for both inbound and outbound paths. |
| 6 | LLM-006 | Prompt blocks are retrieved but may not be visibly assembled into the final prompt unless the upstream gather node maps them into static items or fields. | The database has active `prompt_blocks`, but the assembly code shown here only consumes input items with `section_key` and `content` as static sections. If prompt blocks are used elsewhere in `Gather Prompt Data`, the contract must be explicit. | Assembly code filters `allItems` by `section_key && content`; prompt-block retrieval exists separately in the workflow evidence. | Medium | Inspect/trace `Gather Prompt Data` runtime output: verify whether prompt blocks are incorporated into fields consumed by `Assemble System Prompt` or are orphaned. |
| 7 | LLM-007 | Agent notes are explicitly instruction-followed and truncated at 2,000 characters. | This may be intentional, but it creates a hidden priority surface: agent notes can override behavior, and any content beyond 2,000 characters is silently clipped. | Code block: `## AGENT NOTES ... follow these instructions`; truncates with `... (truncated)`. | Medium | Confirm current agent notes length and contents; decide whether agent notes are operational notes or prompt directives. |
| 8 | LLM-008 | Scheduling mode is hard-coded `OFF` while appointment tools remain connected. | The model receives scheduling tools but context says `SCHEDULING_MODE: OFF`, creating a possible instruction/tool mismatch. | Assembly code sets `SCHEDULING_MODE: OFF`; AI Agent has appointment tools connected. | Medium | Define scheduling contract: whether booking should be allowed, under what qualification state, and how the prompt should state it. |
| 9 | LLM-009 | Output error/leak logging is too narrow to diagnose injection failure. | Existing error/leak logs can catch some output issues, but not missing prompt fragments or stale context. | `ai_output_errors` small count; findings show no prompt-fragment inclusion telemetry. | Medium | Extend logging with redacted prompt-manifest metadata, not raw prompt text. |
| 10 | LLM-010 | Multiple prompt surfaces create operator confusion. | Static sections, prompt blocks, system defaults, agent notes, agent personality, memory summaries, message history, and tier directives all feed or appear to feed the model. Without a registry, the team may edit the wrong surface. | Workflow and database audits show several overlapping prompt-feeding tables and fields. | Medium | Create a single prompt-source registry and edit policy before changing prompt content. |

## What appears sound

The main AI Agent is not obviously disconnected from the assembled prompt. The `AI Agent` node uses `options.systemMessage = {{ $json.systemPrompt }}`, and the `Assemble System Prompt` node returns `systemPrompt` directly before the AI Agent. This means the most likely defect class is **upstream assembly integrity**, not a missing system-message binding.

The active prompt-block library is also not empty. The database-side audit found **18 active of 18 prompt blocks** with no duplicate/ambiguous block IDs in the sampled checks. This lowers the odds that the prompt-block layer is simply missing, but it raises a contract question: **are these blocks actually being incorporated into the final assembled prompt, or are they present in the database but invisible at the final injection point?**

## Immediate validation sequence

| Step | Test | Expected evidence | Owner |
|---:|---|---|---|
| 1 | Add or simulate a non-production prompt-manifest output from `Assemble System Prompt`. | A manifest with `static_section_keys`, `prompt_block_ids`, `message_history_count`, `conversation_summary_length`, `personality_source`, `agent_notes_length`, `final_prompt_length`, and fallback flags. | Developer, after control-plane setup |
| 2 | Run one inbound test and one outbound test through the Brain Engine in a safe environment or controlled manual execution. | Both executions show which prompt sections and runtime context were included before the AI Agent runs. | Developer + Manny review |
| 3 | Compare included prompt sections to the canonical product-intent list. | Any missing or stale section is classified as intentional, deprecated, or broken. | Luke + Manny |
| 4 | Trace three real contacts with weak context summaries. | Determine whether missing context comes from inbound capture backlog, message-log gaps, summary update logic, or assembly parsing. | Manny audit / developer implementation |
| 5 | Decide canonical prompt ownership. | Static sections vs prompt blocks vs default personality vs agent personality documented with one editing policy. | Luke + Manny |

## Sprint recommendation

The LLM injection point should become **Sprint 1B or Sprint 2A**, not an unbounded prompt rewrite. The first implementation should not change model behavior; it should add **prompt assembly observability**. Once the system can prove what was injected, prompt content fixes become safe and much easier to delegate.
