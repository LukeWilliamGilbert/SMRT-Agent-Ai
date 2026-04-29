# GoHighLevel Boundary Map for SMRT

**Author:** Manus AI  
**Date:** 2026-04-29  
**Scope:** Static, read-only extraction from sanitized n8n workflow exports. This map identifies observed GHL entry points, API exits, reads, and Supabase mirror surfaces.

> This is a boundary map, not a production change. It does not prove which GHL records currently exist; it shows where the exported workflows appear to enter, exit, or mirror GoHighLevel data.

## Summary

| Metric | Count |
| --- | ---: |
| Workflows Scanned | 21 |
| Workflows With Ghl Refs | 15 |
| Ghl Relevant Nodes | 133 |

## Direction Counts

| Direction | Nodes |
| --- | ---: |
| `ghl_reference_or_transform` | 61 |
| `exit_to_ghl_api` | 48 |
| `entry_from_ghl_or_external_webhook` | 13 |
| `read_from_ghl_api` | 11 |

## GHL Domain Counts

| Domain | Nodes |
| --- | ---: |
| `webhooks` | 78 |
| `contacts` | 74 |
| `conversations_messages` | 73 |
| `users_locations` | 42 |
| `calendars_appointments` | 18 |
| `opportunities_pipelines` | 13 |

## Supabase Tables Mentioned Near GHL Logic

| Table | Mentions |
| --- | ---: |
| `message_log` | 12 |
| `leads` | 11 |
| `onboarding_requests` | 5 |
| `conversation_context` | 5 |
| `appointments` | 4 |
| `message_send_errors` | 4 |
| `inbound_capture` | 3 |
| `agents` | 3 |
| `Documents` | 1 |
| `newsletter_deliveries` | 1 |
| `agent_rules` | 1 |
| `ai_output_errors` | 1 |

## Workflow-Level Boundary Summary

| Workflow | Active | GHL Nodes | Directions | Domains | Supabase Tables Near GHL Logic |
| --- | --- | ---: | --- | --- | --- |
| 🧠 SMRT Brain Engine | True | 58 | `entry_from_ghl_or_external_webhook`: 2<br>`exit_to_ghl_api`: 23<br>`ghl_reference_or_transform`: 31<br>`read_from_ghl_api`: 2 | `calendars_appointments`: 11<br>`contacts`: 42<br>`conversations_messages`: 31<br>`opportunities_pipelines`: 7<br>`users_locations`: 11<br>`webhooks`: 30 | `agents`: 1<br>`ai_output_errors`: 1<br>`appointments`: 1<br>`conversation_context`: 5<br>`inbound_capture`: 1<br>`leads`: 6<br>`message_log`: 2<br>`message_send_errors`: 1 |
| 🏗️ Onboarding — Part 2: GHL Setup | False | 14 | `entry_from_ghl_or_external_webhook`: 2<br>`exit_to_ghl_api`: 5<br>`ghl_reference_or_transform`: 6<br>`read_from_ghl_api`: 1 | `calendars_appointments`: 2<br>`contacts`: 1<br>`conversations_messages`: 1<br>`opportunities_pipelines`: 3<br>`users_locations`: 9<br>`webhooks`: 5 | `agent_rules`: 1<br>`agents`: 2<br>`appointments`: 1<br>`leads`: 1<br>`onboarding_requests`: 3 |
| ☀️ Contact Created -> Brain Engine | True | 10 | `entry_from_ghl_or_external_webhook`: 1<br>`exit_to_ghl_api`: 4<br>`ghl_reference_or_transform`: 3<br>`read_from_ghl_api`: 2 | `contacts`: 9<br>`conversations_messages`: 5<br>`opportunities_pipelines`: 2<br>`users_locations`: 3<br>`webhooks`: 7 | `leads`: 2 |
| 🎉 Onboarding — Part 1: DB Enrichment | False | 10 | `entry_from_ghl_or_external_webhook`: 3<br>`exit_to_ghl_api`: 1<br>`ghl_reference_or_transform`: 4<br>`read_from_ghl_api`: 2 | `calendars_appointments`: 2<br>`contacts`: 2<br>`conversations_messages`: 3<br>`users_locations`: 2<br>`webhooks`: 8 | `onboarding_requests`: 2 |
| ⏱️ Contact Intake Queue Processor | False | 7 | `exit_to_ghl_api`: 4<br>`ghl_reference_or_transform`: 3 | `contacts`: 7<br>`conversations_messages`: 6<br>`users_locations`: 6<br>`webhooks`: 7 | `message_log`: 3 |
| 📬 GHL Delivery Status Handler | True | 7 | `entry_from_ghl_or_external_webhook`: 2<br>`exit_to_ghl_api`: 2<br>`ghl_reference_or_transform`: 3 | `contacts`: 2<br>`conversations_messages`: 5<br>`users_locations`: 2<br>`webhooks`: 4 | `message_log`: 2<br>`message_send_errors`: 1 |
| 🔍 GHL Conversation Backfill | False | 5 | `exit_to_ghl_api`: 1<br>`ghl_reference_or_transform`: 2<br>`read_from_ghl_api`: 2 | `contacts`: 1<br>`conversations_messages`: 5<br>`users_locations`: 3<br>`webhooks`: 2 | `inbound_capture`: 1 |
| 🔍 GHL Send Status Checker | True | 5 | `exit_to_ghl_api`: 2<br>`ghl_reference_or_transform`: 2<br>`read_from_ghl_api`: 1 | `contacts`: 1<br>`conversations_messages`: 4<br>`users_locations`: 1<br>`webhooks`: 4 | `message_log`: 1<br>`message_send_errors`: 1 |
| ⏰ Appointment Reminders | True | 4 | `exit_to_ghl_api`: 1<br>`ghl_reference_or_transform`: 3 | `calendars_appointments`: 3<br>`contacts`: 3<br>`conversations_messages`: 3<br>`users_locations`: 1<br>`webhooks`: 2 | `appointments`: 2<br>`leads`: 1<br>`message_log`: 2 |
| 🎯 Cap Hit Empirical Test | False | 4 | `exit_to_ghl_api`: 3<br>`read_from_ghl_api`: 1 | `contacts`: 4<br>`conversations_messages`: 4<br>`users_locations`: 2<br>`webhooks`: 2 | `leads`: 1<br>`message_log`: 2<br>`message_send_errors`: 1 |
| 📄 Document Ingestion | True | 3 | `entry_from_ghl_or_external_webhook`: 2<br>`ghl_reference_or_transform`: 1 | `conversations_messages`: 1<br>`users_locations`: 1<br>`webhooks`: 3 | `Documents`: 1 |
| 📬 Newsletter Dispatch | True | 2 | `exit_to_ghl_api`: 1<br>`ghl_reference_or_transform`: 1 | `contacts`: 2<br>`conversations_messages`: 2<br>`opportunities_pipelines`: 1<br>`webhooks`: 1 | `newsletter_deliveries`: 1 |
| 🔁 Inbound Replay | False | 2 | `exit_to_ghl_api`: 1<br>`ghl_reference_or_transform`: 1 | `conversations_messages`: 2<br>`webhooks`: 2 | `inbound_capture`: 1 |
| 📰 Data Source & Newsletter Creation | True | 1 | `ghl_reference_or_transform`: 1 | `conversations_messages`: 1<br>`users_locations`: 1 | none |
| 🧪 Altos Image Test | False | 1 | `entry_from_ghl_or_external_webhook`: 1 | `webhooks`: 1 | none |

