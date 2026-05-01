# Orchestrator-to-Responder Current-State Evidence

- Workflow file: `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json`
- Workflow name: `🧠 SMRT Brain Engine`
- Node count: **174**
- Connection source count: **137**

## Candidate LLM / Agent Nodes

| Node | Type | Incoming | Outgoing | Key Parameters |
|---|---|---:|---:|---|
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | 1 | 1 | modelId, messages, options |
| `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | 17 | 1 | promptType, text, options |
| `KB Tool` | `@n8n/n8n-nodes-langchain.toolVectorStore` | 2 | 1 | description |
| `Docs Store` | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | 1 | 1 | tableName, options |
| `Embeddings` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 0 | 1 | options |
| `RAG LLM` | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 0 | 1 | model, options |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | 1 | 2 | modelId, messages, options |
| `getContact` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 | toolDescription, url, sendHeaders, parametersHeaders |
| `getNotes` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 | toolDescription, url, sendHeaders, parametersHeaders |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 | toolDescription, url, sendHeaders, parametersHeaders |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | description, jsCode, specifyInputSchema, jsonSchemaExample |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `subscribeToNewsletter` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |
| `Anthropic Chat Model` | `@n8n/n8n-nodes-langchain.lmChatAnthropic` | 0 | 1 | model, options |
| `switchChannel` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 | name, description, jsCode, specifyInputSchema, jsonSchemaExample |

## Candidate Tool / Operational Nodes

| Node | Type | Incoming Types | Outgoing Targets |
|---|---|---|---|
| `KB Tool` | `@n8n/n8n-nodes-langchain.toolVectorStore` | `ai_languageModel, ai_vectorStore` | `AI Agent` |
| `searchPastMessages` | `n8n-nodes-base.supabaseTool` | `` | `AI Agent` |
| `getContact` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | `` | `AI Agent` |
| `getNotes` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | `` | `AI Agent` |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | `` | `AI Agent` |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | `` | `AI Agent` |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | `` | `AI Agent` |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `subscribeToNewsletter` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |
| `switchChannel` | `@n8n/n8n-nodes-langchain.toolCode` | `` | `AI Agent` |

## Matched Prompt / Summary / Delivery / Scheduling Nodes

| Node | Type | Incoming | Outgoing |
|---|---|---:|---:|
| `Sticky Note3` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Update Last Agent Message` | `n8n-nodes-base.supabase` | 1 | 2 |
| `logMessageLeads` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Get Agent Config (RAG)` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Get Message History` | `n8n-nodes-base.postgres` | 1 | 1 |
| `Get Conversation Summary` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Assemble System Prompt` | `n8n-nodes-base.code` | 1 | 1 |
| `Log Outbound Message` | `n8n-nodes-base.supabase` | 2 | 4 |
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | 1 | 1 |
| `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | 17 | 1 |
| `KB Tool` | `@n8n/n8n-nodes-langchain.toolVectorStore` | 2 | 1 |
| `Embeddings` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | 0 | 1 |
| `RAG LLM` | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 0 | 1 |
| `Prepare Sentiment Context` | `n8n-nodes-base.code` | 1 | 1 |
| `Sticky Note13` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Log Already Escalated` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Add GHL Tag - Needs Review` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Move GHL Pipeline Stage` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | 1 | 2 |
| `Update Conversation Context` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Determine Action` | `n8n-nodes-base.code` | 2 | 1 |
| `Route by Channel1` | `n8n-nodes-base.switch` | 2 | 2 |
| `Send SMS` | `n8n-nodes-base.httpRequest` | 1 | 2 |
| `Send Email` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Prepare Tier Response` | `n8n-nodes-base.code` | 9 | 1 |
| `Tag Tier 2 in GHL` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Route Intent` | `n8n-nodes-base.switch` | 1 | 6 |
| `Extract Keywords` | `n8n-nodes-base.code` | 1 | 1 |
| `Search Relevant Messages` | `n8n-nodes-base.postgres` | 1 | 1 |
| `Summary Exists?` | `n8n-nodes-base.if` | 1 | 2 |
| `searchPastMessages` | `n8n-nodes-base.supabaseTool` | 0 | 1 |
| `Get Prompt Blocks (SMRT)` | `n8n-nodes-base.postgres` | 2 | 1 |
| `Get Default Personality` | `n8n-nodes-base.postgres` | 1 | 1 |
| `Set Outbound Context` | `n8n-nodes-base.set` | 1 | 4 |
| `Get Outbound Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Get Outbound Message History` | `n8n-nodes-base.postgres` | 1 | 1 |
| `Get Outbound Conversation Summary` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Sticky Note15` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Fetch Outbound Note` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Sticky Note16` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Get Agent Config` | `n8n-nodes-base.supabase` | 1 | 1 |
| `getContact` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 |
| `getNotes` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 0 | 1 |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Has Custom Personality?` | `n8n-nodes-base.if` | 1 | 1 |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Insert Conversation Context` | `n8n-nodes-base.supabase` | 1 | 1 |
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Form Section4` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Sticky Note2` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | 0 | 1 |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | 0 | 1 |
| `Check Qualification Gate` | `n8n-nodes-base.supabase` | 1 | 1 |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Get Lead Memory (After)` | `n8n-nodes-base.supabase` | 2 | 1 |
| `Sync Fields to GHL` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Post Memory Note to GHL` | `n8n-nodes-base.code` | 1 | 0 |
| `Get GHL Contact` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Build GHL Sync Body` | `n8n-nodes-base.code` | 1 | 1 |
| `Move Lead in GHL` | `n8n-nodes-base.code` | 1 | 1 |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Notify Agent` | `n8n-nodes-base.code` | 1 | 0 |
| `Newsletter Offer Needed?` | `n8n-nodes-base.if` | 1 | 2 |
| `Set Newsletter Pending` | `n8n-nodes-base.supabase` | 1 | 0 |
| `Clear Newsletter Flags` | `n8n-nodes-base.supabase` | 1 | 0 |
| `subscribeToNewsletter` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Silence Gate` | `n8n-nodes-base.code` | 1 | 1 |
| `Get Static Prompt Sections` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Gather Prompt Data` | `n8n-nodes-base.set` | 1 | 1 |
| `Gather Sentiment Data1` | `n8n-nodes-base.set` | 2 | 1 |
| `switchChannel` | `@n8n/n8n-nodes-langchain.toolCode` | 0 | 1 |
| `Outbound Bypass?` | `n8n-nodes-base.if` | 1 | 2 |
| `Sticky Note - Wait Window` | `n8n-nodes-base.stickyNote` | 0 | 0 |
| `Send Farewell?` | `n8n-nodes-base.if` | 1 | 2 |
| `Turnaround: Disable DND` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Turnaround: Remove L1 Tag` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Turnaround: Post Note` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Apply L1: Enable DND` | `n8n-nodes-base.httpRequest` | 2 | 1 |
| `Apply L1: Add L1 Tag` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Apply L1: Post Note` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Apply L2: Enable DND` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Apply L2: Add L2 Tag` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Apply L2: Post Note` | `n8n-nodes-base.httpRequest` | 1 | 1 |
| `Newsletter Guard` | `n8n-nodes-base.code` | 1 | 1 |
| `Leak Detected?` | `n8n-nodes-base.if` | 1 | 1 |
| `Log AI Leak` | `n8n-nodes-base.supabase` | 1 | 0 |
| `Save Inbound Capture` | `n8n-nodes-base.supabase` | 1 | 1 |
| `Prep Status Check Input` | `n8n-nodes-base.set` | 1 | 1 |
| `Cap Lock Check` | `n8n-nodes-base.postgres` | 1 | 1 |
| `Quota OK?` | `n8n-nodes-base.if` | 1 | 2 |
| `Log Cap Suppression` | `n8n-nodes-base.supabase` | 1 | 1 |

## Detailed Evidence Snippets

### `Sticky Note3`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width, color`

