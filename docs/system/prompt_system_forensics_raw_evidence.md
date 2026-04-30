# SMRT Prompt System Forensics — Raw Static Evidence

Author: **Manus AI**

Status: **Static, read-only workflow evidence. No production changes were made.**

## Summary

| Metric | Value |
|---|---:|
| `tool_nodes_total` | 15 |
| `ai_agent_connected_tool_count` | 15 |
| `connected_tool_description_chars` | 5170 |
| `connected_tool_description_est_tokens` | 1292 |
| `mandatory_or_critical_connected_tools` | 4 |
| `summary_related_node_count` | 22 |
| `tool_type_counts` | {'@n8n/n8n-nodes-langchain.toolVectorStore': 1, '@n8n/n8n-nodes-langchain.toolHttpRequest': 3, '@n8n/n8n-nodes-langchain.toolCode': 8, 'n8n-nodes-base.supabaseTool': 3} |

## AI Agent Wiring

| Field | Value |
|---|---|
| `present` | `True` |
| `type` | `@n8n/n8n-nodes-langchain.agent` |
| `system_message` | `={{ $json.systemPrompt }}` |
| `text_expression` | `={{ $json.userMessage }}` |
| `max_iterations` | `10` |

## Tools Connected Directly To AI Agent

| Tool | Type | Description chars | Mandatory/critical language | When-to-use | When-not-to-use |
|---|---|---:|---|---|---|
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | 10 | False | False | False |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 10 | False | False | False |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | 512 | False | True | False |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 10 | False | False | False |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 512 | False | True | False |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | 10 | False | False | False |
| `getContact` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 512 | False | True | False |
| `getNotes` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | 512 | False | True | False |
| `KB Tool` | `@n8n/n8n-nodes-langchain.toolVectorStore` | 512 | False | True | False |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | 10 | False | False | False |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | 512 | True | True | False |
| `searchPastMessages` | `n8n-nodes-base.supabaseTool` | 512 | False | True | True |
| `subscribeToNewsletter` | `@n8n/n8n-nodes-langchain.toolCode` | 512 | True | False | False |
| `switchChannel` | `@n8n/n8n-nodes-langchain.toolCode` | 512 | True | False | False |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | 512 | True | False | False |

## Connected Tool Description Excerpts

### `addAppointmentNotes`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **10**.

> [REDACTED]

### `bookAppointment`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **10**.

> [REDACTED]

### `checkQualificationStatus`

Type: `n8n-nodes-base.supabaseTool`. Description chars: **512**.

> Check how many of the 3 qualifying questions this lead has answered so far.  WHEN TO USE: - BEFORE calling saveQualifyingAnswer, to get the current qualifying_answers object - When the lead says they want to book an appointment, to verify they are qualified - When you are unsure which qualifying questions have already been answered  INPUT: No input needed. Automatically looks up this lead's conversation_context record.  OUTPUT: Returns the qualifying_answers JSONB object with keys q1, q2, q3. - …[TRUNCATED]

### `deleteAppointment`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **10**.

> [REDACTED]

### `getAppointments`

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`. Description chars: **512**.

> Fetch all appointments (past and upcoming) for the current lead from GoHighLevel.  WHEN TO USE: - When the lead asks about existing appointments ("when is my appointment?", "do I have anything scheduled?") - When the lead wants to cancel or reschedule (you need the event_id from here) - When you need to check if the lead already has a booking before offering to schedule  INPUT: No input needed. Automatically looks up the current lead.  OUTPUT: List of appointment objects with event IDs, dates, t…[TRUNCATED]

### `getAvailableSlots`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **10**.

> [REDACTED]

### `getContact`

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`. Description chars: **512**.

> Fetch the full contact profile for the current lead from GoHighLevel, including custom fields, tags, lead source, and all contact details.  WHEN TO USE: - When you need lead details NOT available in the conversation (email, address, tags, lead source) - When the lead asks you to confirm their contact information - When you need CRM context about the lead's history or status  INPUT: No input needed. Automatically looks up the current lead.  OUTPUT: Full contact record with name, email, phone, tag…[TRUNCATED]

