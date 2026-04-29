# LLM Injection Audit Findings

This document summarizes a read-only audit of the SMRT LLM injection path, focusing on prompt-feeding records, static prompt sections, agent prompt state, conversation context availability, and output-error evidence. It does not modify production data or workflow behavior.

## Executive Findings

| Finding | Evidence | Impact |
|---|---:|---|
| Prompt block library is present and active | 18 active of 18 prompt blocks | The dynamic prompt-block layer appears populated rather than empty. |
| Static prompt library is partly disabled | 7 active of 26 static sections; 19 inactive | If workflow expects all old sections, only a subset is being injected. If the new 7-section design is intentional, this is a configuration contract that needs to be documented. |
| Agent-level custom personality is not feeding injection | 1 active agent row(s) have custom personality disabled and empty personality_prompt | The workflow may rely on static prompt sections/defaults instead of agent.personality_prompt; this can look like partial injection if people expect the agent row to drive voice. |
| Conversation context is inconsistent | 2 of 25 sampled recent contexts have no summary fields; 4 have near-empty summaries | The LLM may receive thin or missing memory/context even when the base prompt is intact. |
| Prompt/output error surface exists but is small | 4 ai_output_errors; 0 likely prompt leaks | Error logging exists, but it probably does not yet prove whether individual prompt fragments reached the model. |

## Prompt Block Health

| Category | Total | Active | Inactive | Empty Content | Priority Range |
|---|---:|---:|---:|---:|---|
| channel | 4 | 4 | 0 | 0 | 20–20 |
| history | 2 | 2 | 0 | 0 | 40–40 |
| mode | 4 | 4 | 0 | 0 | 10–10 |
| relationship | 3 | 3 | 0 | 0 | 30–30 |
| situation | 5 | 5 | 0 | 0 | 60–100 |

Duplicate/ambiguous prompt-block IDs:

- None found.

## Static Prompt Section Health

| Location ID | Total | Active | Inactive | Empty Content | Sort Range |
|---|---:|---:|---:|---:|---|
| kv1Af9i1qYK7KfIiT0U3 | 26 | 7 | 19 | 0 | 100–9999 |

Active/inactive static-section samples show both a newer all-caps prompt set and older markdown-headed sections in the same location. This is not automatically wrong, but it is a likely source of confusion about which prompt surface is live.

- section_key=conversation_awareness; heading=# Conversation Awareness; is_active=False; sort_order=100; content_length=927
- section_key=core_identity; heading=CORE IDENTITY; is_active=True; sort_order=100; content_length=1166
- section_key=decision_framework; heading=DECISION FRAMEWORK; is_active=True; sort_order=200; content_length=5121
- section_key=progressive_conversation; heading=# Progressive Conversation Flow; is_active=False; sort_order=200; content_length=2834
- section_key=intent_qualifier_directive; heading=## INTENT QUALIFIER DIRECTIVE; is_active=False; sort_order=250; content_length=916
- section_key=hard_guardrails; heading=HARD GUARDRAILS; is_active=True; sort_order=300; content_length=11586
- section_key=memory_updates; heading=# Memory Updates; is_active=False; sort_order=300; content_length=2762
- section_key=channel_preference; heading=# Channel Preference Detection; is_active=False; sort_order=400; content_length=880
- section_key=execution_rules; heading=EXECUTION RULES; is_active=True; sort_order=400; content_length=9395
- section_key=channel_config; heading=CHANNEL CONFIG; is_active=True; sort_order=500; content_length=2141
- section_key=identity; heading=# Identity; is_active=False; sort_order=500; content_length=760
- section_key=operating_philosophy; heading=# Operating Philosophy; is_active=False; sort_order=600; content_length=300
- section_key=style_rules; heading=STYLE RULES; is_active=True; sort_order=600; content_length=2387
- section_key=behavioral_constitution; heading=# Behavioral Constitution; is_active=False; sort_order=700; content_length=1502
- section_key=silence_protocol; heading=SILENCE PROTOCOL; is_active=True; sort_order=700; content_length=244
- section_key=communication_style; heading=# Communication Style; is_active=False; sort_order=800; content_length=1269
- section_key=capabilities; heading=# What You Can and Cannot Do; is_active=False; sort_order=900; content_length=1378
- section_key=scheduling_protocol; heading=# Scheduling Protocol; is_active=False; sort_order=1000; content_length=2104
- section_key=escalation_protocol; heading=# Escalation Protocol; is_active=False; sort_order=1100; content_length=1560
- section_key=negative_scenarios; heading=# Negative Scenario Framework; is_active=False; sort_order=1200; content_length=3208
- … 6 additional rows omitted from Markdown; see clean JSON evidence.

## System Defaults and Agent Prompt State

System-default prompt-like rows found: 1. Mean default value length: 1465 characters.

- key=default_personality_prompt; value_length=1465; description=Default personality prompt used when no custom personality is configured for an agent

Agent prompt state:

- location_id=kv1Af9i1qYK7KfIiT0U3; agent_name=Luke Gilbert; active=True; use_custom_personality=False; personality_prompt_length=0; agent_notes_length=56; coordinator_name=Jon; has_calendar_id=True; has_ghl_user_id=True

Agent-to-static-section health:

- location_id=kv1Af9i1qYK7KfIiT0U3; agent_name=Luke Gilbert; active=True; active_static_sections=7; empty_static_sections=0

## Conversation Context Injection Risk

The sampled recent conversation contexts have an average conversation_summary length of 930.4 characters, but several records have empty or near-empty summary fields. This points to a context/memory injection risk rather than only a base-prompt risk.