**Text at `content`:**

```text
## AI Model (RAG System)

Dynamic context gathering → Prompt assembly → AI response → GHL send
```

### `Update Last Agent Message`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Log Outbound Message', 'main', 0)]`
- Outgoing: `[('Escalation Check?', 'main', 0), ('Newsletter Offer Needed?', 'main', 0)]`
- Parameter keys: `operation, tableId, filters, fieldsUi`

**Text at `fieldsUi.fieldValues[1].fieldValue`:**

```text
={{ (() => { const stage = $('Assemble System Prompt').first().json.pipelineStage || 'MONTHLY'; const days = stage === 'MONTHLY' ? 28 : stage === 'BIWEEKLY' ? 14 : 7; return new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString(); })() }}
```

### `logMessageLeads`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('L2 Hard Block Gate', 'main', 1)]`
- Outgoing: `[('Update Inbound Timestamps', 'main', 0)]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[3].fieldValue`:**

```text
={{ $('LeadDetails').first().json.message }}
```

**Text at `fieldsUi.fieldValues[5].fieldValue`:**

```text
={{ $('LeadDetails').first().json.timestamp_message }}
```

### `Get Agent Config (RAG)`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Set Direction: Inbound2', 'main', 0)]`
- Outgoing: `[('Merge Context', 'main', 0)]`
- Parameter keys: `operation, tableId, filters`

```json
{
  "operation": "get",
  "tableId": "agents",
  "filters": {
    "conditions": [
      {
        "keyName": "location_id",
        "keyValue": "={{ $('LeadDetails').first().json.location_id }}"
      }
    ]
  }
}
```

### `Get Message History`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Set Direction: Inbound2', 'main', 0)]`
- Outgoing: `[('Merge Context', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
=SELECT 
  ml.*,
  (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $('LeadDetails').first().json.contact_id }}') as interaction_count
FROM message_log ml 
WHERE ml.contact_id = '{{ $('LeadDetails').first().json.contact_id }}' 
ORDER BY ml.timestamp DESC 
LIMIT 15
```

### `Get Conversation Summary`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Set Direction: Inbound2', 'main', 0)]`
- Outgoing: `[('Merge Context', 'main', 0)]`
- Parameter keys: `operation, tableId, filters`

```json
{
  "operation": "get",
  "tableId": "conversation_context",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "keyValue": "={{ $('LeadDetails').first().json.contact_id }}"
      }
    ]
  }
}
```

### `Assemble System Prompt`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Gather Prompt Data', 'main', 0)]`
- Outgoing: `[('AI Agent', 'main', 0)]`
- Parameter keys: `jsCode`

```json
{
  "jsCode": "[REDACTED]"
}
```

### `Log Outbound Message`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Send Email', 'main', 0), ('Send SMS', 'main', 0)]`
- Outgoing: `[('Update Last Agent Message', 'main', 0), ('Get Lead Memory (After)', 'main', 0), ('Has Splinter Data?', 'main', 0), ('Prep Status Check Input', 'main', 0)]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

**Text at `fieldsUi.fieldValues[1].fieldValue`:**

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```

**Text at `fieldsUi.fieldValues[3].fieldValue`:**

```text
={{ $('Silence Gate').first().json.responseText || $('AI Agent').item.json.output }}
```

**Text at `fieldsUi.fieldValues[4].fieldValue`:**

```text
={{ $('Assemble System Prompt').item.json.channelType }}
```

### `AI Sentiment Analysis`

- Type: `@n8n/n8n-nodes-langchain.anthropic`
- Incoming: `[('Prepare Sentiment Context', 'main', 0)]`
- Outgoing: `[('Parse Sentiment', 'main', 0)]`
- Parameter keys: `modelId, messages, options`

**Text at `messages.values[0].content`:**

```text
=CONVERSATION CONTEXT (read first — context frames the current message):

Conversation Summary: {{ $json.conversationSummary }}

Recent Messages (newest last):
{{ $json.historyText }}

Lead State:
- First Name: {{ $json.firstName }}
- Agent: {{ $json.agentName }}
- Pipeline Stage: {{ $json.pipelineStage }}
- Pipeline State: {{ $json.pipelineState }}

=== CURRENT MESSAGE (classify using STEP 1 → 4 from system prompt) ===
{{ $json.currentMessage }}

Return ONLY valid JSON. No markdown fences. No e…[TRUNCATED]
```

**Text at `options.system`:**

```text
You are a sentiment classifier for SMRT Bot. You analyze inbound messages and classify them into behavioral tiers to route the Brain Engine correctly.

CRITICAL: Your reasoning field is used INTERNALLY by downstream nodes ONLY. It is NEVER shown to the lead. The Brain Engine AI Agent uses its own prompt to write the actual SMS/email reply. Be thorough in your reasoning - it helps downstream routing, it never leaks to the customer.

=== CLASSIFICATION PRIORITY ORDER ===

Follow these steps IN ORD…[TRUNCATED]
```

### `AI Agent`

- Type: `@n8n/n8n-nodes-langchain.agent`
- Incoming: `[('KB Tool', 'ai_tool', 0), ('getContact', 'ai_tool', 0), ('getNotes', 'ai_tool', 0), ('getAppointments', 'ai_tool', 0), ('deleteAppointment', 'ai_tool', 0), ('Assemble System Prompt', 'main', 0), ('bookAppointment', 'ai_tool', 0), ('addAppointmentNotes', 'ai_tool', 0), ('checkQualificationStatus', 'ai_tool', 0), ('saveQualifyingAnswer', 'ai_tool', 0)]`
- Outgoing: `[('Analyze Conversation', 'main', 0)]`
- Parameter keys: `promptType, text, options`

```json
{
  "promptType": "define",
  "text": "={{ $json.userMessage }}",
  "options": {
    "systemMessage": "={{ $json.systemPrompt }}",
    "maxIterations": 10
  }
}
```

### `Prepare Sentiment Context`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Gather Sentiment Data1', 'main', 0)]`
- Outgoing: `[('AI Sentiment Analysis', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
const d = $input.first().json;

return [{
  json: {
    ...d,
    currentMessage: d.currentMessage || '',
    historyText: d.messageHistory || 'No previous messages',
    conversationSummary: d.conversationSummary || 'No summary',
    lastIntent: 'none',
    agentName: d.agentName || 'Luke Gilbert',
    contactId: d.contactId || '',
    locationId: d.locationId || '',
    firstName: d.firstName || 'Contact',
    pipelineStage: d.pipelineStage || 'MONTHLY',
    pipelineState: d.pipelineState || '…[TRUNCATED]
```