### `getNotes`

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`. Description chars: **512**.

> Fetch all notes recorded on this lead's GoHighLevel contact by agents or the AI system.  WHEN TO USE: - When the lead references a previous conversation or commitment ("someone told me...", "I was promised...") - When you need historical context about what has been discussed or agreed with this lead - Before escalating, to check if there are existing agent notes  INPUT: No input needed. Automatically looks up the current lead.  OUTPUT: List of notes with timestamps and content.  RULES: - Use to …[TRUNCATED]

### `KB Tool`

Type: `@n8n/n8n-nodes-langchain.toolVectorStore`. Description chars: **512**.

> =Search the approved company knowledge base for client location {{ (() => { try { return $('Set Outbound Context').first().json.location_id } catch(e) { return $('LeadDetails').first().json.location_id } })() }}.  WHEN TO USE: - When the lead asks about commission rates, fees, or pricing - When the lead asks about services offered, property types, or areas served - When the lead asks how the team operates or any company-specific question - ANY question about the business, team, or real estate se…[TRUNCATED]

### `rescheduleAppointment`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **10**.

> [REDACTED]

### `saveQualifyingAnswer`

Type: `n8n-nodes-base.supabaseTool`. Description chars: **512**.

> MANDATORY TOOL - Save a qualifying answer to the database after the lead answers one of the 3 qualifying questions.  WHEN TO USE: You MUST call this tool IMMEDIATELY every time the lead provides information that answers Q1, Q2, or Q3. Do NOT wait until all questions are answered. Save each answer the moment you receive it.  The tool updates the qualifying_answers JSONB column in conversation_context for this lead.  INPUT: You must provide a JSON object with the field 'qualifying_answers' contain…[TRUNCATED]

### `searchPastMessages`

Type: `n8n-nodes-base.supabaseTool`. Description chars: **512**.

> Search this lead's past message log beyond the 15 most recent messages already in your context.  WHEN TO USE: - Lead references something old ("I told you", "I mentioned before", "remember when", "weeks ago") - You need to verify a claim about a past conversation - You need to recall a commitment, date, or topic from earlier in the relationship  WHEN NOT TO USE: - For general knowledge or company info (use KB Tool) - For information already visible in RECENT MESSAGES (your 15-turn window)  INPUT…[TRUNCATED]

### `subscribeToNewsletter`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **512**.

> Subscribe the current lead to the weekly market newsletter. Updates leads.newsletter_opted_in = true, tags the contact in GHL, and clears pending flags.  INPUT (required JSON): - contact_id: string - the CONTACT_ID from the context header (always required)  CALL THIS TOOL when the lead signals they want market updates, want to stay in the loop, accept the newsletter offer, or agree to receive periodic info. Call it BEFORE you write your response acknowledging the subscription — never acknowledge…[TRUNCATED]

### `switchChannel`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **512**.

> Switch the lead's communication channel and send a hardcoded bridge message on the new channel. Call this ONLY when the lead explicitly asks to move to a different channel (e.g. "just email me", "text me instead").  SUPPORTED DESTINATIONS: sms, email. You CANNOT switch TO Instagram DM — only FROM it. If a lead asks to be contacted on Instagram, politely decline and offer SMS or email instead.  INPUT (required JSON): - contact_id: string — CONTACT_ID from context - new_channel: string — must be "…[TRUNCATED]

### `updateContactMemory`

Type: `@n8n/n8n-nodes-langchain.toolCode`. Description chars: **512**.

> Update the contact's memory and enrichment fields. Call this when you detect ANY of the signals below. Include ALL detected fields in a single call — never make multiple calls.  INPUT (required JSON): - contact_id: string - CONTACT_ID from context (always required) - Plus any fields below that you detected:  FIELD TRIGGERS — scan every message for these:  IDENTITY / CONTACT INFO - Lead says their name → first_name, last_name - Lead gives their email address → email - Lead gives their phone numbe…[TRUNCATED]

## Summary and Memory Related Nodes

| Node | Type | Text-like chars | Mentions `conversation_context` | Mentions `conversation_summary` |
|---|---|---:|---|---|
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | 149 | False | True |
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | 512 | False | False |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | 1030 | False | True |
| `Check Qualification Gate` | `n8n-nodes-base.supabase` | 0 | True | False |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | 518 | True | False |
| `Clear Newsletter Flags` | `n8n-nodes-base.supabase` | 0 | True | False |
| `Gather Prompt Data` | `n8n-nodes-base.set` | 0 | False | True |
| `Gather Sentiment Data1` | `n8n-nodes-base.set` | 0 | False | True |
| `Get Conversation Summary` | `n8n-nodes-base.supabase` | 0 | True | False |
| `Get Outbound Conversation Summary` | `n8n-nodes-base.supabase` | 0 | True | False |
| `Insert Conversation Context` | `n8n-nodes-base.supabase` | 0 | True | True |
| `Leak Detected?` | `n8n-nodes-base.if` | 0 | False | False |
| `Log AI Leak` | `n8n-nodes-base.supabase` | 0 | False | False |
| `Newsletter Offer Needed?` | `n8n-nodes-base.if` | 0 | False | False |
| `Notify Agent` | `n8n-nodes-base.code` | 512 | False | False |
| `Prepare Sentiment Context` | `n8n-nodes-base.code` | 512 | False | False |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | 518 | True | False |
| `Set Newsletter Pending` | `n8n-nodes-base.supabase` | 0 | True | False |
| `Sticky Note13` | `n8n-nodes-base.stickyNote` | 65 | False | False |
| `Sticky Note15` | `n8n-nodes-base.stickyNote` | 65 | False | False |
| `Summary Exists?` | `n8n-nodes-base.if` | 0 | False | False |
| `Update Conversation Context` | `n8n-nodes-base.supabase` | 0 | True | True |

## Prompt Surface Nodes

| Node | Type | Text-like chars | High-signal fields |
|---|---|---:|---|
| `Assemble System Prompt` | `n8n-nodes-base.code` | 10 | `jsCode` (10) |
| `Gather Prompt Data` | `n8n-nodes-base.set` | 0 |  |
| `Get Prompt Blocks (SMRT)` | `n8n-nodes-base.postgres` | 327 | `query` (327) |
| `Get Static Prompt Sections` | `n8n-nodes-base.supabase` | 0 |  |
| `Get Conversation Summary` | `n8n-nodes-base.supabase` | 0 |  |
| `Get Outbound Conversation Summary` | `n8n-nodes-base.supabase` | 0 |  |
| `Get Message History` | `n8n-nodes-base.postgres` | 272 | `query` (272) |
| `Get Outbound Message History` | `n8n-nodes-base.postgres` | 215 | `query` (215) |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | 1030 | `messages.values[0].content` (512)<br>`messages.values[0].role` (6)<br>`messages.values[1].content` (512) |
| `Update Conversation Context` | `n8n-nodes-base.supabase` | 0 |  |
| `Insert Conversation Context` | `n8n-nodes-base.supabase` | 0 |  |