## Node-Level Evidence

### 🧪 Altos Image Test / Webhook

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Webhook` |
| `type` | `n8n-nodes-base.webhook` |

### ⏰ Appointment Reminders / Mark Reminder Sent

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `calendars_appointments`
- **Nearby Supabase tables:** `appointments`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.tableId` | `appointments` |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Determine Reminder Type').item.json.appointment_id }}` |

### ⏰ Appointment Reminders / Sticky Note

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** `appointments`, `leads`, `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Appointment Reminders Sends SMS reminders at 3 intervals before scheduled appointments: - **24 hours** before - **5 hours** before - **1 hour** before **Safety guards:** - No reminders to DNC/opted-out leads - No reminders for cancelled appointments - No reminders if lead has no phone - Messages logged to message_log so Brain Engine has context …` |

### ⏰ Appointment Reminders / Log to message_log

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `appointment_reminder` |

### ⏰ Appointment Reminders / Send SMS via GHL1

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "SMS", "contactId": "{{ $json.contact_id }}", "message": "{{ $json.message }}" }` |
| `name` | `Send SMS via GHL1` |

### 🎯 Cap Hit Empirical Test / Send Test SMS

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "SMS", "contactId": "{{ $json.target_contactId }}", "message": "{{ $json.test_message }}" }` |
| `notes` | `onError: continueErrorOutput — when GHL returns 4xx/5xx the response goes out main[1] for error logging.` |

### 🎯 Cap Hit Empirical Test / Log Success

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Throttle Loop').item.json.target_contactId }}` |
| `parameters.fieldsUi.fieldValues[5].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ $json.messageId }}` |
| `parameters.fieldsUi.fieldValues[6].fieldId` | `ghl_conversation_id` |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `={{ $json.conversationId }}` |
| `parameters.fieldsUi.fieldValues[7].fieldId` | `ghl_accepted_at` |

### 🎯 Cap Hit Empirical Test / Log Failure (CRITICAL)

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** `message_send_errors`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Throttle Loop').item.json.target_contactId }}` |
| `parameters.fieldsUi.fieldValues[3].fieldId` | `ghl_error_code` |
| `parameters.fieldsUi.fieldValues[4].fieldId` | `ghl_error_name` |
| `notes` | `🎯 GOLDMINE — captures the FULL raw GHL response when the cap is hit. raw_response is jsonb so we can query it post-hoc.` |

### 🎯 Cap Hit Empirical Test / Note

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`
- **Nearby Supabase tables:** `leads`, `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 🎯 Cap Hit Empirical Test **Purpose:** Send up to 260 test SMS to ONLY 2 hardcoded contacts (Daddy Sayeed + Sayeed Hobaid — Hobaid's own numbers) until GHL returns a non-200 (cap hit). **Safety:** - Other leads are unreachable — no query to leads table - onError: continueErrorOutput so loop continues + logs each failure - 1.5s throttle between se…` |

### ☀️ Contact Created -> Brain Engine / GHL Intake Webhook

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `GHL Intake Webhook` |
| `type` | `n8n-nodes-base.webhook` |

### ☀️ Contact Created -> Brain Engine / Insert New Lead

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `opportunities_pipelines`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[19].fieldId` | `ghl_tags` |
| `parameters.fieldsUi.fieldValues[19].fieldValue` | `={{ $json.ghl_tags }}` |
| `parameters.fieldsUi.fieldValues[20].fieldId` | `ghl_source` |
| `parameters.fieldsUi.fieldValues[20].fieldValue` | `={{ $json.ghl_source }}` |
| `parameters.fieldsUi.fieldValues[21].fieldId` | `ghl_source_other` |
| `parameters.fieldsUi.fieldValues[21].fieldValue` | `={{ $json.ghl_source_other }}` |
| `parameters.fieldsUi.fieldValues[22].fieldId` | `ghl_notes` |
| `parameters.fieldsUi.fieldValues[22].fieldValue` | `={{ $json.ghl_notes }}` |

### ☀️ Contact Created -> Brain Engine / Send Intro SMS

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "SMS", "contactId": "{{ $json.contact_id }}", "locationId": "{{ $json.location_id }}", "message": "Hey {{ $json.first_name }}, my name is {{ $json.coordinator_name }} and I'm the newest member of {{ $json.agent_name }}'s real estate team. My job is to make sure everybody we work with is getting the attention they need.\n\nFeel free to re…` |

### ☀️ Contact Created -> Brain Engine / Send Intro Email

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "Email", "contactId": "{{ $json.contact_id }}", "locationId": "{{ $json.location_id }}", "subject": "Quick intro from {{ $json.coordinator_name }} - {{ $json.agent_name }}'s team", "emailFrom": "{{ $json.coordinator_name }} <{{ $json.coordinator_email }}>", "html": "<p>Hi {{ $json.first_name }},</p><p>I'm {{ $json.coordinator_name }}, pa…` |

### ☀️ Contact Created -> Brain Engine / Tag: No Contact Method

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $json.contact_id }}/tags` |

### ☀️ Contact Created -> Brain Engine / Note: Trigger

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Trigger Receives new contact webhooks from a GHL automation when a contact is created. Works for single contacts and bulk spreadsheet imports.` |