### `Log Already Escalated`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Already Escalated?', 'main', 1)]`
- Outgoing: `[('Prepare Tier Response', 'main', 0)]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[2].fieldValue`:**

```text
={{ $('LeadDetails').first().json.message }}
```

### `Add GHL Tag - Needs Review`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Update Lead Escalation', 'main', 0)]`
- Outgoing: `[('Move GHL Pipeline Stage', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"tags\": [\"Needs Human Review\"] }",
  "options": {}
}
```

### `Move GHL Pipeline Stage`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Add GHL Tag - Needs Review', 'main', 0)]`
- Outgoing: `[('Prepare Tier Response', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "PUT",
  "url": "=https://services.leadconnectorhq.com/opportunities/{{ $json.opportunity_id }}",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={\n  \"pipelineId\": \"PLACEHOLDER_PIPELINE_ID\",\n  \"pipelineStageId\": \"PLACEHOLDER_STAGE_ID\"\n}",
  "options": {}
}
```

### `Analyze Conversation`

- Type: `@n8n/n8n-nodes-langchain.openAi`
- Incoming: `[('AI Agent', 'main', 0)]`
- Outgoing: `[('Summary Exists?', 'main', 0), ('Leak Detected?', 'main', 0)]`
- Parameter keys: `modelId, messages, options`

**Text at `messages.values[0].content`:**

```text
You analyze real estate AI conversation exchanges and extract structured signals.

Return ONLY a valid JSON object (no markdown, no explanation):
{
  "summary": "250-350 word accumulative summary",
  "lead_intent": "buy|sell|both|unknown",
  "lead_timeline": "now|3_months|6_months|1_year|unknown",
  "appointment_discussed": true or false,
  "appointment_outcome": "offered|accepted|rejected|rescheduled|null",
  "newsletter_discussed": true or false,
  "newsletter_declined": true or false,
  "news…[TRUNCATED]
```

**Text at `messages.values[1].content`:**

```text
=Previous Summary: {{ (() => { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary } catch(e) { try { return $('Get Conversation Summary').first().json.conversation_summary } catch(e2) { return 'None' } } })() }}
Previous Intent: {{ (() => { try { return $('Get Outbound Conversation Summary').first().json.lead_intent } catch(e) { try { return $('Get Conversation Summary').first().json.lead_intent } catch(e2) { return 'unknown' } } })() }}
Previous Timeline: {{ (…[TRUNCATED]
```

### `Update Conversation Context`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Summary Exists?', 'main', 0)]`
- Outgoing: `[('Determine Action', 'main', 0)]`
- Parameter keys: `operation, tableId, filters, fieldsUi`

**Text at `filters.conditions[0].keyValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ (() => {  const turnCounter = (() => {   try { return parseInt($('searchLeads').first().json.turn_counter) || 0 }   catch(e) {    try { return parseInt($('Get Lead Memory').first().json.turn_counter) || 0 }    catch(e2) {     try { return parseInt($('Get Outbound Lead Memory').first().json.turn_counter) || 0 }     catch(e3) { return 0 }    }   }  })();  const shouldRegen = (turnCounter <= 2 || turnCounter % 10 === 0);  if (shouldRegen) {   try {    const content = $('Analyze Conversation').f…[TRUNCATED]
```

**Text at `fieldsUi.fieldValues[3].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

**Text at `fieldsUi.fieldValues[4].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.lead_timeline || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

**Text at `fieldsUi.fieldValues[5].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' || parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}
```

**Text at `fieldsUi.fieldValues[6].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}
```

**Text at `fieldsUi.fieldValues[7].fieldValue`:**

```text
={{ (() => {  const turnCounter = (() => {   try { return parseInt($('searchLeads').first().json.turn_counter) || 0 }   catch(e) {    try { return parseInt($('Get Lead Memory').first().json.turn_counter) || 0 }    catch(e2) { return 0 }   }  })();  const shouldRegen = (turnCounter <= 2 || turnCounter % 10 === 0);  if (shouldRegen) {   return new Date().toISOString();  } else {   try { return $('Get Outbound Conversation Summary').first().json.last_summarized_at || null }   catch(e) { try { retur…[TRUNCATED]
```

### `Determine Action`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Update Conversation Context', 'main', 0), ('Insert Conversation Context', 'main', 0)]`
- Outgoing: `[('Outbound Bypass?', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
const input = $input.first().json;

// Read AI Agent output directly — upstream Supabase node drops it
let responseText = '';
try { responseText = $('AI Agent').first().json.output || ''; } catch(e) {}
if (!responseText) responseText = input.output || input.text || input.response || '';
if (!responseText && input.message) responseText = input.message;

const agentName = (() => { try { return $('Assemble System Prompt').first().json.agentName || 'Luke'; } catch(e) { return input.agentName || 'Luk…[TRUNCATED]
```

### `Route by Channel1`

- Type: `n8n-nodes-base.switch`
- Incoming: `[('Should Respond?', 'main', 0), ('Outbound Bypass?', 'main', 0)]`
- Outgoing: `[('Cap Lock Check', 'main', 0), ('Send Email', 'main', 1)]`
- Parameter keys: `rules, options`

**Text at `rules.values[0].conditions.conditions[0].leftValue`:**

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

**Text at `rules.values[1].conditions.conditions[0].leftValue`:**

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

**Text at `rules.values[2].conditions.conditions[0].leftValue`:**

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