- contact_id=lEwvRUfBJaJPmr7d73z2; lead_intent=sell; lead_timeline=3_months; appointment_offered=True; appointment_booked=False; conversation_summary_length=1504; summary_length=0; updated_at=2026-04-29T21:00:08.086+00:00
- contact_id=tNkY4jgvKVckTGJ3iBz3; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=906; summary_length=0; updated_at=2026-04-29T20:21:53.923+00:00
- contact_id=an96e4yKpOTczApAh1ta; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=908; summary_length=0; updated_at=2026-04-29T19:50:37.428+00:00
- contact_id=8kv7n2Es1cV0NhIXqas3; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=4; summary_length=0; updated_at=2026-04-29T19:44:38.063871+00:00
- contact_id=kwhTzabuEO8ThYZTptf6; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1502; summary_length=0; updated_at=2026-04-29T19:44:38.063871+00:00
- contact_id=xLbbk1ij9sCHbNs87dAa; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=0; summary_length=0; updated_at=2026-04-29T00:37:43.003147+00:00
- contact_id=fughM6ZbQ4eUFrOwypFb; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=0; summary_length=0; updated_at=2026-04-29T00:37:43.003147+00:00
- contact_id=W1p4zYMdyURdpOt2vmuA; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1008; summary_length=0; updated_at=2026-04-29T00:18:20.898486+00:00
- contact_id=UfKWZIQbjnkZ4a1s540m; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1365; summary_length=0; updated_at=2026-04-29T00:18:20.898486+00:00
- contact_id=fPo84Bot6bjOLKnzYGwd; lead_intent=buy; lead_timeline=unknown; appointment_offered=True; appointment_booked=False; conversation_summary_length=1792; summary_length=0; updated_at=2026-04-28T22:47:37.768+00:00
- contact_id=bfijluboiS56wM1bkPSV; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1219; summary_length=0; updated_at=2026-04-28T17:39:11.381+00:00
- contact_id=zmfJrTF9DJnDGfgf3Njc; lead_intent=sell; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1343; summary_length=0; updated_at=2026-04-27T19:40:47.909+00:00
- contact_id=RpOdr46RRUnKjrZbwwey; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1234; summary_length=0; updated_at=2026-04-26T01:07:34.889+00:00
- contact_id=vkDwtd0XDzA4iWiyC1M3; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=697; summary_length=0; updated_at=2026-04-26T01:02:44.39+00:00
- contact_id=JQD45vnycfHE00GPQPfa; lead_intent=buy; lead_timeline=3_months; appointment_offered=True; appointment_booked=False; conversation_summary_length=1446; summary_length=0; updated_at=2026-04-25T23:59:44.298+00:00
- contact_id=KCOWpt8FVCWRdL9yK6Q9; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=697; summary_length=0; updated_at=2026-04-25T22:23:19.697+00:00
- contact_id=1A9WwUnLiEI9QHnmL8Wx; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1317; summary_length=0; updated_at=2026-04-25T22:22:21.748+00:00
- contact_id=MYMhA7iBEu1lvDlRCwco; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1403; summary_length=0; updated_at=2026-04-25T22:11:00.736+00:00
- contact_id=vEnUJ5Z6WaptJqvkrWic; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=637; summary_length=0; updated_at=2026-04-25T21:51:52.878+00:00
- contact_id=SxPUoPfWEF0l6fp1pCe6; lead_intent=unknown; lead_timeline=unknown; appointment_offered=False; appointment_booked=False; conversation_summary_length=1189; summary_length=0; updated_at=2026-04-25T21:48:55.032+00:00
- … 5 additional rows omitted from Markdown; see clean JSON evidence.

## Preliminary Defect Hypotheses

| ID | Hypothesis | Evidence | Severity | Next Validation |
|---|---|---|---|---|
| LLM-001 | The live system prompt may be assembled from static_prompt_sections and prompt_blocks, while agent.personality_prompt is not used. | Active agent has use_custom_personality=false and personality_prompt_length=0. | Medium | Confirm exact workflow expression mapping into the AI Agent systemMessage and test with a known marker in a non-production prompt section. |
| LLM-002 | Prompt injection may be partially intentional because only 7 of 26 static sections are active, but this contract is undocumented. | 19 inactive static sections coexist with 7 active sections. | High | Define the canonical active prompt-section set and remove/deprecate or label inactive historical sections. |
| LLM-003 | Context injection is unreliable for some conversations because memory summaries are empty or near-empty. | Recent context sample includes empty and 4-character summaries. | High | Trace the context builder and context update nodes against message_log/inbound_capture for those contact IDs. |
| LLM-004 | Current error logging does not capture prompt-fragment inclusion/exclusion. | ai_output_errors has only 4 rows and no prompt-leak markers. | Medium | Add non-sensitive prompt assembly telemetry: section keys included, block IDs included, context length, model input length, and fallback flags. |
| LLM-005 | Duplicate or overlapping prompt surfaces may make the developer and operators misdiagnose behavior. | Static prompt samples include old markdown section headings and newer canonical headings in one location. | Medium | Create a prompt registry document and enforce status labels: live, deprecated, experimental. |

## Evidence Files

- Clean structured evidence: `data/supabase/llm_injection_audit_clean.json`
- Raw read-only query result: `data/supabase/llm_injection_audit_raw.json`
- Prompt schema columns: `data/supabase/prompt_schema_columns.txt`
- Workflow-side map: `docs/system/llm_injection_workflow_map.md`
- Focused Brain Engine chain: `docs/system/brain_engine_llm_chain.md`
- Full prompt assembly evidence: `docs/system/brain_engine_prompt_assembly_full.md`

