# Brain Engine LLM Injection Chain Evidence

Author: **Manus AI**
Date: **2026-04-29**

This file captures static evidence from the active Brain Engine workflow export. It does not modify production.

## Focus-node connection table

| Node | Type | Incoming | Outgoing | Relevant fields |
| --- | --- | --- | --- | ---: |
| `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | KB Tool (ai_tool), getContact (ai_tool), getNotes (ai_tool), getAppointments (ai_tool), deleteAppointment (ai_tool), Assemble System Prompt (main), bookAppointment (ai_tool), addAppointmentNotes (ai_tool), checkQualificationStatus (ai_tool), saveQualifyingAnswer (ai_tool), getAvailableSlots (ai_tool), searchPastMessages (ai_tool), rescheduleAppointment (ai_tool), updateContactMemory (ai_tool), subscribeToNewsletter (ai_tool), Anthropic Chat Model (ai_languageModel), switchChannel (ai_tool) | Analyze Conversation (main) | 3 |
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | Prepare Sentiment Context (main) | Parse Sentiment (main) | 6 |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | AI Agent (main) | Summary Exists? (main), Leak Detected? (main) | 7 |
| `Anthropic Chat Model` | `@n8n/n8n-nodes-langchain.lmChatAnthropic` | — | AI Agent (ai_languageModel) | 5 |
| `Apply Time Decay` | `n8n-nodes-base.postgres` | Business Hours Check (main) | Fetch Outbound Candidates (main) | 1 |
| `Assemble System Prompt` | `n8n-nodes-base.code` | Gather Prompt Data (main) | AI Agent (main) | 0 |
| `Cap Lock Check` | `n8n-nodes-base.postgres` | Route by Channel1 (main) | Quota OK? (main) | 1 |
| `Check Qualification Gate` | `n8n-nodes-base.supabase` | Route Intent (main) | Is Qualified? (main) | 2 |
| `Clear Newsletter Flags` | `n8n-nodes-base.supabase` | Newsletter Guard (main) | — | 3 |
| `Determine Action` | `n8n-nodes-base.code` | Update Conversation Context (main), Insert Conversation Context (main) | Outbound Bypass? (main) | 1 |
| `Docs Store` | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Embeddings (ai_embedding) | KB Tool (ai_vectorStore) | 4 |
| `Embeddings` | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | — | Docs Store (ai_embedding) | 0 |
| `Fetch Outbound Note` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Form Section4` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Gather Prompt Data` | `n8n-nodes-base.set` | Get Static Prompt Sections (main) | Assemble System Prompt (main) | 47 |
| `Gather Sentiment Data1` | `n8n-nodes-base.set` | Check Keyword Search (main), Merge & Deduplicate Messages (main) | Prepare Sentiment Context (main) | 13 |
| `Get Agent Config` | `n8n-nodes-base.supabase` | LeadDetails (main) | inboundTrue? (main) | 2 |
| `Get Agent Config (RAG)` | `n8n-nodes-base.supabase` | Set Direction: Inbound2 (main) | Merge Context (main) | 2 |
| `Get Conversation Summary` | `n8n-nodes-base.supabase` | Set Direction: Inbound2 (main) | Merge Context (main) | 2 |
| `Get Default Personality` | `n8n-nodes-base.postgres` | Has Custom Personality? (main) | Get Static Prompt Sections (main) | 1 |
| `Get Lead Memory (After)` | `n8n-nodes-base.supabase` | Log Outbound Message (main), Should Respond? (main) | Compare Memory (main) | 2 |
| `Get Message History` | `n8n-nodes-base.postgres` | Set Direction: Inbound2 (main) | Merge Context (main) | 1 |
| `Get Outbound Agent Config` | `n8n-nodes-base.supabase` | Set Outbound Context (main) | Merge Outbound Context (main) | 2 |
| `Get Outbound Conversation Summary` | `n8n-nodes-base.supabase` | Set Outbound Context (main) | Merge Outbound Context (main) | 2 |
| `Get Outbound Message History` | `n8n-nodes-base.postgres` | Set Outbound Context (main) | Merge Outbound Context (main) | 1 |
| `Get Prompt Blocks (SMRT)` | `n8n-nodes-base.postgres` | Prepare Tier Response (main), Merge Outbound Context (main) | Has Custom Personality? (main) | 1 |
| `Get Static Prompt Sections` | `n8n-nodes-base.supabase` | Get Default Personality (main) | Gather Prompt Data (main) | 2 |
| `Insert Conversation Context` | `n8n-nodes-base.supabase` | Summary Exists? (main) | Determine Action (main) | 12 |
| `KB Tool` | `@n8n/n8n-nodes-langchain.toolVectorStore` | Docs Store (ai_vectorStore), RAG LLM (ai_languageModel) | AI Agent (ai_tool) | 1 |
| `LeadDetails` | `n8n-nodes-base.set` | Set Direction: Inbound (main) | Get Agent Config (main) | 14 |
| `Leak Detected?` | `n8n-nodes-base.if` | Analyze Conversation (main) | Log AI Leak (main) | 1 |
| `Log AI Leak` | `n8n-nodes-base.supabase` | Leak Detected? (main) | — | 7 |
| `Log Cap Suppression` | `n8n-nodes-base.supabase` | Quota OK? (main) | Cap Locked Silent (main) | 5 |
| `Log Outbound Message` | `n8n-nodes-base.supabase` | Send Email (main), Send SMS (main) | Update Last Agent Message (main), Get Lead Memory (After) (main), Has Splinter Data? (main), Prep Status Check Input (main) | 10 |
| `Newsletter Guard` | `n8n-nodes-base.code` | Newsletter Offer Needed? (main) | Clear Newsletter Flags (main) | 1 |
| `Newsletter Offer Needed?` | `n8n-nodes-base.if` | Update Last Agent Message (main) | Set Newsletter Pending (main), Newsletter Guard (main) | 4 |
| `Outbound Bypass?` | `n8n-nodes-base.if` | Determine Action (main) | Route by Channel1 (main), Silence Gate (main) | 1 |
| `Parse Sentiment` | `n8n-nodes-base.code` | AI Sentiment Analysis (main) | Turnaround Gate (main) | 1 |
| `Prep Status Check Input` | `n8n-nodes-base.set` | Log Outbound Message (main) | Trigger Status Check (main) | 4 |
| `Prepare Sentiment Context` | `n8n-nodes-base.code` | Gather Sentiment Data1 (main) | AI Sentiment Analysis (main) | 1 |
| `Prepare Tier Response` | `n8n-nodes-base.code` | Tag Tier 2 in GHL (main), Tier Sub-Router1 (main), Route Intent (main), Log Already Escalated (main), Is Qualified? (main), Move GHL Pipeline Stage (main), Fetch Slots (main), Turnaround: Post Note (main), Send Farewell? (main) | Get Prompt Blocks (SMRT) (main) | 1 |
| `RAG LLM` | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | — | KB Tool (ai_languageModel) | 3 |
| `Route by Channel1` | `n8n-nodes-base.switch` | Should Respond? (main), Outbound Bypass? (main) | Cap Lock Check (main), Send Email (main) | 9 |
| `Search Relevant Messages` | `n8n-nodes-base.postgres` | Check Keyword Search (main) | Merge Messages (main) | 1 |
| `Send Email` | `n8n-nodes-base.httpRequest` | Route by Channel1 (main) | Log Outbound Message (main) | 3 |
| `Send SMS` | `n8n-nodes-base.httpRequest` | Quota OK? (main) | Log Outbound Message (main), Post-Farewell DND Gate (main) | 3 |
| `Set Newsletter Pending` | `n8n-nodes-base.supabase` | Newsletter Offer Needed? (main) | — | 2 |
| `Silence Gate` | `n8n-nodes-base.code` | Outbound Bypass? (main) | Should Respond? (main) | 1 |
| `Sticky Note13` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Sticky Note15` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Sticky Note2` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Sticky Note3` | `n8n-nodes-base.stickyNote` | — | — | 1 |
| `Summary Exists?` | `n8n-nodes-base.if` | Analyze Conversation (main) | Update Conversation Context (main), Insert Conversation Context (main) | 2 |
| `Turnaround Gate` | `n8n-nodes-base.if` | Parse Sentiment (main) | Turnaround: Clear State (main), L1 Drop Gate (main) | 2 |
| `Turnaround: Clear State` | `n8n-nodes-base.postgres` | Turnaround Gate (main) | Turnaround: Disable DND (main) | 1 |
| `Update Conversation Context` | `n8n-nodes-base.supabase` | Summary Exists? (main) | Determine Action (main) | 12 |
| `Update Last Agent Message` | `n8n-nodes-base.supabase` | Log Outbound Message (main) | Escalation Check? (main), Newsletter Offer Needed? (main) | 4 |
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 1 |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 1 |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | — | AI Agent (ai_tool) | 3 |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 1 |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | — | AI Agent (ai_tool) | 2 |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 1 |
| `getContact` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | — | AI Agent (ai_tool) | 2 |
| `getNotes` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | — | AI Agent (ai_tool) | 2 |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 1 |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | — | AI Agent (ai_tool) | 4 |
| `searchPastMessages` | `n8n-nodes-base.supabaseTool` | — | AI Agent (ai_tool) | 3 |
| `subscribeToNewsletter` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 2 |
| `switchChannel` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 2 |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | — | AI Agent (ai_tool) | 3 |