### `Send SMS`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Quota OK?', 'main', 0)]`
- Outgoing: `[('Log Outbound Message', 'main', 0), ('Post-Farewell DND Gate', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `url`:**

```text
https://services.leadconnectorhq.com/conversations/messages
```

**Text at `jsonBody`:**

```text
={{ JSON.stringify({ type: 'SMS', contactId: $('Assemble System Prompt').first().json.contactId, message: $json.responseText || $('AI Agent').first().json.output }) }}
```

### `Send Email`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Route by Channel1', 'main', 1)]`
- Outgoing: `[('Log Outbound Message', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `url`:**

```text
https://services.leadconnectorhq.com/conversations/messages
```

**Text at `jsonBody`:**

```text
={{ (() => { const raw = $json.responseText || $('AI Agent').first().json.output; const contactId = $('Assemble System Prompt').first().json.contactId; const coordinatorEmail = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_email } catch(e) { return $('Get Agent Config').first().json.coordinator_email } })(); const coordinatorName = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name } catch(e) { try { return $('Get Agent Config').fir…[TRUNCATED]
```

### `Prepare Tier Response`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Tag Tier 2 in GHL', 'main', 0), ('Tier Sub-Router1', 'main', 1), ('Route Intent', 'main', 4), ('Log Already Escalated', 'main', 0), ('Is Qualified?', 'main', 1), ('Move GHL Pipeline Stage', 'main', 0), ('Fetch Slots', 'main', 0), ('Turnaround: Post Note', 'main', 0), ('Send Farewell?', 'main', 0)]`
- Outgoing: `[('Get Prompt Blocks (SMRT)', 'main', 0)]`
- Parameter keys: `mode, jsCode`

**Text at `jsCode`:**

```text
// Prepare tier-specific response instructions for the AI Agent
// Pull tier/sentiment/sms_action from Parse Sentiment directly — input $json may be from Apply L1: Mark Lead (no tier)
const ps = (() => { try { return $('Parse Sentiment').first().json; } catch(e) { return {}; } })();
const tier = ps.tier || $json.tier || 'normal';
const sentiment = ps.sentiment || $json.sentiment || 'neutral';
const smsAction = ps.sms_action || $json.sms_action || 'none';

const tierInstructions = {
  tier_1_conf…[TRUNCATED]
```

### `Tag Tier 2 in GHL`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Pause SMS 30 Days (Tier 2)', 'main', 0)]`
- Outgoing: `[('Prepare Tier Response', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `jsonBody`:**

```text
={"tags": ["SMRT-Tier-2-Hostile", "SMS-Paused-30-Days"]}
```

### `Route Intent`

- Type: `n8n-nodes-base.switch`
- Incoming: `[('L1 Drop Gate', 'main', 1)]`
- Outgoing: `[('Apply L1: Mark Lead', 'main', 0), ('Tier Sub-Router1', 'main', 1), ('Block Level Router', 'main', 2), ('Check Escalation State', 'main', 3), ('Prepare Tier Response', 'main', 4), ('Check Qualification Gate', 'main', 5)]`
- Parameter keys: `rules, options`

```json
{
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-optout",
              "leftValue": "={{ $json.action }}",
              "rightValue": "opt_out",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Opt-Out"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-negative",
              "leftValue": "={{ $json.action }}",
              "rightValue": "flag_review",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Negative"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-ignore",
              "leftValue": "={{ $json.action }}",
              "rightValue": "ignore",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "a
...[truncated 1979 chars]
```

### `Extract Keywords`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Merge Context', 'main', 0)]`
- Outgoing: `[('Check Keyword Search', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
const input = $input.first().json;
const currentMessage = (input.message || input.message_body || '').toLowerCase();

const keywordPatterns = {
  pricing: /\b(price|pricing|cost|fee|rate|charge|dollar|\$|expensive|cheap|afford)\b/i,
  property: /\b(house|home|property|apartment|condo|bedroom|bath|sqft|square|lot)\b/i,
  location: /\b(address|where|location|area|neighborhood|city|street|zip)\b/i,
  availability: /\b(available|availability|vacancy|vacant|ready|move.?in|when|schedule|showing)\b/i,
…[TRUNCATED]
```

### `Search Relevant Messages`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Check Keyword Search', 'main', 0)]`
- Outgoing: `[('Merge Messages', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
=SELECT 
  id,
  message_body,
  direction,
  timestamp,
  message_type,
  'keyword_match' as source
FROM message_log
WHERE contact_id = '{{ $json.contact_id }}'
  AND id NOT IN (
    SELECT id 
    FROM message_log 
    WHERE contact_id = '{{ $json.contact_id }}'
    ORDER BY timestamp DESC 
    LIMIT 10
  )
  AND (
    {{ $json.keywords.map(k => "message_body ILIKE '%" + k + "%'").join(' OR ') }}
  )
ORDER BY timestamp DESC
LIMIT 5
```

### `searchPastMessages`

- Type: `n8n-nodes-base.supabaseTool`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `descriptionType, toolDescription, operation, tableId, limit, matchType, filters`

**Text at `toolDescription`:**

```text
Search this lead's past message log beyond the 15 most recent messages already in your context.

WHEN TO USE:
- Lead references something old ("I told you", "I mentioned before", "remember when", "weeks ago")
- You need to verify a claim about a past conversation
- You need to recall a commitment, date, or topic from earlier in the relationship

WHEN NOT TO USE:
- For general knowledge or company info (use KB Tool)
- For information already visible in RECENT MESSAGES (your 15-turn window)

INPUT…[TRUNCATED]
```

**Text at `filters.conditions[0].keyValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

### `Get Prompt Blocks (SMRT)`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Prepare Tier Response', 'main', 0), ('Merge Outbound Context', 'main', 0)]`
- Outgoing: `[('Has Custom Personality?', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
SELECT 
  pb.block_id,
  pb.category,
  pb.prompt_content,
  pb.priority,
  pb.conditions
FROM prompt_blocks pb
WHERE pb.is_active = true
ORDER BY 
  CASE pb.category 
    WHEN 'mode' THEN 1
    WHEN 'channel' THEN 2
    WHEN 'relationship' THEN 3
    WHEN 'history' THEN 4
    WHEN 'situation' THEN 5
  END,
  pb.priority DESC
```

### `Get Default Personality`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Has Custom Personality?', 'main', 1)]`
- Outgoing: `[('Get Static Prompt Sections', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
SELECT value FROM system_defaults WHERE key = 'default_personality_prompt' LIMIT 1
```

### `Set Outbound Context`

- Type: `n8n-nodes-base.set`
- Incoming: `[('Fetch Outbound Candidates', 'main', 0)]`
- Outgoing: `[('Get Outbound Agent Config', 'main', 0), ('Get Outbound Message History', 'main', 0), ('Get Outbound Conversation Summary', 'main', 0), ('Get Outbound Lead Memory', 'main', 0)]`
- Parameter keys: `assignments, options`

```json
{
  "assignments": {
    "assignments": [
      {
        "id": "1",
        "name": "direction",
        "value": "outbound",
        "type": "string"
      },
      {
        "id": "2",
        "name": "channel",
        "value": "={{ $json.channel || 'sms' }}",
        "type": "string"
      },
      {
        "id": "3",
        "name": "contact_id",
        "value": "={{ $json.contact_id }}",
        "type": "string"
      },
      {
        "id": "4",
        "name": "location_id",
        "value": "={{ $json.location_id }}",
        "type": "string"
      },
      {
        "id": "5",
        "name": "first_name",
        "value": "={{ $json.first_name }}",
        "type": "string"
      },
      {
        "id": "6",
        "name": "lead_temp",
        "value": "={{ $json.pipeline_state || 'warm' }}",
        "type": "string"
      },
      {
        "id": "7",
        "name": "message",
        "value": "={{ (() => { const stage = ($json.pipeline_stage || 'MONTHLY').toLowerCase(); const dv = $json.delivery_variants || {}; const touchpoint = dv[stage + '_touchpoint'] || $json.splinter_content || ''; const firstName = $json.first_name || 'them'; const coordinatorName = $json.coordinator_name || 'a teammate'; const agentName = $json.agent_name || 'the team'; const marketName = $json.market_name || 'the local market'; const pref = ($json.contact_preference || '').toLowerCase(); const channel = (pref…[TRUNCATED]",
        "type": "string"
      },
      {
        "id": "8",
        "name": "splinter_id",
        "value": "={{ $json.splinter_id }}",
        "type": "string"
      },
      {
        "id": "9",
        "name": "splinter_topic",
        "value": "={{ $json.splinter_topic }}",
        "type": "string"
      },
      {
        "id": "10",
        "name": "
...[truncated 1071 chars]
```

### `Get Outbound Agent Config`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Set Outbound Context', 'main', 0)]`
- Outgoing: `[('Merge Outbound Context', 'main', 0)]`
- Parameter keys: `operation, tableId, filters`

```json
{
  "operation": "get",
  "tableId": "agents",
  "filters": {
    "conditions": [
      {
        "keyName": "location_id",
        "keyValue": "={{ $json.location_id }}"
      }
    ]
  }
}
```

### `Get Outbound Message History`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Set Outbound Context', 'main', 0)]`
- Outgoing: `[('Merge Outbound Context', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id = '{{ $json.contact_id }}' ORDER BY ml.timestamp DESC LIMIT 15
```

### `Get Outbound Conversation Summary`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Set Outbound Context', 'main', 0)]`
- Outgoing: `[('Merge Outbound Context', 'main', 0)]`
- Parameter keys: `operation, tableId, filters`

```json
{
  "operation": "get",
  "tableId": "conversation_context",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "keyValue": "={{ $json.contact_id }}"
      }
    ]
  }
}
```

### `Fetch Outbound Note`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width, color`

**Text at `content`:**

```text
## Fetch Outbound Candidates

**What it pulls:**
- contact_id, location_id, first_name, channel
- pipeline_state (hot / warm / cold)
- agent_name, market_name
- Most recent active splinter per agent (splinter_id, splinter_content, splinter_topic, splinter_data_point)

**Conditions:**
- status = 'active_conversation'
- pipeline_stage != 'DNC'
- agent_dormant = false
- sms_paused_until IS NULL or has expired
- next_outbound_due_at IS NULL or has passed

**Ordered by:** next_outbound_due_at ASC (ol…[TRUNCATED]
```

### `Sticky Note16`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width, color`

```json
{
  "content": "## Gohighlevel Tools\n\n\n",
  "height": 608,
  "width": 1136,
  "color": 4
}
```

### `Get Agent Config`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('LeadDetails', 'main', 0)]`
- Outgoing: `[('inboundTrue?', 'main', 0)]`
- Parameter keys: `operation, tableId, limit, filters`

```json
{
  "operation": "getAll",
  "tableId": "agents",
  "limit": 1,
  "filters": {
    "conditions": [
      {
        "keyName": "location_id",
        "condition": "eq",
        "keyValue": "={{ $json.location_id }}"
      }
    ]
  }
}
```

### `getContact`

- Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `toolDescription, url, sendHeaders, parametersHeaders`

**Text at `toolDescription`:**

```text
Fetch the full contact profile for the current lead from GoHighLevel, including custom fields, tags, lead source, and all contact details.

WHEN TO USE:
- When you need lead details NOT available in the conversation (email, address, tags, lead source)
- When the lead asks you to confirm their contact information
- When you need CRM context about the lead's history or status

INPUT: No input needed. Automatically looks up the current lead.

OUTPUT: Full contact record with name, email, phone, tag…[TRUNCATED]
```

**Text at `url`:**

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}
```

### `getNotes`

- Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `toolDescription, url, sendHeaders, parametersHeaders`

**Text at `toolDescription`:**

```text
Fetch all notes recorded on this lead's GoHighLevel contact by agents or the AI system.

WHEN TO USE:
- When the lead references a previous conversation or commitment ("someone told me...", "I was promised...")
- When you need historical context about what has been discussed or agreed with this lead
- Before escalating, to check if there are existing agent notes

INPUT: No input needed. Automatically looks up the current lead.

OUTPUT: List of notes with timestamps and content.

RULES:
- Use to …[TRUNCATED]
```

**Text at `url`:**

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/notes
```

### `getAppointments`

- Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `toolDescription, url, sendHeaders, parametersHeaders`

**Text at `toolDescription`:**

```text
Fetch all appointments (past and upcoming) for the current lead from GoHighLevel.

WHEN TO USE:
- When the lead asks about existing appointments ("when is my appointment?", "do I have anything scheduled?")
- When the lead wants to cancel or reschedule (you need the event_id from here)
- When you need to check if the lead already has a booking before offering to schedule

INPUT: No input needed. Automatically looks up the current lead.

OUTPUT: List of appointment objects with event IDs, dates, t…[TRUNCATED]
```

**Text at `url`:**

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/appointments
```

### `deleteAppointment`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `name, description, jsCode, specifyInputSchema, jsonSchemaExample`

```json
{
  "name": "deleteAppointment",
  "description": "[REDACTED]",
  "jsCode": "[REDACTED]",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"event_id\":\"abc123\"}"
}
```

### `Has Custom Personality?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Get Prompt Blocks (SMRT)', 'main', 0)]`
- Outgoing: `[('Get Default Personality', 'main', 1)]`
- Parameter keys: `conditions, options`

```json
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "leftValue": "",
      "typeValidation": "strict",
      "version": 1
    },
    "conditions": [
      {
        "id": "personality-check",
        "leftValue": "={{ (() => { try { return $('Get Outbound Agent Config').first().json.use_custom_personality } catch(e) { try { return $('Get Agent Config').first().json.use_custom_personality } catch(e2) { return false } } })() }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "equals"
        }
      }
    ],
    "combinator": "and"
  },
  "options": {}
}
```

### `bookAppointment`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `name, description, jsCode, specifyInputSchema, jsonSchemaExample`

```json
{
  "name": "bookAppointment",
  "description": "[REDACTED]",
  "jsCode": "[REDACTED]",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"selected_slot\":\"2026-04-10T09:00:00-06:00\"}"
}
```

### `Insert Conversation Context`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Summary Exists?', 'main', 1)]`
- Outgoing: `[('Determine Action', 'main', 0)]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

**Text at `fieldsUi.fieldValues[1].fieldValue`:**

```text
={{ $('Assemble System Prompt').first().json.locationId }}
```

**Text at `fieldsUi.fieldValues[2].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.summary || content; } catch(e) { return $('Analyze Conversation').first().json.message?.content || ''; } })() }}
```

**Text at `fieldsUi.fieldValues[4].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

