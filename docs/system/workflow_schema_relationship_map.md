# SMRT Workflow–Schema Relationship Map

This map is generated from a static, read-only scan of the sanitized n8n workflow exports and the live Supabase schema inventory. It identifies where workflow nodes reference database tables, SQL-like operations, Supabase REST endpoints, or persistence concepts. Because n8n expressions can construct URLs and SQL dynamically, this document should be treated as a **high-confidence static map**, not a replacement for runtime tracing.

> **Read-only audit note:** This extraction inspected exported workflow JSON only. It did not change workflows, credentials, database rows, schema, prompt configuration, or production routing.

## Coverage Summary

The scan covered **21 workflows** and found **199 workflow nodes** with database or schema-relevant references.

| Metric | Count |
| --- | ---: |
| Public schema relations inventoried | 33 |
| Relations referenced by workflows | 23 |
| Relations not directly observed in workflow exports | 10 |
| Database-relevant workflow nodes | 199 |

## Table-to-Workflow Map

| Table | Workflow References | Operation Signals |
| --- | --- | --- |
| `agent_rules` | 🏗️ Onboarding — Part 2: GHL Setup | create: 1 |
| `agent_sending_stats` | 📈 Daily Pacing Roll-up | update: 1 |
| `agents` | ⏱️ Contact Intake Queue Processor<br>☀️ Contact Created -> Brain Engine<br>🎉 Onboarding — Part 1: DB Enrichment<br>🎯 Cap Hit Empirical Test<br>🏗️ Onboarding — Part 2: GHL Setup<br>📄 Document Ingestion<br>📈 Daily Pacing Roll-up<br>📬 Newsletter Dispatch<br>📰 Data Source & Newsletter Creation<br>🔍 GHL Conversation Backfill<br>🧠 SMRT Brain Engine | create: 3, read: 18, reference: 2, update: 5 |
| `ai_output_errors` | 🧠 SMRT Brain Engine | create: 1 |
| `altos_weekly_stats` | 📰 Data Source & Newsletter Creation | read: 1, reference: 2 |
| `appointments` | ⏰ Appointment Reminders<br>🏗️ Onboarding — Part 2: GHL Setup<br>🧠 SMRT Brain Engine | create: 1, read: 1, reference: 1, update: 1 |
| `audit_log` | not observed | not observed |
| `channel_prompts` | not observed | not observed |
| `contact_intake_queue` | ⏱️ Contact Intake Queue Processor<br>☀️ Contact Created -> Brain Engine | read: 1, reference: 2, update: 6 |
| `content_splinters` | 📰 Data Source & Newsletter Creation | delete: 1, reference: 1, update: 1 |
| `conversation_context` | 🧠 SMRT Brain Engine | create: 1, read: 3, reference: 1, update: 5 |
| `documents` | 🎉 Onboarding — Part 1: DB Enrichment<br>📄 Document Ingestion<br>📰 Data Source & Newsletter Creation<br>🧠 Bio Embedding Worker<br>🧠 SMRT Brain Engine | create: 2, delete: 3, read: 6, update: 3 |
| `dormancy_events` | not observed | not observed |
| `inbound_capture` | 🔁 Inbound Replay<br>🔍 GHL Conversation Backfill<br>🧠 SMRT Brain Engine | create: 2, read: 2, update: 1 |
| `leads` | ⏰ Appointment Reminders<br>⏱️ Contact Intake Queue Processor<br>☀️ Contact Created -> Brain Engine<br>🎉 Onboarding — Part 1: DB Enrichment<br>🎯 Cap Hit Empirical Test<br>🏗️ Onboarding — Part 2: GHL Setup<br>📬 GHL Delivery Status Handler<br>📬 Newsletter Dispatch<br>🔍 GHL Send Status Checker<br>🧠 SMRT Brain Engine | create: 4, read: 6, reference: 7, update: 14 |
| `message_log` | ⏰ Appointment Reminders<br>⏱️ Contact Intake Queue Processor<br>🎯 Cap Hit Empirical Test<br>📬 GHL Delivery Status Handler<br>🔍 GHL Send Status Checker<br>🧠 SMRT Brain Engine | create: 12, read: 6, reference: 3, update: 2 |
| `message_send_errors` | 🎯 Cap Hit Empirical Test<br>📬 GHL Delivery Status Handler<br>🔍 GHL Send Status Checker<br>🧠 SMRT Brain Engine | create: 4 |
| `newsletter_deliveries` | 📬 Newsletter Dispatch | create: 2, read: 1 |
| `newsletters` | 📰 Data Source & Newsletter Creation | read: 1, reference: 4 |
| `onboarding_requests` | 🎉 Onboarding — Part 1: DB Enrichment<br>🏗️ Onboarding — Part 2: GHL Setup | create: 1, read: 2, reference: 2, update: 1 |
| `personality_options` | not observed | not observed |
| `pipeline_transitions` | not observed | not observed |
| `prompt_blocks` | 🧠 SMRT Brain Engine | read: 1 |
| `smrt_admin_emails` | not observed | not observed |
| `smrt_saas_submissions` | not observed | not observed |
| `splinter_usage` | 🧠 SMRT Brain Engine | reference: 1 |
| `static_prompt_sections` | 🧠 SMRT Brain Engine | read: 1 |
| `system_defaults` | 🧠 SMRT Brain Engine | create: 1, read: 2 |
| `system_errors` | 🔥 Error Catch<br>🧠 Bio Embedding Worker | create: 2 |
| `timezones` | ⏱️ Contact Intake Queue Processor | reference: 1 |
| `v_agent_delivery_health` | not observed | not observed |
| `v_quota_status` | not observed | not observed |
| `v_send_errors_24h` | not observed | not observed |

## Workflow Persistence Summary

| Workflow | Active | Nodes | DB-Relevant Nodes | Tables Referenced |
| --- | --- | ---: | ---: | --- |
| My workflow | False | 0 | 0 | none observed |
| My workflow 2 | False | 2 | 0 | none observed |
| My workflow 3 | False | 0 | 0 | none observed |
| ⏰ Appointment Reminders | True | 9 | 3 | `appointments` (2), `leads` (1), `message_log` (2) |
| ⏱️ Contact Intake Queue Processor | False | 28 | 16 | `agents` (1), `contact_intake_queue` (6), `leads` (2), `message_log` (3), `timezones` (1) |
| ☀️ Contact Created -> Brain Engine | True | 26 | 11 | `agents` (2), `contact_intake_queue` (2), `leads` (4) |
| 🎉 Onboarding — Part 1: DB Enrichment | False | 23 | 12 | `agents` (1), `documents` (2), `leads` (1), `onboarding_requests` (3) |
| 🎯 Cap Hit Empirical Test | False | 10 | 5 | `agents` (1), `leads` (1), `message_log` (2), `message_send_errors` (1) |
| 🏗️ Onboarding — Part 2: GHL Setup | False | 23 | 12 | `agent_rules` (1), `agents` (5), `appointments` (1), `leads` (1), `onboarding_requests` (3) |
| 📄 Document Ingestion | True | 27 | 13 | `agents` (3), `documents` (4) |
| 📈 Daily Pacing Roll-up | False | 6 | 3 | `agent_sending_stats` (1), `agents` (2) |
| 📬 GHL Delivery Status Handler | True | 16 | 5 | `leads` (1), `message_log` (2), `message_send_errors` (1) |
| 📬 Newsletter Dispatch | True | 15 | 7 | `agents` (2), `leads` (1), `newsletter_deliveries` (3) |
| 📰 Data Source & Newsletter Creation | True | 37 | 18 | `agents` (1), `altos_weekly_stats` (3), `content_splinters` (2), `documents` (2), `newsletters` (5) |
| 🔁 Inbound Replay | False | 7 | 2 | `inbound_capture` (2) |
| 🔍 GHL Conversation Backfill | False | 8 | 6 | `agents` (1), `inbound_capture` (1) |
| 🔍 GHL Send Status Checker | True | 14 | 4 | `leads` (1), `message_log` (1), `message_send_errors` (1) |
| 🔥 Error Catch | True | 3 | 1 | `system_errors` (1) |
| 🧠 Bio Embedding Worker | True | 9 | 5 | `documents` (1), `system_errors` (1) |
| 🧠 SMRT Brain Engine | True | 174 | 70 | `agents` (4), `ai_output_errors` (1), `appointments` (1), `conversation_context` (9), `documents` (1), `inbound_capture` (1), `leads` (16), `message_log` (8), `message_send_errors` (1), `prompt_blocks` (1), `splinter_usage` (1), `static_prompt_sections` (1), `system_defaults` (2) |
| 🧪 Altos Image Test | False | 12 | 6 | none observed |