### ☀️ Contact Created -> Brain Engine / Note: Prepare

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `opportunities_pipelines`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Prepare Lead Data Normalises the GHL payload and determines the default channel: - Has email -> Email (intro always goes email first) - No email + has phone -> SMS fallback - Neither -> none Sets pipeline defaults: cold / MONTHLY.` |

### ☀️ Contact Created -> Brain Engine / Note: Channel Routing

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Channel Routing and Send Routes the intro message for new leads only: - SMS (default) - sent if phone exists - Email (fallback) - sent if no phone - No Contact Method - tags lead in GHL and stops NOTE: SMS and Email nodes are placeholders. Add message content before activating.` |

### ☀️ Contact Created -> Brain Engine / Fetch Full GHL Contact

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Fetch Full GHL Contact` |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('Process Check Result').first().json.contact_id }}` |

### ☀️ Contact Created -> Brain Engine / Fetch GHL Contact Notes

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Fetch GHL Contact Notes` |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('Process Check Result').first().json.contact_id }}/notes` |

### ⏱️ Contact Intake Queue Processor / Send Intro SMS

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "SMS", "contactId": "{{ $('Parse Payload').item.json.payload.contact_id }}", "locationId": "{{ $('Parse Payload').item.json.payload.location_id }}", "message": "Hey {{ $('Parse Payload').item.json.payload.first_name }}, my name is {{ $('Parse Payload').item.json.payload.coordinator_name }} and I'm the newest member of {{ $('Parse Payload…` |

### ⏱️ Contact Intake Queue Processor / Send Intro Email

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "Email", "contactId": "{{ $('Parse Payload').item.json.payload.contact_id }}", "locationId": "{{ $('Parse Payload').item.json.payload.location_id }}", "subject": "Quick intro from {{ $('Parse Payload').item.json.payload.coordinator_name }} - {{ $('Parse Payload').item.json.payload.agent_name }}'s team", "emailFrom": "{{ $('Parse Payload'…` |

### ⏱️ Contact Intake Queue Processor / Tag No Contact Method

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('Parse Payload').item.json.payload.contact_id }}/tags` |

### ⏱️ Contact Intake Queue Processor / Send SMS Follow-up

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "SMS", "contactId": "{{ $json.payload.contact_id }}", "locationId": "{{ $json.payload.location_id }}", "message": "Hey {{ $json.payload.first_name }}, this is {{ $json.payload.coordinator_name }} with {{ $json.payload.agent_name }}'s real estate team. Shot you an email just a few minutes ago, but wanted to follow up here in case you pref…` |

### ⏱️ Contact Intake Queue Processor / Log Followup SMS Sent

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[5].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ $json.messageId }}` |
| `parameters.fieldsUi.fieldValues[6].fieldId` | `ghl_conversation_id` |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `={{ $json.conversationId }}` |
| `parameters.fieldsUi.fieldValues[7].fieldId` | `ghl_accepted_at` |

### ⏱️ Contact Intake Queue Processor / Log Intro SMS Sent

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[5].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ $json.messageId }}` |
| `parameters.fieldsUi.fieldValues[6].fieldId` | `ghl_conversation_id` |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `={{ $json.conversationId }}` |
| `parameters.fieldsUi.fieldValues[7].fieldId` | `ghl_accepted_at` |

### ⏱️ Contact Intake Queue Processor / Log Intro Email Sent

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[5].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ $json.messageId }}` |
| `parameters.fieldsUi.fieldValues[6].fieldId` | `ghl_conversation_id` |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `={{ $json.conversationId }}` |
| `parameters.fieldsUi.fieldValues[7].fieldId` | `ghl_accepted_at` |

### 📰 Data Source & Newsletter Creation / Prepare Storage Data

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://kfoijgcbkjeizxxyiwxv.supabase.co/storage/v1/object/public/newsletter-images/${locationId}/${weekStart}.jpeg`\ncon…[TRUNCATED]`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `const sourceData = $('Prep Data for AI').first().json; const newsletterContent = $('Generate Newsletter').first().json.message?.content \|\| ''; const rawSplinters = $('Extract Splinters').first().json.message?.content?.trim() \|\| '[]'; // Build permanent Supabase Storage URL const locationId = sourceData.location_id; const weekStart = sourceData.week…` |

### 📄 Document Ingestion / Cleanup Trigger

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.webhook` |

### 📄 Document Ingestion / Cleanup Response

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.respondToWebhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** `Documents`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.respondToWebhook` |

### 📄 Document Ingestion / Sticky Note Cleanup

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 🗑️ Document Cleanup (Offboarding) POST to /webhook/document-cleanup with: - file_id: Delete specific file - location_id: Delete all docs for a location - agent_name: Delete all docs for an agent` |

### 🔍 GHL Conversation Backfill / Search Conversations

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/search`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/conversations/search` |
| `parameters.queryParameters.parameters[0].name` | `locationId` |

### 🔍 GHL Conversation Backfill / Extract Conversations

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `conversations_messages`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// GHL response shape: {conversations: [...], total, traceId} const convs = $input.first().json.conversations \|\| []; const startMs = $('Set Backfill Window').first().json.start_ms; const endMs = $('Set Backfill Window').first().json.end_ms; // Filter conversations whose lastMessageDate falls in the window const inWindow = convs.filter(c => { const …` |