**Text at `fieldsUi.fieldValues[5].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_timeline || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

**Text at `fieldsUi.fieldValues[8].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' || parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}
```

**Text at `fieldsUi.fieldValues[9].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}
```

### `addAppointmentNotes`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `name, description, jsCode, specifyInputSchema, jsonSchemaExample`

**Text at `jsonSchemaExample`:**

```text
{"appointment_time":"2026-04-10T09:00","qualifying_summary":"Buyer, 500k, pre-approved","conversation_summary":"Lead relocating"}
```

### `Form Section4`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width, color`

**Text at `content`:**

```text
##  Booking Agent Routing
#### Book Intent in conversation

```

### `Sticky Note2`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width`

**Text at `content`:**

```text
## Prompt Selection & Assemebly  
**Double click** to edit me. [Guide](https://docs.n8n.io/workflows/sticky-notes/)
```

### `checkQualificationStatus`

- Type: `n8n-nodes-base.supabaseTool`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `descriptionType, toolDescription, operation, tableId, limit, matchType, filters`

**Text at `toolDescription`:**

```text
Check how many of the 3 qualifying questions this lead has answered so far.

WHEN TO USE:
- BEFORE calling saveQualifyingAnswer, to get the current qualifying_answers object
- When the lead says they want to book an appointment, to verify they are qualified
- When you are unsure which qualifying questions have already been answered

INPUT: No input needed. Automatically looks up this lead's conversation_context record.

OUTPUT: Returns the qualifying_answers JSONB object with keys q1, q2, q3.
- …[TRUNCATED]
```

### `saveQualifyingAnswer`

