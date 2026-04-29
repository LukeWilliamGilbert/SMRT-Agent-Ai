# HANDOFF 005: LLM Injection Observability v1

Author: **Manus AI**  
Date: **2026-04-29**  
Status: **Ready for developer scoping after workflow control-plane discipline is confirmed**  
Related audit: [`docs/system/SMRT_LLM_INJECTION_AUDIT.md`](../system/SMRT_LLM_INJECTION_AUDIT.md)

## Objective

Implement a safe, non-sensitive prompt assembly manifest for the SMRT Brain Engine so the team can verify which prompt fragments, static sections, prompt blocks, memory inputs, and fallback paths are included before each AI Agent response.

The goal is **not** to rewrite the prompt. The goal is to make prompt injection observable enough that future prompt or workflow fixes can be made from evidence instead of behavior guesses.

## Current problem

The Brain Engine `AI Agent` appears to be wired to `{{ $json.systemPrompt }}`, and the `Assemble System Prompt` code node returns that field. The likely failure class is not a totally disconnected LLM node. The likely failure class is **partial or silent upstream injection failure**.

| Risk | Current evidence |
|---|---|
| Static prompt ambiguity | 7 active of 26 static prompt sections; 19 inactive sections may be mistaken for live prompt content. |
| Missing runtime proof | No durable manifest records which sections, prompt blocks, summaries, history, or fallback paths were included. |
| Context starvation | Recent conversation-context samples include empty or near-empty summaries. |
| Message-history loss | The assembly node parses `d.messageHistory` as JSON and silently drops history on parse failure. |
| Personality confusion | Active agent has custom personality disabled and empty `personality_prompt`. |
| Scheduling mismatch | Prompt context says `SCHEDULING_MODE: OFF` while appointment tools are still connected. |

## Scope

This handoff covers a **metadata-only observability layer**. It must not log raw lead messages, raw prompt text, raw summaries, API keys, credentials, or private contact data.

| In scope | Out of scope |
|---|---|
| Add prompt assembly manifest fields. | Rewriting static prompt sections. |
| Record section keys, counts, lengths, and fallback flags. | Changing model provider or model settings. |
| Detect message-history parse failures. | Changing GHL message send behavior. |
| Record whether prompt blocks are included, unused, or unavailable. | Rebuilding the memory architecture. |
| Add optional non-production/manual validation execution. | Deploying automatic production changes without rollback. |

## Implementation requirements

Add a metadata manifest at or immediately after the `Assemble System Prompt` node. The manifest can be returned in the workflow JSON payload and optionally logged to a dedicated Supabase table if one exists or is created through an explicit migration.

| Field | Required behavior |
|---|---|
| `prompt_manifest_version` | Static version string, e.g. `v1`. |
| `contact_id_present` | Boolean only; do not duplicate raw contact data unless already operationally required. |
| `direction` | `inbound` or `outbound`. |
| `channel` | Runtime channel value. |
| `static_section_keys_included` | Array of included static section keys. |
| `static_section_count` | Count of included static sections. |
| `prompt_block_ids_included` | Array of included prompt-block IDs if prompt blocks are actually inserted into the final prompt. |
| `prompt_blocks_retrieved_count` | Count retrieved upstream if available. |
| `prompt_blocks_used_count` | Count actually included in final prompt. |
| `conversation_summary_length` | Character length only. |
| `message_history_parse_ok` | Boolean. |
| `message_history_count` | Number of parsed recent messages included. |
| `personality_source` | One of `agent_custom`, `system_default`, `static_section`, `none`, or `unknown`. |
| `agent_notes_length` | Character length only. |
| `agent_notes_truncated` | Boolean. |
| `final_prompt_length` | Character length of final `systemPrompt`. |
| `fallback_flags` | Array such as `missing_summary`, `history_parse_failed`, `no_static_sections`, `default_personality`, `context_starved`. |

## Acceptance tests

| Test | Pass condition |
|---|---|
| Static section inclusion | A controlled run reports the exact static section keys included in the final prompt. |
| Message history parsing | A run with known recent messages reports `message_history_parse_ok=true` and the expected message count. |
| History failure visibility | A deliberately malformed non-production history payload reports `message_history_parse_ok=false` and a fallback flag. |
| Context starvation visibility | A run with no summary/history reports `context_starved` without exposing raw message content. |
| Personality source clarity | Current production-like config reports the correct personality source and does not imply custom agent personality is active. |
| Prompt block clarity | Manifest distinguishes prompt blocks retrieved from prompt blocks actually inserted into the final prompt. |
| No sensitive logging | Manifest contains no raw prompt text, raw lead messages, API keys, or full conversation summaries. |

## Deployment guardrails

This work should be performed only after the workflow JSON control-plane process is confirmed. The developer should pull the current active Brain Engine workflow from Hostinger/n8n, compare it to the repository version, apply the change in a branch, run local validation, manually import or deploy with rollback available, then verify through controlled executions.

## Definition of done

This handoff is complete when the team can inspect one recent Brain Engine execution and answer, without guessing, which static sections, prompt blocks, memory fields, history records, personality source, and fallback flags were used to assemble the system prompt.