### 🔍 GHL Conversation Backfill / Get Messages In Conv

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/conversations/{{ $json.conversationId }}/messages` |

### 🔍 GHL Conversation Backfill / Filter Inbound In Window

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// Find inbound messages within window from each conv response const startMs = $('Set Backfill Window').first().json.start_ms; const endMs = $('Set Backfill Window').first().json.end_ms; const locationId = $('Set Backfill Window').first().json.location_id; const output = []; for (const item of $input.all()) { const messages = item.json.messages?.me…` |

### 🔍 GHL Conversation Backfill / Save To Inbound Capture

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** `inbound_capture`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `ghl_backfill` |
| `parameters.fieldsUi.fieldValues[2].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[2].fieldValue` | `={{ $json.ghl_message_id }}` |
| `parameters.fieldsUi.fieldValues[7].fieldValue` | `Backfilled from GHL during recovery` |

### 📬 GHL Delivery Status Handler / Webhook

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Webhook` |
| `type` | `n8n-nodes-base.webhook` |
| `parameters.path` | `ghl-delivery-status` |

### 📬 GHL Delivery Status Handler / Immediate Response

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.respondToWebhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.respondToWebhook` |

### 📬 GHL Delivery Status Handler / Parse Event

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// Defensive parser. GHL OutboundMessage payload shape TBD until Phase 1.5 test. // Captures raw event for forensics regardless of shape. const input = $input.first().json; const body = input.body \|\| input; const headers = input.headers \|\| {}; return [{ json: { ghl_message_id: body.messageId \|\| body.message_id \|\| body.id, ghl_conversation_id: body.…` |

### 📬 GHL Delivery Status Handler / Has Message ID?

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.if`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.conditions.conditions[0].leftValue` | `={{ $json.ghl_message_id }}` |

### 📬 GHL Delivery Status Handler / Update Message Log

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyName` | `ghl_message_id` |
| `parameters.filters.conditions[0].keyValue` | `={{ $json.ghl_message_id }}` |

### 📬 GHL Delivery Status Handler / Log Send Error

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** `message_send_errors`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[2].fieldId` | `ghl_error_code` |
| `parameters.fieldsUi.fieldValues[3].fieldId` | `ghl_error_name` |

### 📬 GHL Delivery Status Handler / Note

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 📬 GHL Delivery Status Handler Receives OutboundMessage events from GHL and updates message_log.delivery_status. **Subscribe in GHL:** App Marketplace → Webhooks → OutboundMessage → POST URL = this webhook's path. **Always returns 200 OK** — GHL only retries on 429. **Phase 1.5 capture:** payload shape TBD until empirical test. Parser is defensiv…` |

### 🔍 GHL Send Status Checker / Wait 5s

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.wait`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

### 🔍 GHL Send Status Checker / GET Message Status

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/conversations/messages/{{ $('Execute Trigger').item.json.messageId }}` |

### 🔍 GHL Send Status Checker / Parse Response

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `const trigger = $('Execute Trigger').first().json; const raw = $input.first().json \|\| {}; // GHL message endpoint shape: { message: { id, status, error, body, ... }, traceId } const msg = raw.message \|\| raw.data \|\| raw; const status = String(msg.status \|\| msg.deliveryStatus \|\| '').toLowerCase(); const errorCode = String(msg.errorCode \|\| msg.error_c…` |

### 🔍 GHL Send Status Checker / Update Message Log

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `conversations_messages`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyName` | `ghl_message_id` |
| `parameters.filters.conditions[0].keyValue` | `={{ $json.messageId }}` |

### 🔍 GHL Send Status Checker / Log Send Error

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_send_errors`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[2].fieldId` | `ghl_error_code` |
| `parameters.fieldsUi.fieldValues[3].fieldId` | `ghl_error_name` |

### 🔁 Inbound Replay / Get Unprocessed Messages

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.postgres`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** `inbound_capture`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.query` | `SELECT id, payload, headers, ghl_message_id, captured_at, replay_count FROM inbound_capture WHERE processed = false ORDER BY captured_at ASC LIMIT 100` |

### 🔁 Inbound Replay / Replay To Brain Engine

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://twodegreesnorth.tech/webhook/80ceecaf-7e88-403c-b229-0855030701b8`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://twodegreesnorth.tech/webhook/80ceecaf-7e88-403c-b229-0855030701b8` |

### 📬 Newsletter Dispatch / Send Email via GHL

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={ "type": "Email", "contactId": "{{ $json.contact_id }}", "emailFrom": "{{ $json.coordinatorEmail }}", "html": {{ JSON.stringify($json.html) }}, "subject": "{{ $json.subject }}" }` |
| `name` | `Send Email via GHL` |

### 📬 Newsletter Dispatch / Sticky Note - Send & Log

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `opportunities_pipelines`
- **Nearby Supabase tables:** `newsletter_deliveries`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 3. BUILD, SEND & LOG **Build HTML Email** wraps `full_content` in HTML template with unsubscribe footer (Reply STOP). **Send Email via GHL** sends as Email type via conversations/messages API. **Log Delivery** inserts into `newsletter_deliveries` with status=sent + lead_id. After logging, loops back to next agent. **To test:** Hit Test Workflow …` |