- Type: `n8n-nodes-base.supabaseTool`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `descriptionType, toolDescription, operation, tableId, matchType, filters, fieldsUi`

**Text at `toolDescription`:**

```text
MANDATORY TOOL - Save a qualifying answer to the database after the lead answers one of the 3 qualifying questions.

WHEN TO USE: You MUST call this tool IMMEDIATELY every time the lead provides information that answers Q1, Q2, or Q3. Do NOT wait until all questions are answered. Save each answer the moment you receive it.

The tool updates the qualifying_answers JSONB column in conversation_context for this lead.

INPUT: You must provide a JSON object with the field 'qualifying_answers' contain…[TRUNCATED]
```

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ $fromAI('qualifying_answers', 'The complete qualifying_answers JSON object with keys q1, q2, q3. Each key is either a string summary of the lead answer or null if not yet answered. Example: {"q1": "Buying, 3 month timeline", "q2": "Budget around 500k", "q3": null}. IMPORTANT: Include ALL existing answers plus the new one.', 'json') }}
```

### `Check Qualification Gate`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Route Intent', 'main', 5)]`
- Outgoing: `[('Is Qualified?', 'main', 0)]`
- Parameter keys: `operation, tableId, limit, matchType, filters`

```json
{
  "operation": "getAll",
  "tableId": "conversation_context",
  "limit": 1,
  "matchType": "allFilters",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "condition": "eq",
        "keyValue": "={{ $('LeadDetails').first().json.contact_id }}"
      }
    ]
  }
}
```

### `rescheduleAppointment`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `description, jsCode, specifyInputSchema, jsonSchemaExample`

```json
{
  "description": "[REDACTED]",
  "jsCode": "[REDACTED]",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"event_id\":\"abc\",\"start_time\":\"2026-04-10T10:00:00-06:00\"}"
}
```

### `Get Lead Memory (After)`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Log Outbound Message', 'main', 0), ('Should Respond?', 'main', 1)]`
- Outgoing: `[('Compare Memory', 'main', 0)]`
- Parameter keys: `operation, tableId, filters`

**Text at `filters.conditions[0].keyValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

### `Sync Fields to GHL`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Build GHL Sync Body', 'main', 0)]`
- Outgoing: `[('Post Memory Note to GHL', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `url`:**

```text
=https://services.leadconnectorhq.com/contacts/{{ $('Build GHL Sync Body').first().json.contactId }}
```

**Text at `jsonBody`:**

```text
={{ JSON.stringify(Object.assign({}, $('Build GHL Sync Body').first().json.coreFields, { customFields: $('Build GHL Sync Body').first().json.customFields })) }}
```

### `Post Memory Note to GHL`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Sync Fields to GHL', 'main', 0)]`
- Outgoing: `[]`
- Parameter keys: `jsCode`

```json
{
  "jsCode": "[REDACTED]"
}
```

### `Get GHL Contact`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Memory Changed?', 'main', 0)]`
- Outgoing: `[('Build GHL Sync Body', 'main', 0)]`
- Parameter keys: `url, sendHeaders, headerParameters, options`

```json
{
  "url": "=https://services.leadconnectorhq.com/locations/{{ $('Get Lead Memory (After)').first().json.location_id }}/customFields",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      }
    ]
  },
  "options": {
    "timeout": 10000
  }
}
```

### `Build GHL Sync Body`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Get GHL Contact', 'main', 0)]`
- Outgoing: `[('Sync Fields to GHL', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
// Get GHL custom field definitions from input (Get GHL Contact)
const ghlFields = $input.first().json.customFields || [];

// Get memory + enrichment values from Compare Memory
const mem = $('Compare Memory').first().json;

// === CORE FIELDS (standard GHL contact fields) ===
const coreFields = {};
if (mem.first_name) coreFields.firstName = mem.first_name;
if (mem.last_name) coreFields.lastName = mem.last_name;
if (mem.email) coreFields.email = mem.email;
if (mem.phone) coreFields.phone = mem.p…[TRUNCATED]
```

### `Move Lead in GHL`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Pipeline Changed?', 'main', 0)]`
- Outgoing: `[('Update Pipeline in DB', 'main', 0)]`
- Parameter keys: `jsCode`

```json
{
  "jsCode": "[REDACTED]"
}
```

### `Notify Agent`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Escalation Check?', 'main', 0)]`
- Outgoing: `[]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
const input = $input.first().json;

const agentEmail = input.agent_email || null;
const agentPhone = input.agent_phone || null;
const agentName = input.agent_name || input.agentName || 'Agent';
const firstName = input.first_name || input.firstName || 'A lead';
const message = input.message || input.message_body || '';
const responseText = input.responseText || input.output || '';
const contactId = input.contact_id || input.contactId || '';

const summary = firstName + ' needs ' + agentName + "\'…[TRUNCATED]
```

### `Newsletter Offer Needed?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Update Last Agent Message', 'main', 0)]`
- Outgoing: `[('Set Newsletter Pending', 'main', 0), ('Newsletter Guard', 'main', 1)]`
- Parameter keys: `conditions, options`

**Text at `conditions.conditions[0].leftValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed === true && parsed.appointment_outcome === 'rejected'; } catch(e) { return false; } })() }}
```

**Text at `conditions.conditions[2].leftValue`:**

```text
={{ (() => { try { return $('Get Conversation Summary').first().json.newsletter_offer_declined } catch(e) { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_declined } catch(e2) { return false } } })() }}
```

**Text at `conditions.conditions[3].leftValue`:**

```text
={{ (() => { try { return $('Assemble System Prompt').first().json.direction } catch(e) { return 'inbound' } })() }}
```

### `Set Newsletter Pending`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Newsletter Offer Needed?', 'main', 0)]`
- Outgoing: `[]`
- Parameter keys: `operation, tableId, matchType, filters, fieldsUi`

**Text at `filters.conditions[0].keyValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

### `Clear Newsletter Flags`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Newsletter Guard', 'main', 0)]`
- Outgoing: `[]`
- Parameter keys: `operation, tableId, matchType, filters, fieldsUi`

**Text at `filters.conditions[0].keyValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

**Text at `fieldsUi.fieldValues[1].fieldValue`:**

```text
={{ (() => { try { const leadMemory = $('Get Lead Memory (After)').first()?.json || $('Get Outbound Lead Memory').first()?.json || {}; if (leadMemory.newsletter_opted_in === true) return false; const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.newsletter_declined === true; } catch(e) { return false; } })() }}
```

### `subscribeToNewsletter`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `name, description, jsCode, specifyInputSchema, jsonSchemaExample`

**Text at `description`:**

```text
Subscribe the current lead to the weekly market newsletter. Updates leads.newsletter_opted_in = true, tags the contact in GHL, and clears pending flags.

INPUT (required JSON):
- contact_id: string - the CONTACT_ID from the context header (always required)