## Relevant prompt/context fields

### AI Agent

Type: `@n8n/n8n-nodes-langchain.agent`

#### `promptType` (6 chars)

```text
define
```

#### `text` (24 chars)

```text
={{ $json.userMessage }}
```

#### `options.systemMessage` (25 chars)

```text
={{ $json.systemPrompt }}
```


### AI Sentiment Analysis

Type: `@n8n/n8n-nodes-langchain.anthropic`

#### `modelId.__rl` (4 chars)

```text
True
```

#### `modelId.value` (25 chars)

```text
claude-haiku-4-5-20251001
```

#### `modelId.mode` (2 chars)

```text
id
```

#### `messages.values[0].content` (512 chars)

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

#### `options.system` (512 chars)

```text
You are a sentiment classifier for SMRT Bot. You analyze inbound messages and classify them into behavioral tiers to route the Brain Engine correctly.

CRITICAL: Your reasoning field is used INTERNALLY by downstream nodes ONLY. It is NEVER shown to the lead. The Brain Engine AI Agent uses its own prompt to write the actual SMS/email reply. Be thorough in your reasoning - it helps downstream routing, it never leaks to the customer.

=== CLASSIFICATION PRIORITY ORDER ===

Follow these steps IN ORD…[TRUNCATED]
```

#### `options.temperature` (1 chars)

```text
0
```


### Analyze Conversation

Type: `@n8n/n8n-nodes-langchain.openAi`

#### `modelId.__rl` (4 chars)

```text
True
```

#### `modelId.mode` (4 chars)

```text
list
```

#### `modelId.value` (11 chars)

```text
gpt-4o-mini
```

#### `messages.values[0].content` (512 chars)

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

#### `messages.values[0].role` (6 chars)

```text
system
```

#### `messages.values[1].content` (512 chars)

```text
=Previous Summary: {{ (() => { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary } catch(e) { try { return $('Get Conversation Summary').first().json.conversation_summary } catch(e2) { return 'None' } } })() }}
Previous Intent: {{ (() => { try { return $('Get Outbound Conversation Summary').first().json.lead_intent } catch(e) { try { return $('Get Conversation Summary').first().json.lead_intent } catch(e2) { return 'unknown' } } })() }}
Previous Timeline: {{ (…[TRUNCATED]
```

#### `options.temperature` (3 chars)

```text
0.3
```


### Anthropic Chat Model

Type: `@n8n/n8n-nodes-langchain.lmChatAnthropic`

#### `model.__rl` (4 chars)

```text
True
```

#### `model.value` (17 chars)

```text
claude-sonnet-4-6
```

#### `model.mode` (4 chars)

```text
list
```

#### `model.cachedResultName` (17 chars)

```text
Claude Sonnet 4.6
```

#### `options.temperature` (1 chars)

```text
0
```


### Apply Time Decay

Type: `n8n-nodes-base.postgres`