### 🎉 Onboarding — Part 1: DB Enrichment / Sticky Note: Main

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** `onboarding_requests`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 🎉 Onboarding — Part 1: DB Enrichment Handles all safe, reversible onboarding work: 1. Validates all required fields (stops here if missing) 2. Fetches personality chunks and assembles personality prompt 3. Creates Google Drive KB folder 4. Creates FAQ Google Doc 5. Saves everything to the onboarding_requests staging table 6. Triggers Part 2 (GHL…` |

### 🎉 Onboarding — Part 1: DB Enrichment / Sticky Note: DB Staging Section

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** `onboarding_requests`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Database Staging Saves all enriched onboarding data to the onboarding_requests table. This is the handoff point — the staging record ID is passed to Part 2 (GHL Setup). If GHL setup fails, re-trigger Part 2 via POST /onboarding-ghl-setup with the onboarding_request_id.` |

### 🎉 Onboarding — Part 1: DB Enrichment / Note: Onboarding Call Checklist

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`, `users_locations`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Onboarding Call Checklist Collect all of the following before or during the onboarding call. ### Agent Info - Full name - Business name - Email address - Phone number - Timezone - City and state - Target ZIP codes (service area) ### GHL Sub-Account - Sub-account Location ID (Agency -> Locations -> click location -> Settings -> grab ID from URL) …` |

### 🎉 Onboarding — Part 1: DB Enrichment / Onboarding Form Webhook

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Onboarding Form Webhook` |
| `type` | `n8n-nodes-base.webhook` |

### 🎉 Onboarding — Part 1: DB Enrichment / Extract Agent Data

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.assignments.assignments[6].name` | `calendar_link` |
| `parameters.assignments.assignments[6].value` | `={{ $json.body.calendar_link }}` |

### 🎉 Onboarding — Part 1: DB Enrichment / Error Response

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.respondToWebhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.respondToWebhook` |

### 🎉 Onboarding — Part 1: DB Enrichment / Prepare GHL Handoff

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `prepare-ghl-handoff` |
| `name` | `Prepare GHL Handoff` |

### 🎉 Onboarding — Part 1: DB Enrichment / Trigger GHL Setup

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.executeWorkflow`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `trigger-ghl-setup` |
| `name` | `Trigger GHL Setup` |

### 🎉 Onboarding — Part 1: DB Enrichment / Success Response

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.respondToWebhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.respondToWebhook` |
| `parameters.responseBody` | `={"success": true, "message": "Agent {{ $('Extract Agent Data').first().json.agent_name }} onboarding started. GHL setup triggered.", "onboarding_request_id": "{{ $('Prepare GHL Handoff').first().json.onboarding_request_id }}"}` |

### 🎉 Onboarding — Part 1: DB Enrichment / Build Bio Paragraphs

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `const body = $('Onboarding Form Webhook').first().json.body \|\| {}; const location_id = body.agent_info?.location_id; if (!location_id) { throw new Error('location_id missing — expected at body.agent_info.location_id'); } const paragraphs = body.bio_template?.paragraphs \|\| {}; const topics = ['areas_served', 'specialties', 'style', 'background', 'fa…` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - Main

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `opportunities_pipelines`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## 🏗️ Onboarding — Part 2: GHL Setup Triggered by Part 1 (DB Enrichment) ONLY when all required fields are validated. Receives an `onboarding_request_id` → loads the staged record → creates GHL sub-account → applies snapshot → saves full agent config to Supabase. **Safety gate:** If GHL creation fails, the workflow stops immediately. No partial sta…` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - GHL

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `sticky-ghl` |
| `name` | `Sticky Note - GHL` |
| `parameters.content` | `## GHL Sub-Account Creation Create new sub-account and apply SMRT snapshot. **SNAPSHOT_ID** must be set as an n8n variable (`$vars.SNAPSHOT_ID`) or hardcoded here. GHL Created? gate stops the flow if creation fails.` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - DB Config

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`
- **Nearby Supabase tables:** `agents`, `onboarding_requests`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Database Configuration Inserts full agent config into Supabase agents table using location_id returned by GHL. Data sourced from onboarding_requests staging record.` |

### 🏗️ Onboarding — Part 2: GHL Setup / Sticky Note - Calendar Setup

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `calendars_appointments`, `users_locations`
- **Nearby Supabase tables:** `agents`
- **URLs:** `https://services.leadconnectorhq.com/calendars/?[REDACTED_QUERY]\n2.`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `sticky-calendar` |
| `name` | `Sticky Note - Calendar Setup` |
| `parameters.content` | `## Calendar Setup (Post-Snapshot) After GHL snapshot is applied, the agent's calendar ID needs to be stored in Supabase. ### agents table field - buyer_calendar_id — stores the agent's single calendar ID ### To do after W2 is live 1. HTTP GET https://services.leadconnectorhq.com/calendars/?[REDACTED_QUERY] 2. Find the correct calendar by name 3. UP…` |

### 🏗️ Onboarding — Part 2: GHL Setup / Webhook - Manual Rerun

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Webhook - Manual Rerun` |
| `type` | `n8n-nodes-base.webhook` |
| `parameters.path` | `onboarding-ghl-setup` |

### 🏗️ Onboarding — Part 2: GHL Setup / Normalize Webhook Input

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Normalize Webhook Input` |

### 🏗️ Onboarding — Part 2: GHL Setup / Load Onboarding Request

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.postgres`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** none classified
- **Nearby Supabase tables:** `onboarding_requests`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.query` | `SELECT * FROM onboarding_requests WHERE id = '{{ $json.onboarding_request_id }}'::uuid AND status = 'pending_ghl' LIMIT 1;` |

### 🏗️ Onboarding — Part 2: GHL Setup / Create GHL Sub-Account

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/locations/`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `ghl-create` |
| `name` | `Create GHL Sub-Account` |
| `parameters.url` | `https://services.leadconnectorhq.com/locations/` |

### 🏗️ Onboarding — Part 2: GHL Setup / GHL Created?

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.if`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `id` | `ghl-check` |
| `name` | `GHL Created?` |

### 🏗️ Onboarding — Part 2: GHL Setup / Apply GHL Snapshot

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `users_locations`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/snapshots/jLXUgLpYQvN7XrqscvLv/locations/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Apply GHL Snapshot` |
| `parameters.url` | `=https://services.leadconnectorhq.com/snapshots/jLXUgLpYQvN7XrqscvLv/locations/{{ $json.location_id }}` |

### 🏗️ Onboarding — Part 2: GHL Setup / Insert Default Agent Rules

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.postgres`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `calendars_appointments`, `users_locations`
- **Nearby Supabase tables:** `agent_rules`, `appointments`, `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.query` | `INSERT INTO agent_rules (location_id, rule_type, rule_content, priority) VALUES ('{{ $('Extract Location ID').first().json.location_id }}', 'greeting', 'Always greet leads warmly and professionally', 1), ('{{ $('Extract Location ID').first().json.location_id }}', 'scheduling', 'Push for appointments when lead shows interest', 2), ('{{ $('Extract Lo…` |

### 🏗️ Onboarding — Part 2: GHL Setup / GET GHL Pipelines

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `users_locations`, `opportunities_pipelines`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/opportunities/pipelines?[REDACTED_QUERY]`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `GET GHL Pipelines` |
| `parameters.url` | `=https://services.leadconnectorhq.com/opportunities/pipelines?[REDACTED_QUERY] $(''Extract Location ID'').first().json.location_id }}` |

### 🏗️ Onboarding — Part 2: GHL Setup / Build Pipeline Config

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`, `opportunities_pipelines`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// n8n 2.x safe: uses $input only — no $() calls const { pipelines: pipelinesRaw, location_id: locationId } = $input.first().json; const pipelines = Array.isArray(pipelinesRaw) ? pipelinesRaw : []; function findPipeline(list, keywords) { return list.find(p => keywords.some(k => p.name.toLowerCase().includes(k.toLowerCase()))); } function buildStage…` |

### 🏗️ Onboarding — Part 2: GHL Setup / Complete Onboarding Request

- **Active workflow:** False
- **Node type:** `n8n-nodes-base.postgres`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `users_locations`
- **Nearby Supabase tables:** `onboarding_requests`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.query` | `UPDATE onboarding_requests SET status = 'ghl_complete', location_id = '{{ $(''Extract Location ID'').first().json.location_id }}', updated_at = NOW() WHERE id = '{{ $(''Load Onboarding Request'').first().json.id }}'::uuid;` |

### 🧠 SMRT Brain Engine / Sticky Note1

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Webhook` |

### 🧠 SMRT Brain Engine / Sticky Note3

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## AI Model (RAG System) Dynamic context gathering → Prompt assembly → AI response → GHL send` |

### 🧠 SMRT Brain Engine / Webhook

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.webhook`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `type` | `n8n-nodes-base.webhook` |
| `name` | `Webhook` |

### 🧠 SMRT Brain Engine / searchLeads

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Webhook').item.json.body.contact_id }}` |

### 🧠 SMRT Brain Engine / carryContactID

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `carryContactID` |

### 🧠 SMRT Brain Engine / Log Outbound Message

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Assemble System Prompt').item.json.contactId }}` |
| `parameters.fieldsUi.fieldValues[1].fieldValue` | `={{ $('Assemble System Prompt').item.json.locationId }}` |
| `parameters.fieldsUi.fieldValues[7].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[7].fieldValue` | `={{ $json.messageId }}` |
| `parameters.fieldsUi.fieldValues[8].fieldId` | `ghl_conversation_id` |
| `parameters.fieldsUi.fieldValues[8].fieldValue` | `={{ $json.conversationId }}` |
| `parameters.fieldsUi.fieldValues[9].fieldId` | `ghl_accepted_at` |

### 🧠 SMRT Brain Engine / Prepare Sentiment Context

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `opportunities_pipelines`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `const d = $input.first().json; return [{ json: { ...d, currentMessage: d.currentMessage \|\| '', historyText: d.messageHistory \|\| 'No previous messages', conversationSummary: d.conversationSummary \|\| 'No summary', lastIntent: 'none', agentName: d.agentName \|\| 'Luke Gilbert', contactId: d.contactId \|\| '', locationId: d.locationId \|\| '', firstName: d.f…` |

### 🧠 SMRT Brain Engine / Add GHL Tag - Needs Review

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags` |
| `name` | `Add GHL Tag - Needs Review` |

### 🧠 SMRT Brain Engine / Move GHL Pipeline Stage

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `opportunities_pipelines`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/opportunities/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/opportunities/{{ $json.opportunity_id }}` |
| `name` | `Move GHL Pipeline Stage` |

### 🧠 SMRT Brain Engine / Analyze Conversation

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.openAi`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.messages.values[0].content` | `You analyze real estate AI conversation exchanges and extract structured signals. Return ONLY a valid JSON object (no markdown, no explanation): { "summary": "250-350 word accumulative summary", "lead_intent": "buy\|sell\|both\|unknown", "lead_timeline": "now\|3_months\|6_months\|1_year\|unknown", "appointment_discussed": true or false, "appointment_outco…` |

### 🧠 SMRT Brain Engine / Update Conversation Context

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** `conversation_context`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |
| `parameters.fieldsUi.fieldValues[5].fieldId` | `appointment_offered` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content \|\| $('Analyze Conversation').first().json.text \|\| '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' \|\| parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}` |
| `parameters.fieldsUi.fieldValues[6].fieldId` | `appointment_booked` |
| `parameters.fieldsUi.fieldValues[6].fieldValue` | `={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content \|\| $('Analyze Conversation').first().json.text \|\| '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}` |

### 🧠 SMRT Brain Engine / Send SMS

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={{ JSON.stringify({ type: 'SMS', contactId: $('Assemble System Prompt').first().json.contactId, message: $json.responseText \|\| $('AI Agent').first().json.output }) }}` |

### 🧠 SMRT Brain Engine / Send Email

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/conversations/messages`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `https://services.leadconnectorhq.com/conversations/messages` |
| `parameters.jsonBody` | `={{ (() => { const raw = $json.responseText \|\| $('AI Agent').first().json.output; const contactId = $('Assemble System Prompt').first().json.contactId; const coordinatorEmail = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_email } catch(e) { return $('Get Agent Config').first().json.coordinator_email } })(); const co…` |

### 🧠 SMRT Brain Engine / Pause SMS 30 Days (Tier 2)

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `opportunities_pipelines`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('carryContactID').first().json.contact_id }}` |

### 🧠 SMRT Brain Engine / Tag Tier 2 in GHL

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $json.contact_id }}/tags` |
| `name` | `Tag Tier 2 in GHL` |

### 🧠 SMRT Brain Engine / searchPastMessages

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabaseTool`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`
- **Nearby Supabase tables:** `message_log`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / Sticky Note16

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.stickyNote`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.content` | `## Gohighlevel Tools` |

### 🧠 SMRT Brain Engine / getContact

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.toolDescription` | `Fetch the full contact profile for the current lead from GoHighLevel, including custom fields, tags, lead source, and all contact details. WHEN TO USE: - When you need lead details NOT available in the conversation (email, address, tags, lead source) - When the lead asks you to confirm their contact information - When you need CRM context about the…` |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}` |

### 🧠 SMRT Brain Engine / getNotes

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** `agents`
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.toolDescription` | `Fetch all notes recorded on this lead's GoHighLevel contact by agents or the AI system. WHEN TO USE: - When the lead references a previous conversation or commitment ("someone told me...", "I was promised...") - When you need historical context about what has been discussed or agreed with this lead - Before escalating, to check if there are existin…` |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/notes` |

### 🧠 SMRT Brain Engine / getAppointments

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolHttpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `calendars_appointments`, `webhooks`
- **Nearby Supabase tables:** `appointments`
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.toolDescription` | `Fetch all appointments (past and upcoming) for the current lead from GoHighLevel. WHEN TO USE: - When the lead asks about existing appointments ("when is my appointment?", "do I have anything scheduled?") - When the lead wants to cancel or reschedule (you need the event_id from here) - When you need to check if the lead already has a booking before…` |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/appointments` |
| `name` | `getAppointments` |

### 🧠 SMRT Brain Engine / deleteAppointment

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.name` | `deleteAppointment` |
| `name` | `deleteAppointment` |

### 🧠 SMRT Brain Engine / bookAppointment

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.name` | `bookAppointment` |
| `name` | `bookAppointment` |

### 🧠 SMRT Brain Engine / Insert Conversation Context

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`, `users_locations`
- **Nearby Supabase tables:** `conversation_context`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |
| `parameters.fieldsUi.fieldValues[1].fieldValue` | `={{ $('Assemble System Prompt').first().json.locationId }}` |
| `parameters.fieldsUi.fieldValues[8].fieldId` | `appointment_offered` |
| `parameters.fieldsUi.fieldValues[8].fieldValue` | `={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content \|\| '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' \|\| parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}` |
| `parameters.fieldsUi.fieldValues[9].fieldId` | `appointment_booked` |
| `parameters.fieldsUi.fieldValues[9].fieldValue` | `={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content \|\| '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}` |

### 🧠 SMRT Brain Engine / addAppointmentNotes

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.name` | `addAppointmentNotes` |
| `parameters.jsonSchemaExample` | `{"appointment_time":"2026-04-10T09:00","qualifying_summary":"Buyer, 500k, pre-approved","conversation_summary":"Lead relocating"}` |
| `name` | `addAppointmentNotes` |

### 🧠 SMRT Brain Engine / checkQualificationStatus

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabaseTool`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** `conversation_context`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.toolDescription` | `Check how many of the 3 qualifying questions this lead has answered so far. WHEN TO USE: - BEFORE calling saveQualifyingAnswer, to get the current qualifying_answers object - When the lead says they want to book an appointment, to verify they are qualified - When you are unsure which qualifying questions have already been answered INPUT: No input n…` |

### 🧠 SMRT Brain Engine / rescheduleAppointment

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `rescheduleAppointment` |

### 🧠 SMRT Brain Engine / Get Lead Memory (After)

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / Sync Fields to GHL

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('Build GHL Sync Body').first().json.contactId }}` |
| `parameters.jsonBody` | `={{ JSON.stringify(Object.assign({}, $('Build GHL Sync Body').first().json.coreFields, { customFields: $('Build GHL Sync Body').first().json.customFields })) }}` |
| `name` | `Sync Fields to GHL` |

### 🧠 SMRT Brain Engine / Post Memory Note to GHL

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Post Memory Note to GHL` |

### 🧠 SMRT Brain Engine / Get GHL Contact

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/locations/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/locations/{{ $('Get Lead Memory (After)').first().json.location_id }}/customFields` |
| `name` | `Get GHL Contact` |

### 🧠 SMRT Brain Engine / Build GHL Sync Body

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// Get GHL custom field definitions from input (Get GHL Contact) const ghlFields = $input.first().json.customFields \|\| []; // Get memory + enrichment values from Compare Memory const mem = $('Compare Memory').first().json; // === CORE FIELDS (standard GHL contact fields) === const coreFields = {}; if (mem.first_name) coreFields.firstName = mem.firs…` |
| `name` | `Build GHL Sync Body` |

### 🧠 SMRT Brain Engine / Update Inbound Timestamps

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `opportunities_pipelines`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('carryContactID').first().json.contact_id }}` |

### 🧠 SMRT Brain Engine / Update Pipeline in DB

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `opportunities_pipelines`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Evaluate Pipeline Stage').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / Move Lead in GHL

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** none classified
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `name` | `Move Lead in GHL` |

### 🧠 SMRT Brain Engine / Notify Agent

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `const input = $input.first().json; const agentEmail = input.agent_email \|\| null; const agentPhone = input.agent_phone \|\| null; const agentName = input.agent_name \|\| input.agentName \|\| 'Agent'; const firstName = input.first_name \|\| input.firstName \|\| 'A lead'; const message = input.message \|\| input.message_body \|\| ''; const responseText = input.resp…` |

### 🧠 SMRT Brain Engine / Newsletter Offer Needed?

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.if`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `conversations_messages`, `calendars_appointments`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.conditions.conditions[0].leftValue` | `={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content \|\| '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed === true && parsed.appointment_outcome === 'rejected'; } catch(e) { return false; } })() }}` |

### 🧠 SMRT Brain Engine / Set Newsletter Pending

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`
- **Nearby Supabase tables:** `conversation_context`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / Clear Newsletter Flags

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`
- **Nearby Supabase tables:** `conversation_context`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.filters.conditions[0].keyValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / subscribeToNewsletter

- **Active workflow:** True
- **Node type:** `@n8n/n8n-nodes-langchain.toolCode`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`
- **Nearby Supabase tables:** `leads`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.description` | `Subscribe the current lead to the weekly market newsletter. Updates leads.newsletter_opted_in = true, tags the contact in GHL, and clears pending flags. INPUT (required JSON): - contact_id: string - the CONTACT_ID from the context header (always required) CALL THIS TOOL when the lead signals they want market updates, want to stay in the loop, accep…` |

### 🧠 SMRT Brain Engine / Gather Prompt Data

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `read_from_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `calendars_appointments`, `users_locations`, `opportunities_pipelines`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://kfoijgcbkjeizxxyiwxv.supabase.co`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.assignments.assignments[7].name` | `contactId` |
| `parameters.assignments.assignments[8].name` | `locationId` |
| `parameters.assignments.assignments[29].name` | `calendarId` |
| `parameters.assignments.assignments[29].value` | `={{ (() => { try { return $('Get Outbound Agent Config').first().json.calendar_id; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.calendar_id; } catch(e2) { return ''; } } })() }}` |
| `parameters.assignments.assignments[30].name` | `ghlUserId` |
| `parameters.assignments.assignments[30].value` | `={{ (() => { try { return $('Get Outbound Agent Config').first().json.ghl_user_id; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.ghl_user_id; } catch(e2) { return ''; } } })() }}` |

### 🧠 SMRT Brain Engine / Gather Sentiment Data1

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `opportunities_pipelines`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.assignments.assignments[1].name` | `contactId` |
| `parameters.assignments.assignments[2].name` | `locationId` |