CALL THIS TOOL when the lead signals they want market updates, want to stay in the loop, accept the newsletter offer, or agree to receive periodic info. Call it BEFORE you write your response acknowledging the subscription — never acknowledge…[TRUNCATED]
```

### `Silence Gate`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Outbound Bypass?', 'main', 1)]`
- Outgoing: `[('Should Respond?', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
const input = $input.first().json;
const direction = input.direction || 'inbound';

// Style normalizer — strip punctuation the prompt bans but LLMs still emit.
// Rules: no em dashes, no en dashes, no exclamation marks, no hyphen-as-separator.
// Preserves compound words (first-time) and phone numbers (208-555-1234).
function normalizeStyle(text) {
  if (!text || typeof text !== 'string') return text;
  let s = text;
  s = s.replace(/\s*\u2014\s*/g, ', ');
  s = s.replace(/\s*\u2013\s*/g, ', ')…[TRUNCATED]
```

### `Get Static Prompt Sections`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Get Default Personality', 'main', 0)]`
- Outgoing: `[('Gather Prompt Data', 'main', 0)]`
- Parameter keys: `operation, tableId, returnAll, matchType, filters`

```json
{
  "operation": "getAll",
  "tableId": "static_prompt_sections",
  "returnAll": true,
  "matchType": "allFilters",
  "filters": {
    "conditions": [
      {
        "keyName": "location_id",
        "condition": "eq",
        "keyValue": "={{ (() => { try { return $('Get Agent Config (RAG)').first().json.location_id } catch(e) { try { return $('Get Outbound Agent Config').first().json.location_id } catch(e2) { return 'kv1Af9i1qYK7KfIiT0U3' } } })() }}"
      },
      {
        "keyName": "is_active",
        "condition": "eq",
        "keyValue": "true"
      }
    ]
  }
}
```

### `Gather Prompt Data`

- Type: `n8n-nodes-base.set`
- Incoming: `[('Get Static Prompt Sections', 'main', 0)]`
- Outgoing: `[('Assemble System Prompt', 'main', 0)]`
- Parameter keys: `duplicateItem, assignments, includeOtherFields, options`

**Text at `assignments.assignments[5].value`:**

```text
={{ (() => { try { return $('Set Outbound Context').first().json.channel; } catch(e) { try { return $('LeadDetails').first().json.channel; } catch(e2) { return 'sms'; } } })() }}
```

**Text at `assignments.assignments[11].value`:**

```text
={{ (() => { try { return $('Prepare Tier Response').first().json.tier; } catch(e) { return 'standard'; } })() }}
```

**Text at `assignments.assignments[12].value`:**

```text
={{ (() => { try { const b = $('Check Batch Leader').first().json.batchedMessageBody; if (b) return b; } catch(e) {} try { return $('Set Outbound Context').first().json.message; } catch(e) { try { return $('LeadDetails').first().json.message_body || $('LeadDetails').first().json.message; } catch(e2) { return ''; } } })() }}
```

**Text at `assignments.assignments[13].value`:**

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary; } catch(e) { try { return $('Get Conversation Summary').first().json.conversation_summary; } catch(e2) { return ''; } } })() }}
```

**Text at `assignments.assignments[19].value`:**

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.short_summary_note; } catch(e) { try { return $('Get Lead Memory').first().json.short_summary_note; } catch(e2) { return ''; } } })() }}
```

**Text at `assignments.assignments[20].value`:**

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_pending || false; } catch(e) { try { return $('Get Conversation Summary').first().json.newsletter_offer_pending || false; } catch(e2) { return false; } } })() }}
```

**Text at `assignments.assignments[22].value`:**

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_declined || false; } catch(e) { try { return $('Get Conversation Summary').first().json.newsletter_offer_declined || false; } catch(e2) { return false; } } })() }}
```

**Text at `assignments.assignments[27].value`:**

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.lead_intent; } catch(e) { try { return $('Get Conversation Summary').first().json.lead_intent; } catch(e2) { return 'unknown'; } } })() }}
```

### `Gather Sentiment Data1`

- Type: `n8n-nodes-base.set`
- Incoming: `[('Check Keyword Search', 'main', 1), ('Merge & Deduplicate Messages', 'main', 0)]`
- Outgoing: `[('Prepare Sentiment Context', 'main', 0)]`
- Parameter keys: `assignments, options`

**Text at `assignments.assignments[0].value`:**

```text
={{ (() => { try { const b = $('Check Batch Leader').first().json.batchedMessageBody; if (b) return b; } catch(e) {} try { return $('LeadDetails').first().json.message; } catch(e) { try { return $('Set Outbound Context').first().json.message; } catch(e2) { return ''; } } })() }}
```

**Text at `assignments.assignments[4].value`:**

```text
={{ (() => { try { return $('Get Conversation Summary').first().json.conversation_summary || ''; } catch(e) { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary || ''; } catch(e2) { return ''; } } })() }}
```

**Text at `assignments.assignments[6].value`:**

```text
={{ (() => { try { const msgs = $('Get Message History').all(); return msgs.slice(0, 15).map(m => (m.json.direction === 'inbound' ? '[lead] ' : '[bot] ') + m.json.message_body).join('\n'); } catch(e) { return 'No previous messages'; } })() }}
```

### `switchChannel`

- Type: `@n8n/n8n-nodes-langchain.toolCode`
- Incoming: `[]`
- Outgoing: `[('AI Agent', 'ai_tool', 0)]`
- Parameter keys: `name, description, jsCode, specifyInputSchema, jsonSchemaExample`

**Text at `description`:**

```text
Switch the lead's communication channel and send a hardcoded bridge message on the new channel. Call this ONLY when the lead explicitly asks to move to a different channel (e.g. "just email me", "text me instead").

SUPPORTED DESTINATIONS: sms, email. You CANNOT switch TO Instagram DM — only FROM it. If a lead asks to be contacted on Instagram, politely decline and offer SMS or email instead.

INPUT (required JSON):
- contact_id: string — CONTACT_ID from context
- new_channel: string — must be "…[TRUNCATED]
```

### `Outbound Bypass?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Determine Action', 'main', 0)]`
- Outgoing: `[('Route by Channel1', 'main', 0), ('Silence Gate', 'main', 1)]`
- Parameter keys: `conditions, options`

**Text at `conditions.conditions[0].leftValue`:**

```text
={{ $('Assemble System Prompt').first().json.direction }}
```

### `Sticky Note - Wait Window`

- Type: `n8n-nodes-base.stickyNote`
- Incoming: `[]`
- Outgoing: `[]`
- Parameter keys: `content, height, width, color`

**Text at `content`:**

```text
## Wait Window — Message Batching

**60s debounce + batch leader election.**

Stamp log ID → wait 60s → query message_log for last 90s of inbound messages from this contact → newest message (by timestamp, id tiebreaker) is the leader.

- TRUE (leader): proceeds through pipeline with `batchedMessageBody` (all messages joined)
- FALSE (not leader): dead-ends silently — another execution will respond

If query fails, node fail-safes to leader with single message body (so we never drop a response).
```

### `Send Farewell?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Apply L1: Post Note', 'main', 0)]`
- Outgoing: `[('Prepare Tier Response', 'main', 0), ('Apply L1: Enable DND', 'main', 1)]`
- Parameter keys: `conditions, options`

```json
{
  "conditions": {
    "options": {
      "version": 2,
      "leftValue": "",
      "caseSensitive": true,
      "typeValidation": "loose"
    },
    "combinator": "and",
    "conditions": [
      {
        "id": "is-opt-out",
        "leftValue": "={{ (() => { try { return $('Parse Sentiment').first().json.action } catch(e) { return 'continue' } })() }}",
        "rightValue": "opt_out",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ]
  },
  "options": {}
}
```