## Node-Level Evidence

### 🧪 Altos Image Test / Fetch Hash

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const PAI = '690acaf9'; const FIPS = '16001'; const resp = await globalThis.fetch(`https://altos.re/api/v2/reports?[REDACTED_QUERY] const data = await resp.json(); if (!data.id) { throw new Error('No hash returned from Altos: ' + JSON.stringify(data)); } return [{ json: { hash: data.id, pai: PAI } }];` |

### 🧪 Altos Image Test / Upload Share

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### 🧪 Altos Image Test / Upload Market Action

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### 🧪 Altos Image Test / Upload Table

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### 🧪 Altos Image Test / Upload Chart Price

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### 🧪 Altos Image Test / Upload Chart Advanced

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### ⏰ Appointment Reminders / Mark Reminder Sent

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `appointments`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `appointments` |

### ⏰ Appointment Reminders / Sticky Note

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `appointments`, `leads`, `message_log`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Appointment Reminders Sends SMS reminders at 3 intervals before scheduled appointments: - **24 hours** before - **5 hours** before - **1 hour** before **Safety guards:** - No reminders to DNC/opted-out leads - No reminders for cancelled appointments - No reminders if lead has no phone - Messages logged to message_log so Brain Engine has context - Reminder flags prevent duplicate sends **Schedule:** Every 30 minutes` |

### ⏰ Appointment Reminders / Log to message_log

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 🧠 Bio Embedding Worker / Fetch + Claim Pending Rows

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `documents`
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `WITH candidates AS ( SELECT id FROM documents WHERE document_type = 'agent_bio' AND metadata->>'needs_embedding' = 'true' AND COALESCE((metadata->>'embedding_attempts')::int, 0) < 5 AND length(content) BETWEEN 1 AND 50000 AND ( metadata->>'embedding_started_at' IS NULL OR (metadata->>'embedding_started_at')::timestamptz < (now() - interval '10 minutes') ) ORDER BY (metadata->>'updated_at')::timestamptz ASC NULLS LAST LIMIT 50 FOR UPDATE SKIP LOCKED ) U…[TRUNCATED]` |

### 🧠 Bio Embedding Worker / Pair Embeddings

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const apiResponse = $input.first().json; const data = apiResponse.data \|\| []; const previousNode = $('Build OpenAI Batch').first().json; const rowIds = previousNode.rowIds \|\| []; if (data.length !== rowIds.length) { throw new Error(`Embedding count mismatch: got ${data.length}, expected ${rowIds.length}`); } const updates = data.map((d, i) => ({ id: rowIds[i], embedding: '[' + d.embedding.join(',') + ']' })); return [{ json: { updates } }];` |

### 🧠 Bio Embedding Worker / Apply Embeddings

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT public.embed_agent_bio_batch('{{ JSON.stringify($json.updates).replace(/'/g, "''") }}'::jsonb) AS rows_updated;` |

### 🧠 Bio Embedding Worker / Bump Attempts

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT public.mark_bio_embedding_failed('{{ $json.id }}'::uuid, '{{ ($json.error \|\| '').replace(/'/g, "''") }}'::text);` |

### 🧠 Bio Embedding Worker / Log to system_errors

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `system_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=INSERT INTO system_errors (source, workflow_name, node_name, error_message, error_level, payload, created_at) VALUES ( 'bio-embedding-worker', 'Bio Embedding Worker', 'OpenAI Embeddings API', '{{ ($json.error \|\| '').replace(/'/g, "''") }}', 'error', jsonb_build_object('document_id', '{{ $json.id }}'), now() );` |

### 🎯 Cap Hit Empirical Test / Test Config

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🎯 Cap Hit Empirical Test / Get Agent API Key

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 🎯 Cap Hit Empirical Test / Log Success

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 🎯 Cap Hit Empirical Test / Log Failure (CRITICAL)

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_send_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_send_errors` |

### 🎯 Cap Hit Empirical Test / Note

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `leads`, `message_log`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 🎯 Cap Hit Empirical Test **Purpose:** Send up to 260 test SMS to ONLY 2 hardcoded contacts (Daddy Sayeed + Sayeed Hobaid — Hobaid's own numbers) until GHL returns a non-200 (cap hit). **Safety:** - Other leads are unreachable — no query to leads table - onError: continueErrorOutput so loop continues + logs each failure - 1.5s throttle between sends **What it captures:** - Success → row in message_log with delivery_status=sent, ghl_message_id - Failure → FULL raw response in message_send_er…[T…` |