### 🧠 SMRT Brain Engine / Wait 90s

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.wait`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.amount` | `={{ $('Webhook').first().json.body.test_mode === true ? 0 : 90 }}` |

### 🧠 SMRT Brain Engine / Turnaround: Disable DND

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}` |

### 🧠 SMRT Brain Engine / Turnaround: Remove L1 Tag

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags` |

### 🧠 SMRT Brain Engine / Turnaround: Post Note

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes` |

### 🧠 SMRT Brain Engine / Apply L1: Enable DND

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}` |

### 🧠 SMRT Brain Engine / Apply L1: Add L1 Tag

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags` |

### 🧠 SMRT Brain Engine / Apply L1: Post Note

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes` |

### 🧠 SMRT Brain Engine / Apply L2: Enable DND

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}` |

### 🧠 SMRT Brain Engine / Apply L2: Add L2 Tag

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags` |

### 🧠 SMRT Brain Engine / Apply L2: Post Note

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.httpRequest`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `webhooks`
- **Nearby Supabase tables:** none observed
- **URLs:** `https://services.leadconnectorhq.com/contacts/{{`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.url` | `=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes` |

### 🧠 SMRT Brain Engine / Newsletter Guard

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// Always guarantee 1 item with a stable contact_id so Clear Newsletter Flags never receives 0 items const ctx = $('Assemble System Prompt').first().json; return [{ json: { contactId: ctx.contactId } }];` |