### `Turnaround: Disable DND`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Turnaround: Clear State', 'main', 0)]`
- Outgoing: `[('Turnaround: Remove L1 Tag', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `jsonBody`:**

```text
{ "dnd": false, "dndSettings": { "Call": { "status": "inactive" }, "Email": { "status": "inactive" }, "SMS": { "status": "inactive" }, "WhatsApp": { "status": "inactive" }, "GMB": { "status": "inactive" }, "FB": { "status": "inactive" } } }
```

### `Turnaround: Remove L1 Tag`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Turnaround: Disable DND', 'main', 0)]`
- Outgoing: `[('Turnaround: Post Note', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "DELETE",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "{ \"tags\": [\"SMRT-OptOut-L1\"] }",
  "options": {}
}
```

### `Turnaround: Post Note`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Turnaround: Remove L1 Tag', 'main', 0)]`
- Outgoing: `[('Prepare Tier Response', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"body\": \"SMRT Turnaround Detected - Lead re-engaged warmly. Prior opt-out was on {{ $('searchLeads').first().json.opted_out_at }}. State cleared, flows resumed.\" }",
  "options": {}
}
```

### `Apply L1: Enable DND`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Send Farewell?', 'main', 1), ('Post-Farewell DND Gate', 'main', 0)]`
- Outgoing: `[('L1 Silent Drop', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `jsonBody`:**

```text
{ "dnd": true, "dndSettings": { "Call": { "status": "active" }, "Email": { "status": "active" }, "SMS": { "status": "active" }, "WhatsApp": { "status": "active" }, "GMB": { "status": "active" }, "FB": { "status": "active" } } }
```

### `Apply L1: Add L1 Tag`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Apply L1: Mark Lead', 'main', 0)]`
- Outgoing: `[('Apply L1: Post Note', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "{ \"tags\": [\"SMRT-OptOut-L1\"] }",
  "options": {}
}
```

### `Apply L1: Post Note`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Apply L1: Add L1 Tag', 'main', 0)]`
- Outgoing: `[('Send Farewell?', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"body\": \"SMRT Auto Opt-Out (Level 1 - Soft/Reversible). Reason: {{ $('Parse Sentiment').first().json.reason }}\" }",
  "options": {}
}
```

### `Apply L2: Enable DND`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Apply L2: Mark Lead', 'main', 0)]`
- Outgoing: `[('Apply L2: Add L2 Tag', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

**Text at `jsonBody`:**

```text
{ "dnd": true, "dndSettings": { "Call": { "status": "active" }, "Email": { "status": "active" }, "SMS": { "status": "active" }, "WhatsApp": { "status": "active" }, "GMB": { "status": "active" }, "FB": { "status": "active" } } }
```

### `Apply L2: Add L2 Tag`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Apply L2: Enable DND', 'main', 0)]`
- Outgoing: `[('Apply L2: Post Note', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/tags",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "{ \"tags\": [\"SMRT-OptOut-L2-Blocked\"] }",
  "options": {}
}
```

### `Apply L2: Post Note`

- Type: `n8n-nodes-base.httpRequest`
- Incoming: `[('Apply L2: Add L2 Tag', 'main', 0)]`
- Outgoing: `[('L2 Post-Block Silent', 'main', 0)]`
- Parameter keys: `method, url, sendHeaders, headerParameters, sendBody, specifyBody, jsonBody, options`

```json
{
  "method": "POST",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ $('LeadDetails').first().json.contact_id }}/notes",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "[REDACTED]",
        "value": "[REDACTED]"
      },
      {
        "name": "Version",
        "value": "2021-07-28"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"body\": \"SMRT Auto Block (Level 2 - Hard/Incoming Blocked). Reason: {{ $('Parse Sentiment').first().json.reason }}\" }",
  "options": {}
}
```

### `Newsletter Guard`

- Type: `n8n-nodes-base.code`
- Incoming: `[('Newsletter Offer Needed?', 'main', 1)]`
- Outgoing: `[('Clear Newsletter Flags', 'main', 0)]`
- Parameter keys: `jsCode`

**Text at `jsCode`:**

```text
// Always guarantee 1 item with a stable contact_id so Clear Newsletter Flags never receives 0 items
const ctx = $('Assemble System Prompt').first().json;
return [{ json: { contactId: ctx.contactId } }];
```

### `Leak Detected?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Analyze Conversation', 'main', 0)]`
- Outgoing: `[('Log AI Leak', 'main', 0)]`
- Parameter keys: `conditions, options`

**Text at `conditions.conditions[0].leftValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.internal_reasoning_leak_detected === true; } catch(e) { return false; } })() }}
```

### `Log AI Leak`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Leak Detected?', 'main', 0)]`
- Outgoing: `[]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

**Text at `fieldsUi.fieldValues[3].fieldValue`:**

```text
={{ $('Assemble System Prompt').first().json.channelType || '' }}
```

**Text at `fieldsUi.fieldValues[6].fieldValue`:**

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.leak_phrase || ''; } catch(e) { return 'parse_error'; } })() }}
```

### `Save Inbound Capture`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Webhook', 'main', 0)]`
- Outgoing: `[('Check Capture Mode', 'main', 0)]`
- Parameter keys: `tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[3].fieldValue`:**

```text
={{ $json.body?.messageId || $json.body?.message?.id || $json.body?.message_id || null }}
```

### `Prep Status Check Input`

- Type: `n8n-nodes-base.set`
- Incoming: `[('Log Outbound Message', 'main', 0)]`
- Outgoing: `[('Trigger Status Check', 'main', 0)]`
- Parameter keys: `assignments, options`

**Text at `assignments.assignments[2].value`:**

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

**Text at `assignments.assignments[3].value`:**

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```

### `Cap Lock Check`

- Type: `n8n-nodes-base.postgres`
- Incoming: `[('Route by Channel1', 'main', 0)]`
- Outgoing: `[('Quota OK?', 'main', 0)]`
- Parameter keys: `operation, query, options`

**Text at `query`:**

```text
=SELECT can_send, current_level, daily_cap, sent_today, remaining, reset_at, block_reason FROM check_sending_quota('{{ $('Assemble System Prompt').item.json.locationId }}'::text);
```

### `Quota OK?`

- Type: `n8n-nodes-base.if`
- Incoming: `[('Cap Lock Check', 'main', 0)]`
- Outgoing: `[('Send SMS', 'main', 0), ('Log Cap Suppression', 'main', 1)]`
- Parameter keys: `conditions`

```json
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "typeValidation": "loose",
      "version": 2
    },
    "conditions": [
      {
        "id": "quota-ok-check",
        "leftValue": "={{ $json.can_send }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "true",
          "singleValue": true
        }
      }
    ],
    "combinator": "and"
  }
}
```

### `Log Cap Suppression`

- Type: `n8n-nodes-base.supabase`
- Incoming: `[('Quota OK?', 'main', 1)]`
- Outgoing: `[('Cap Locked Silent', 'main', 0)]`
- Parameter keys: `operation, tableId, fieldsUi`

**Text at `fieldsUi.fieldValues[0].fieldValue`:**

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

**Text at `fieldsUi.fieldValues[1].fieldValue`:**

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```