### ☀️ Contact Created -> Brain Engine / Check Lead Exists

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### ☀️ Contact Created -> Brain Engine / Enrich Existing Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### ☀️ Contact Created -> Brain Engine / Insert New Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### ☀️ Contact Created -> Brain Engine / Send Intro Email

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsonBody` | `={ "type": "Email", "contactId": "{{ $json.contact_id }}", "locationId": "{{ $json.location_id }}", "subject": "Quick intro from {{ $json.coordinator_name }} - {{ $json.agent_name }}'s team", "emailFrom": "{{ $json.coordinator_name }} <{{ $json.coordinator_email }}>", "html": "<p>Hi {{ $json.first_name }},</p><p>I'm {{ $json.coordinator_name }}, part of {{ $json.agent_name }}'s real estate team. {{ $json.agent_name }} and I want to make sure you have a direct line to someone on the team if anyth…` |

### ☀️ Contact Created -> Brain Engine / Note: Trigger

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Trigger Receives new contact webhooks from a GHL automation when a contact is created. Works for single contacts and bulk spreadsheet imports.` |

### ☀️ Contact Created -> Brain Engine / Note: Duplicate Check

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Duplicate Check Queries Supabase for an existing lead by contact_id. - Found: enriches the record (name, email, phone, city, state, source) and stops. No intro sent again. - Not found: continues to insert as a new lead.` |

### ☀️ Contact Created -> Brain Engine / Note: Channel Routing

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `leads`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Channel Routing and Send Routes the intro message for new leads only: - SMS (default) - sent if phone exists - Email (fallback) - sent if no phone - No Contact Method - tags lead in GHL and stops NOTE: SMS and Email nodes are placeholders. Add message content before activating.` |

### ☀️ Contact Created -> Brain Engine / Get Agent Config

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### ☀️ Contact Created -> Brain Engine / Queue Intro Message

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `contact_intake_queue` |

### ☀️ Contact Created -> Brain Engine / Queue Follow-up SMS

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `contact_intake_queue` |

### ☀️ Contact Created -> Brain Engine / Fetch Agent Config (Pre-Insert)

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### ⏱️ Contact Intake Queue Processor / Business Hours Now?

- **Node type:** `n8n-nodes-base.code`
- **Tables:** `timezones`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Check if current time is within business hours for any agent // We use a general check here - queue items have their own scheduled_for const now = $now; const utcHour = now.hour; // We process the queue if it's between 6am-11pm UTC (covers all US timezones 9am-8pm) const isProcessingWindow = utcHour >= 13 && utcHour <= 24 \|\| utcHour >= 0 && utcHour <= 3; return [{ json: { should_process: true, checked_at: now.toISO() } }];` |

### ⏱️ Contact Intake Queue Processor / Mark Processing

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `contact_intake_queue` |

### ⏱️ Contact Intake Queue Processor / Send Intro Email

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsonBody` | `={ "type": "Email", "contactId": "{{ $('Parse Payload').item.json.payload.contact_id }}", "locationId": "{{ $('Parse Payload').item.json.payload.location_id }}", "subject": "Quick intro from {{ $('Parse Payload').item.json.payload.coordinator_name }} - {{ $('Parse Payload').item.json.payload.agent_name }}'s team", "emailFrom": "{{ $('Parse Payload').item.json.payload.coordinator_name }} <{{ $('Parse Payload').item.json.payload.coordinator_email }}>", "html": "<p>Hi {{ $('Parse Payload').item.jso…` |

### ⏱️ Contact Intake Queue Processor / Mark Intro Complete

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `contact_intake_queue` |

### ⏱️ Contact Intake Queue Processor / Check Lead State

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### ⏱️ Contact Intake Queue Processor / Update Channel to SMS

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### ⏱️ Contact Intake Queue Processor / Mark Followup Complete

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `contact_intake_queue` |

### ⏱️ Contact Intake Queue Processor / Fetch Pending Items

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `contact_intake_queue`
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `-- Recover stuck items (processing for >15 min) UPDATE contact_intake_queue SET status = 'pending' WHERE status = 'processing' AND updated_at < NOW() - INTERVAL '15 minutes'; -- Mark items with 5+ attempts as failed UPDATE contact_intake_queue SET status = 'failed' WHERE status = 'pending' AND attempts >= 5; -- Fetch up to 50 PER AGENT (location_id), prevents one agent starving others WITH ranked AS ( SELECT *, ROW_NUMBER() OVER (PARTITION BY location_id ORDER BY scheduled_for ASC)…[TRUNCATED]` |

### ⏱️ Contact Intake Queue Processor / Get Agent Config

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### ⏱️ Contact Intake Queue Processor / Check Agent Hours

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const agent = $('Get Agent Config').first().json; const tz = agent.timezone \|\| 'America/Denver'; const now = $now.setZone(tz); const hour = now.hour; const weekday = now.weekday; const withinHours = weekday < 6 && hour >= 9 && hour < 20; let nextBusinessHourUtc = null; if (!withinHours) { let t = now; if (hour >= 20) t = t.plus({ days: 1 }); while (t.weekday >= 6) t = t.plus({ days: 1 }); t = t.set({ hour: 9, minute: 0, second: 0, millisecond: 0 }); nextBusinessHourUtc = t.toUTC().toI…[TRUNCATED…` |

### ⏱️ Contact Intake Queue Processor / Re-queue for Later

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `contact_intake_queue` |

### ⏱️ Contact Intake Queue Processor / Quota Gate

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT can_send, current_level, daily_cap, sent_today, remaining, reset_at, block_reason FROM check_sending_quota('{{ $('Get Agent Config').item.json.location_id }}'::text)` |

### ⏱️ Contact Intake Queue Processor / Re-queue Cap Hit

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `contact_intake_queue`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `contact_intake_queue` |

### ⏱️ Contact Intake Queue Processor / Log Followup SMS Sent

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### ⏱️ Contact Intake Queue Processor / Log Intro SMS Sent

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### ⏱️ Contact Intake Queue Processor / Log Intro Email Sent

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 📈 Daily Pacing Roll-up / Run Daily Roll-up

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT * FROM run_daily_pacing_rollup()` |

### 📈 Daily Pacing Roll-up / Format Bump Alert

- **Node type:** `n8n-nodes-base.code`
- **Tables:** `agents`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Build a summary of agents that earned level bumps const bumps = $input.all().map(item => { const j = item.json; return { location_id: j.out_location_id, current_level: j.out_level, new_level: j.out_recommended_new_level, sent_yesterday: j.out_sent, delivery_rate: j.out_delivery_rate }; }); return [{ json: { summary: `${bumps.length} agent(s) earned a level bump`, details: bumps, next_action: 'Manually bump agents.sending_level via Supabase UI (audit tr…[TRUNCATED]` |

### 📈 Daily Pacing Roll-up / Note

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agent_sending_stats`, `agents`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 📈 Daily Pacing Roll-up **Schedule:** Cron `0 12 * * *` = 12:00 UTC daily = 6am MT (works with DST too — close enough). **What it does:** 1. Runs `run_daily_pacing_rollup()` SQL function 2. Per agent: counts yesterday's sent+delivered, inserts agent_sending_stats row 3. Flags agents that hit cap = recommend level bump **Manual step:** Level bump UPDATE blocked by audit trigger bug. Admin bumps `agents.sending_level` manually via Supabase UI when notified. **Activate after Phase 1.5 test da…[TR…` |

### 📰 Data Source & Newsletter Creation / Get Newsletter Agents

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 📰 Data Source & Newsletter Creation / Generate Newsletter

- **Node type:** `@n8n/n8n-nodes-langchain.openAi`
- **Tables:** `newsletters`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `messages.values[1].content` | `=Generate a weekly market newsletter for **{{ $json.market_name }}**. ## Local Market Data (Altos Research) {{ JSON.stringify($json.altos_data, null, 2) }} ## National/Global Context & Local Impact {{ JSON.stringify($json.perplexity_data, null, 2) }} ## Previous Newsletters (last 2 weeks -- for continuity and week-over-week context) {{ $json.previous_newsletters && $json.previous_newsletters.length > 0 ? JSON.stringify($json.previous_newsletters, null, 2) : 'No previous newsletters available …[T…` |

### 📰 Data Source & Newsletter Creation / Extract Splinters

- **Node type:** `@n8n/n8n-nodes-langchain.openAi`
- **Tables:** none explicitly matched
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `messages.values[0].content` | `SMRT NEWSLETTER SPLINTER LAYER - CANONICAL RECORD GENERATOR You are a post-newsletter processing layer inside the SMRT system. Your job is to take a completed weekly real estate market newsletter and convert it into a small set of structured market splinter records. PRIMARY OBJECTIVE: Convert one completed newsletter into 3 to 5 canonical market splinter records. Each splinter record should: 1. capture one distinct market shift, tension, or behavioral insight 2. be semantically rich enough fo…[T…` |

### 📰 Data Source & Newsletter Creation / Store Newsletter

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `newsletters`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `newsletters` |

### 📰 Data Source & Newsletter Creation / Store Splinter

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `content_splinters`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `content_splinters` |

### 📰 Data Source & Newsletter Creation / Set File Content

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const data = $input.first().json; const binaryData = Buffer.from(data.docContent, 'utf8'); return { json: data, binary: { data: { data: binaryData.toString('base64'), mimeType: 'text/markdown', fileName: data.fileName + '.md' } } };` |

### 📰 Data Source & Newsletter Creation / Get Last Week Stats

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `altos_weekly_stats`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `altos_weekly_stats` |

### 📰 Data Source & Newsletter Creation / Prep Data for AI

- **Node type:** `n8n-nodes-base.code`
- **Tables:** `newsletters`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const condensedData = $('Condense Altos Data').first().json; const grokResponse = $('Grok National Context').first().json; let nationalContext = ''; if (grokResponse.choices && grokResponse.choices[0]?.message?.content) { nationalContext = grokResponse.choices[0].message.content; } else if (grokResponse.message?.content) { nationalContext = grokResponse.message.content; } else if (grokResponse.content) { nationalContext = grokResponse.content; } // Previous newsletters for week-over-week…[TRUNCA…` |

### 📰 Data Source & Newsletter Creation / Store Weekly Stats

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `altos_weekly_stats`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `altos_weekly_stats` |

### 📰 Data Source & Newsletter Creation / Check Week Stats Exist

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `altos_weekly_stats`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `altos_weekly_stats` |

### 📰 Data Source & Newsletter Creation / Check Newsletter For Week

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `newsletters`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `newsletters` |

### 📰 Data Source & Newsletter Creation / Delete Old Splinters

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `content_splinters`
- **Operation signals:** delete, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `content_splinters` |

### 📰 Data Source & Newsletter Creation / Remove Old Market Docs

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `documents`
- **Operation signals:** delete

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `delete` |
| `tableId` | `documents` |

### 📰 Data Source & Newsletter Creation / Store Embedded Doc

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** `documents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `url` | `https://kfoijgcbkjeizxxyiwxv.supabase.co/rest/v1/documents` |
| `jsonBody` | `={{ (() => { const doc = $('Prepare Storage Data').item.json.market_doc; const emb = $json.data[0].embedding; return JSON.stringify({ content: doc.content, metadata: doc.metadata, embedding: '[' + emb.join(',') + ']', location_id: doc.location_id, document_type: 'market_weekly', week_start_date: doc.week_start_date }); })() }}` |

### 📰 Data Source & Newsletter Creation / Upload to Supabase Storage

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `headerParameters.parameters[1].name` | `x-upsert` |

### 📰 Data Source & Newsletter Creation / Get Altos Hash

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const agentData = $('Prepare Agent Data').first().json; const countyFips = agentData.county_fips \|\| '16001'; const pai = agentData.pai \|\| '690acaf9'; const resp = await globalThis.fetch('https://altos.re/api/v2/reports?[REDACTED_QUERY]' + countyFips + '&pai=' + pai); const data = await resp.json(); if (!data.id) throw new Error('No hash from Altos: ' + JSON.stringify(data)); return [{ json: { hash: data.id } }];` |

### 📰 Data Source & Newsletter Creation / Get Previous Newsletters

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `newsletters`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `newsletters` |

### 📰 Data Source & Newsletter Creation / Pass Location ID

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 📄 Document Ingestion / Default Data Loader

- **Node type:** `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `options.metadata.metadataValues[0].value` | `={{ $('Set Location from Lookup').first().json.file_id }}` |
| `options.metadata.metadataValues[1].value` | `={{ $('Set Location from Lookup').first().json.location_id }}` |
| `options.metadata.metadataValues[2].value` | `={{ $('Set Location from Lookup').first().json.agent_name }}` |

### 📄 Document Ingestion / Download File

- **Node type:** `n8n-nodes-base.googleDrive`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `fileId.value` | `={{ $('Set Location from Lookup').first().json.file_id }}` |

### 📄 Document Ingestion / Set File ID

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 📄 Document Ingestion / Insert into Supabase Vectorstore

- **Node type:** `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- **Tables:** `documents`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `mode` | `insert` |
| `tableName.value` | `documents` |
| `tableName.cachedResultName` | `documents` |
| `options.queryName` | `match_documents` |

### 📄 Document Ingestion / Sticky Note4

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agents`, `documents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 📥 Document Ingestion Flow (Polling) **Trigger:** Polls every 60 minutes for new files **How it works:** 1. Get all agent folder IDs from `agents` table 2. Search Google Drive for files created in last 65 mins in those folders 3. For each new file → Lookup agent by parent folder 4. Check for duplicates in `documents` table 5. If new → Download, extract text, generate embeddings 6. Store in Supabase with metadata **Folder Structure:** ``` SMRT/ ├── Agent Name (locID)/ │ ├── FAQ.pdf │…[TRUNCATED…` |

### 📄 Document Ingestion / Check for Duplicate

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `documents`
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT id FROM documents WHERE metadata->>'file_id' = '{{ $('Set File ID').first().json.file_id }}' LIMIT 1;` |

### 📄 Document Ingestion / Lookup Agent by Folder

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT location_id, agent_name, knowledge_base_folder_name FROM agents WHERE TRIM(REPLACE(knowledge_base_folder_id, E'\n', '')) = '{{ $json.parent_folder_id }}' LIMIT 1;` |

### 📄 Document Ingestion / Set Location from Lookup

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `assignments.assignments[0].id` | `file-id-set` |
| `assignments.assignments[0].value` | `={{ $('Set File ID').first().json.file_id }}` |
| `assignments.assignments[1].id` | `location-id-set` |
| `assignments.assignments[2].id` | `agent-name-set` |

### 📄 Document Ingestion / Delete Documents

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `documents`
- **Operation signals:** delete, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=DELETE FROM documents WHERE (metadata->>'file_id' = '{{ $json.file_id }}' AND '{{ $json.file_id }}' != '') OR (metadata->>'location_id' = '{{ $json.location_id }}' AND '{{ $json.location_id }}' != '') OR (metadata->>'agent_name' = '{{ $json.agent_name }}' AND '{{ $json.agent_name }}' != '') RETURNING id;` |

### 📄 Document Ingestion / Sticky Note Cleanup

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** none explicitly matched
- **Operation signals:** create, delete

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 🗑️ Document Cleanup (Offboarding) POST to /webhook/document-cleanup with: - file_id: Delete specific file - location_id: Delete all docs for a location - agent_name: Delete all docs for an agent` |

### 📄 Document Ingestion / Get Agent Folders

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT knowledge_base_folder_id FROM agents WHERE knowledge_base_folder_id IS NOT NULL;` |

### 📄 Document Ingestion / Build Search Query

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const folderIds = $input.all() .map(item => item.json.knowledge_base_folder_id) .filter(id => id) .map(id => String(id).trim().replace(/\n/g, '')); if (folderIds.length === 0) { return [{ json: { skip: true, reason: 'No agent folders configured' } }]; } const parentsQuery = folderIds.map(id => `'${id}' in parents`).join(' or '); const sixtyFiveMinutesAgo = new Date(Date.now() - 65 * 60 * 1000).toISOString(); // Google Docs only const searchQuery = `(${parentsQuery}) and createdTime > …[TRUNCATED…` |

### 📄 Document Ingestion / Sanitize Text

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** create, delete, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Enhanced sanitization for DOCX and other document types // Prevents vector database corruption from binary artifacts and formatting codes const items = $input.all(); const results = []; for (const item of items) { // Get text from either 'data' or 'text' field let text = item.json.data \|\| item.json.text \|\| ''; // Skip empty items if (!text \|\| text.length === 0) { console.log('Skipping item: empty data'); continue; } // === PHASE 1: Remove binary and control charact…[TRUNCATED]` |

### 🔥 Error Catch / Log to system_errors

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `system_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `insert` |
| `tableId` | `system_errors` |

### 🔍 GHL Conversation Backfill / Set Backfill Window

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🔍 GHL Conversation Backfill / Get Agent API Key

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 🔍 GHL Conversation Backfill / Search Conversations

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `queryParameters.parameters[0].value` | `={{ $('Set Backfill Window').first().json.location_id }}` |

### 🔍 GHL Conversation Backfill / Extract Conversations

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// GHL response shape: {conversations: [...], total, traceId} const convs = $input.first().json.conversations \|\| []; const startMs = $('Set Backfill Window').first().json.start_ms; const endMs = $('Set Backfill Window').first().json.end_ms; // Filter conversations whose lastMessageDate falls in the window const inWindow = convs.filter(c => { const ts = c.lastMessageDate \|\| c.dateUpdated; if (!ts) return false; const ms = typeof ts === 'number' ? ts : new Date(ts).getTime(); return ms >=…[TRUNCAT…` |

### 🔍 GHL Conversation Backfill / Filter Inbound In Window

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Find inbound messages within window from each conv response const startMs = $('Set Backfill Window').first().json.start_ms; const endMs = $('Set Backfill Window').first().json.end_ms; const locationId = $('Set Backfill Window').first().json.location_id; const output = []; for (const item of $input.all()) { const messages = item.json.messages?.messages \|\| item.json.messages \|\| []; for (const m of messages) { if (m.direction !== 'inbound') continue; const ts = m.dateAdded \|\| m.date…[TRUNCATED]` |

### 🔍 GHL Conversation Backfill / Save To Inbound Capture

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `inbound_capture`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `inbound_capture` |
| `fieldsUi.fieldValues[7].fieldValue` | `Backfilled from GHL during recovery` |

### 📬 GHL Delivery Status Handler / Update Message Log

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `message_log` |

### 📬 GHL Delivery Status Handler / Log Send Error

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_send_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_send_errors` |

### 📬 GHL Delivery Status Handler / Note

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `message_log`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 📬 GHL Delivery Status Handler Receives OutboundMessage events from GHL and updates message_log.delivery_status. **Subscribe in GHL:** App Marketplace → Webhooks → OutboundMessage → POST URL = this webhook's path. **Always returns 200 OK** — GHL only retries on 429. **Phase 1.5 capture:** payload shape TBD until empirical test. Parser is defensive.` |

### 📬 GHL Delivery Status Handler / Record Cap Hit

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT public.record_cap_hit('{{ $json.location_id }}', '{{ $json.received_at }}'::timestamptz) AS result;` |

### 📬 GHL Delivery Status Handler / Auto Block Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🔍 GHL Send Status Checker / Update Message Log

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `message_log` |

### 🔍 GHL Send Status Checker / Log Send Error

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_send_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_send_errors` |

### 🔍 GHL Send Status Checker / Record Cap Hit

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT public.record_cap_hit('{{ $('Parse Response').item.json.location_id }}', '{{ $('Parse Response').item.json.checked_at }}'::timestamptz, NULLIF('{{ $('Parse Response').item.json.parsed_reset_at }}', '')::timestamptz) AS result;` |

### 🔍 GHL Send Status Checker / Auto Block Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🔁 Inbound Replay / Get Unprocessed Messages

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `inbound_capture`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT id, payload, headers, ghl_message_id, captured_at, replay_count FROM inbound_capture WHERE processed = false ORDER BY captured_at ASC LIMIT 100` |

### 🔁 Inbound Replay / Mark As Processed

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `inbound_capture`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `inbound_capture` |

### 📬 Newsletter Dispatch / Fetch Active Agents

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 📬 Newsletter Dispatch / Log Delivery

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `newsletter_deliveries`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `newsletter_deliveries` |

### 📬 Newsletter Dispatch / Sticky Note - Trigger

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 1. TRIGGER & AGENT FETCH **Weekly Schedule** fires every Monday at 10 AM (America/Denver). **Fetch Active Agents** pulls all agents where `newsletter_enabled = true`. Loop iterates one agent at a time.` |

### 📬 Newsletter Dispatch / Sticky Note - Newsletter + Cadence

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `leads`, `newsletter_deliveries`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 2. NEWSLETTER + CADENCE FILTERING **Get Newest Newsletter** fetches latest by `week_start_date DESC` for this agent's location. **Fetch Eligible Leads** pulls opted-in leads, then filters by cadence: - WEEKLY/APPT_SET/APPT_OFFERED: every week - BIWEEKLY: every 2 weeks - MONTHLY/cold: every 4 weeks Checks `newsletter_deliveries` for last send date per lead.` |

### 📬 Newsletter Dispatch / Sticky Note - Send & Log

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `newsletter_deliveries`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 3. BUILD, SEND & LOG **Build HTML Email** wraps `full_content` in HTML template with unsubscribe footer (Reply STOP). **Send Email via GHL** sends as Email type via conversations/messages API. **Log Delivery** inserts into `newsletter_deliveries` with status=sent + lead_id. After logging, loops back to next agent. **To test:** Hit Test Workflow in the editor. Your lead (Hobaid) is opted in with APPT_OFFERED stage = WEEKLY cadence.` |

### 📬 Newsletter Dispatch / Update Send Counts

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 📬 Newsletter Dispatch / Stamp Supabase Key

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🎉 Onboarding — Part 1: DB Enrichment / Sticky Note: Main

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `onboarding_requests`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## 🎉 Onboarding — Part 1: DB Enrichment Handles all safe, reversible onboarding work: 1. Validates all required fields (stops here if missing) 2. Fetches personality chunks and assembles personality prompt 3. Creates Google Drive KB folder 4. Creates FAQ Google Doc 5. Saves everything to the onboarding_requests staging table 6. Triggers Part 2 (GHL Setup) only if ALL fields are complete **Nothing irreversible happens in this workflow.**` |

### 🎉 Onboarding — Part 1: DB Enrichment / Sticky Note: DB Staging Section

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `onboarding_requests`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Database Staging Saves all enriched onboarding data to the onboarding_requests table. This is the handoff point — the staging record ID is passed to Part 2 (GHL Setup). If GHL setup fails, re-trigger Part 2 via POST /onboarding-ghl-setup with the onboarding_request_id.` |

### 🎉 Onboarding — Part 1: DB Enrichment / Note: Onboarding Call Checklist

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Onboarding Call Checklist Collect all of the following before or during the onboarding call. ### Agent Info - Full name - Business name - Email address - Phone number - Timezone - City and state - Target ZIP codes (service area) ### GHL Sub-Account - Sub-account Location ID (Agency -> Locations -> click location -> Settings -> grab ID from URL) - Buyer calendar ID (GHL -> Calendars -> click calendar -> grab ID from URL) - Seller calendar ID - GHL user ID (GHL -> Settings -> My Profile…[TRUNCA…` |

### 🎉 Onboarding — Part 1: DB Enrichment / Extract Agent Data

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🎉 Onboarding — Part 1: DB Enrichment / Set Default Personality

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `assignments.assignments[0].value` | `# Agent Personality You are calm, steady, and structurally precise. You speak the way a competent professional thinks — clearly, without filler, without performance. Your presence is the point. You show up consistently, deliver something useful, and leave space. You are not trying to earn a response. You are not measuring whether your messages "work." You are maintaining a rhythm of awareness that the other person can lean into whenever they're ready — or never. You are diagnostic, not reacti…[T…` |

### 🎉 Onboarding — Part 1: DB Enrichment / Set Folder ID

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🎉 Onboarding — Part 1: DB Enrichment / Create FAQ Google Doc

- **Node type:** `n8n-nodes-base.googleDrive`
- **Tables:** none explicitly matched
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `folderId.value` | `={{ $('Set Folder ID').first().json.knowledge_base_folder_id }}` |

### 🎉 Onboarding — Part 1: DB Enrichment / Add FAQ Questions

- **Node type:** `n8n-nodes-base.googleDocs`
- **Tables:** `agents`, `leads`
- **Operation signals:** create, read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `actionsUi.actionFields[0].text` | `SMRT Knowledge Base - Agent FAQ Please fill out the answers below. This document will be used by your AI assistant (SMRT) to respond to leads on your behalf. --- 1. What areas do you serve? Answer: 2. What types of clients do you work with? Answer: 3. What is your typical process from first contact to closing? Answer: 4. How do you prefer to communicate with leads? Answer: 5. What sets you apart from other agents? Answer: 6. What questions do leads most commonly ask? Answer: 7. Ar…[TRUNCATED]` |

### 🎉 Onboarding — Part 1: DB Enrichment / Save to onboarding_requests

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `onboarding_requests`
- **Operation signals:** reference

### 🎉 Onboarding — Part 1: DB Enrichment / Prepare GHL Handoff

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🎉 Onboarding — Part 1: DB Enrichment / Delete Old Agent Bio

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `documents`
- **Operation signals:** delete, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=DELETE FROM documents WHERE location_id = '{{ $json.location_id }}' AND document_type = 'agent_bio';` |

### 🎉 Onboarding — Part 1: DB Enrichment / Insert Bio to Vectorstore

- **Node type:** `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- **Tables:** `documents`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `mode` | `insert` |
| `tableName.value` | `documents` |
| `tableName.cachedResultName` | `documents` |
| `options.queryName` | `match_documents` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - GHL

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** none explicitly matched
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## GHL Sub-Account Creation Create new sub-account and apply SMRT snapshot. **SNAPSHOT_ID** must be set as an n8n variable (`$vars.SNAPSHOT_ID`) or hardcoded here. GHL Created? gate stops the flow if creation fails.` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - DB Config

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agents`, `onboarding_requests`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Database Configuration Inserts full agent config into Supabase agents table using location_id returned by GHL. Data sourced from onboarding_requests staging record.` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - Pipeline Config

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agents`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Pipeline Config Auto-Pull After snapshot applied, fetches all pipelines and builds pipeline_config JSONB for agents table. Matches pipelines by name keywords: incubator/nurture/lead, buyer/buying, seller/selling/listing Stage names normalized to UPPER_SNAKE_CASE.` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - Calendar Setup

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `agents`
- **Operation signals:** create, read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Calendar Setup (Post-Snapshot) After GHL snapshot is applied, the agent's calendar ID needs to be stored in Supabase. ### agents table field - buyer_calendar_id — stores the agent's single calendar ID ### To do after W2 is live 1. HTTP GET https://services.leadconnectorhq.com/calendars/?[REDACTED_QUERY] 2. Find the correct calendar by name 3. UPDATE agents SET buyer_calendar_id = ... WHERE location_id = ... ### Collect during onboarding call - Calendar name (for auto-pull matching) - ghl_…[TR…` |

### 🏗️ Onboarding — Part 2: GHL Setup / Normalize Webhook Input

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🏗️ Onboarding — Part 2: GHL Setup / Load Onboarding Request

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `onboarding_requests`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT * FROM onboarding_requests WHERE id = '{{ $json.onboarding_request_id }}'::uuid AND status = 'pending_ghl' LIMIT 1;` |

### 🏗️ Onboarding — Part 2: GHL Setup / Extract Location ID

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🏗️ Onboarding — Part 2: GHL Setup / Insert Default Agent Rules

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `agent_rules`, `appointments`, `leads`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `INSERT INTO agent_rules (location_id, rule_type, rule_content, priority) VALUES ('{{ $('Extract Location ID').first().json.location_id }}', 'greeting', 'Always greet leads warmly and professionally', 1), ('{{ $('Extract Location ID').first().json.location_id }}', 'scheduling', 'Push for appointments when lead shows interest', 2), ('{{ $('Extract Location ID').first().json.location_id }}', 'escalation', 'Transfer to human if lead asks for specific agent or becomes frustrated', 3);` |

### 🏗️ Onboarding — Part 2: GHL Setup / Gather Pipeline Context

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🏗️ Onboarding — Part 2: GHL Setup / Save Pipeline Config

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `agents`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `UPDATE agents SET pipeline_config = '{{ JSON.stringify($json.pipeline_config) }}'::jsonb, updated_at = NOW() WHERE location_id = '{{ $json.location_id }}';` |

### 🏗️ Onboarding — Part 2: GHL Setup / Mark Agent as Live

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `agents`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `UPDATE agents SET active = true, onboarding_completed_at = NOW(), updated_at = NOW() WHERE location_id = '{{ $(''Extract Location ID'').first().json.location_id }}';` |

### 🏗️ Onboarding — Part 2: GHL Setup / Complete Onboarding Request

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `onboarding_requests`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `UPDATE onboarding_requests SET status = 'ghl_complete', location_id = '{{ $(''Extract Location ID'').first().json.location_id }}', updated_at = NOW() WHERE id = '{{ $(''Load Onboarding Request'').first().json.id }}'::uuid;` |

### 🧠 SMRT Brain Engine / LeadDetails

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / searchLeads

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / addLead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / errorLogMessageType

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** none explicitly matched
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |

### 🧠 SMRT Brain Engine / carryContactID

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Set Direction: Inbound

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Update Last Agent Message

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / logMessageLeads

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 🧠 SMRT Brain Engine / Get Agent Config (RAG)

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 🧠 SMRT Brain Engine / Get Message History

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `message_log`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $('LeadDetails').first().json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id = '{{ $('LeadDetails').first().json.contact_id }}' ORDER BY ml.timestamp DESC LIMIT 15` |

### 🧠 SMRT Brain Engine / Get Conversation Summary

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / Log Outbound Message

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 🧠 SMRT Brain Engine / AI Sentiment Analysis

- **Node type:** `@n8n/n8n-nodes-langchain.anthropic`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `messages.values[0].content` | `=CONVERSATION CONTEXT (read first — context frames the current message): Conversation Summary: {{ $json.conversationSummary }} Recent Messages (newest last): {{ $json.historyText }} Lead State: - First Name: {{ $json.firstName }} - Agent: {{ $json.agentName }} - Pipeline Stage: {{ $json.pipelineStage }} - Pipeline State: {{ $json.pipelineState }} === CURRENT MESSAGE (classify using STEP 1 → 4 from system prompt) === {{ $json.currentMessage }} Return ONLY valid JSON. No markdown fences. No e…[TRU…` |
| `options.system` | `You are a sentiment classifier for SMRT Bot. You analyze inbound messages and classify them into behavioral tiers to route the Brain Engine correctly. CRITICAL: Your reasoning field is used INTERNALLY by downstream nodes ONLY. It is NEVER shown to the lead. The Brain Engine AI Agent uses its own prompt to write the actual SMS/email reply. Be thorough in your reasoning - it helps downstream routing, it never leaks to the customer. === CLASSIFICATION PRIORITY ORDER === Follow these steps IN ORD…[T…` |

### 🧠 SMRT Brain Engine / Parse Sentiment

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const input = $json; let parsed; try { let text = ''; if (input.content && Array.isArray(input.content)) { text = input.content.map(c => c.text \|\| '').join(''); } else if (input.message && input.message.content) { text = input.message.content; } else if (input.text) { text = input.text; } else if (typeof input === 'string') { text = input; } else { text = JSON.stringify(input); } const fenceMatch = text.match(/\`\`\`(?:json)?\n?([\s\S]*?)\`\`\`/); if (fe…[TRUNCATED]` |

### 🧠 SMRT Brain Engine / KB Tool

- **Node type:** `@n8n/n8n-nodes-langchain.toolVectorStore`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `description` | `=Search the approved company knowledge base for client location {{ (() => { try { return $('Set Outbound Context').first().json.location_id } catch(e) { return $('LeadDetails').first().json.location_id } })() }}. WHEN TO USE: - When the lead asks about commission rates, fees, or pricing - When the lead asks about services offered, property types, or areas served - When the lead asks how the team operates or any company-specific question - ANY question about the business, team, or real estate se……` |

### 🧠 SMRT Brain Engine / Docs Store

- **Node type:** `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- **Tables:** `documents`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableName.value` | `documents` |
| `tableName.cachedResultName` | `documents` |
| `options.queryName` | `match_documents` |
| `options.metadata.metadataValues[0].value` | `={{ (() => { try { return $('Set Outbound Context').first().json.location_id } catch(e) { return $('LeadDetails').first().json.location_id } })() }}` |

### 🧠 SMRT Brain Engine / Set Direction: Inbound2

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Apply Time Decay

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `UPDATE leads SET pipeline_state = CASE WHEN pipeline_state = 'hot' AND last_customer_message_at < NOW() - INTERVAL '14 days' THEN 'warm' WHEN pipeline_state = 'warm' AND last_customer_message_at < NOW() - INTERVAL '42 days' THEN 'cold' ELSE pipeline_state END WHERE status = 'active_conversation' AND pipeline_state IN ('hot', 'warm') AND last_customer_message_at IS NOT NULL AND location_id = '{{ $json.location_id }}' AND ( (pipeline_state = 'hot' AND last_customer_me…[TRUNCATED]` |

### 🧠 SMRT Brain Engine / Fetch Outbound Candidates

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `WITH eligible_splinter AS ( SELECT cs.id AS splinter_id, cs.location_id, cs.content AS splinter_content, cs.topic AS splinter_topic, cs.data_point AS splinter_data_point, cs.splinter_title, cs.dominant_theme, cs.signal_type, cs.insight_core, cs.interpretation, cs.behavioral_implication, cs.audience_fit, cs.stage_fit, cs.embedding_text, cs.delivery_variants, cs.priority, cs.week_start_date, cs.created_at FROM content_spli…[TRUNCATED]` |

### 🧠 SMRT Brain Engine / Check Escalation State

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Log Already Escalated

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_log`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_log` |

### 🧠 SMRT Brain Engine / Update Lead Escalation

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Update Conversation Context

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / Prepare Tier Response

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Prepare tier-specific response instructions for the AI Agent // Pull tier/sentiment/sms_action from Parse Sentiment directly — input $json may be from Apply L1: Mark Lead (no tier) const ps = (() => { try { return $('Parse Sentiment').first().json; } catch(e) { return {}; } })(); const tier = ps.tier \|\| $json.tier \|\| 'normal'; const sentiment = ps.sentiment \|\| $json.sentiment \|\| 'neutral'; const smsAction = ps.sms_action \|\| $json.sms_action \|\| 'none'; const tierInstructions = { tier_1_conf…[T…` |

### 🧠 SMRT Brain Engine / Pause SMS 30 Days (Tier 2)

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Extract Keywords

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** none

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `const input = $input.first().json; const currentMessage = (input.message \|\| input.message_body \|\| '').toLowerCase(); const keywordPatterns = { pricing: /\b(price\|pricing\|cost\|fee\|rate\|charge\|dollar\|\$\|expensive\|cheap\|afford)\b/i, property: /\b(house\|home\|property\|apartment\|condo\|bedroom\|bath\|sqft\|square\|lot)\b/i, location: /\b(address\|where\|location\|area\|neighborhood\|city\|street\|zip)\b/i, availability: /\b(available\|availability\|vacancy\|vacant\|ready\|move.?in\|when\|schedule\|showing)\b/i, …[TRUNCAT…` |

### 🧠 SMRT Brain Engine / Search Relevant Messages

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `message_log`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT id, message_body, direction, timestamp, message_type, 'keyword_match' as source FROM message_log WHERE contact_id = '{{ $json.contact_id }}' AND id NOT IN ( SELECT id FROM message_log WHERE contact_id = '{{ $json.contact_id }}' ORDER BY timestamp DESC LIMIT 10 ) AND ( {{ $json.keywords.map(k => "message_body ILIKE '%" + k + "%'").join(' OR ') }} ) ORDER BY timestamp DESC LIMIT 5` |

### 🧠 SMRT Brain Engine / Merge & Deduplicate Messages

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** create, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Merge recent messages + keyword-matched messages, deduplicate by id const allMessages = $input.all().map(item => item.json); // Deduplicate by id (not message_id) const seen = new Set(); const uniqueMessages = []; for (const msg of allMessages) { const msgId = msg.id \|\| msg.message_id; // Support both field names if (!seen.has(msgId)) { seen.add(msgId); uniqueMessages.push(msg); } } // Sort by timestamp (newest first) uniqueMessages.sort((a, b) => { const timeA = new Date(a…[TRUNCATED]` |

### 🧠 SMRT Brain Engine / searchPastMessages

- **Node type:** `n8n-nodes-base.supabaseTool`
- **Tables:** `message_log`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `Search this lead's past message log beyond the 15 most recent messages already in your context. WHEN TO USE: - Lead references something old ("I told you", "I mentioned before", "remember when", "weeks ago") - You need to verify a claim about a past conversation - You need to recall a commitment, date, or topic from earlier in the relationship WHEN NOT TO USE: - For general knowledge or company info (use KB Tool) - For information already visible in RECENT MESSAGES (your 15-turn window) INPUT…[T…` |
| `tableId` | `message_log` |

### 🧠 SMRT Brain Engine / Get Prompt Blocks (SMRT)

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `prompt_blocks`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT pb.block_id, pb.category, pb.prompt_content, pb.priority, pb.conditions FROM prompt_blocks pb WHERE pb.is_active = true ORDER BY CASE pb.category WHEN 'mode' THEN 1 WHEN 'channel' THEN 2 WHEN 'relationship' THEN 3 WHEN 'history' THEN 4 WHEN 'situation' THEN 5 END, pb.priority DESC` |

### 🧠 SMRT Brain Engine / Get Default Personality

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `system_defaults`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT value FROM system_defaults WHERE key = 'default_personality_prompt' LIMIT 1` |

### 🧠 SMRT Brain Engine / Set Outbound Context

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Get Outbound Agent Config

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 🧠 SMRT Brain Engine / Get Outbound Message History

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `message_log`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id = '{{ $json.contact_id }}' ORDER BY ml.timestamp DESC LIMIT 15` |

### 🧠 SMRT Brain Engine / Get Outbound Conversation Summary

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / Get Agent Config

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `agents` |

### 🧠 SMRT Brain Engine / getContact

- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `Fetch the full contact profile for the current lead from GoHighLevel, including custom fields, tags, lead source, and all contact details. WHEN TO USE: - When you need lead details NOT available in the conversation (email, address, tags, lead source) - When the lead asks you to confirm their contact information - When you need CRM context about the lead's history or status INPUT: No input needed. Automatically looks up the current lead. OUTPUT: Full contact record with name, email, phone, tag…[T…` |

### 🧠 SMRT Brain Engine / getNotes

- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Tables:** `agents`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `Fetch all notes recorded on this lead's GoHighLevel contact by agents or the AI system. WHEN TO USE: - When the lead references a previous conversation or commitment ("someone told me...", "I was promised...") - When you need historical context about what has been discussed or agreed with this lead - Before escalating, to check if there are existing agent notes INPUT: No input needed. Automatically looks up the current lead. OUTPUT: List of notes with timestamps and content. RULES: - Use to …[TR…` |

### 🧠 SMRT Brain Engine / getAppointments

- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Tables:** `appointments`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `Fetch all appointments (past and upcoming) for the current lead from GoHighLevel. WHEN TO USE: - When the lead asks about existing appointments ("when is my appointment?", "do I have anything scheduled?") - When the lead wants to cancel or reschedule (you need the event_id from here) - When you need to check if the lead already has a booking before offering to schedule INPUT: No input needed. Automatically looks up the current lead. OUTPUT: List of appointment objects with event IDs, dates, t…[T…` |
| `url` | `=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/appointments` |

### 🧠 SMRT Brain Engine / Insert Conversation Context

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / checkQualificationStatus

- **Node type:** `n8n-nodes-base.supabaseTool`
- **Tables:** `conversation_context`
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `Check how many of the 3 qualifying questions this lead has answered so far. WHEN TO USE: - BEFORE calling saveQualifyingAnswer, to get the current qualifying_answers object - When the lead says they want to book an appointment, to verify they are qualified - When you are unsure which qualifying questions have already been answered INPUT: No input needed. Automatically looks up this lead's conversation_context record. OUTPUT: Returns the qualifying_answers JSONB object with keys q1, q2, q3. - …[T…` |
| `tableId` | `conversation_context` |
| `filters.conditions[0].keyValue` | `={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}` |

### 🧠 SMRT Brain Engine / saveQualifyingAnswer

- **Node type:** `n8n-nodes-base.supabaseTool`
- **Tables:** `conversation_context`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `toolDescription` | `MANDATORY TOOL - Save a qualifying answer to the database after the lead answers one of the 3 qualifying questions. WHEN TO USE: You MUST call this tool IMMEDIATELY every time the lead provides information that answers Q1, Q2, or Q3. Do NOT wait until all questions are answered. Save each answer the moment you receive it. The tool updates the qualifying_answers JSONB column in conversation_context for this lead. INPUT: You must provide a JSON object with the field 'qualifying_answers' contain…[T…` |
| `operation` | `update` |
| `tableId` | `conversation_context` |
| `filters.conditions[0].keyValue` | `={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}` |

### 🧠 SMRT Brain Engine / Check Qualification Gate

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / Get Lead Memory

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Get Lead Memory (After)

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Build GHL Sync Body

- **Node type:** `n8n-nodes-base.code`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `jsCode` | `// Get GHL custom field definitions from input (Get GHL Contact) const ghlFields = $input.first().json.customFields \|\| []; // Get memory + enrichment values from Compare Memory const mem = $('Compare Memory').first().json; // === CORE FIELDS (standard GHL contact fields) === const coreFields = {}; if (mem.first_name) coreFields.firstName = mem.first_name; if (mem.last_name) coreFields.lastName = mem.last_name; if (mem.email) coreFields.email = mem.email; if (mem.phone) coreFields.phone = mem.p…[…` |

### 🧠 SMRT Brain Engine / Update Inbound Timestamps

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Update Pipeline in DB

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / updateContactMemory

- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `description` | `Update the contact's memory and enrichment fields. Call this when you detect ANY of the signals below. Include ALL detected fields in a single call — never make multiple calls. INPUT (required JSON): - contact_id: string - CONTACT_ID from context (always required) - Plus any fields below that you detected: FIELD TRIGGERS — scan every message for these: IDENTITY / CONTACT INFO - Lead says their name → first_name, last_name - Lead gives their email address → email - Lead gives their phone numbe…[T…` |

### 🧠 SMRT Brain Engine / Get Outbound Lead Memory

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Set Newsletter Pending

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / Clear Newsletter Flags

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `conversation_context`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `conversation_context` |

### 🧠 SMRT Brain Engine / subscribeToNewsletter

- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Tables:** `leads`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `description` | `Subscribe the current lead to the weekly market newsletter. Updates leads.newsletter_opted_in = true, tags the contact in GHL, and clears pending flags. INPUT (required JSON): - contact_id: string - the CONTACT_ID from the context header (always required) CALL THIS TOOL when the lead signals they want market updates, want to stay in the loop, accept the newsletter offer, or agree to receive periodic info. Call it BEFORE you write your response acknowledging the subscription — never acknowledge…[…` |

### 🧠 SMRT Brain Engine / Get Static Prompt Sections

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `static_prompt_sections`
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `static_prompt_sections` |

### 🧠 SMRT Brain Engine / Record Splinter Usage

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `splinter_usage`
- **Operation signals:** reference

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `splinter_usage` |

### 🧠 SMRT Brain Engine / Gather Prompt Data

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `assignments.assignments[4].value` | `={{ (() => { try { return $('Set Outbound Context').first().json.direction; } catch(e) { try { return $('LeadDetails').first().json.direction \|\| 'inbound'; } catch(e2) { return 'inbound'; } } })() }}` |
| `assignments.assignments[5].value` | `={{ (() => { try { return $('Set Outbound Context').first().json.channel; } catch(e) { try { return $('LeadDetails').first().json.channel; } catch(e2) { return 'sms'; } } })() }}` |
| `assignments.assignments[6].value` | `={{ (() => { try { return $('Set Outbound Context').first().json.first_name; } catch(e) { try { return $('LeadDetails').first().json.first_name; } catch(e2) { return 'Contact'; } } })() }}` |
| `assignments.assignments[7].value` | `={{ (() => { try { return $('Set Outbound Context').first().json.contact_id; } catch(e) { try { return $('LeadDetails').first().json.contact_id; } catch(e2) { return ''; } } })() }}` |

### 🧠 SMRT Brain Engine / Gather Sentiment Data1

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** read, update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `assignments.assignments[0].value` | `={{ (() => { try { const b = $('Check Batch Leader').first().json.batchedMessageBody; if (b) return b; } catch(e) {} try { return $('LeadDetails').first().json.message; } catch(e) { try { return $('Set Outbound Context').first().json.message; } catch(e2) { return ''; } } })() }}` |
| `assignments.assignments[1].value` | `={{ (() => { try { return $('LeadDetails').first().json.contact_id; } catch(e) { try { return $('Set Outbound Context').first().json.contact_id; } catch(e2) { return ''; } } })() }}` |
| `assignments.assignments[2].value` | `={{ (() => { try { return $('LeadDetails').first().json.location_id; } catch(e) { try { return $('Set Outbound Context').first().json.location_id; } catch(e2) { return ''; } } })() }}` |
| `assignments.assignments[3].value` | `={{ (() => { try { return $('LeadDetails').first().json.first_name; } catch(e) { try { return $('Set Outbound Context').first().json.first_name; } catch(e2) { return 'Contact'; } } })() }}` |

### 🧠 SMRT Brain Engine / switchChannel

- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `description` | `Switch the lead's communication channel and send a hardcoded bridge message on the new channel. Call this ONLY when the lead explicitly asks to move to a different channel (e.g. "just email me", "text me instead"). SUPPORTED DESTINATIONS: sms, email. You CANNOT switch TO Instagram DM — only FROM it. If a lead asks to be contacted on Instagram, politely decline and offer SMS or email instead. INPUT (required JSON): - contact_id: string — CONTACT_ID from context - new_channel: string — must be "…[…` |

### 🧠 SMRT Brain Engine / Stamp Batch Key

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Sticky Note - Wait Window

- **Node type:** `n8n-nodes-base.stickyNote`
- **Tables:** `message_log`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `content` | `## Wait Window — Message Batching **60s debounce + batch leader election.** Stamp log ID → wait 60s → query message_log for last 90s of inbound messages from this contact → newest message (by timestamp, id tiebreaker) is the leader. - TRUE (leader): proceeds through pipeline with `batchedMessageBody` (all messages joined) - FALSE (not leader): dead-ends silently — another execution will respond If query fails, node fail-safes to leader with single message body (so we never drop a response).` |

### 🧠 SMRT Brain Engine / Turnaround: Clear State

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=UPDATE leads SET opt_out_level=NULL, opted_out_at=NULL, opt_out_reason=NULL, sms_paused_until=NULL, status='active_conversation' WHERE contact_id='{{ $('LeadDetails').first().json.contact_id }}'` |

### 🧠 SMRT Brain Engine / Turnaround: Remove L1 Tag

- **Node type:** `n8n-nodes-base.httpRequest`
- **Tables:** none explicitly matched
- **Operation signals:** delete

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `method` | `DELETE` |

### 🧠 SMRT Brain Engine / Apply L1: Mark Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Apply L2: Mark Lead

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `leads`
- **Operation signals:** update

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `operation` | `update` |
| `tableId` | `leads` |

### 🧠 SMRT Brain Engine / Log AI Leak

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `ai_output_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `ai_output_errors` |

### 🧠 SMRT Brain Engine / Save Inbound Capture

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `inbound_capture`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `inbound_capture` |

### 🧠 SMRT Brain Engine / Check Capture Mode

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** `system_defaults`
- **Operation signals:** create, read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `SELECT value FROM system_defaults WHERE key = 'inbound_capture_mode' LIMIT 1` |

### 🧠 SMRT Brain Engine / Prep Status Check Input

- **Node type:** `n8n-nodes-base.set`
- **Tables:** none explicitly matched
- **Operation signals:** update

### 🧠 SMRT Brain Engine / Cap Lock Check

- **Node type:** `n8n-nodes-base.postgres`
- **Tables:** none explicitly matched
- **Operation signals:** read

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `query` | `=SELECT can_send, current_level, daily_cap, sent_today, remaining, reset_at, block_reason FROM check_sending_quota('{{ $('Assemble System Prompt').item.json.locationId }}'::text);` |

### 🧠 SMRT Brain Engine / Log Cap Suppression

- **Node type:** `n8n-nodes-base.supabase`
- **Tables:** `message_send_errors`
- **Operation signals:** create

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `tableId` | `message_send_errors` |