### 🧠 SMRT Brain Engine / Log AI Leak

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** `ai_output_errors`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Assemble System Prompt').first().json.contactId }}` |

### 🧠 SMRT Brain Engine / Save Inbound Capture

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`, `webhooks`
- **Nearby Supabase tables:** `inbound_capture`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $json.headers && $json.headers['x-replay'] === '1' ? 'replay' : 'webhook' }}` |
| `parameters.fieldsUi.fieldValues[3].fieldId` | `ghl_message_id` |
| `parameters.fieldsUi.fieldValues[3].fieldValue` | `={{ $json.body?.messageId \|\| $json.body?.message?.id \|\| $json.body?.message_id \|\| null }}` |
| `parameters.fieldsUi.fieldValues[4].fieldValue` | `={{ $json.body?.contact_id \|\| $json.body?.contactId \|\| $json.body?.contact?.id \|\| null }}` |
| `parameters.fieldsUi.fieldValues[5].fieldValue` | `={{ $json.body?.location?.id \|\| $json.body?.locationId \|\| $json.body?.location_id \|\| null }}` |

### 🧠 SMRT Brain Engine / Restore Webhook Context

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.code`
- **Boundary direction:** `entry_from_ghl_or_external_webhook`
- **GHL domains:** `conversations_messages`, `webhooks`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.jsCode` | `// Re-emit the original Webhook output so downstream nodes see body/headers as before // (Save Inbound Capture + Check Capture Mode replaced $json with their own outputs) return $('Webhook').all();` |
| `name` | `Restore Webhook Context` |