#### `query` (512 chars)

```text
UPDATE leads
SET
  pipeline_state = CASE
    WHEN pipeline_state = 'hot'  AND last_customer_message_at < NOW() - INTERVAL '14 days' THEN 'warm'
    WHEN pipeline_state = 'warm' AND last_customer_message_at < NOW() - INTERVAL '42 days' THEN 'cold'
    ELSE pipeline_state
  END
WHERE status = 'active_conversation'
  AND pipeline_state IN ('hot', 'warm')
  AND last_customer_message_at IS NOT NULL
  AND location_id = '{{ $json.location_id }}'
  AND (
    (pipeline_state = 'hot'  AND last_customer_me…[TRUNCATED]
```


### Cap Lock Check

Type: `n8n-nodes-base.postgres`

#### `query` (179 chars)

```text
=SELECT can_send, current_level, daily_cap, sent_today, remaining, reset_at, block_reason FROM check_sending_quota('{{ $('Assemble System Prompt').item.json.locationId }}'::text);
```


### Check Qualification Gate

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (47 chars)

```text
={{ $('LeadDetails').first().json.contact_id }}
```


### Clear Newsletter Flags

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue` (438 chars)

```text
={{ (() => { try { const leadMemory = $('Get Lead Memory (After)').first()?.json || $('Get Outbound Lead Memory').first()?.json || {}; if (leadMemory.newsletter_opted_in === true) return false; const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.newsletter_declined === true; } catch(e) { return false; } })() }}
```


### Determine Action

Type: `n8n-nodes-base.code`

#### `jsCode` (512 chars)

```text
const input = $input.first().json;

// Read AI Agent output directly — upstream Supabase node drops it
let responseText = '';
try { responseText = $('AI Agent').first().json.output || ''; } catch(e) {}
if (!responseText) responseText = input.output || input.text || input.response || '';
if (!responseText && input.message) responseText = input.message;

const agentName = (() => { try { return $('Assemble System Prompt').first().json.agentName || 'Luke'; } catch(e) { return input.agentName || 'Luk…[TRUNCATED]
```


### Docs Store

Type: `@n8n/n8n-nodes-langchain.vectorStoreSupabase`

#### `tableName.value` (9 chars)

```text
documents
```

#### `tableName.cachedResultName` (9 chars)

```text
documents
```

#### `options.queryName` (15 chars)

```text
match_documents
```

#### `options.metadata.metadataValues[0].value` (148 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.location_id } catch(e) { return $('LeadDetails').first().json.location_id } })() }}
```


### Fetch Outbound Note

Type: `n8n-nodes-base.stickyNote`

#### `content` (512 chars)

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


### Form Section4

Type: `n8n-nodes-base.stickyNote`

#### `content` (59 chars)

```text
##  Booking Agent Routing
#### Book Intent in conversation

```


### Gather Prompt Data

Type: `n8n-nodes-base.set`

#### `assignments.assignments[0].name` (9 chars)

```text
agentName
```

#### `assignments.assignments[0].value` (206 chars)

```text
={{ (() => { try { return $('Get Outbound Agent Config').first().json.agent_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.agent_name; } catch(e2) { return 'the agent'; } } })() }}
```

#### `assignments.assignments[1].value` (212 chars)

```text
={{ (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.coordinator_name; } catch(e2) { return 'Jon'; } } })() }}
```

#### `assignments.assignments[2].value` (199 chars)

```text
={{ (() => { try { return $('Get Outbound Agent Config').first().json.market_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.market_name; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[3].value` (207 chars)

```text
={{ (() => { try { return $('Get Outbound Agent Config').first().json.timezone; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.timezone; } catch(e2) { return 'America/Denver'; } } })() }}
```

#### `assignments.assignments[4].value` (199 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.direction; } catch(e) { try { return $('LeadDetails').first().json.direction || 'inbound'; } catch(e2) { return 'inbound'; } } })() }}
```

#### `assignments.assignments[5].value` (178 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.channel; } catch(e) { try { return $('LeadDetails').first().json.channel; } catch(e2) { return 'sms'; } } })() }}
```

#### `assignments.assignments[6].value` (188 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.first_name; } catch(e) { try { return $('LeadDetails').first().json.first_name; } catch(e2) { return 'Contact'; } } })() }}
```

#### `assignments.assignments[7].value` (181 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.contact_id; } catch(e) { try { return $('LeadDetails').first().json.contact_id; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[8].value` (183 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.location_id; } catch(e) { try { return $('LeadDetails').first().json.location_id; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[9].value` (204 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.pipeline_stage; } catch(e) { try { return $('Get Lead Memory').first().json.pipeline_stage; } catch(e2) { return 'MONTHLY'; } } })() }}
```

#### `assignments.assignments[10].value` (197 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.intent_level; } catch(e) { try { return $('Get Lead Memory').first().json.intent_level; } catch(e2) { return 'none'; } } })() }}
```

#### `assignments.assignments[11].name` (4 chars)

```text
tier
```

#### `assignments.assignments[11].value` (113 chars)

```text
={{ (() => { try { return $('Prepare Tier Response').first().json.tier; } catch(e) { return 'standard'; } })() }}
```

#### `assignments.assignments[12].name` (11 chars)

```text
userMessage
```

#### `assignments.assignments[12].value` (325 chars)

```text
={{ (() => { try { const b = $('Check Batch Leader').first().json.batchedMessageBody; if (b) return b; } catch(e) {} try { return $('Set Outbound Context').first().json.message; } catch(e) { try { return $('LeadDetails').first().json.message_body || $('LeadDetails').first().json.message; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[13].name` (19 chars)

```text
conversationSummary
```

#### `assignments.assignments[13].value` (227 chars)

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary; } catch(e) { try { return $('Get Conversation Summary').first().json.conversation_summary; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[14].value` (210 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.relationship_type; } catch(e) { try { return $('Get Lead Memory').first().json.relationship_type; } catch(e2) { return 'unknown'; } } })() }}
```

#### `assignments.assignments[15].value` (198 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.market_role; } catch(e) { try { return $('Get Lead Memory').first().json.market_role; } catch(e2) { return 'unknown'; } } })() }}
```

#### `assignments.assignments[16].value` (193 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.intent_topic; } catch(e) { try { return $('Get Lead Memory').first().json.intent_topic; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[17].value` (187 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.open_loop; } catch(e) { try { return $('Get Lead Memory').first().json.open_loop; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[18].value` (212 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.contact_preference; } catch(e) { try { return $('Get Lead Memory').first().json.contact_preference; } catch(e2) { return 'unknown'; } } })() }}
```

#### `assignments.assignments[19].name` (16 chars)

```text
shortSummaryNote
```

#### `assignments.assignments[19].value` (205 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.short_summary_note; } catch(e) { try { return $('Get Lead Memory').first().json.short_summary_note; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[20].value` (256 chars)

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_pending || false; } catch(e) { try { return $('Get Conversation Summary').first().json.newsletter_offer_pending || false; } catch(e2) { return false; } } })() }}
```

#### `assignments.assignments[21].value` (228 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.newsletter_opted_in || false; } catch(e) { try { return $('Get Lead Memory').first().json.newsletter_opted_in || false; } catch(e2) { return false; } } })() }}
```

#### `assignments.assignments[22].value` (258 chars)

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_declined || false; } catch(e) { try { return $('Get Conversation Summary').first().json.newsletter_offer_declined || false; } catch(e2) { return false; } } })() }}
```

#### `assignments.assignments[23].value` (122 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.splinter_content || ''; } catch(e) { return ''; } })() }}
```

