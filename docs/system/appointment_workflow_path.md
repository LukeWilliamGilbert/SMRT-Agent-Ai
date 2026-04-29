# Appointment Workflow Path Evidence

This file is generated from the raw n8n workflow export and focuses on nodes that mention appointments, booking, calendar, slots, or qualification. It is read-only evidence for the missing-appointment audit.

## 📬 Newsletter Dispatch (`XDcom3gft8yqwa5O`)

Active: **True**. Archived: **False**. Matched nodes: **2**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Fetch Eligible Leads` | `n8n-nodes-base.code` | main |
| `Build HTML Email` | `n8n-nodes-base.code` | main |

### Fetch Eligible Leads

Type: `n8n-nodes-base.code`. Node ID: `f2267155-04f4-4ec7-a62c-aa610c411638`.

```json
{
  "jsCode": "const newsletter = $input.first().json;\nconst locationId = newsletter.location_id;\nconst newsletterId = newsletter.id;\nconst agent = newsletter.agent;\n\n// Pass newsletter display fields forward so downstream code nodes don't need cross-node refs\nconst newsletterFields = {\n  newsletterFullContent: newsletter.full_content || '',\n  newsletterSubjectLine: newsletter.subject_line || 'Weekly Market Update',\n  newsletterImageUrl: newsletter.image_url || '',\n  newsletterWeekStartDate: newsletter.week_start_date || '',\n  newsletterLocationId: newsletter.location_id,\n};\n\nconst supabaseUrl = newsletter.agent._sbUrl;\nconst supabaseKey = newsletter.agent._sbKey;\n\nconst leadsResp = await globalThis.fetch(\n  `${supabaseUrl}/rest/v1/leads?newsletter_opted_in=eq.true&location_id=eq.${locationId}&status=neq.opted_out&select=id,contact_id,first_name,last_name,email,pipeline_stage,location_id`,\n  { headers: { 'apikey': supabaseKey, 'Authorization': `Bearer ${supabaseKey}` } }\n);\nconst leads = await leadsResp.json();\n\nif (!leads || leads.length === 0) {\n  return [{ json: { _skip: true, reason: 'no_opted_in_leads' } }];\n}\n\nconst leadIds = leads.map(l => l.id);\nconst deliveriesResp = await globalThis.fetch(\n  `${supabaseUrl}/rest/v1/newsletter_deliveries?lead_id=in.(${leadIds.join(',')})&status=eq.sent&order=sent_at.desc&select=lead_id,sent_at`,\n  { headers: { 'apikey': supabaseKey, 'Authorization': `Bearer ${supabaseKey}` } }\n);\nconst deliveries = await deliveriesResp.json();\n\nconst lastSentMap = {};\nfor (const d of (deliveries || [])) {\n  if (!lastSentMap[d.lead_id]) {\n    lastSentMap[d.lead_id] = d.sent_at;\n  }\n}\n\nconst now = new Date();\nconst dayMs = 24 * 60 * 60 * 1000;\nconst cadenceMap = { 'WEEKLY': 6, 'BIWEEKLY': 13, 'MONTHLY': 27 };\n\nconst eligible = [];\nfor (const lead of leads) {\n  const stage = lead.pipeline_stage || 'MONTHLY';\n  let cadence = 'MONTHLY';\n  if (stage === 'WEEKLY' || stage === 'APPT_BOOKED' || stage === 'APPT_OFFERED') cadence = 'WEEKLY';\n  else if (stage === 'BIWEEKLY') cadence = 'BIWEEKLY';\n\n  const minDays = cadenceMap[cadence] || 27;\n  const lastSent = lastSentMap[lead.id];\n\n  if (!lastSent) {\n    eligible.push(lead);\n  } else {\n    const daysSince = (now - new Date(lastSent)) / dayMs;\n    if (daysSince >= minDays) {\n      eligible.push(lead);\n    }\n  }\n}\n\nif (eligible.len
...[truncated]
```

### Build HTML Email

Type: `n8n-nodes-base.code`. Node ID: `2cfda966-caad-43ae-9ed1-1c504a1c632d`.

```json
{
  "jsCode": "// All data comes from $input — newsletter fields were forwarded by Fetch Eligible Leads\nconst lead = $input.first().json;\nconst agentName = lead.agentName || 'Luke Gilbert';\nconst businessName = lead.businessName || 'Open House Boise';\nconst firstName = lead.firstName || '';\nconst calendarLink = lead.calendarLink || 'https://openhouseboise.net';\n\nconst content = lead.newsletterFullContent || '';\nconst subject = lead.newsletterSubjectLine || 'Weekly Market Update';\nconst imageUrl = lead.newsletterImageUrl || '';\nconst smrtLogo = 'https://kfoijgcbkjeizxxyiwxv.supabase.co/storage/v1/object/public/newsletter-images/branding/smrt-logo.jpeg';\n\n// Build week label from newsletter date\nconst weekDate = new Date(lead.newsletterWeekStartDate);\nconst monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];\nconst weekNum = Math.ceil(weekDate.getDate() / 7);\nconst titleLine = `${monthNames[weekDate.getMonth()].toUpperCase()} | WEEK ${weekNum} | ${(lead.marketName || 'ADA COUNTY').toUpperCase()} HOUSING MARKET`;\n\n// Convert markdown-style content to HTML sections\n// Colors matched to SMRT funnel landing page:\n// background: #f9f7f4 | foreground: #2c3039 | primary: #bb6e4d\n// card: #f5f2ef | muted-foreground: #757c89 | border: #e4e1db\nconst formatContent = (text) => {\n  const lines = text.split('\\n');\n  let html = '';\n  for (const line of lines) {\n    const trimmed = line.trim();\n    if (!trimmed) {\n      html += '<br>';\n    } else if (trimmed.startsWith('### ')) {\n      html += `<h3 style=\"color: #2c3039; font-family: 'DM Serif Display', Georgia, serif; font-size: 18px; font-weight: 400; margin: 28px 0 10px 0; padding-bottom: 8px; border-bottom: 2px solid #bb6e4d; letter-spacing: -0.02em;\">${trimmed.replace('### ', '')}</h3>`;\n    } else if (trimmed.startsWith('## ')) {\n      html += `<h2 style=\"color: #2c3039; font-family: 'DM Serif Display', Georgia, serif; font-size: 22px; font-weight: 400; margin: 28px 0 10px 0; letter-spacing: -0.02em;\">${trimmed.replace('## ', '')}</h2>`;\n    } else if (trimmed.startsWith('- ')) {\n      html += `<p style=\"margin: 4px 0 4px 16px; color: #757c89; line-height: 1.75; font-weight: 300;\">&#8226; ${trimmed.replace('- ', '')}</p>`;\n    } else {\n      html += `<p style=\"margin: 8px 0; color: #757c89; line-height: 1
...[truncated]
```

## 📰 Data Source & Newsletter Creation (`gI097yamrw7gDU6C`)

Active: **True**. Archived: **False**. Matched nodes: **1**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Prepare Agent Data` | `n8n-nodes-base.code` | main |

### Prepare Agent Data

Type: `n8n-nodes-base.code`. Node ID: `ef046ace-6949-4bf0-958e-a16a74378c94`.

```json
{
  "jsCode": "const agent = $input.first().json;\nconst zips = agent.target_zips || [];\nconst pai = agent.altos_pai || '690acaf9';\nconst existingHashes = agent.altos_location_hashes || {};\n\nconst stateAbbreviations = {\n  'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR', 'california': 'CA',\n  'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'district of columbia': 'DC',\n  'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL',\n  'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA',\n  'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN',\n  'mississippi': 'MS', 'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',\n  'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',\n  'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK', 'oregon': 'OR',\n  'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC', 'south dakota': 'SD',\n  'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT', 'virginia': 'VA',\n  'washington': 'WA', 'west virginia': 'WV', 'wisconsin': 'WI', 'wyoming': 'WY'\n};\n\nlet stateRaw = (agent.state || '').trim();\nlet state = stateRaw.toUpperCase();\nif (state.length !== 2) {\n  state = stateAbbreviations[stateRaw.toLowerCase()] || stateRaw;\n}\n\nconst today = new Date();\nconst dayOfWeek = today.getDay();\nconst monday = new Date(today);\nmonday.setDate(today.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));\nconst weekStartDate = monday.toISOString().split('T')[0];\n\nreturn {\n  json: {\n    agent,\n    agent_id: (agent.id || '').toString().trim(),\n    location_id: (agent.location_id || '').toString().trim(),\n    ghl_api_key: (agent.ghl_api_key || '').toString().trim(),\n    calendar_id: (agent.calendar_id || '').toString().trim(),\n    market_name: agent.market_name || 'Local Market',\n    target_zips: zips,\n    state: state,\n    city: (agent.city || '').trim(),\n    zip: (zips[0] || '').trim(),\n    pai,\n    county_fips: agent.county_fips || '16001',\n    existingHashes,\n    weekStartDate\n  }\n};\n"
}
```

## 🎉 Onboarding — Part 1: DB Enrichment (`XJxoDt1SJ6SWUIim`)

Active: **False**. Archived: **False**. Matched nodes: **3**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Note: Onboarding Call Checklist` | `n8n-nodes-base.stickyNote` | none |
| `Extract Agent Data` | `n8n-nodes-base.set` | main |
| `Save to onboarding_requests` | `n8n-nodes-base.postgres` | main |

### Note: Onboarding Call Checklist

Type: `n8n-nodes-base.stickyNote`. Node ID: `def03a43-2b68-41eb-84eb-9d27bd08e55d`.

```json
{
  "content": "## Onboarding Call Checklist\nCollect all of the following before or during the onboarding call.\n\n### Agent Info\n- Full name\n- Business name\n- Email address\n- Phone number\n- Timezone\n- City and state\n- Target ZIP codes (service area)\n\n### GHL Sub-Account\n- Sub-account Location ID\n  (Agency -> Locations -> click location -> Settings -> grab ID from URL)\n- Buyer calendar ID\n  (GHL -> Calendars -> click calendar -> grab ID from URL)\n- Seller calendar ID\n- GHL user ID\n  (GHL -> Settings -> My Profile -> copy User ID)\n\n### Market Info\n- Market name (e.g. Ada County, Idaho)\n- Market area description\n- Lead sources they use (Zillow, Realtor.com, referrals etc.)\n- Specialties (buyer, seller, investor, luxury etc.)\n\n### AI Setup\n- Personality preferences (casual, professional, warm etc.)\n- Any custom rules or things the AI must never say\n- Knowledge base documents to upload (FAQ, listings, bio)",
  "height": 776,
  "width": 532,
  "color": 5
}
```

### Extract Agent Data

Type: `n8n-nodes-base.set`. Node ID: `93994faa-74cc-4ced-87e7-0f17d51b28ba`.

```json
{
  "assignments": {
    "assignments": [
      {
        "name": "agent_name",
        "value": "={{ $json.body.agent_name }}",
        "type": "string"
      },
      {
        "name": "agent_email",
        "value": "={{ $json.body.agent_email }}",
        "type": "string"
      },
      {
        "name": "agent_phone",
        "value": "={{ $json.body.agent_phone }}",
        "type": "string"
      },
      {
        "name": "business_name",
        "value": "={{ $json.body.business_name }}",
        "type": "string"
      },
      {
        "name": "market_area",
        "value": "={{ $json.body.market_area }}",
        "type": "string"
      },
      {
        "name": "brand_voice",
        "value": "={{ $json.body.brand_voice }}",
        "type": "string"
      },
      {
        "name": "calendar_link",
        "value": "={{ $json.body.calendar_link }}",
        "type": "string"
      },
      {
        "name": "openai_api_key",
        "value": "={{ $json.body.openai_api_key }}",
        "type": "string"
      },
      {
        "name": "personality_tone",
        "value": "={{ $json.body.personality_tone }}",
        "type": "string"
      },
      {
        "name": "personality_style",
        "value": "={{ $json.body.personality_style }}",
        "type": "string"
      },
      {
        "name": "personality_communication",
        "value": "={{ $json.body.personality_communication }}",
        "type": "string"
      },
      {
        "name": "knowledge_files",
        "value": "={{ $json.body.knowledge_files }}",
        "type": "array"
      }
    ]
  },
  "options": {}
}
```

### Save to onboarding_requests

Type: `n8n-nodes-base.postgres`. Node ID: `save-to-staging`.

```json
{
  "operation": "executeQuery",
  "query": "=INSERT INTO onboarding_requests (\n  agent_name, agent_email, agent_phone, business_name,\n  market_area, brand_voice, calendar_link, openai_api_key,\n  personality_prompt,\n  knowledge_base_folder_id, knowledge_base_folder_name,\n  faq_doc_id, faq_doc_url,\n  status\n) VALUES (\n  '{{ $('Extract Agent Data').first().json.agent_name.replace(/'/g, \"''\") }}',\n  '{{ $('Extract Agent Data').first().json.agent_email.replace(/'/g, \"''\") }}',\n  '{{ $('Extract Agent Data').first().json.agent_phone }}',\n  '{{ $('Extract Agent Data').first().json.business_name.replace(/'/g, \"''\") }}',\n  '{{ $('Extract Agent Data').first().json.market_area.replace(/'/g, \"''\") }}',\n  '{{ ($('Extract Agent Data').first().json.brand_voice || '').replace(/'/g, \"''\") }}',\n  '{{ ($('Extract Agent Data').first().json.calendar_link || '').replace(/'/g, \"''\") }}',\n  '{{ $('Extract Agent Data').first().json.openai_api_key }}',\n  '{{ ($('Set Default Personality').first().json.personality_prompt || '').replace(/'/g, \"''\") }}',\n  '{{ $('Set Folder ID').first().json.knowledge_base_folder_id }}',\n  '{{ ($('Set Folder ID').first().json.knowledge_base_folder_name || '').replace(/'/g, \"''\") }}',\n  '',\n  '',\n  'pending_ghl'\n)\nRETURNING id;",
  "options": {}
}
```

## 🧠 SMRT Brain Engine (`mlR5dZuzXxP_JYGaqrqpu`)

Active: **True**. Archived: **False**. Matched nodes: **28**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Assemble System Prompt` | `n8n-nodes-base.code` | main |
| `AI Sentiment Analysis` | `@n8n/n8n-nodes-langchain.anthropic` | main |
| `Parse Sentiment` | `n8n-nodes-base.code` | main |
| `Analyze Conversation` | `@n8n/n8n-nodes-langchain.openAi` | main |
| `Update Conversation Context` | `n8n-nodes-base.supabase` | main |
| `Route by Channel1` | `n8n-nodes-base.switch` | main |
| `Prepare Tier Response` | `n8n-nodes-base.code` | main |
| `Route Intent` | `n8n-nodes-base.switch` | main |
| `Extract Keywords` | `n8n-nodes-base.code` | main |
| `searchPastMessages` | `n8n-nodes-base.supabaseTool` | ai_tool |
| `getAppointments` | `@n8n/n8n-nodes-langchain.toolHttpRequest` | ai_tool |
| `deleteAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `bookAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `getAvailableSlots` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `Insert Conversation Context` | `n8n-nodes-base.supabase` | main |
| `Is Qualified?` | `n8n-nodes-base.if` | main |
| `addAppointmentNotes` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `Form Section4` | `n8n-nodes-base.stickyNote` | none |
| `Fetch Slots` | `n8n-nodes-base.code` | main |
| `checkQualificationStatus` | `n8n-nodes-base.supabaseTool` | ai_tool |
| `saveQualifyingAnswer` | `n8n-nodes-base.supabaseTool` | ai_tool |
| `Check Qualification Gate` | `n8n-nodes-base.supabase` | main |
| `rescheduleAppointment` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `Evaluate Pipeline Stage` | `n8n-nodes-base.code` | main |
| `updateContactMemory` | `@n8n/n8n-nodes-langchain.toolCode` | ai_tool |
| `Newsletter Offer Needed?` | `n8n-nodes-base.if` | main |
| `Silence Gate` | `n8n-nodes-base.code` | main |
| `Gather Prompt Data` | `n8n-nodes-base.set` | main |

### Assemble System Prompt

Type: `n8n-nodes-base.code`. Node ID: `faa9ffb0-6a03-4e05-9663-1cc750ab4f85`.

```json
{
  "jsCode": "const NL = String.fromCharCode(10);\nconst NL2 = NL + NL;\n\nconst allItems = $input.all();\nconst d = allItems[0].json;\nconst staticSections = allItems.map(i => i.json).filter(i => i.section_key && i.content);\n\nconst agentName = d.agentName || 'the agent';\nconst coordinatorName = d.coordinatorName || 'Jon';\nconst marketName = d.marketName || '';\nconst timezone = d.timezone || 'America/Denver';\nconst direction = d.direction || 'inbound';\nconst channel = d.channel || 'sms';\nconst firstName = d.firstName || 'Contact';\nconst contactId = d.contactId || '';\nconst locationId = d.locationId || '';\nconst pipelineStage = d.pipelineStage || 'MONTHLY';\nconst intentLevel = d.intentLevel || 'none';\nconst tier = d.tier || 'standard';\nconst isTieredResponse = tier !== 'standard' && tier !== 'normal';\nconst leadTemp = d.leadTemp || 'warm';\nconst leadIntent = d.leadIntent || 'unknown';\nconst splinterContent = d.splinterContent || '';\nconst splinterTopic = d.splinterTopic || '';\nconst splinterDataPoint = d.splinterDataPoint || '';\nconst newsletterPending = d.newsletterPending === true || d.newsletterPending === 'true';\nconst newsletterOptedIn = d.newsletterOptedIn === true || d.newsletterOptedIn === 'true';\nconst newsletterDeclined = d.newsletterDeclined === true || d.newsletterDeclined === 'true';\n\n// Pull website + funnel + active toggles from agent config (handles inbound + outbound paths)\nconst getAgentField = (field) => {\n  try { const v = $('Get Agent Config').first().json[field]; if (v !== undefined && v !== null) return v; } catch(e) {}\n  try { const v = $('Get Outbound Agent Config').first().json[field]; if (v !== undefined && v !== null) return v; } catch(e) {}\n  return undefined;\n};\nconst rawWebsite = (getAgentField('agent_website') || '').toString().trim();\nconst rawFunnel = (getAgentField('agent_funnel_url') || '').toString().trim();\nconst websiteActiveRaw = getAgentField('agent_website_active');\nconst funnelActiveRaw = getAgentField('agent_funnel_active');\nconst websiteActive = websiteActiveRaw === false || websiteActiveRaw === 'false' ? false : true;\nconst funnelActive = funnelActiveRaw === false || funnelActiveRaw === 'false' ? false : true;\nconst shareableFunnel = (funnelActive && rawFunnel) ? rawFunnel : '';\nconst shareableWebsite = (websiteActive && rawWebsite) ? rawWebsite : '';\n\nconst memFields = [\n 
...[truncated]
```

### AI Sentiment Analysis

Type: `@n8n/n8n-nodes-langchain.anthropic`. Node ID: `6aefff39-5ec7-4b37-9e76-918072c9daf3`.

```json
{
  "modelId": {
    "__rl": true,
    "value": "claude-haiku-4-5-20251001",
    "mode": "id"
  },
  "messages": {
    "values": [
      {
        "content": "=CONVERSATION CONTEXT (read first — context frames the current message):\n\nConversation Summary: {{ $json.conversationSummary }}\n\nRecent Messages (newest last):\n{{ $json.historyText }}\n\nLead State:\n- First Name: {{ $json.firstName }}\n- Agent: {{ $json.agentName }}\n- Pipeline Stage: {{ $json.pipelineStage }}\n- Pipeline State: {{ $json.pipelineState }}\n\n=== CURRENT MESSAGE (classify using STEP 1 → 4 from system prompt) ===\n{{ $json.currentMessage }}\n\nReturn ONLY valid JSON. No markdown fences. No extra text."
      }
    ]
  },
  "options": {
    "system": "You are a sentiment classifier for SMRT Bot. You analyze inbound messages and classify them into behavioral tiers to route the Brain Engine correctly.\n\nCRITICAL: Your reasoning field is used INTERNALLY by downstream nodes ONLY. It is NEVER shown to the lead. The Brain Engine AI Agent uses its own prompt to write the actual SMS/email reply. Be thorough in your reasoning - it helps downstream routing, it never leaks to the customer.\n\n=== CLASSIFICATION PRIORITY ORDER ===\n\nFollow these steps IN ORDER. First matching step wins.\n\n=== STEP 1 - HARD STOP OVERRIDE (with scope + abuse checks) ===\n\n(1) Scan the CURRENT MESSAGE for explicit removal verbs:\n- \"stop\", \"stop texting\", \"stop messaging\", \"stop contacting\"\n- \"unsubscribe\"\n- \"remove me\", \"remove from list\", \"take me off\", \"take off list\"\n- \"opt out\", \"opt me out\"\n- \"do not contact\", \"don't contact\"\n- \"delete me\", \"erase me\"\n- \"cease\", \"cease communication\"\n\nIF no removal verb found -> skip to STEP 2.\n\n(1.5) CONDITIONAL/HYPOTHETICAL CHECK (only runs if a removal verb WAS found):\n\nIf the removal verb sits inside a CONDITIONAL or HYPOTHETICAL clause, the lead is NOT requesting opt-out right now - they are granting future permission or describing a contingent state. Treat as context-dependent and defer to STEP 4. Do NOT fire opt-out at STEP 1.\n\nConditional / hypothetical markers (the removal verb sits inside one of these clauses):\n- \"if [I don't / I'm not / it doesn't / this isn't / etc]\" - explicit conditional\n- \"you can [remove / take off / unsubscribe]\" - granting future permission, not requesting now\n- \"feel free to [remov
...[truncated]
```

### Parse Sentiment

Type: `n8n-nodes-base.code`. Node ID: `d841fa41-fc17-4017-9e0c-b2bc993e8be0`.

```json
{
  "jsCode": "const input = $json;\n\nlet parsed;\ntry {\n  let text = '';\n  if (input.content && Array.isArray(input.content)) {\n    text = input.content.map(c => c.text || '').join('');\n  } else if (input.message && input.message.content) {\n    text = input.message.content;\n  } else if (input.text) {\n    text = input.text;\n  } else if (typeof input === 'string') {\n    text = input;\n  } else {\n    text = JSON.stringify(input);\n  }\n  \n  const fenceMatch = text.match(/\\`\\`\\`(?:json)?\\n?([\\s\\S]*?)\\`\\`\\`/);\n  if (fenceMatch) {\n    text = fenceMatch[1].trim();\n  }\n  \n  const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);\n  if (jsonMatch) {\n    parsed = JSON.parse(jsonMatch[0]);\n  } else {\n    throw new Error('No JSON found in response');\n  }\n} catch (e) {\n  parsed = {\n    sentiment: 'neutral',\n    tier: 'normal',\n    signal_type: 'none',\n    confidence: 'low',\n    action: 'continue',\n    sms_action: 'none',\n    pipeline_update: 'no_change',\n    message_intent: 'Parse error: ' + e.message,\n    reason: 'Failed to parse AI response - defaulting to normal tier',\n    should_suppress: false,\n    suppress_reason: 'none',\n    block_level: null\n  };\n}\n\nlet tier = parsed.tier || 'normal';\nif (!parsed.tier && parsed.action) {\n  if (parsed.action === 'opt_out_immediately') tier = 'tier_3_optout';\n  else if (parsed.action === 'flag_review') tier = 'tier_2_hostile';\n  else if (parsed.action === 'human_escalation') tier = 'emotional';\n  else if (parsed.action === 'ignore') tier = 'normal';\n  else if (parsed.action === 'booking') tier = 'booking';\n}\n\nconst validActions = ['opt_out', 'flag_review', 'ignore', 'human_escalation', 'continue', 'booking'];\n\n// PRIORITY 1: trust AI's action if it's one of the 6 valid values\nlet action = validActions.includes(parsed.action) ? parsed.action : null;\n\n// PRIORITY 2: fallback — derive from tier when AI did not provide a valid action\nif (!action) {\n  if (tier === 'tier_3_optout') action = 'opt_out';\n  else if (tier === 'tier_2_hostile') action = 'flag_review';\n  else if (tier === 'spam') action = 'ignore';\n  else if (tier === 'emotional') action = 'human_escalation';\n  else if (tier === 'booking') action = 'booking';\n  else action = 'continue'; // normal, tier_1_confused, declined_meeting, turnaround\n}\n\n// SAFETY: final guardrail — only the 6 valid values pass\nif (!vali
...[truncated]
```

### Analyze Conversation

Type: `@n8n/n8n-nodes-langchain.openAi`. Node ID: `62189b40-4e6d-45de-9583-6c9daf9af7eb`.

```json
{
  "modelId": {
    "__rl": true,
    "mode": "list",
    "value": "gpt-4o-mini"
  },
  "messages": {
    "values": [
      {
        "content": "You analyze real estate AI conversation exchanges and extract structured signals.\n\nReturn ONLY a valid JSON object (no markdown, no explanation):\n{\n  \"summary\": \"250-350 word accumulative summary\",\n  \"lead_intent\": \"buy|sell|both|unknown\",\n  \"lead_timeline\": \"now|3_months|6_months|1_year|unknown\",\n  \"appointment_discussed\": true or false,\n  \"appointment_outcome\": \"offered|accepted|rejected|rescheduled|null\",\n  \"newsletter_discussed\": true or false,\n  \"newsletter_declined\": true or false,\n  \"newsletter_offer_needed\": true or false,\n  \"internal_reasoning_leak_detected\": true or false,\n  \"leak_phrase\": \"exact forbidden phrase found in SMRT output\" or null\n}\n\nRULES FOR summary (CRITICAL — accumulative, not overwrite):\n- Write 250-350 words.\n- PRESERVE every concrete fact from the Previous Summary: names, dates, commitments, pivots, property addresses, budgets, timelines, topics discussed, scheduling history, outcomes.\n- Layer in what this turn ADDED or CHANGED. Do NOT drop any prior fact unless the lead explicitly retracted it.\n- If the lead pivoted (e.g., buyer -> seller, Meridian -> Eagle, 3-month -> 6-month, sell -> keep as rental), PRESERVE the pivot history: \"Originally expressed X, pivoted to Y on [date or relative time].\"\n- Focus on CUSTOMER statements and commitments. SMRT responses matter only when they contain commitments (e.g., times offered, appointments booked, data shared).\n- Continuous narrative prose. No bullets, no JSON, no meta-commentary.\n- If the Previous Summary is 'None' or empty, build from scratch using the Recent Conversation + Latest Exchange.\n\nRULES FOR lead_intent:\n- \"buy\" = mentions looking for home, searching, wants to purchase\n- \"sell\" = mentions selling, listing, moving out\n- \"both\" = mentions both\n- \"unknown\" = no clear intent\n\nRULES FOR lead_timeline:\n- \"now\" = ready immediately, ASAP, this month\n- \"3_months\" = next few months, soon\n- \"6_months\" = later this year\n- \"1_year\" = next year, eventually\n- \"unknown\" = no timeline mentioned\n\nRULES FOR appointment_discussed:\n- true ONLY when this exchange involved appointment, booking, scheduling, calendar, consultation, meeting, or call talk\n- false if a
...[truncated]
```

### Update Conversation Context

Type: `n8n-nodes-base.supabase`. Node ID: `6e6be3cb-3055-4579-a496-7bef75d2528f`.

```json
{
  "operation": "update",
  "tableId": "conversation_context",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "condition": "eq",
        "keyValue": "={{ $('Assemble System Prompt').first().json.contactId }}"
      }
    ]
  },
  "fieldsUi": {
    "fieldValues": [
      {
        "fieldId": "conversation_summary",
        "fieldValue": "={{ (() => {  const turnCounter = (() => {   try { return parseInt($('searchLeads').first().json.turn_counter) || 0 }   catch(e) {    try { return parseInt($('Get Lead Memory').first().json.turn_counter) || 0 }    catch(e2) {     try { return parseInt($('Get Outbound Lead Memory').first().json.turn_counter) || 0 }     catch(e3) { return 0 }    }   }  })();  const shouldRegen = (turnCounter <= 2 || turnCounter % 10 === 0);  if (shouldRegen) {   try {    const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}';    const parsed = JSON.parse(content);    return parsed.summary || content;   } catch(e) {    return $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '';   }  } else {   try { return $('Get Outbound Conversation Summary').first().json.conversation_summary || '' }   catch(e) { try { return $('Get Conversation Summary').first().json.conversation_summary || '' } catch(e2) { return '' } }  } })() }}"
      },
      {
        "fieldId": "last_intent",
        "fieldValue": "={{ (() => { try { return $('Parse Sentiment').first().json.sentiment_analysis ? $('Parse Sentiment').first().json.sentiment_analysis.action : 'continue'; } catch(e) { return 'continue'; } })() }}"
      },
      {
        "fieldId": "updated_at",
        "fieldValue": "={{ new Date().toISOString() }}"
      },
      {
        "fieldId": "lead_intent",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}"
      },
      {
        "fieldId": "lead_timeline",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); retur
...[truncated]
```

### Route by Channel1

Type: `n8n-nodes-base.switch`. Node ID: `6a17903b-236d-43a5-bd25-ecfe9b2624d5`.

```json
{
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-sms",
              "leftValue": "=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}",
              "rightValue": "SMS",
              "operator": {
                "type": "string",
                "operation": "contains"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "SMS"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-email",
              "leftValue": "=={{ (() => { const ctx = $('Assemble System Prompt').first().json; if (ctx.direction === 'inbound') return ctx.channel || 'sms'; try { const pref = $('Get Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} try { const pref = $('Get Outbound Lead Memory').first().json.contact_preference; if (pref && pref !== 'unknown') return pref; } catch(e) {} return ctx.channel || 'sms'; })() }}",
              "rightValue": "Email",
              "operator": {
                "type": "string",
                "operation": "contains"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Email"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "id": "route-fb",
              "leftValue": "=={{ (() 
...[truncated]
```

### Prepare Tier Response

Type: `n8n-nodes-base.code`. Node ID: `af67488b-cca7-4808-8793-d280bab7a370`.

```json
{
  "mode": "runOnceForEachItem",
  "jsCode": "// Prepare tier-specific response instructions for the AI Agent\n// Pull tier/sentiment/sms_action from Parse Sentiment directly — input $json may be from Apply L1: Mark Lead (no tier)\nconst ps = (() => { try { return $('Parse Sentiment').first().json; } catch(e) { return {}; } })();\nconst tier = ps.tier || $json.tier || 'normal';\nconst sentiment = ps.sentiment || $json.sentiment || 'neutral';\nconst smsAction = ps.sms_action || $json.sms_action || 'none';\n\nconst tierInstructions = {\n  tier_1_confused: {\n    instruction: `TIER 1 RESPONSE - CONFUSED/ANNOYED\\nThe lead is confused or annoyed but has NOT opted out.\\n\\nYour response MUST:\\n- De-escalate the situation\\n- Clarify who you are: \"I'm part of Luke's team and sent an email earlier this week introducing myself.\"\\n- Clarify your role: \"My role is to help coordinate communication so everyone we work with gets the attention they deserve.\"\\n- STOP after clarifying - no question, no business ask\\n\\nExample: \"Totally fair... I should clarify. I'm part of Luke's team and sent an email earlier this week introducing myself. My role is to help coordinate communication so everyone we work with gets the attention they deserve.\"\\n\\nDO NOT: Ask questions, make business asks, apologize excessively, push appointments`,\n    suppressSMS: false,\n    pauseDays: 0\n  },\n  tier_2_hostile: {\n    instruction: `TIER 2 RESPONSE - HOSTILE (NO EXPLICIT STOP)\\nThe lead is hostile but has NOT explicitly opted out.\\n\\nYour response MUST be brief and respectful. Example: \"Understood, no worries at all.\" or \"Got it, I'll stop reaching out for now.\"\\n\\nDO NOT: Apologize, explain, offer removal, ask questions, defend the company, pivot to newsletter.`,\n    suppressSMS: false,\n    pauseDays: 30\n  },\n  tier_3_optout: {\n    instruction: `TIER 3 RESPONSE - EXPLICIT OPT-OUT\\nThe lead has explicitly requested to stop contact.\\n\\nYour response MUST be a brief respectful farewell. Example: \"Got it, I'll stop reaching out. Wishing you the best.\" or \"Understood. Take care.\"\\n\\nDO NOT: Persuade, defend, offer alternatives, reopen conversation, ask if they want anything else, apologize, mention the newsletter.`,\n    suppressSMS: true,\n    pauseDays: -1\n  },\n  emotional: {\n    instruction: `EMOTIONAL RESPONSE - SENSITIVE SITUATION\\nThe lead has shar
...[truncated]
```

### Route Intent

Type: `n8n-nodes-base.switch`. Node ID: `6859a1a7-02b8-465d-bded-83cd0918f0c9`.

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
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Ignored"
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
              "id": "route-emotional",
              "leftValue": "={{ $json.action }}",
              "rightValue": "human_escalation",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ]
...[truncated]
```

### Extract Keywords

Type: `n8n-nodes-base.code`. Node ID: `4fb1f71a-8f9c-4a24-af55-582b12fceac8`.

```json
{
  "jsCode": "const input = $input.first().json;\nconst currentMessage = (input.message || input.message_body || '').toLowerCase();\n\nconst keywordPatterns = {\n  pricing: /\\b(price|pricing|cost|fee|rate|charge|dollar|\\$|expensive|cheap|afford)\\b/i,\n  property: /\\b(house|home|property|apartment|condo|bedroom|bath|sqft|square|lot)\\b/i,\n  location: /\\b(address|where|location|area|neighborhood|city|street|zip)\\b/i,\n  availability: /\\b(available|availability|vacancy|vacant|ready|move.?in|when|schedule|showing)\\b/i,\n  application: /\\b(apply|application|approve|qualify|credit|income|lease|rent)\\b/i,\n  maintenance: /\\b(repair|fix|broken|leak|maintenance|issue|problem|work.?order)\\b/i\n};\n\nconst foundKeywords = [];\nfor (const [category, pattern] of Object.entries(keywordPatterns)) {\n  if (pattern.test(currentMessage)) {\n    foundKeywords.push(category);\n  }\n}\n\nreturn [{\n  json: {\n    ...input,\n    keywords: foundKeywords,\n    has_keywords: foundKeywords.length > 0,\n    keyword_count: foundKeywords.length\n  }\n}];"
}
```

### searchPastMessages

Type: `n8n-nodes-base.supabaseTool`. Node ID: `c17eed39-5b2a-445d-a4d1-38516ff7cd15`.

```json
{
  "descriptionType": "manual",
  "toolDescription": "Search this lead's past message log beyond the 15 most recent messages already in your context.\n\nWHEN TO USE:\n- Lead references something old (\"I told you\", \"I mentioned before\", \"remember when\", \"weeks ago\")\n- You need to verify a claim about a past conversation\n- You need to recall a commitment, date, or topic from earlier in the relationship\n\nWHEN NOT TO USE:\n- For general knowledge or company info (use KB Tool)\n- For information already visible in RECENT MESSAGES (your 15-turn window)\n\nINPUT: No input needed. The tool is pre-scoped to the current lead's contact_id.\n\nOUTPUT: Returns up to 20 most recent messages for this lead, ordered newest first. Each row has:\n- timestamp: when the message was sent\n- message_body: the actual message text\n- channel: which channel it came through\n- direction: 'inbound' (from lead) or 'outbound' (from you)\nIgnore other columns (id, location_id, ai_processed, etc) - use only the four above.\n\nANTI-HALLUCINATION RULE (CRITICAL):\n- If this tool returns ZERO rows, that means nothing was found. You MUST respond with uncertainty. Tell the lead you don't have that on record and offer to flag it for Luke Gilbert.\n- NEVER fabricate dates, bookings, commitments, or specifics when the tool returns empty.\n- NEVER say phrases like \"I found\", \"I did find\", \"based on my records\", \"in my system\", \"on my end\", \"conversation history\", \"contact memory\", \"on file\". These are forbidden.\n- If you cite information to the lead, it must come from this tool's output in THIS turn, or from the CONTACT MEMORY / RECENT MESSAGES block in your system prompt.\n- Attribute recalled info to \"from what you told me before\" or \"what we discussed earlier\" - never describe internal storage.",
  "operation": "getAll",
  "tableId": "message_log",
  "limit": 20,
  "matchType": "allFilters",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "condition": "eq",
        "keyValue": "={{ $('Assemble System Prompt').first().json.contactId }}"
      }
    ]
  }
}
```

### getAppointments

Type: `@n8n/n8n-nodes-langchain.toolHttpRequest`. Node ID: `aee7ae79-59ec-41c0-92c0-5eccf7a95add`.

```json
{
  "toolDescription": "Fetch all appointments (past and upcoming) for the current lead from GoHighLevel.\n\nWHEN TO USE:\n- When the lead asks about existing appointments (\"when is my appointment?\", \"do I have anything scheduled?\")\n- When the lead wants to cancel or reschedule (you need the event_id from here)\n- When you need to check if the lead already has a booking before offering to schedule\n\nINPUT: No input needed. Automatically looks up the current lead.\n\nOUTPUT: List of appointment objects with event IDs, dates, times, and statuses.\n\nRULES:\n- You MUST call this before deleteAppointment to get the correct event_id\n- Present appointment info in a readable format\n- If no appointments found, let the lead know they have nothing scheduled",
  "url": "=https://services.leadconnectorhq.com/contacts/{{ (() => { try { return $('Assemble System Prompt').first().json.contactId } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}/appointments",
  "sendHeaders": true,
  "parametersHeaders": {
    "values": [
      {
        "name": "Authorization",
        "valueProvider": "fieldValue",
        "value": "=Bearer {{ (() => { try { return $('Get Outbound Agent Config').first().json.ghl_api_key } catch(e) { return $('Get Agent Config').first().json.ghl_api_key } })() }}"
      },
      {
        "name": "Version",
        "valueProvider": "fieldValue",
        "value": "2021-07-28"
      }
    ]
  }
}
```

### deleteAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `41ab183f-4a4c-46eb-a9ae-dbc07301866c`.

```json
{
  "name": "deleteAppointment",
  "description": "Cancel an existing appointment.\n\nINPUT (required JSON):\n- event_id: string - from getAppointments\n- ghl_api_key: string - from system context\n\nCall getAppointments first to get the event_id.",
  "jsCode": "let input = {};\nif (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {event_id:query}; } } else if (typeof query === 'object' && query !== null) { input = query; }\nconst ctx = $('Assemble System Prompt').first().json;\nconst apiKey = ctx.ghlApiKey;\nconst calendarId = ctx.calendarId;\nconst ghlUserId = ctx.ghlUserId;\nconst locationId = ctx.locationId;\nconst contactId = ctx.contactId || input.contact_id;\nconst firstName = ctx.firstName || input.first_name || 'Lead';\nconst channel = ctx.channel || input.channel || 'sms';\nconst eventId = input.event_id;\nif (!eventId || !apiKey) return 'Error: event_id required and GHL credentials not configured.';\ntry {\n  const r = await fetch('https://services.leadconnectorhq.com/calendars/events/'+eventId, {method:'DELETE',headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28'}});\n  const data = await r.json();\n  // Update Supabase appointment status to cancelled\n  try {\n    const sbKey = ctx.supabaseServiceKey;\n    const sbUrl = ctx.supabaseUrl;\n    if (sbKey && sbUrl && eventId) {\n      await fetch(sbUrl + '/rest/v1/appointments?ghl_event_id=eq.' + eventId, {\n        method: 'PATCH',\n        headers: {\n          'apikey': sbKey,\n          'Authorization': 'Bearer ' + sbKey,\n          'Content-Type': 'application/json',\n          'Prefer': 'return=minimal'\n        },\n        body: JSON.stringify({ status: 'cancelled', updated_at: new Date().toISOString() })\n      });\n    }\n  } catch (sbErr) { /* best-effort */ }\n  return JSON.stringify(data);\n} catch(e) { return 'Error: '+e.message; }",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"event_id\":\"abc123\"}"
}
```

### bookAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `179bf9dc-f500-4a11-9bbd-b14550f5206c`.

```json
{
  "name": "bookAppointment",
  "description": "Book a consultation appointment.\n\nINPUT (required JSON):\n- selected_slot: string - ISO datetime from getAvailableSlots\n- ghl_api_key: string - from system context\n- calendar_id: string - from system context\n- ghl_user_id: string - from system context\n- contact_id: string - CONTACT_ID from context\n- location_id: string - from context\n- first_name: string - lead first name\n\nCall getAvailableSlots first.",
  "jsCode": "let input = {};\nif (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {selected_slot:query}; } } else if (typeof query === 'object' && query !== null) { input = query; }\nconst ctx = $('Assemble System Prompt').first().json;\nconst apiKey = ctx.ghlApiKey;\nconst calendarId = ctx.calendarId;\nconst ghlUserId = ctx.ghlUserId;\nconst locationId = ctx.locationId;\nconst contactId = ctx.contactId || input.contact_id;\nconst firstName = ctx.firstName || input.first_name || 'Lead';\nconst channel = ctx.channel || input.channel || 'sms';\nconst slot = input.selected_slot;\nif (!slot || !apiKey) return 'Error: selected_slot required and GHL credentials not configured.';\nconst body = {calendarId,locationId,contactId,startTime:slot,title:'Consultation - '+firstName,appointmentStatus:'confirmed',assignedUserId:ghlUserId};\ntry {\n  const r = await fetch('https://services.leadconnectorhq.com/calendars/events/appointments',{method:'POST',headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28','Content-Type':'application/json'},body:JSON.stringify(body)});\n  const data = await r.json();\n  // Write to Supabase appointments table\n  try {\n    const sbKey = ctx.supabaseServiceKey;\n    const sbUrl = ctx.supabaseUrl;\n    if (sbKey && sbUrl && data.id) {\n      const endTime = data.endTime || new Date(new Date(slot).getTime() + 30 * 60000).toISOString();\n      await fetch(sbUrl + '/rest/v1/appointments', {\n        method: 'POST',\n        headers: {\n          'apikey': sbKey,\n          'Authorization': 'Bearer ' + sbKey,\n          'Content-Type': 'application/json',\n          'Prefer': 'return=minimal'\n        },\n        body: JSON.stringify({\n          agent_id: ctx.agentId || null,\n          lead_id: ctx.leadId || null,\n          contact_id: contactId,\n          location_id: locationId,\n          ghl_event_id: data.id,\n          calendar_id: ca
...[truncated]
```

### getAvailableSlots

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `44d17ad9-6060-40b4-ac97-88242cf72bf8`.

```json
{
  "name": "getAvailableSlots",
  "description": "Fetch available appointment slots for the next 7 days. Returns pre-formatted slots with day names so you do NOT need to calculate which day of the week a date falls on.\n\nINPUT (required JSON):\n- ghl_api_key: string - from the system context\n- calendar_id: string - from the system context\n- timezone: string - from the system context\n\nYou MUST pass these from the CONTEXT.",
  "jsCode": "let input = {};\nif (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {}; } } else if (typeof query === 'object' && query !== null) { input = query; }\n// Read credentials from workflow context — NOT from AI input\nconst ctx = $('Assemble System Prompt').first().json;\nconst apiKey = ctx.ghlApiKey;\nconst calendarId = ctx.calendarId;\nconst ghlUserId = ctx.ghlUserId;\nconst locationId = ctx.locationId;\nconst contactId = ctx.contactId || input.contact_id;\nconst firstName = ctx.firstName || input.first_name || 'Lead';\nconst channel = ctx.channel || input.channel || 'sms';\nconst calId = calendarId;\nconst tz = input.timezone || ctx.timezone || 'America/Denver';\nconst targetDate = input.target_date || null;\nif (!apiKey || !calId) return 'Error: GHL credentials not configured.';\nlet startDate, endDate;\nif (targetDate) {\n  startDate = new Date(targetDate).getTime();\n  const d = new Date(targetDate);\n  d.setDate(d.getDate() + 1);\n  endDate = d.getTime();\n} else {\n  const now = new Date();\n  startDate = now.getTime();\n  const end = new Date(now);\n  end.setDate(end.getDate() + 8);\n  endDate = end.getTime();\n}\ntry {\n  const r = await fetch('https://services.leadconnectorhq.com/calendars/'+calId+'/free-slots?startDate='+startDate+'&endDate='+endDate+'&timezone='+tz, {headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28'}});\n  const data = await r.json();\n  return JSON.stringify(data);\n} catch(e) { return 'Error: '+e.message; }",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"timezone\":\"America/Denver\",\"target_date\":\"2026-04-15\"}"
}
```

### Insert Conversation Context

Type: `n8n-nodes-base.supabase`. Node ID: `888419bf-dd95-43b0-93ff-4fa8f0c23ec4`.

```json
{
  "tableId": "conversation_context",
  "fieldsUi": {
    "fieldValues": [
      {
        "fieldId": "contact_id",
        "fieldValue": "={{ $('Assemble System Prompt').first().json.contactId }}"
      },
      {
        "fieldId": "location_id",
        "fieldValue": "={{ $('Assemble System Prompt').first().json.locationId }}"
      },
      {
        "fieldId": "conversation_summary",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || $('Analyze Conversation').first().json.text || '{}'; const parsed = JSON.parse(content); return parsed.summary || content; } catch(e) { return $('Analyze Conversation').first().json.message?.content || ''; } })() }}"
      },
      {
        "fieldId": "last_intent",
        "fieldValue": "={{ (() => { try { return $('Parse Sentiment').first().json.sentiment_analysis ? $('Parse Sentiment').first().json.sentiment_analysis.action : 'continue'; } catch(e) { return 'continue'; } })() }}"
      },
      {
        "fieldId": "lead_intent",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_intent || 'unknown'; } catch(e) { return 'unknown'; } })() }}"
      },
      {
        "fieldId": "lead_timeline",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.lead_timeline || 'unknown'; } catch(e) { return 'unknown'; } })() }}"
      },
      {
        "fieldId": "first_contact_at",
        "fieldValue": "={{ new Date().toISOString() }}"
      },
      {
        "fieldId": "updated_at",
        "fieldValue": "={{ new Date().toISOString() }}"
      },
      {
        "fieldId": "appointment_offered",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed && (parsed.appointment_outcome === 'offered' || parsed.appointment_outcome === 'accepted'); } catch(e) { return false; } })() }}"
      },
      {
        "fieldId": "appointment_booked",
        "fieldValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(cont
...[truncated]
```

### Is Qualified?

Type: `n8n-nodes-base.if`. Node ID: `213a3192-876b-4d4b-823d-92ed970341ef`.

```json
{
  "conditions": {
    "options": {
      "version": 2,
      "leftValue": "",
      "caseSensitive": true,
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "qual-check",
        "leftValue": "={{ Object.values($json.qualifying_answers || {}).filter(v => v !== null && v !== undefined && v !== '').length >= 3 }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "true",
          "singleValue": true
        }
      }
    ],
    "combinator": "and"
  },
  "options": {}
}
```

### addAppointmentNotes

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `6ecbe0a0-36ef-4a7f-b3cc-99c042801614`.

```json
{
  "name": "addAppointmentNotes",
  "description": "Post a summary note to the lead's GHL contact after booking.\n\nINPUT (required JSON):\n- appointment_time: string\n- qualifying_summary: string\n- conversation_summary: string\n- contact_id: string - CONTACT_ID from context\n- ghl_api_key: string - from system context\n- channel: string\n\nONLY call after successful bookAppointment.",
  "jsCode": "let input = {};\nif (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {note:query}; } } else if (typeof query === 'object' && query !== null) { input = query; }\n// Read credentials from workflow context — NOT from AI input\nconst ctx = $('Assemble System Prompt').first().json;\nconst apiKey = ctx.ghlApiKey;\nconst calendarId = ctx.calendarId;\nconst ghlUserId = ctx.ghlUserId;\nconst locationId = ctx.locationId;\nconst contactId = ctx.contactId || input.contact_id;\nconst firstName = ctx.firstName || input.first_name || 'Lead';\nconst channel = ctx.channel || input.channel || 'sms';\nif (!contactId || !apiKey) return 'Error: contact_id required and GHL credentials not configured.';\nconst note = [input.appointment_time ? 'Appt: '+input.appointment_time : '', input.qualifying_summary || '', input.conversation_summary || ''].filter(Boolean).join(' | ');\ntry {\n  await fetch('https://services.leadconnectorhq.com/contacts/'+contactId+'/notes',{method:'POST',headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28','Content-Type':'application/json'},body:JSON.stringify({body:note})});\n  return 'Note posted for '+contactId;\n} catch(e) { return 'Error: '+e.message; }",
  "specifyInputSchema": true,
  "jsonSchemaExample": "{\"appointment_time\":\"2026-04-10T09:00\",\"qualifying_summary\":\"Buyer, 500k, pre-approved\",\"conversation_summary\":\"Lead relocating\"}"
}
```

### Form Section4

Type: `n8n-nodes-base.stickyNote`. Node ID: `68a913f7-40d3-40c0-8860-07261a637338`.

```json
{
  "content": "##  Booking Agent Routing\n#### Book Intent in conversation\n",
  "height": 288,
  "width": 944,
  "color": 3
}
```

### Fetch Slots

Type: `n8n-nodes-base.code`. Node ID: `f759a90a-8071-4fda-9140-293e5833fb31`.

```json
{
  "jsCode": "const input = $input.first().json;\nconst calendarId = input.calendar_id || '';\nconst ghlApiKey = input.ghl_api_key || '';\n\nlet slotOptions = '';\nlet availableSlots = [];\n\nif (calendarId && ghlApiKey) {\n  try {\n    const now = new Date();\n    const endDate = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);\n    const startStr = now.toISOString().split('T')[0];\n    const endStr = endDate.toISOString().split('T')[0];\n    \n    const result = await this.helpers.httpRequest({\n      method: 'GET',\n      url: 'https://services.leadconnectorhq.com/calendars/' + calendarId + '/free-slots?startDate=' + startStr + '&endDate=' + endStr,\n      headers: {\n        'Authorization': 'Bearer ' + ghlApiKey,\n        'Version': '2021-07-28'\n      }\n    });\n    \n    const slots = result.slots || result;\n    if (typeof slots === 'object') {\n      const entries = Object.entries(slots);\n      let formatted = [];\n      for (const [date, times] of entries) {\n        if (Array.isArray(times) && times.length > 0) {\n          for (const slot of times.slice(0, 3)) {\n            const start = new Date(slot.startTime || slot);\n            formatted.push(start.toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) + ' (startTime: ' + (slot.startTime || slot) + ', endTime: ' + (slot.endTime || '') + ')');\n          }\n        }\n        if (formatted.length >= 6) break;\n      }\n      slotOptions = formatted.join('\\n');\n      availableSlots = formatted;\n    }\n  } catch (e) {\n    slotOptions = 'Error fetching slots: ' + e.message;\n  }\n}\n\nreturn [{\n  json: {\n    ...input,\n    isSchedulingFlow: true,\n    slotOptions: slotOptions,\n    availableSlots: availableSlots,\n    direction: 'inbound'\n  }\n}];"
}
```

### checkQualificationStatus

Type: `n8n-nodes-base.supabaseTool`. Node ID: `e5010ff8-a0c6-4efd-9d17-81ea31854a60`.

```json
{
  "descriptionType": "manual",
  "toolDescription": "Check how many of the 3 qualifying questions this lead has answered so far.\n\nWHEN TO USE:\n- BEFORE calling saveQualifyingAnswer, to get the current qualifying_answers object\n- When the lead says they want to book an appointment, to verify they are qualified\n- When you are unsure which qualifying questions have already been answered\n\nINPUT: No input needed. Automatically looks up this lead's conversation_context record.\n\nOUTPUT: Returns the qualifying_answers JSONB object with keys q1, q2, q3.\n- If a key has a value: that question is answered\n- If a key is null: that question still needs to be asked\n- When all 3 are non-null: lead is QUALIFIED and ready to book\n\nThe 3 questions are:\n  q1 = Buying or selling? Timeline?\n  q2 = Budget or price range?\n  q3 = Financing status?\n\nRULES:\n- Always call this BEFORE saveQualifyingAnswer so you have the current state\n- If all 3 answered, proceed to getAvailableSlots for booking\n- If not all answered, continue the conversation and ask the missing ones naturally",
  "operation": "getAll",
  "tableId": "conversation_context",
  "limit": 1,
  "matchType": "allFilters",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "condition": "eq",
        "keyValue": "={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}"
      }
    ]
  }
}
```

### saveQualifyingAnswer

Type: `n8n-nodes-base.supabaseTool`. Node ID: `5d5b2a1d-c388-427b-bca0-01b753af72f2`.

```json
{
  "descriptionType": "manual",
  "toolDescription": "MANDATORY TOOL - Save a qualifying answer to the database after the lead answers one of the 3 qualifying questions.\n\nWHEN TO USE: You MUST call this tool IMMEDIATELY every time the lead provides information that answers Q1, Q2, or Q3. Do NOT wait until all questions are answered. Save each answer the moment you receive it.\n\nThe tool updates the qualifying_answers JSONB column in conversation_context for this lead.\n\nINPUT: You must provide a JSON object with the field 'qualifying_answers' containing the COMPLETE qualifying_answers object. IMPORTANT: First call checkQualificationStatus to get the current answers, then merge your new answer into that object.\n\nThe qualifying_answers object has keys q1, q2, q3:\n  q1 = Buying or selling? What is their timeline?\n  q2 = What is their budget or price range?\n  q3 = What is their financing status? (pre-approved, cash buyer, need pre-approval)\n\nExample input: {\"qualifying_answers\": {\"q1\": \"Buying, 3 month timeline\", \"q2\": null, \"q3\": null}}\n\nRULES:\n- Call checkQualificationStatus FIRST to get existing answers\n- Include ALL existing answers plus the new one (do not overwrite previous answers with null)\n- Only 3 questions total. Do NOT ask more than 3.\n- After saving all 3, the lead is qualified and ready to book",
  "operation": "update",
  "tableId": "conversation_context",
  "matchType": "allFilters",
  "filters": {
    "conditions": [
      {
        "keyName": "contact_id",
        "condition": "eq",
        "keyValue": "={{ (() => { try { return $('Set Outbound Context').first().json.contact_id } catch(e) { return $('LeadDetails').first().json.contact_id } })() }}"
      }
    ]
  },
  "fieldsUi": {
    "fieldValues": [
      {
        "fieldId": "qualifying_answers",
        "fieldValue": "={{ $fromAI('qualifying_answers', 'The complete qualifying_answers JSON object with keys q1, q2, q3. Each key is either a string summary of the lead answer or null if not yet answered. Example: {\"q1\": \"Buying, 3 month timeline\", \"q2\": \"Budget around 500k\", \"q3\": null}. IMPORTANT: Include ALL existing answers plus the new one.', 'json') }}"
      }
    ]
  }
}
```

### Check Qualification Gate

Type: `n8n-nodes-base.supabase`. Node ID: `dfab2608-8b15-499a-a900-125e77bf33f1`.

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

### rescheduleAppointment

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `a8e090cc-852a-4abd-9fbf-67be87f002f5`.

```json
{
  "description": "Reschedule an existing appointment.\n\nINPUT (required JSON):\n- event_id: string - from getAppointments\n- start_time: string - new time from getAvailableSlots\n- ghl_api_key: string - from system context\n- calendar_id: string - from system context\n- first_name: string\n\nCall getAppointments then getAvailableSlots first.",
  "jsCode": "let input = {};\nif (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {}; } } else if (typeof query === 'object' && query !== null) { input = query; }\nconst ctx = $('Assemble System Prompt').first().json;\nconst apiKey = ctx.ghlApiKey;\nconst calendarId = ctx.calendarId;\nconst ghlUserId = ctx.ghlUserId;\nconst locationId = ctx.locationId;\nconst contactId = ctx.contactId || input.contact_id;\nconst firstName = ctx.firstName || input.first_name || 'Lead';\nconst channel = ctx.channel || input.channel || 'sms';\nconst eventId = input.event_id;\nconst startTime = input.start_time;\nif (!eventId || !startTime || !apiKey) return 'Error: event_id, start_time required and GHL credentials not configured.';\nconst endMs = new Date(startTime).getTime() + 30*60*1000;\nconst endTime = new Date(endMs).toISOString();\nconst body = {calendarId,startTime,endTime};\ntry {\n  const r = await fetch('https://services.leadconnectorhq.com/calendars/events/appointments/'+eventId,{method:'PUT',headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28','Content-Type':'application/json'},body:JSON.stringify(body)});\n  const data = await r.json();\n  // Update Supabase appointment with new time + reset all reminder flags\n  try {\n    const sbKey = ctx.supabaseServiceKey;\n    const sbUrl = ctx.supabaseUrl;\n    if (sbKey && sbUrl && eventId) {\n      await fetch(sbUrl + '/rest/v1/appointments?ghl_event_id=eq.' + eventId, {\n        method: 'PATCH',\n        headers: {\n          'apikey': sbKey,\n          'Authorization': 'Bearer ' + sbKey,\n          'Content-Type': 'application/json',\n          'Prefer': 'return=minimal'\n        },\n        body: JSON.stringify({\n          start_time: startTime,\n          end_time: endTime,\n          updated_at: new Date().toISOString(),\n          reminder_24h_sent_at: null,\n          reminder_5h_sent_at: null,\n          reminder_1h_sent_at: null\n        })\n      });\n    }\n  } catch (sbErr) { /* best-effort */ }\n  return JSON.stringify(d
...[truncated]
```

### Evaluate Pipeline Stage

Type: `n8n-nodes-base.code`. Node ID: `09d05f40-b581-4b64-a317-45c406992d0f`.

```json
{
  "jsCode": "const input = $input.first().json;\n\nconst contactId = input.contactId || input.contact_id || '';\nconst currentStage = input.pipeline_stage || 'MONTHLY';\nconst intentLevel = input.intent_level || 'none';\nconst marketRole = input.market_role || 'unknown';\nconst agentDormant = input.agent_dormant || false;\nconst status = input.status || 'active_conversation';\nconst locationId = input.location_id || '';\n\nconst pipelineConfig = input.pipeline_config || {};\nconst incubator = pipelineConfig.incubator || {};\nconst incubatorStages = incubator.stages || {};\n\nconst appointmentBooked = input.appointment_booked || false;\nconst appointmentOffered = input.appointment_offered || false;\n\nif (['AGENT_HANDLING', 'DNC'].includes(currentStage)) {\n  return [{ json: { stageChanged: false, currentStage, targetStage: currentStage, contactId, reason: 'locked_stage' } }];\n}\n\nif (status === 'opted_out' && currentStage !== 'DNC') {\n  return [{ json: { stageChanged: true, currentStage, targetStage: 'DNC', pipelineId: incubator.id, stageId: incubatorStages.DNC, contactId, reason: 'opted_out' } }];\n}\n\nif (agentDormant && currentStage !== 'AGENT_HANDLING') {\n  return [{ json: { stageChanged: true, currentStage, targetStage: 'AGENT_HANDLING', pipelineId: incubator.id, stageId: incubatorStages.AGENT_HANDLING, contactId, reason: 'agent_takeover' } }];\n}\n\nif (appointmentBooked && currentStage !== 'APPT_BOOKED') {\n  return [{ json: { stageChanged: true, currentStage, targetStage: 'APPT_BOOKED', pipelineId: incubator.id, stageId: incubatorStages.APPT_BOOKED, marketRole, contactId, reason: 'appointment_booked' } }];\n}\n\nif (appointmentOffered && !appointmentBooked && currentStage !== 'APPT_OFFERED') {\n  return [{ json: { stageChanged: true, currentStage, targetStage: 'APPT_OFFERED', pipelineId: incubator.id, stageId: incubatorStages.APPT_OFFERED, contactId, reason: 'appointment_offered' } }];\n}\n\nconst stageOrder = ['MONTHLY', 'BIWEEKLY', 'WEEKLY', 'APPT_OFFERED', 'APPT_BOOKED'];\nconst currentIdx = stageOrder.indexOf(currentStage);\n\nlet targetStage = currentStage;\nlet reason = 'no_change';\n\nif (intentLevel === 'active' && currentIdx < stageOrder.indexOf('WEEKLY')) {\n  targetStage = 'WEEKLY'; reason = 'active_intent';\n} else if (intentLevel === 'moderate' && currentIdx < stageOrder.indexOf('BIWEEKLY')) {\n  targetStage = 'BIWEEKLY'; reason =
...[truncated]
```

### updateContactMemory

Type: `@n8n/n8n-nodes-langchain.toolCode`. Node ID: `d9d4d69d-575d-46a3-b6dd-3f6c32786274`.

```json
{
  "name": "updateContactMemory",
  "description": "Update the contact's memory and enrichment fields. Call this when you detect ANY of the signals below. Include ALL detected fields in a single call — never make multiple calls.\n\nINPUT (required JSON):\n- contact_id: string - CONTACT_ID from context (always required)\n- Plus any fields below that you detected:\n\nFIELD TRIGGERS — scan every message for these:\n\nIDENTITY / CONTACT INFO\n- Lead says their name → first_name, last_name\n- Lead gives their email address → email\n- Lead gives their phone number → phone (only if they explicitly provide it)\n- Lead mentions a street address → address, city, state, postal_code\n- Lead mentions a city, area, or neighborhood they live in or want → city, state\n- Lead gives a ZIP/postal code → postal_code\n\nINTENT & RELATIONSHIP\n- Lead says what they want to do (buy/sell/invest/rent) → market_role, intent_topic\n- Lead gives a timeline or urgency signal → intent_level (active=specific deadline, moderate=general readiness, light=vague/just browsing)\n- Lead says how they prefer to be contacted (text/email/call) → contact_preference (sms/email/call)\n- Lead says they were referred by someone, OR mentions being a past client, OR is an investor → relationship_type (sphere=referred/knows agent, past_client=worked with agent before, investor_contact=investor)\n\nUNRESOLVED THREADS & HANDOFFS\n- Lead mentions an unresolved blocker or dependency (must sell first, waiting on spouse, pending inspection, relocating on date X, checking with partner) → open_loop (one-line description of the hanging thread)\n- Lead needs something beyond your scope (legal question, complex contract issue, specific listing negotiation, formal complaint) → handoff_reason (one-line why this needs the human agent)\n- Lead is emotionally distressed, in crisis, or signals the situation genuinely needs human attention → needs_human_review (true), review_reason (one-line why)\n\nBOUNDARIES & SENSITIVE SIGNALS\n- Lead sets a boundary (do not call, time windows, sensitive topic, language preference) → boundary_flags (short phrase capturing the boundary)\n\nSUMMARY\n- You have name + intent + area → short_summary_note (one-line lead summary, e.g. \"Mike, buyer, Eagle Idaho, 450k, end of summer\")\n\nCRITICAL RULES — open_loop vs short_summary_note:\n- These are INDEPENDENT fields. If a blocker/dependency/
...[truncated]
```

### Newsletter Offer Needed?

Type: `n8n-nodes-base.if`. Node ID: `81c1030a-d3e3-47d9-8bbd-df1daee1f228`.

```json
{
  "conditions": {
    "options": {
      "version": 2,
      "leftValue": "",
      "caseSensitive": true,
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "newsletter-check-appt-rejected",
        "leftValue": "={{ (() => { try { const content = $('Analyze Conversation').first().json.message?.content || '{}'; const parsed = JSON.parse(content); return parsed.appointment_discussed === true && parsed.appointment_outcome === 'rejected'; } catch(e) { return false; } })() }}",
        "rightValue": "",
        "operator": {
          "type": "boolean",
          "operation": "true",
          "singleValue": true
        }
      },
      {
        "id": "newsletter-check-not-opted-in",
        "leftValue": "={{ (() => { try { return $('Get Lead Memory').first().json.newsletter_opted_in } catch(e) { try { return $('Get Outbound Lead Memory').first().json.newsletter_opted_in } catch(e2) { return false } } })() }}",
        "rightValue": "",
        "operator": {
          "type": "boolean",
          "operation": "false",
          "singleValue": true
        }
      },
      {
        "id": "newsletter-check-not-declined",
        "leftValue": "={{ (() => { try { return $('Get Conversation Summary').first().json.newsletter_offer_declined } catch(e) { try { return $('Get Outbound Conversation Summary').first().json.newsletter_offer_declined } catch(e2) { return false } } })() }}",
        "rightValue": "",
        "operator": {
          "type": "boolean",
          "operation": "false",
          "singleValue": true
        }
      },
      {
        "id": "newsletter-check-not-outbound",
        "leftValue": "={{ (() => { try { return $('Assemble System Prompt').first().json.direction } catch(e) { return 'inbound' } })() }}",
        "rightValue": "outbound",
        "operator": {
          "type": "string",
          "operation": "notEquals"
        }
      }
    ],
    "combinator": "and"
  },
  "options": {}
}
```

### Silence Gate

Type: `n8n-nodes-base.code`. Node ID: `4b936bf7-febd-4e01-9bc0-aa756202409e`.

```json
{
  "jsCode": "const input = $input.first().json;\nconst direction = input.direction || 'inbound';\n\n// Style normalizer — strip punctuation the prompt bans but LLMs still emit.\n// Rules: no em dashes, no en dashes, no exclamation marks, no hyphen-as-separator.\n// Preserves compound words (first-time) and phone numbers (208-555-1234).\nfunction normalizeStyle(text) {\n  if (!text || typeof text !== 'string') return text;\n  let s = text;\n  s = s.replace(/\\s*\\u2014\\s*/g, ', ');\n  s = s.replace(/\\s*\\u2013\\s*/g, ', ');\n  s = s.replace(/(?<!\\w)-(?!\\w)/g, ',');\n  s = s.replace(/ ,/g, ',');\n  s = s.replace(/!/g, '.');\n  s = s.replace(/,\\s*,/g, ',');\n  s = s.replace(/,\\s*\\./g, '.');\n  s = s.replace(/\\.\\s*,/g, '.');\n  s = s.replace(/  +/g, ' ');\n  s = s.replace(/,(\\S)/g, ', $1');\n  s = s.replace(/\\.([A-Z])/g, '. $1');\n  s = s.replace(/,\\s*$/g, '.');\n  return s.trim();\n}\n\n// Apply normalizer to incoming text fields\nconst rawResponseText = (input.responseText || input.output || '').trim();\nconst responseText = normalizeStyle(rawResponseText);\n\n// Determine tier from Parse Sentiment (source of truth)\nlet tier = 'normal';\ntry { tier = $('Parse Sentiment').first().json.tier || 'normal'; } catch(e) { tier = input.tier || 'normal'; }\n\n// Tiered responses MUST always respond — defense-in-depth override\n// regardless of classifier's should_suppress value\nconst TIERED_MUST_RESPOND = ['tier_1_confused', 'tier_2_hostile', 'tier_3_optout', 'emotional', 'turnaround', 'booking', 'declined_meeting'];\nconst isTiered = TIERED_MUST_RESPOND.includes(tier);\n\nif (!responseText) {\n  const fallbacks = {\n    emotional: \"I'm really sorry to hear that. No pressure at all, take care of yourself.\",\n    tier_2_hostile: \"Understood, no worries at all.\",\n    tier_3_optout: \"Got it, I'll stop reaching out. Wishing you the best.\",\n    tier_1_confused: \"No worries. Happy to help clarify anything.\"\n  };\n\n  const fallback = fallbacks[tier];\n  if (fallback) {\n    return [{ json: { ...input, responseText: fallback, output: fallback, shouldRespond: true, silenceReason: 'empty_ai_fallback_' + tier } }];\n  }\n\n  // Normal tier with empty response — suppress\n  return [{ json: { ...input, shouldRespond: false, silenceReason: 'empty_ai_response' } }];\n}\n\n// Outbound always sends\nif (direction === 'outbound') {\n  return [{ json: { ...inpu
...[truncated]
```

### Gather Prompt Data

Type: `n8n-nodes-base.set`. Node ID: `gather-prompt-data`.

```json
{
  "duplicateItem": true,
  "assignments": {
    "assignments": [
      {
        "id": "g1",
        "name": "agentName",
        "value": "={{ (() => { try { return $('Get Outbound Agent Config').first().json.agent_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.agent_name; } catch(e2) { return 'the agent'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g2",
        "name": "coordinatorName",
        "value": "={{ (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.coordinator_name; } catch(e2) { return 'Jon'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g3",
        "name": "marketName",
        "value": "={{ (() => { try { return $('Get Outbound Agent Config').first().json.market_name; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.market_name; } catch(e2) { return ''; } } })() }}",
        "type": "string"
      },
      {
        "id": "g4",
        "name": "timezone",
        "value": "={{ (() => { try { return $('Get Outbound Agent Config').first().json.timezone; } catch(e) { try { return $('Get Agent Config (RAG)').first().json.timezone; } catch(e2) { return 'America/Denver'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g5",
        "name": "direction",
        "value": "={{ (() => { try { return $('Set Outbound Context').first().json.direction; } catch(e) { try { return $('LeadDetails').first().json.direction || 'inbound'; } catch(e2) { return 'inbound'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g6",
        "name": "channel",
        "value": "={{ (() => { try { return $('Set Outbound Context').first().json.channel; } catch(e) { try { return $('LeadDetails').first().json.channel; } catch(e2) { return 'sms'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g7",
        "name": "firstName",
        "value": "={{ (() => { try { return $('Set Outbound Context').first().json.first_name; } catch(e) { try { return $('LeadDetails').first().json.first_name; } catch(e2) { return 'Contact'; } } })() }}",
        "type": "string"
      },
      {
        "id": "g8",
        "name": "contactId",
        "value": "={{ (() => { try { return $('Set Outbound Context').first().json.contact_id; } ca
...[truncated]
```

## 🏗️ Onboarding — Part 2: GHL Setup (`iMG9ggquVeLbmKuv`)

Active: **False**. Archived: **False**. Matched nodes: **4**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Sticky Note - Manual Actions` | `n8n-nodes-base.stickyNote` | none |
| `Sticky Note - Calendar Setup` | `n8n-nodes-base.stickyNote` | none |
| `Save Agent Config to Supabase` | `n8n-nodes-base.postgres` | main |
| `Insert Default Agent Rules` | `n8n-nodes-base.postgres` | main |

### Sticky Note - Manual Actions

Type: `n8n-nodes-base.stickyNote`. Node ID: `sticky-manual`.

```json
{
  "width": 532,
  "height": 688,
  "color": 3,
  "content": "## Manual Actions: GHL Private Integration\nMust be done manually after the onboarding call. Required for SMS and email sending.\n\n### Step 1 - Create the Private Integration\n1. Log into GHL at the SUB-ACCOUNT level (not agency)\n2. Go to Settings -> Private Integrations\n3. Click Create New Integration\n4. Enable these scopes:\n   - Contacts (read + write)\n   - Conversations (read + write)\n   - Conversations / Messages (write)\n   - Calendars (read + write)\n5. Copy the API key\n\n### Step 2 - Store in Supabase\n1. Open Supabase -> agents table\n2. Find the agent row by location_id\n3. Paste the API key into the ghl_api_key column\n4. Save\n\n### Step 3 - Set Up GHL Automation\n1. In the sub-account go to Automations\n2. Create a new workflow trigger: Contact Created\n3. Add a Webhook action pointing to: https://twodegreesnorth.tech/webhook/intake-lead\n4. Activate the automation"
}
```

### Sticky Note - Calendar Setup

Type: `n8n-nodes-base.stickyNote`. Node ID: `sticky-calendar`.

```json
{
  "width": 500,
  "height": 380,
  "color": 2,
  "content": "## Calendar Setup (Post-Snapshot)\n\nAfter GHL snapshot is applied, the agent's calendar ID needs to be stored in Supabase.\n\n### agents table field\n- buyer_calendar_id — stores the agent's single calendar ID\n\n### To do after W2 is live\n1. HTTP GET https://services.leadconnectorhq.com/calendars/?locationId={location_id}\n2. Find the correct calendar by name\n3. UPDATE agents SET buyer_calendar_id = ... WHERE location_id = ...\n\n### Collect during onboarding call\n- Calendar name (for auto-pull matching)\n- ghl_user_id (from GHL Settings -> My Profile)"
}
```

### Save Agent Config to Supabase

Type: `n8n-nodes-base.postgres`. Node ID: `save-config`.

```json
{
  "operation": "executeQuery",
  "query": "INSERT INTO agents (\n  location_id, agent_name, agent_email, business_name, market_area,\n  brand_voice, calendar_link, openai_api_key, ghl_api_key,\n  personality_prompt, knowledge_base_folder_id, knowledge_base_folder_name,\n  knowledge_base_faq_doc_id, knowledge_base_faq_doc_url, active, created_at\n) VALUES (\n  '{{ $('Extract Location ID').first().json.location_id }}',\n  '{{ $('Load Onboarding Request').first().json.agent_name.replace(/'/g, \"''\") }}',\n  '{{ $('Load Onboarding Request').first().json.agent_email.replace(/'/g, \"''\") }}',\n  '{{ ($('Load Onboarding Request').first().json.business_name || '').replace(/'/g, \"''\") }}',\n  '{{ ($('Load Onboarding Request').first().json.market_area || '').replace(/'/g, \"''\") }}',\n  '{{ ($('Load Onboarding Request').first().json.brand_voice || '').replace(/'/g, \"''\") }}',\n  '{{ ($('Load Onboarding Request').first().json.calendar_link || '').replace(/'/g, \"''\") }}',\n  '{{ $('Load Onboarding Request').first().json.openai_api_key }}',\n  '{{ $('Extract Location ID').first().json.ghl_api_key }}',\n  '{{ ($('Load Onboarding Request').first().json.personality_prompt || '').replace(/'/g, \"''\") }}',\n  '{{ $('Load Onboarding Request').first().json.knowledge_base_folder_id }}',\n  '{{ ($('Load Onboarding Request').first().json.knowledge_base_folder_name || '').replace(/'/g, \"''\") }}',\n  '{{ $('Load Onboarding Request').first().json.faq_doc_id }}',\n  '{{ ($('Load Onboarding Request').first().json.faq_doc_url || '').replace(/'/g, \"''\") }}',\n  true, NOW()\n)\nON CONFLICT (location_id) DO UPDATE SET\n  agent_name = EXCLUDED.agent_name,\n  agent_email = EXCLUDED.agent_email,\n  ghl_api_key = EXCLUDED.ghl_api_key,\n  personality_prompt = EXCLUDED.personality_prompt,\n  knowledge_base_folder_id = EXCLUDED.knowledge_base_folder_id,\n  updated_at = NOW()\nRETURNING id, location_id;",
  "options": {}
}
```

### Insert Default Agent Rules

Type: `n8n-nodes-base.postgres`. Node ID: `insert-rules`.

```json
{
  "operation": "executeQuery",
  "query": "INSERT INTO agent_rules (location_id, rule_type, rule_content, priority) VALUES \n  ('{{ $('Extract Location ID').first().json.location_id }}', 'greeting', 'Always greet leads warmly and professionally', 1),\n  ('{{ $('Extract Location ID').first().json.location_id }}', 'scheduling', 'Push for appointments when lead shows interest', 2),\n  ('{{ $('Extract Location ID').first().json.location_id }}', 'escalation', 'Transfer to human if lead asks for specific agent or becomes frustrated', 3);",
  "options": {}
}
```

## ⏰ Appointment Reminders (`CVHL7qHNCzQOhaqE`)

Active: **True**. Archived: **False**. Matched nodes: **4**.

| Node | Type | Outgoing connection summary |
|---|---|---|
| `Query Pending Reminders` | `n8n-nodes-base.postgres` | main |
| `Mark Reminder Sent` | `n8n-nodes-base.supabase` | none |
| `Sticky Note` | `n8n-nodes-base.stickyNote` | none |
| `Log to message_log` | `n8n-nodes-base.supabase` | main |

### Query Pending Reminders

Type: `n8n-nodes-base.postgres`. Node ID: `query-reminders`.

```json
{
  "operation": "executeQuery",
  "query": "SELECT a.id as appointment_id, a.contact_id, a.location_id, a.ghl_event_id, a.start_time, a.end_time, a.appointment_type, a.reminder_24h_sent_at, a.reminder_5h_sent_at, a.reminder_1h_sent_at, l.first_name, l.phone, l.pipeline_stage, l.status as lead_status, ag.ghl_api_key, ag.agent_name, ag.timezone as agent_timezone, ag.location_id as agent_location_id FROM appointments a JOIN leads l ON a.contact_id = l.contact_id JOIN agents ag ON a.location_id = ag.location_id WHERE a.status = 'scheduled' AND a.start_time > NOW() AND l.status != 'opted_out' AND l.pipeline_stage != 'DNC' AND l.phone IS NOT NULL AND ( (a.reminder_24h_sent_at IS NULL AND a.start_time BETWEEN NOW() + INTERVAL '23 hours' AND NOW() + INTERVAL '25 hours') OR (a.reminder_5h_sent_at IS NULL AND a.start_time BETWEEN NOW() + INTERVAL '4 hours' AND NOW() + INTERVAL '6 hours') OR (a.reminder_1h_sent_at IS NULL AND a.start_time BETWEEN NOW() + INTERVAL '30 minutes' AND NOW() + INTERVAL '90 minutes') )",
  "options": {}
}
```

### Mark Reminder Sent

Type: `n8n-nodes-base.supabase`. Node ID: `mark-sent`.

```json
{
  "operation": "update",
  "tableId": "appointments",
  "filters": {
    "conditions": [
      {
        "keyName": "id",
        "condition": "eq",
        "keyValue": "={{ $('Determine Reminder Type').item.json.appointment_id }}"
      }
    ]
  },
  "fieldsUi": {
    "fieldValues": [
      {
        "fieldId": "={{ $('Determine Reminder Type').item.json.sentAtColumn }}",
        "fieldValue": "={{ $now }}"
      }
    ]
  }
}
```

### Sticky Note

Type: `n8n-nodes-base.stickyNote`. Node ID: `sticky-info`.

```json
{
  "content": "## Appointment Reminders\n\nSends SMS reminders at 3 intervals before scheduled appointments:\n- **24 hours** before\n- **5 hours** before  \n- **1 hour** before\n\n**Safety guards:**\n- No reminders to DNC/opted-out leads\n- No reminders for cancelled appointments\n- No reminders if lead has no phone\n- Messages logged to message_log so Brain Engine has context\n- Reminder flags prevent duplicate sends\n\n**Schedule:** Every 30 minutes",
  "height": 380,
  "width": 340
}
```

### Log to message_log

Type: `n8n-nodes-base.supabase`. Node ID: `log-message`.

```json
{
  "tableId": "message_log",
  "fieldsUi": {
    "fieldValues": [
      {
        "fieldId": "contact_id",
        "fieldValue": "={{ $('Determine Reminder Type').item.json.contact_id }}"
      },
      {
        "fieldId": "location_id",
        "fieldValue": "={{ $('Determine Reminder Type').item.json.location_id }}"
      },
      {
        "fieldId": "message_body",
        "fieldValue": "={{ $('Determine Reminder Type').item.json.message }}"
      },
      {
        "fieldId": "direction",
        "fieldValue": "outbound"
      },
      {
        "fieldId": "channel",
        "fieldValue": "sms"
      },
      {
        "fieldId": "ai_processed",
        "fieldValue": "false"
      },
      {
        "fieldId": "ai_intent",
        "fieldValue": "appointment_reminder"
      },
      {
        "fieldId": "timestamp",
        "fieldValue": "={{ $now }}"
      }
    ]
  }
}
```

