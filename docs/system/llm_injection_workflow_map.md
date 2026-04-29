# SMRT LLM Injection Workflow Map

Author: **Manus AI**
Date: **2026-04-29**
Status: **Static workflow evidence; no production changes**

## Summary

| Metric | Count |
| --- | ---: |
| `workflow_count` | 21 |
| `active_count` | 10 |
| `llm_node_count` | 39 |
| `prompt_related_node_count` | 37 |
| `memory_context_node_count` | 171 |
| `supabase_prompt_feed_node_count` | 93 |

## Static issue counters

| Issue | Count |
| --- | ---: |
| `llm_without_inputs` | 5 |
| `llm_without_prompt_fields` | 35 |

## Workflow-level LLM surfaces

### ⏰ Appointment Reminders — `workflows/active/Appointment_Reminders__CVHL7qHNCzQOhaqE.json`

Active flag: `True`; directory: `active`

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Mark Reminder Sent` | tableid | — |
| `Log to message_log` | — | — |

### 🧠 Bio Embedding Worker — `workflows/active/Bio_Embedding_Worker__VmHyMwqplMNBaecl.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Build OpenAI Batch` | `n8n-nodes-base.code` | 1 | 1 | 0 | 0 | — |
| `OpenAI Embeddings API` | `n8n-nodes-base.httpRequest` | 1 | 2 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Fetch + Claim Pending Rows` | documents, skip | `query`: WITH candidates AS ( SELECT id FROM documents WHERE document_type = 'agent_bio' AND metadata->>'needs_embedding' = 'true' AND COALESCE((metadata->>'embedding_attempts')::int, 0) <  |
| `Apply Embeddings` | — | `query`: =SELECT public.embed_agent_bio_batch('{{ JSON.stringify($json.updates).replace(/'/g, "''") }}'::jsonb) AS rows_updated; |
| `Bump Attempts` | — | `query`: =SELECT public.mark_bio_embedding_failed('{{ $json.id }}'::uuid, '{{ ($json.error || '').replace(/'/g, "''") }}'::text); |
| `Log to system_errors` | system_errors | `query`: =INSERT INTO system_errors (source, workflow_name, node_name, error_message, error_level, payload, created_at) VALUES ( 'bio-embedding-worker', 'Bio Embedding Worker', 'OpenAI Embe |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Build OpenAI Batch` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `OpenAI Embeddings API` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### ☀️ Contact Created -> Brain Engine — `workflows/active/Contact_Created_Brain_Engine__57VOr1qmDwdO2mZj.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Get Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |
| `Merge Agent + Lead Data` | `n8n-nodes-base.code` | 1 | 1 | 0 | 0 | — |
| `Fetch Agent Config (Pre-Insert)` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | Process Check Result |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Check Lead Exists` | — | — |
| `Enrich Existing Lead` | tableid | — |
| `Insert New Lead` | — | — |
| `Send Intro Email` | — | `jsonBody`: ={ "type": "Email", "contactId": "{{ $json.contact_id }}", "locationId": "{{ $json.location_id }}", "subject": "Quick intro from {{ $json.coordinator_name }} - {{ $json.agent_name  |
| `Note: Duplicate Check` | — | `content`: ## Duplicate Check Queries Supabase for an existing lead by contact_id. - Found: enriches the record (name, email, phone, city, state, source) and stops. No intro sent again. - Not |
| `Note: Write to DB` | — | `content`: ## Write to Supabase New lead: inserts full record with pipeline_state=cold, pipeline_stage=MONTHLY, status=active_conversation. Existing lead: updates contact info only. Pipeline  |
| `Queue Follow-up SMS` | — | — |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Agent Config` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Merge Agent + Lead Data` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Fetch Agent Config (Pre-Insert)` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 📰 Data Source & Newsletter Creation — `workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Get Newsletter Agents` | `n8n-nodes-base.supabase` | 1 | 1 | 0 | 0 | — |
| `Loop Agents` | `n8n-nodes-base.splitInBatches` | 3 | 1 | 0 | 0 | — |
| `Generate Newsletter` | `@n8n/n8n-nodes-langchain.openAi` | 1 | 1 | 2 | 0 | Prepare Agent Data |
| `Extract Splinters` | `@n8n/n8n-nodes-langchain.openAi` | 1 | 1 | 1 | 0 | Condense Altos Data, Generate Newsletter, Prep Data for AI |
| `Back to Agent Loop` | `n8n-nodes-base.noOp` | 3 | 1 | 0 | 0 | — |
| `Prepare Agent Data` | `n8n-nodes-base.code` | 1 | 1 | 0 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Store Splinter` | — | — |
| `Store Weekly Stats` | — | — |
| `Store Embedded Doc` | — | `url`: https://kfoijgcbkjeizxxyiwxv.supabase.co/rest/v1/documents |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Newsletter Agents` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Loop Agents` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Generate Newsletter` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Extract Splinters` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Back to Agent Loop` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Prepare Agent Data` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 📄 Document Ingestion — `workflows/active/Document_Ingestion__4hojpHNg50GyCOJB.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Embeddings OpenAI1` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 0 | 1 | 0 | 0 | — |
| `Lookup Agent by Folder` | `n8n-nodes-base.postgres` | 1 | 1 | 1 | 0 | — |
| `Get Agent Folders` | `n8n-nodes-base.postgres` | 1 | 1 | 0 | 0 | — |
| `Has Agent?` | `n8n-nodes-base.if` | 1 | 1 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Sticky Note4` | — | `content`: ## 📥 Document Ingestion Flow (Polling) **Trigger:** Polls every 60 minutes for new files **How it works:** 1. Get all agent folder IDs from `agents` table 2. Search Google Drive fo |

| Severity | Node | Issue |
| --- | --- | --- |
| high | `Embeddings OpenAI1` | LLM/agent node has neither expression fields nor incoming connection evidence in export. |
| medium | `Embeddings OpenAI1` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Lookup Agent by Folder` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Get Agent Folders` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Has Agent?` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 📬 GHL Delivery Status Handler — `workflows/active/GHL_Delivery_Status_Handler__PbnY3U8jOANRd1yB.json`

Active flag: `True`; directory: `active`

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Update Message Log` | message, tableid | — |
| `Note` | ghl | `content`: ## 📬 GHL Delivery Status Handler Receives OutboundMessage events from GHL and updates message_log.delivery_status. **Subscribe in GHL:** App Marketplace → Webhooks → OutboundMessag |
| `Auto Block Lead` | tableid | — |

### 🔍 GHL Send Status Checker — `workflows/active/GHL_Send_Status_Checker__KsuBnpK9sEXUPgJC.json`

Active flag: `True`; directory: `active`

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Update Message Log` | message, tableid | — |
| `Auto Block Lead` | tableid | — |

### 📬 Newsletter Dispatch — `workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Fetch Active Agents` | `n8n-nodes-base.supabase` | 1 | 1 | 0 | 0 | — |
| `Loop Agents` | `n8n-nodes-base.splitInBatches` | 4 | 1 | 0 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Log Delivery` | — | — |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Fetch Active Agents` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Loop Agents` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 🧠 SMRT Brain Engine — `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json`

Active flag: `True`; directory: `active`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Update Last Agent Message` | `n8n-nodes-base.supabase` | 1 | 2 | 3 | 1 | Assemble System Prompt |
| `Get Agent Config (RAG)` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | LeadDetails |
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | 1 | 1 | 1 | 2 | — |
| `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | 17 | 1 | 2 | 2 | — |
| `Embeddings` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 0 | 1 | 0 | 0 | — |
| `RAG LLM` | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 0 | 1 | 0 | 0 | — |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | 1 | 2 | 1 | 0 | Get Conversation Summary, Get Outbound Conversation Summary |
| `Get Outbound Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |
| `Get Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |
| `Notify Agent` | `n8n-nodes-base.code` | 1 | 0 | 0 | 0 | — |
| `Anthropic Chat Model` | `@n8n/n8n-nodes-langchain.lmChatAnthropic` | 0 | 1 | 0 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `searchLeads` | — | — |
| `addLead` | — | — |
| `Update Last Agent Message` | last, tableid | — |
| `logMessageLeads` | — | — |
| `Get Agent Config (RAG)` | — | — |
| `Get Message History` | message_log | `query`: =SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $('LeadDetails').first().json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id =  |
| `Get Conversation Summary` | — | — |
| `Log Outbound Message` | — | — |
| `AI Sentiment Analysis` | behavioral, system | `messages.values[0].content`: =CONVERSATION CONTEXT (read first — context frames the current message): Conversation Summary: {{ $json.conversationSummary }} Recent Messages (newest last): {{ $json.historyText } |
| `Docs Store` | — | — |
| `Apply Time Decay` | leads | `query`: UPDATE leads SET pipeline_state = CASE WHEN pipeline_state = 'hot' AND last_customer_message_at < NOW() - INTERVAL '14 days' THEN 'warm' WHEN pipeline_state = 'warm' AND last_custo |
| `Fetch Outbound Candidates` | content_spli | `query`: WITH eligible_splinter AS ( SELECT cs.id AS splinter_id, cs.location_id, cs.content AS splinter_content, cs.topic AS splinter_topic, cs.data_point AS splinter_data_point, cs.splint |
| `Check Escalation State` | — | — |
| `Log Already Escalated` | — | — |
| `Update Lead Escalation` | lead, tableid | `fieldsUi.fieldValues[7].fieldValue`: ={{ $('Parse Sentiment').first().json.pipeline_update }} |
| `Update Conversation Context` | conversation, tableid | — |
| `Determine Action` | — | `jsCode`: const input = $input.first().json; // Read AI Agent output directly — upstream Supabase node drops it let responseText = ''; try { responseText = $('AI Agent').first().json.output  |
| `Prepare Tier Response` | apply, parse | `jsCode`: // Prepare tier-specific response instructions for the AI Agent // Pull tier/sentiment/sms_action from Parse Sentiment directly — input $json may be from Apply L1: Mark Lead (no ti |
| `Pause SMS 30 Days (Tier 2)` | tableid | — |
| `Search Relevant Messages` | message_log | `query`: =SELECT id, message_body, direction, timestamp, message_type, 'keyword_match' as source FROM message_log WHERE contact_id = '{{ $json.contact_id }}' AND id NOT IN ( SELECT id FROM  |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Agent Config (RAG)` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| high | `Embeddings` | LLM/agent node has neither expression fields nor incoming connection evidence in export. |
| medium | `Embeddings` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| high | `RAG LLM` | LLM/agent node has neither expression fields nor incoming connection evidence in export. |
| medium | `RAG LLM` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Analyze Conversation` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Get Outbound Agent Config` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Get Agent Config` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Notify Agent` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| high | `Anthropic Chat Model` | LLM/agent node has neither expression fields nor incoming connection evidence in export. |
| medium | `Anthropic Chat Model` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 🎯 Cap Hit Empirical Test — `workflows/inactive/Cap_Hit_Empirical_Test__oWxfl8hqJR5BcHfL.json`

Active flag: `False`; directory: `inactive`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Get Agent API Key` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Log Success` | — | — |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Agent API Key` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### ⏱️ Contact Intake Queue Processor — `workflows/inactive/Contact_Intake_Queue_Processor__i3aF2rmEAZRJbKYp.json`

Active flag: `False`; directory: `inactive`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Get Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |
| `Check Agent Hours` | `n8n-nodes-base.code` | 1 | 1 | 1 | 0 | Get Agent Config |
| `Within Agent Hours?` | `n8n-nodes-base.if` | 1 | 2 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Send Intro Email` | — | `jsonBody`: ={ "type": "Email", "contactId": "{{ $('Parse Payload').item.json.payload.contact_id }}", "locationId": "{{ $('Parse Payload').item.json.payload.location_id }}", "subject": "Quick  |
| `Check Lead State` | — | — |
| `Update Channel to SMS` | channel, tableid | — |
| `Log Followup SMS Sent` | — | — |
| `Log Intro SMS Sent` | — | — |
| `Log Intro Email Sent` | — | — |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Agent Config` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Check Agent Hours` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Within Agent Hours?` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 📈 Daily Pacing Roll-up — `workflows/inactive/Daily_Pacing_Roll_up__5i9pAmUho0LwFwTI.json`

Active flag: `False`; directory: `inactive`

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Format Bump Alert` | — | `jsCode`: // Build a summary of agents that earned level bumps const bumps = $input.all().map(item => { const j = item.json; return { location_id: j.out_location_id, current_level: j.out_lev |

### 🔍 GHL Conversation Backfill — `workflows/inactive/GHL_Conversation_Backfill__LA83yImjwZBdhYqw.json`

Active flag: `False`; directory: `inactive`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Get Agent API Key` | `n8n-nodes-base.supabase` | 1 | 1 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Save To Inbound Capture` | ghl | `fieldsUi.fieldValues[7].fieldValue`: Backfilled from GHL during recovery |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Get Agent API Key` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 🔁 Inbound Replay — `workflows/inactive/Inbound_Replay__JeHSBH713tRZKBQD.json`

Active flag: `False`; directory: `inactive`

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Get Unprocessed Messages` | inbound_capture | `query`: SELECT id, payload, headers, ghl_message_id, captured_at, replay_count FROM inbound_capture WHERE processed = false ORDER BY captured_at ASC LIMIT 100 |
| `Mark As Processed` | tableid | — |

### 🎉 Onboarding — Part 1: DB Enrichment — `workflows/inactive/Onboarding_Part_1_DB_Enrichment__XJxoDt1SJ6SWUIim.json`

Active flag: `False`; directory: `inactive`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Extract Agent Data` | `n8n-nodes-base.set` | 1 | 1 | 11 | 6 | — |
| `Delete Old Agent Bio` | `n8n-nodes-base.postgres` | 1 | 1 | 1 | 0 | — |
| `Bio Embeddings` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 0 | 1 | 0 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Add FAQ Questions` | documenturl, first, other | `actionsUi.actionFields[0].text`: SMRT Knowledge Base - Agent FAQ Please fill out the answers below. This document will be used by your AI assistant (SMRT) to respond to leads on your behalf. --- 1. What areas do y |
| `Delete Old Agent Bio` | documents | `query`: =DELETE FROM documents WHERE location_id = '{{ $json.location_id }}' AND document_type = 'agent_bio'; |
| `Insert Bio to Vectorstore` | — | — |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Delete Old Agent Bio` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| high | `Bio Embeddings` | LLM/agent node has neither expression fields nor incoming connection evidence in export. |
| medium | `Bio Embeddings` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

### 🏗️ Onboarding — Part 2: GHL Setup — `workflows/inactive/Onboarding_Part_2_GHL_Setup__iMG9ggquVeLbmKuv.json`

Active flag: `False`; directory: `inactive`

| LLM/agent node | Type | Incoming | Outgoing | Expression fields | Prompt-like fields | Referenced nodes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `Save Agent Config to Supabase` | `n8n-nodes-base.postgres` | 1 | 1 | 0 | 0 | — |
| `Insert Default Agent Rules` | `n8n-nodes-base.postgres` | 1 | 1 | 1 | 0 | Extract Location ID |
| `Mark Agent as Live` | `n8n-nodes-base.postgres` | 1 | 1 | 1 | 0 | — |

| Supabase / prompt-feed node | Tables referenced | Query/payload field examples |
| --- | --- | --- |
| `Sticky Note - Calendar Setup` | agents | `content`: ## Calendar Setup (Post-Snapshot) After GHL snapshot is applied, the agent's calendar ID needs to be stored in Supabase. ### agents table field - buyer_calendar_id — stores the age |
| `Insert Default Agent Rules` | agent_rules | `query`: INSERT INTO agent_rules (location_id, rule_type, rule_content, priority) VALUES ('{{ $('Extract Location ID').first().json.location_id }}', 'greeting', 'Always greet leads warmly a |

| Severity | Node | Issue |
| --- | --- | --- |
| medium | `Save Agent Config to Supabase` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Insert Default Agent Rules` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |
| medium | `Mark Agent as Live` | LLM/agent node has no obvious prompt-like parameter fields in static export; prompt may be coming from hidden credential/node defaults or upstream data only. |