#### `assignments.assignments[24].value` (120 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.splinter_topic || ''; } catch(e) { return ''; } })() }}
```

#### `assignments.assignments[25].value` (125 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.splinter_data_point || ''; } catch(e) { return ''; } })() }}
```

#### `assignments.assignments[26].name` (8 chars)

```text
leadTemp
```

#### `assignments.assignments[26].value` (201 chars)

```text
={{ (() => { try { return $('Get Outbound Lead Memory').first().json.pipeline_state; } catch(e) { try { return $('Get Lead Memory').first().json.pipeline_state; } catch(e2) { return 'warm'; } } })() }}
```

#### `assignments.assignments[27].name` (10 chars)

```text
leadIntent
```

#### `assignments.assignments[27].value` (216 chars)

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.lead_intent; } catch(e) { try { return $('Get Conversation Summary').first().json.lead_intent; } catch(e2) { return 'unknown'; } } })() }}
```


### Gather Sentiment Data1

Type: `n8n-nodes-base.set`

#### `assignments.assignments[0].name` (14 chars)

```text
currentMessage
```

#### `assignments.assignments[0].value` (279 chars)

```text
={{ (() => { try { const b = $('Check Batch Leader').first().json.batchedMessageBody; if (b) return b; } catch(e) {} try { return $('LeadDetails').first().json.message; } catch(e) { try { return $('Set Outbound Context').first().json.message; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[1].value` (181 chars)

```text
={{ (() => { try { return $('LeadDetails').first().json.contact_id; } catch(e) { try { return $('Set Outbound Context').first().json.contact_id; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[2].value` (183 chars)

```text
={{ (() => { try { return $('LeadDetails').first().json.location_id; } catch(e) { try { return $('Set Outbound Context').first().json.location_id; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[3].value` (188 chars)

```text
={{ (() => { try { return $('LeadDetails').first().json.first_name; } catch(e) { try { return $('Set Outbound Context').first().json.first_name; } catch(e2) { return 'Contact'; } } })() }}
```

#### `assignments.assignments[4].name` (19 chars)

```text
conversationSummary
```

#### `assignments.assignments[4].value` (239 chars)

```text
={{ (() => { try { return $('Get Conversation Summary').first().json.conversation_summary || ''; } catch(e) { try { return $('Get Outbound Conversation Summary').first().json.conversation_summary || ''; } catch(e2) { return ''; } } })() }}
```

#### `assignments.assignments[5].name` (9 chars)

```text
agentName
```

#### `assignments.assignments[5].value` (209 chars)

```text
={{ (() => { try { return $('Get Agent Config (RAG)').first().json.agent_name; } catch(e) { try { return $('Get Outbound Agent Config').first().json.agent_name; } catch(e2) { return 'Luke Gilbert'; } } })() }}
```

#### `assignments.assignments[6].name` (14 chars)

```text
messageHistory
```

#### `assignments.assignments[6].value` (242 chars)

```text
={{ (() => { try { const msgs = $('Get Message History').all(); return msgs.slice(0, 15).map(m => (m.json.direction === 'inbound' ? '[lead] ' : '[bot] ') + m.json.message_body).join('\n'); } catch(e) { return 'No previous messages'; } })() }}
```

#### `assignments.assignments[7].value` (230 chars)

```text
={{ (() => { try { return $('Get Lead Memory').first().json.pipeline_stage || 'MONTHLY'; } catch(e) { try { return $('Get Outbound Lead Memory').first().json.pipeline_stage || 'MONTHLY'; } catch(e2) { return 'MONTHLY'; } } })() }}
```

#### `assignments.assignments[8].value` (221 chars)

```text
={{ (() => { try { return $('Get Lead Memory').first().json.pipeline_state || 'warm'; } catch(e) { try { return $('Get Outbound Lead Memory').first().json.pipeline_state || 'warm'; } catch(e2) { return 'warm'; } } })() }}
```


### Get Agent Config

Type: `n8n-nodes-base.supabase`

#### `tableId` (6 chars)

```text
agents
```

#### `filters.conditions[0].keyValue` (24 chars)

```text
={{ $json.location_id }}
```


### Get Agent Config (RAG)

Type: `n8n-nodes-base.supabase`

#### `tableId` (6 chars)

```text
agents
```

#### `filters.conditions[0].keyValue` (48 chars)

```text
={{ $('LeadDetails').first().json.location_id }}
```


### Get Conversation Summary

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (47 chars)

```text
={{ $('LeadDetails').first().json.contact_id }}
```


### Get Default Personality

Type: `n8n-nodes-base.postgres`

#### `query` (82 chars)

```text
SELECT value FROM system_defaults WHERE key = 'default_personality_prompt' LIMIT 1
```


### Get Lead Memory (After)

Type: `n8n-nodes-base.supabase`

#### `tableId` (5 chars)

```text
leads
```

#### `filters.conditions[0].keyValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```


### Get Message History

Type: `n8n-nodes-base.postgres`

#### `query` (272 chars)

```text
=SELECT 
  ml.*,
  (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $('LeadDetails').first().json.contact_id }}') as interaction_count
FROM message_log ml 
WHERE ml.contact_id = '{{ $('LeadDetails').first().json.contact_id }}' 
ORDER BY ml.timestamp DESC 
LIMIT 15
```


### Get Outbound Agent Config

Type: `n8n-nodes-base.supabase`

#### `tableId` (6 chars)

```text
agents
```

#### `filters.conditions[0].keyValue` (24 chars)

```text
={{ $json.location_id }}
```


### Get Outbound Conversation Summary

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (23 chars)

```text
={{ $json.contact_id }}
```


### Get Outbound Message History

Type: `n8n-nodes-base.postgres`

#### `query` (215 chars)

```text
SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id = '{{ $json.contact_id }}' ORDER BY ml.timestamp DESC LIMIT 15
```


### Get Prompt Blocks (SMRT)

Type: `n8n-nodes-base.postgres`

#### `query` (327 chars)

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


### Get Static Prompt Sections

Type: `n8n-nodes-base.supabase`

#### `tableId` (22 chars)

```text
static_prompt_sections
```

#### `filters.conditions[0].keyValue` (216 chars)

```text
={{ (() => { try { return $('Get Agent Config (RAG)').first().json.location_id } catch(e) { try { return $('Get Outbound Agent Config').first().json.location_id } catch(e2) { return 'kv1Af9i1qYK7KfIiT0U3' } } })() }}
```


### Insert Conversation Context

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `fieldsUi.fieldValues[0].fieldValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue` (58 chars)

```text
={{ $('Assemble System Prompt').first().json.locationId }}
```

#### `fieldsUi.fieldValues[2].fieldId` (20 chars)

```text
conversation_summary
```

#### `fieldsUi.fieldValues[2].fieldValue` (309 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.summary || content; } catch(e) { return $('Analyze Conversation').first().json.message?.content || ''; } })() }}
```

#### `fieldsUi.fieldValues[3].fieldValue` (196 chars)

```text
={{ (() => { try { return $('Parse Sentiment').first().json.sentiment_analysis ? $('Parse Sentiment').first().json.sentiment_analysis.action : 'continue'; } catch(e) { return 'continue'; } })() }}
```

#### `fieldsUi.fieldValues[4].fieldId` (11 chars)

```text
lead_intent
```

#### `fieldsUi.fieldValues[4].fieldValue` (216 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

#### `fieldsUi.fieldValues[5].fieldId` (13 chars)

```text
lead_timeline
```

#### `fieldsUi.fieldValues[5].fieldValue` (218 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_timeline || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

#### `fieldsUi.fieldValues[8].fieldValue` (300 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' || parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}
```

#### `fieldsUi.fieldValues[9].fieldValue` (254 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}
```


### KB Tool

Type: `@n8n/n8n-nodes-langchain.toolVectorStore`

#### `description` (512 chars)

```text
=Search the approved company knowledge base for client location {{ (() => { try { return $('Set Outbound Context').first().json.location_id } catch(e) { return $('LeadDetails').first().json.location_id } })() }}.

WHEN TO USE:
- When the lead asks about commission rates, fees, or pricing
- When the lead asks about services offered, property types, or areas served
- When the lead asks how the team operates or any company-specific question
- ANY question about the business, team, or real estate se…[TRUNCATED]
```


### LeadDetails

Type: `n8n-nodes-base.set`

#### `assignments.assignments[0].value` (29 chars)

```text
={{ $json.body.location.id }}
```

#### `assignments.assignments[1].value` (28 chars)

```text
={{ $json.body.contact_id }}
```

#### `assignments.assignments[2].name` (17 chars)

```text
timestamp_message
```

#### `assignments.assignments[3].name` (7 chars)

```text
message
```

#### `assignments.assignments[3].value` (30 chars)

```text
={{ $json.body.message.body }}
```

#### `assignments.assignments[4].value` (28 chars)

```text
={{ $json.body.first_name }}
```

#### `assignments.assignments[5].value` (27 chars)

```text
={{ $json.body.last_name }}
```

#### `assignments.assignments[6].value` (23 chars)

```text
={{ $json.body.email }}
```

#### `assignments.assignments[7].value` (23 chars)

```text
={{ $json.body.phone }}
```

#### `assignments.assignments[8].value` (22 chars)

```text
={{ $json.body.city }}
```

#### `assignments.assignments[9].value` (23 chars)

```text
={{ $json.body.state }}
```

#### `assignments.assignments[11].name` (12 chars)

```text
message_type
```

#### `assignments.assignments[11].value` (30 chars)

```text
={{ $json.body.message.type }}
```

#### `assignments.assignments[12].value` (31 chars)

```text
={{ $json.body.workflow.name }}
```


### Leak Detected?

Type: `n8n-nodes-base.if`

#### `conditions.conditions[0].leftValue` (276 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.internal_reasoning_leak_detected === true; } catch(e) { return false; } })() }}
```


### Log AI Leak

Type: `n8n-nodes-base.supabase`

#### `tableId` (16 chars)

```text
ai_output_errors
```

#### `fieldsUi.fieldValues[0].fieldValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue` (190 chars)

```text
={{ (() => { try { return $('Get Agent Config').first().json.location_id } catch(e) { try { return $('Get Outbound Agent Config').first().json.location_id } catch(e2) { return '' } } })() }}
```

#### `fieldsUi.fieldValues[3].fieldValue` (65 chars)

```text
={{ $('Assemble System Prompt').first().json.channelType || '' }}
```

#### `fieldsUi.fieldValues[5].fieldId` (10 chars)

```text
raw_output
```

#### `fieldsUi.fieldValues[5].fieldValue` (40 chars)

```text
={{ $('AI Agent').first().json.output }}
```

#### `fieldsUi.fieldValues[6].fieldValue` (260 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.leak_phrase || ''; } catch(e) { return 'parse_error'; } })() }}
```


### Log Cap Suppression

Type: `n8n-nodes-base.supabase`

#### `tableId` (19 chars)

```text
message_send_errors
```

#### `fieldsUi.fieldValues[0].fieldValue` (54 chars)

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue` (55 chars)

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```

#### `fieldsUi.fieldValues[4].fieldId` (11 chars)

```text
raw_message
```

#### `fieldsUi.fieldValues[4].fieldValue` (167 chars)

```text
=Send suppressed by Brain Engine Cap Lock Check. block_reason: {{ $('Cap Lock Check').item.json.block_reason }}, reset_at: {{ $('Cap Lock Check').item.json.reset_at }}
```


### Log Outbound Message

Type: `n8n-nodes-base.supabase`

#### `tableId` (11 chars)

```text
message_log
```

#### `fieldsUi.fieldValues[0].fieldValue` (54 chars)

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue` (55 chars)

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```

#### `fieldsUi.fieldValues[3].fieldId` (12 chars)

```text
message_body
```

#### `fieldsUi.fieldValues[3].fieldValue` (84 chars)

```text
={{ $('Silence Gate').first().json.responseText || $('AI Agent').item.json.output }}
```

#### `fieldsUi.fieldValues[4].fieldValue` (56 chars)

```text
={{ $('Assemble System Prompt').item.json.channelType }}
```

#### `fieldsUi.fieldValues[7].fieldId` (14 chars)

```text
ghl_message_id
```

#### `fieldsUi.fieldValues[7].fieldValue` (22 chars)

```text
={{ $json.messageId }}
```

#### `fieldsUi.fieldValues[8].fieldId` (19 chars)

```text
ghl_conversation_id
```

#### `fieldsUi.fieldValues[8].fieldValue` (27 chars)

```text
={{ $json.conversationId }}
```


### Newsletter Guard

Type: `n8n-nodes-base.code`

#### `jsCode` (203 chars)

```text
// Always guarantee 1 item with a stable contact_id so Clear Newsletter Flags never receives 0 items
const ctx = $('Assemble System Prompt').first().json;
return [{ json: { contactId: ctx.contactId } }];
```


### Newsletter Offer Needed?

Type: `n8n-nodes-base.if`

#### `conditions.conditions[0].leftValue` (263 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed === true && parsed.appointment_outcome === 'rejected'; } catch(e) { return false; } })() }}
```

#### `conditions.conditions[1].leftValue` (207 chars)

```text
={{ (() => { try { return $('Get Lead Memory').first().json.newsletter_opted_in } catch(e) { try { return $('Get Outbound Lead Memory').first().json.newsletter_opted_in } catch(e2) { return false } } })() }}
```

#### `conditions.conditions[2].leftValue` (237 chars)

```text
={{ (() => { try { return $('Get Conversation Summary').first().json.newsletter_offer_declined } catch(e) { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_declined } catch(e2) { return false } } })() }}
```

#### `conditions.conditions[3].leftValue` (116 chars)

```text
={{ (() => { try { return $('Assemble System Prompt').first().json.direction } catch(e) { return 'inbound' } })() }}
```


### Outbound Bypass?

Type: `n8n-nodes-base.if`

#### `conditions.conditions[0].leftValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.direction }}
```


### Parse Sentiment

Type: `n8n-nodes-base.code`

#### `jsCode` (512 chars)

```text
const input = $json;

let parsed;
try {
  let text = '';
  if (input.content && Array.isArray(input.content)) {
    text = input.content.map(c => c.text || '').join('');
  } else if (input.message && input.message.content) {
    text = input.message.content;
  } else if (input.text) {
    text = input.text;
  } else if (typeof input === 'string') {
    text = input;
  } else {
    text = JSON.stringify(input);
  }
  
  const fenceMatch = text.match(/\`\`\`(?:json)?\n?([\s\S]*?)\`\`\`/);
  if (fe…[TRUNCATED]
```


### Prep Status Check Input

Type: `n8n-nodes-base.set`

#### `assignments.assignments[0].name` (9 chars)

```text
messageId
```

#### `assignments.assignments[0].value` (27 chars)

```text
={{ $json.ghl_message_id }}
```

#### `assignments.assignments[2].value` (54 chars)

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

#### `assignments.assignments[3].value` (55 chars)

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```


### Prepare Sentiment Context

Type: `n8n-nodes-base.code`

#### `jsCode` (512 chars)

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


### Prepare Tier Response

Type: `n8n-nodes-base.code`

#### `jsCode` (512 chars)

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


### RAG LLM

Type: `@n8n/n8n-nodes-langchain.lmChatOpenAi`

#### `model.__rl` (4 chars)

```text
True
```

#### `model.mode` (4 chars)

```text
list
```

#### `model.value` (11 chars)

```text
gpt-4o-mini
```


### Route by Channel1

Type: `n8n-nodes-base.switch`

#### `rules.values[0].conditions.conditions[0].leftValue` (439 chars)

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

#### `rules.values[0].renameOutput` (4 chars)

```text
True
```

#### `rules.values[0].outputKey` (3 chars)

```text
SMS
```

#### `rules.values[1].conditions.conditions[0].leftValue` (439 chars)

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

#### `rules.values[1].renameOutput` (4 chars)

```text
True
```

#### `rules.values[1].outputKey` (5 chars)

```text
Email
```

#### `rules.values[2].conditions.conditions[0].leftValue` (439 chars)

```text
=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}
```

#### `rules.values[2].renameOutput` (4 chars)

```text
True
```

#### `rules.values[2].outputKey` (8 chars)

```text
Facebook
```


### Search Relevant Messages

Type: `n8n-nodes-base.postgres`

#### `query` (437 chars)

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


### Send Email

Type: `n8n-nodes-base.httpRequest`

#### `url` (59 chars)

```text
https://services.leadconnectorhq.com/conversations/messages
```

#### `specifyBody` (4 chars)

```text
json
```

#### `jsonBody` (512 chars)

```text
={{ (() => { const raw = $json.responseText || $('AI Agent').first().json.output; const contactId = $('Assemble System Prompt').first().json.contactId; const coordinatorEmail = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_email } catch(e) { return $('Get Agent Config').first().json.coordinator_email } })(); const coordinatorName = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name } catch(e) { try { return $('Get Agent Config').fir…[TRUNCATED]
```


### Send SMS

Type: `n8n-nodes-base.httpRequest`

#### `url` (59 chars)

```text
https://services.leadconnectorhq.com/conversations/messages
```

#### `specifyBody` (4 chars)

```text
json
```

#### `jsonBody` (167 chars)

```text
={{ JSON.stringify({ type: 'SMS', contactId: $('Assemble System Prompt').first().json.contactId, message: $json.responseText || $('AI Agent').first().json.output }) }}
```


### Set Newsletter Pending

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```


### Silence Gate

Type: `n8n-nodes-base.code`

#### `jsCode` (512 chars)

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


### Sticky Note13

Type: `n8n-nodes-base.stickyNote`

#### `content` (65 chars)

```text
## Pull Memory

1. Message Logs
2. Conversation_summary/context


```


### Sticky Note15

Type: `n8n-nodes-base.stickyNote`

#### `content` (65 chars)

```text
## Pull Memory

1. Message Logs
2. Conversation_summary/context


```


### Sticky Note2

Type: `n8n-nodes-base.stickyNote`

#### `content` (115 chars)

```text
## Prompt Selection & Assemebly  
**Double click** to edit me. [Guide](https://docs.n8n.io/workflows/sticky-notes/)
```


### Sticky Note3

Type: `n8n-nodes-base.stickyNote`

#### `content` (94 chars)

```text
## AI Model (RAG System)

Dynamic context gathering → Prompt assembly → AI response → GHL send
```


### Summary Exists?

Type: `n8n-nodes-base.if`

#### `conditions.conditions[0].id` (17 chars)

```text
summary-check-001
```

#### `conditions.conditions[0].leftValue` (195 chars)

```text
={{ (() => { try { return $('Get Outbound Conversation Summary').first().json.id } catch(e) { try { return $('Get Conversation Summary').first().json.id } catch(e2) { return undefined } } })() }}
```


### Turnaround Gate

Type: `n8n-nodes-base.if`

#### `conditions.conditions[0].leftValue` (104 chars)

```text
={{ (() => { try { return $('searchLeads').first().json.opt_out_level } catch(e) { return null } })() }}
```

#### `conditions.conditions[1].leftValue` (19 chars)

```text
={{ $json.action }}
```


### Turnaround: Clear State

Type: `n8n-nodes-base.postgres`

#### `query` (195 chars)

```text
=UPDATE leads SET opt_out_level=NULL, opted_out_at=NULL, opt_out_reason=NULL, sms_paused_until=NULL, status='active_conversation' WHERE contact_id='{{ $('LeadDetails').first().json.contact_id }}'
```


### Update Conversation Context

Type: `n8n-nodes-base.supabase`

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```

#### `fieldsUi.fieldValues[0].fieldId` (20 chars)

```text
conversation_summary
```

#### `fieldsUi.fieldValues[0].fieldValue` (512 chars)

```text
={{ (() => {  const turnCounter = (() => {   try { return parseInt($('searchLeads').first().json.turn_counter) || 0 }   catch(e) {    try { return parseInt($('Get Lead Memory').first().json.turn_counter) || 0 }    catch(e2) {     try { return parseInt($('Get Outbound Lead Memory').first().json.turn_counter) || 0 }     catch(e3) { return 0 }    }   }  })();  const shouldRegen = (turnCounter <= 2 || turnCounter % 10 === 0);  if (shouldRegen) {   try {    const content = $('Analyze Conversation').f…[TRUNCATED]
```

#### `fieldsUi.fieldValues[1].fieldValue` (196 chars)

```text
={{ (() => { try { return $('Parse Sentiment').first().json.sentiment_analysis ? $('Parse Sentiment').first().json.sentiment_analysis.action : 'continue'; } catch(e) { return 'continue'; } })() }}
```

#### `fieldsUi.fieldValues[3].fieldId` (11 chars)

```text
lead_intent
```

#### `fieldsUi.fieldValues[3].fieldValue` (263 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

#### `fieldsUi.fieldValues[4].fieldId` (13 chars)

```text
lead_timeline
```

#### `fieldsUi.fieldValues[4].fieldValue` (265 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.lead_timeline || 'unknown'; } catch(e) { return 'unknown'; } })() }}
```

#### `fieldsUi.fieldValues[5].fieldValue` (347 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' || parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}
```

#### `fieldsUi.fieldValues[6].fieldValue` (301 chars)

```text
={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && parsed.appointment_outcome === 'accepted'; } catch(e) { return false; } })() }}
```

#### `fieldsUi.fieldValues[7].fieldValue` (512 chars)

```text
={{ (() => {  const turnCounter = (() => {   try { return parseInt($('searchLeads').first().json.turn_counter) || 0 }   catch(e) {    try { return parseInt($('Get Lead Memory').first().json.turn_counter) || 0 }    catch(e2) { return 0 }   }  })();  const shouldRegen = (turnCounter <= 2 || turnCounter % 10 === 0);  if (shouldRegen) {   return new Date().toISOString();  } else {   try { return $('Get Outbound Conversation Summary').first().json.last_summarized_at || null }   catch(e) { try { retur…[TRUNCATED]
```


### Update Last Agent Message

Type: `n8n-nodes-base.supabase`

#### `tableId` (5 chars)

```text
leads
```

#### `filters.conditions[0].keyValue` (23 chars)

```text
={{ $json.contact_id }}
```

#### `fieldsUi.fieldValues[0].fieldId` (21 chars)

```text
last_agent_message_at
```

#### `fieldsUi.fieldValues[1].fieldValue` (246 chars)

```text
={{ (() => { const stage = $('Assemble System Prompt').first().json.pipelineStage || 'MONTHLY'; const days = stage === 'MONTHLY' ? 28 : stage === 'BIWEEKLY' ? 14 : 7; return new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString(); })() }}
```


### addAppointmentNotes

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `jsonSchemaExample` (129 chars)

```text
{"appointment_time":"2026-04-10T09:00","qualifying_summary":"Buyer, 500k, pre-approved","conversation_summary":"Lead relocating"}
```


### bookAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `jsonSchemaExample` (45 chars)

```text
{"selected_slot":"2026-04-10T09:00:00-06:00"}
```


### checkQualificationStatus

Type: `n8n-nodes-base.supabaseTool`

#### `toolDescription` (512 chars)

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

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (146 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}
```


### deleteAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `jsonSchemaExample` (21 chars)

```text
{"event_id":"abc123"}
```


### getAppointments

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`

#### `toolDescription` (512 chars)

```text
Fetch all appointments (past and upcoming) for the current lead from GoHighLevel.

WHEN TO USE:
- When the lead asks about existing appointments ("when is my appointment?", "do I have anything scheduled?")
- When the lead wants to cancel or reschedule (you need the event_id from here)
- When you need to check if the lead already has a booking before offering to schedule

INPUT: No input needed. Automatically looks up the current lead.

OUTPUT: List of appointment objects with event IDs, dates, t…[TRUNCATED]
```

#### `url` (206 chars)

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/appointments
```


### getAvailableSlots

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `jsonSchemaExample` (56 chars)

```text
{"timezone":"America/Denver","target_date":"2026-04-15"}
```


### getContact

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`

#### `toolDescription` (512 chars)

```text
Fetch the full contact profile for the current lead from GoHighLevel, including custom fields, tags, lead source, and all contact details.

WHEN TO USE:
- When you need lead details NOT available in the conversation (email, address, tags, lead source)
- When the lead asks you to confirm their contact information
- When you need CRM context about the lead's history or status

INPUT: No input needed. Automatically looks up the current lead.

OUTPUT: Full contact record with name, email, phone, tag…[TRUNCATED]
```

#### `url` (193 chars)

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}
```


### getNotes

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`

#### `toolDescription` (512 chars)

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

#### `url` (199 chars)

```text
=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/notes
```


### rescheduleAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `jsonSchemaExample` (59 chars)

```text
{"event_id":"abc","start_time":"2026-04-10T10:00:00-06:00"}
```


### saveQualifyingAnswer

Type: `n8n-nodes-base.supabaseTool`

#### `toolDescription` (512 chars)

```text
MANDATORY TOOL - Save a qualifying answer to the database after the lead answers one of the 3 qualifying questions.

WHEN TO USE: You MUST call this tool IMMEDIATELY every time the lead provides information that answers Q1, Q2, or Q3. Do NOT wait until all questions are answered. Save each answer the moment you receive it.

The tool updates the qualifying_answers JSONB column in conversation_context for this lead.

INPUT: You must provide a JSON object with the field 'qualifying_answers' contain…[TRUNCATED]
```

#### `tableId` (20 chars)

```text
conversation_context
```

#### `filters.conditions[0].keyValue` (146 chars)

```text
={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}
```

#### `fieldsUi.fieldValues[0].fieldValue` (340 chars)

```text
={{ $fromAI('qualifying_answers', 'The complete qualifying_answers JSON object with keys q1, q2, q3. Each key is either a string summary of the lead answer or null if not yet answered. Example: {"q1": "Buying, 3 month timeline", "q2": "Budget around 500k", "q3": null}. IMPORTANT: Include ALL existing answers plus the new one.', 'json') }}
```


### searchPastMessages

Type: `n8n-nodes-base.supabaseTool`

#### `toolDescription` (512 chars)

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

#### `tableId` (11 chars)

```text
message_log
```

#### `filters.conditions[0].keyValue` (57 chars)

```text
={{ $('Assemble System Prompt').first().json.contactId }}
```


### subscribeToNewsletter

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `description` (512 chars)

```text
Subscribe the current lead to the weekly market newsletter. Updates leads.newsletter_opted_in = true, tags the contact in GHL, and clears pending flags.

INPUT (required JSON):
- contact_id: string - the CONTACT_ID from the context header (always required)

CALL THIS TOOL when the lead signals they want market updates, want to stay in the loop, accept the newsletter offer, or agree to receive periodic info. Call it BEFORE you write your response acknowledging the subscription — never acknowledge…[TRUNCATED]
```

#### `jsonSchemaExample` (24 chars)

```text
{"contact_id": "abc123"}
```


### switchChannel

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `description` (512 chars)

```text
Switch the lead's communication channel and send a hardcoded bridge message on the new channel. Call this ONLY when the lead explicitly asks to move to a different channel (e.g. "just email me", "text me instead").

SUPPORTED DESTINATIONS: sms, email. You CANNOT switch TO Instagram DM — only FROM it. If a lead asks to be contacted on Instagram, politely decline and offer SMS or email instead.

INPUT (required JSON):
- contact_id: string — CONTACT_ID from context
- new_channel: string — must be "…[TRUNCATED]
```

#### `jsonSchemaExample` (45 chars)

```text
{"contact_id":"abc123","new_channel":"email"}
```


### updateContactMemory

Type: `@n8n/n8n-nodes-langchain.toolCode`

#### `name` (19 chars)

```text
updateContactMemory
```

#### `description` (512 chars)

```text
Update the contact's memory and enrichment fields. Call this when you detect ANY of the signals below. Include ALL detected fields in a single call — never make multiple calls.

INPUT (required JSON):
- contact_id: string - CONTACT_ID from context (always required)
- Plus any fields below that you detected:

FIELD TRIGGERS — scan every message for these:

IDENTITY / CONTACT INFO
- Lead says their name → first_name, last_name
- Lead gives their email address → email
- Lead gives their phone numbe…[TRUNCATED]
```

#### `jsonSchemaExample` (512 chars)

```text
{"contact_id":"abc123","first_name":"Mike","last_name":"Johnson","email":"mike@test.com","phone":"208-555-1234","address":"123 Oak St","city":"Eagle","state":"Idaho","postal_code":"83616","market_role":"buyer","intent_topic":"buying","intent_level":"active","contact_preference":"sms","relationship_type":"sphere","open_loop":"needs to sell CA house before buying, target June","handoff_reason":"wants legal advice on lease","needs_human_review":true,"review_reason":"recent bereavement, pause outrea…[TRUNCATED]
```