### 🧠 SMRT Brain Engine / Prep Status Check Input

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.set`
- **Boundary direction:** `exit_to_ghl_api`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.assignments.assignments[0].name` | `messageId` |
| `parameters.assignments.assignments[0].value` | `={{ $json.ghl_message_id }}` |
| `parameters.assignments.assignments[2].value` | `={{ $('Assemble System Prompt').item.json.contactId }}` |
| `parameters.assignments.assignments[3].value` | `={{ $('Assemble System Prompt').item.json.locationId }}` |

### 🧠 SMRT Brain Engine / Cap Lock Check

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.postgres`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `users_locations`
- **Nearby Supabase tables:** none observed

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.query` | `=SELECT can_send, current_level, daily_cap, sent_today, remaining, reset_at, block_reason FROM check_sending_quota('{{ $('Assemble System Prompt').item.json.locationId }}'::text);` |

### 🧠 SMRT Brain Engine / Log Cap Suppression

- **Active workflow:** True
- **Node type:** `n8n-nodes-base.supabase`
- **Boundary direction:** `ghl_reference_or_transform`
- **GHL domains:** `contacts`, `conversations_messages`, `users_locations`
- **Nearby Supabase tables:** `message_send_errors`

| Parameter Path | Evidence Excerpt |
| --- | --- |
| `parameters.fieldsUi.fieldValues[0].fieldValue` | `={{ $('Assemble System Prompt').item.json.contactId }}` |
| `parameters.fieldsUi.fieldValues[1].fieldValue` | `={{ $('Assemble System Prompt').item.json.locationId }}` |
| `parameters.fieldsUi.fieldValues[2].fieldId` | `ghl_error_code` |
| `parameters.fieldsUi.fieldValues[3].fieldId` | `ghl_error_name` |

## References

[1]: ./workflow_schema_relationship_map.md "SMRT Workflow-Schema Relationship Map"  
[2]: ./SMRT_SCHEMA_WORKFLOW_AUDIT.md "SMRT Schema-Workflow Audit and Hardening Plan"
