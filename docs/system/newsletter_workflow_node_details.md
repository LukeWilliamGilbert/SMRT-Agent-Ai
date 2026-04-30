# SMRT Newsletter Workflow Node Details

This is targeted local evidence for the newsletter forensic audit. Secrets and credential-like values are defensively redacted. The file intentionally preserves prompt, code, SQL, and API-body surfaces needed to map actual behavior.

## Data Source & Newsletter Creation

Workflow file: `workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json`

Node count: `37`

### Weekly Schedule

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.scheduleTrigger` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "rule": {
    "interval": [
      {
        "triggerAtHour": 3
      }
    ]
  }
}
```

### Get Newsletter Agents

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "operation": "getAll",
  "tableId": "agents",
  "returnAll": true
}
```

### Get Altos Hash

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `jsCode`

```javascript
const agentData = $('Prepare Agent Data').first().json;
const countyFips = agentData.county_fips || '16001';
const pai = agentData.pai || '690acaf9';
const resp = await globalThis.fetch('https://altos.re/api/v2/[REDACTED_QUERY]' + countyFips + '&pai=' + pai);
const data = await resp.json();
if (!data.id) throw new Error('No hash from Altos: ' + JSON.stringify(data));
return [{ json: { hash: data.id } }];
```

### Altos Get Stats

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `jsCode`

```javascript
const agentData = $('Prepare Agent Data').first().json;
const targetZips = agentData.target_zips || [];
const state = agentData.state;
const pai = agentData.pai;

const countyFips = agentData.county_fips || '16001';

const stats = [
  'price_median', 'count', 'per_sqft_median', 'dom_median',
  'new_price_median',
  'price_decreased_percent', 'price_increased_percent',
  'price_mean', 'dom_mean', 'mai'
];

const allZipData = [];
const errors = [];

try {
  const reportsResp = await globalThis.fet…[TRUNCATED]
```

### Condense Altos Data

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### Grok National Context

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
https://api.x.ai/v1/chat/completions
```

#### `headerParameters.parameters[0].name`

```text
Content-Type
```

#### `headerParameters.parameters[0].value`

```text
application/json
```

#### `specifyBody`

```text
json
```

### Prep Data for AI

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `jsCode`

```javascript
const condensedData = $('Condense Altos Data').first().json;
const grokResponse = $('Grok National Context').first().json;

let nationalContext = '';
if (grokResponse.choices && grokResponse.choices[0]?.message?.content) {
  nationalContext = grokResponse.choices[0].message.content;
} else if (grokResponse.message?.content) {
  nationalContext = grokResponse.message.content;
} else if (grokResponse.content) {
  nationalContext = grokResponse.content;
}

// Previous newsletters for week-over-week…[TRUNCATED]
```

### Get Previous Newsletters

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
newsletters
```

#### `filterString`

```text
=location_id=eq.{{ $('Prepare Agent Data').first().json.location_id }}&active=eq.true&order=week_start_date.desc
```

### Generate Newsletter

| Field | Value |
| --- | --- |
| Type | `@n8n/n8n-nodes-langchain.openAi` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `messages.values[0].role`

```text
system
```

#### `messages.values[0].content`

```text
=## Agent Context

You are writing on behalf of **{{ $('Prepare Agent Data').first().json.agent.agent_name }}**{{ $('Prepare Agent Data').first().json.agent.business_name ? ', ' + $('Prepare Agent Data').first().json.agent.business_name : '' }}, serving the **{{ $json.market_name }}** real estate market.

---

## Who You Are

You are a trusted local advisor writing to real people -- buyers, sellers, homeowners, and curious neighbors. You are NOT a research analyst writing a market report. Your t…[TRUNCATED]
```

#### `messages.values[1].content`

```text
=Generate a weekly market newsletter for **{{ $json.market_name }}**.

## Local Market Data (Altos Research)
{{ JSON.stringify($json.altos_data, null, 2) }}

## National/Global Context & Local Impact
{{ JSON.stringify($json.perplexity_data, null, 2) }}

## Previous Newsletters (last 2 weeks -- for continuity and week-over-week context)
{{ $json.previous_newsletters && $json.previous_newsletters.length > 0 ? JSON.stringify($json.previous_newsletters, null, 2) : 'No previous newsletters available …[TRUNCATED]
```

### Extract Splinters

| Field | Value |
| --- | --- |
| Type | `@n8n/n8n-nodes-langchain.openAi` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `messages.values[0].content`

```text
SMRT NEWSLETTER SPLINTER LAYER - CANONICAL RECORD GENERATOR

You are a post-newsletter processing layer inside the SMRT system. Your job is to take a completed weekly real estate market newsletter and convert it into a small set of structured market splinter records.

PRIMARY OBJECTIVE: Convert one completed newsletter into 3 to 5 canonical market splinter records.

Each splinter record should:
1. capture one distinct market shift, tension, or behavioral insight
2. be semantically rich enough fo…[TRUNCATED]
```

#### `messages.values[0].role`

```text
system
```

#### `messages.values[1].content`

```text
=newsletter_id: pending
market: {{ $('Prep Data for AI').first().json.market_name }}
newsletter_date: {{ $('Prep Data for AI').first().json.weekStartDate }}

Week-over-week market data:
{{ $('Condense Altos Data').first().json.altosTextSummary }}

Raw WoW changes:
{{ JSON.stringify($('Condense Altos Data').first().json.wowChanges) }}

Full newsletter text:
{{ $('Generate Newsletter').first().json.message.content }}
```

### Prepare Storage Data

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `jsCode`

```javascript
const sourceData = $('Prep Data for AI').first().json;
const newsletterContent = $('Generate Newsletter').first().json.message?.content || '';
const rawSplinters = $('Extract Splinters').first().json.message?.content?.trim() || '[]';

// Build permanent Supabase Storage URL
const locationId = sourceData.location_id;
const weekStart = sourceData.weekStartDate;
const imageUrl = `https://kfoijgcbkjeizxxyiwxv.supabase.co/storage/v1/object/public/newsletter-images/${locationId}/${weekStart}.jpeg`
con…[TRUNCATED]
```

### Store Newsletter

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
newsletters
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $json.newsletter.agent_id }}
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $json.newsletter.location_id }}
```

#### `fieldsUi.fieldValues[2].fieldValue`

```text
={{ $json.newsletter.week_start_date }}
```

#### `fieldsUi.fieldValues[3].fieldId`

```text
full_content
```

#### `fieldsUi.fieldValues[3].fieldValue`

```text
={{ $json.newsletter.full_content }}
```

#### `fieldsUi.fieldValues[4].fieldValue`

```text
={{ $json.newsletter.subject_line }}
```

#### `fieldsUi.fieldValues[5].fieldId`

```text
raw_altos_data
```

#### `fieldsUi.fieldValues[5].fieldValue`

```text
={{ JSON.stringify($json.newsletter.raw_altos_data) }}
```

#### `fieldsUi.fieldValues[6].fieldId`

```text
raw_perplexity_data
```

#### `fieldsUi.fieldValues[6].fieldValue`

```text
={{ JSON.stringify($json.newsletter.raw_perplexity_data) }}
```

#### `fieldsUi.fieldValues[7].fieldValue`

```text
={{ $json.newsletter.image_url }}
```

#### `fieldsUi.fieldValues[9].fieldId`

```text
generation_status
```

### Store Splinter

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
content_splinters
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $json.splinter.location_id }}
```

#### `fieldsUi.fieldValues[1].fieldId`

```text
content
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $json.splinter.content }}
```

#### `fieldsUi.fieldValues[2].fieldValue`

```text
={{ $json.splinter.topic }}
```

#### `fieldsUi.fieldValues[3].fieldValue`

```text
={{ $json.splinter.data_point }}
```

#### `fieldsUi.fieldValues[5].fieldValue`

```text
={{ $json.splinter.priority }}
```

#### `fieldsUi.fieldValues[6].fieldValue`

```text
={{ $json.splinter.week_start_date }}
```

#### `fieldsUi.fieldValues[7].fieldId`

```text
splinter_title
```

#### `fieldsUi.fieldValues[7].fieldValue`

```text
={{ $json.splinter.splinter_title }}
```

#### `fieldsUi.fieldValues[8].fieldValue`

```text
={{ $json.splinter.dominant_theme }}
```

#### `fieldsUi.fieldValues[9].fieldValue`

```text
={{ $json.splinter.signal_type }}
```

#### `fieldsUi.fieldValues[10].fieldValue`

```text
={{ $json.splinter.insight_core }}
```

#### `fieldsUi.fieldValues[11].fieldValue`

```text
={{ $json.splinter.interpretation }}
```

#### `fieldsUi.fieldValues[12].fieldId`

```text
behavioral_implication
```

#### `fieldsUi.fieldValues[12].fieldValue`

```text
={{ $json.splinter.behavioral_implication }}
```

#### `fieldsUi.fieldValues[13].fieldValue`

```text
={{ $json.splinter.audience_fit }}
```

#### `fieldsUi.fieldValues[14].fieldValue`

```text
={{ $json.splinter.stage_fit }}
```

#### `fieldsUi.fieldValues[15].fieldValue`

```text
={{ $json.splinter.relevance_tags }}
```

#### `fieldsUi.fieldValues[16].fieldId`

```text
send_eligibility_note
```

#### `fieldsUi.fieldValues[16].fieldValue`

```text
={{ $json.splinter.send_eligibility_note }}
```

#### `fieldsUi.fieldValues[17].fieldValue`

```text
={{ $json.splinter.rationale }}
```

#### `fieldsUi.fieldValues[18].fieldValue`

```text
={{ $json.splinter.source_excerpt }}
```

#### `fieldsUi.fieldValues[19].fieldValue`

```text
={{ $json.splinter.embedding_text }}
```

#### `fieldsUi.fieldValues[20].fieldId`

```text
delivery_variants
```

#### `fieldsUi.fieldValues[20].fieldValue`

```text
={{ JSON.stringify($json.splinter.delivery_variants) }}
```

### Store Weekly Stats

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
altos_weekly_stats
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $('Condense Altos Data').first().json.location_id }}
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $('Condense Altos Data').first().json.weekStartDate }}
```

#### `fieldsUi.fieldValues[2].fieldValue`

```text
={{ $('Condense Altos Data').first().json.zipsProcessed }}
```

#### `fieldsUi.fieldValues[3].fieldValue`

```text
={{ $('Condense Altos Data').first().json.totalZips }}
```

#### `fieldsUi.fieldValues[4].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.price_median?.current }}
```

#### `fieldsUi.fieldValues[5].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.count?.current }}
```

#### `fieldsUi.fieldValues[6].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.per_sqft_median?.current }}
```

#### `fieldsUi.fieldValues[7].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.dom_median?.current }}
```

#### `fieldsUi.fieldValues[8].fieldId`

```text
absorbed_price_median
```

#### `fieldsUi.fieldValues[8].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.absorbed_price_median?.current }}
```

#### `fieldsUi.fieldValues[9].fieldId`

```text
absorbed_dom_median
```

#### `fieldsUi.fieldValues[9].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.absorbed_dom_median?.current }}
```

#### `fieldsUi.fieldValues[10].fieldId`

```text
median_ppsqft_absorbed
```

#### `fieldsUi.fieldValues[10].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.median_ppsqft_of_listings_absorbed?.current }}
```

#### `fieldsUi.fieldValues[11].fieldId`

```text
new_price_median
```

#### `fieldsUi.fieldValues[11].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.new_price_median?.current }}
```

#### `fieldsUi.fieldValues[12].fieldId`

```text
price_decreased_percent
```

#### `fieldsUi.fieldValues[12].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.price_decreased_percent?.current }}
```

#### `fieldsUi.fieldValues[13].fieldId`

```text
price_increased_percent
```

#### `fieldsUi.fieldValues[13].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.price_increased_percent?.current }}
```

#### `fieldsUi.fieldValues[14].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.price_mean?.current }}
```

#### `fieldsUi.fieldValues[15].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.dom_mean?.current }}
```

#### `fieldsUi.fieldValues[16].fieldValue`

```text
={{ $('Condense Altos Data').first().json.altosSummary.mai?.current }}
```

#### `fieldsUi.fieldValues[17].fieldValue`

```text
={{ JSON.stringify($('Condense Altos Data').first().json.altosSummary) }}
```

### Generate Embedding

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
https://api.openai.com/v1/embeddings
```

#### `headerParameters.parameters[0].name`

```text
Content-Type
```

#### `headerParameters.parameters[0].value`

```text
application/json
```

#### `specifyBody`

```text
json
```

#### `jsonBody`

```text
={{ JSON.stringify({ model: 'text-embedding-3-small', input: $json.market_doc.content }) }}
```

### Store Embedded Doc

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
https://kfoijgcbkjeizxxyiwxv.supabase.co/rest/v1/documents
```

#### `headerParameters.parameters[0].name`

```text
Content-Type
```

#### `headerParameters.parameters[0].value`

```text
application/json
```

#### `headerParameters.parameters[1].value`

```text
return=representation
```

#### `specifyBody`

```text
json
```

#### `jsonBody`

```text
={{ (() => { const doc = $('Prepare Storage Data').item.json.market_doc; const emb = $json.data[0].embedding; return JSON.stringify({ content: doc.content, metadata: doc.metadata, embedding: '[' + emb.join(',') + ']', location_id: doc.location_id, document_type: 'market_weekly', week_start_date: doc.week_start_date }); })() }}
```

### Create Newsletter Doc

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `jsCode`

```javascript
const prepData = $('Prep Data for AI').first().json;
const storageData = $('Prepare Storage Data').first().json;
const newsletterContent = storageData.newsletter.full_content;

const weekStart = new Date(prepData.weekStartDate);
const dateStr = weekStart.toISOString().split('T')[0];
const weekNum = Math.ceil((weekStart - new Date(weekStart.getFullYear(), 0, 1)) / (7 * 24 * 60 * 60 * 1000));
const year = weekStart.getFullYear();

const agentName = prepData.agent_name || 'Agent';
const marketName …[TRUNCATED]
```

### Upload to Supabase Storage

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
=https://kfoijgcbkjeizxxyiwxv.supabase.co/storage/v1/object/newsletter-images/{{ $('Condense Altos Data').first().json.location_id }}/{{ $('Condense Altos Data').first().json.weekStartDate }}.jpeg
```

#### `headerParameters.parameters[0].name`

```text
Content-Type
```

### Delete Old Splinters

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `operation`

```text
update
```

#### `tableId`

```text
content_splinters
```

#### `filterString`

```text
location_id=eq.{{ $json.location_id }}&active=eq.true
```

### Check Newsletter For Week

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
newsletters
```

#### `filterString`

```text
=agent_id=eq.{{ $json.agent_id }}&week_start_date=eq.{{ $json.weekStartDate }}
```

### Check Week Stats Exist

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
altos_weekly_stats
```

#### `filterString`

```text
=location_id=eq.{{ $('Condense Altos Data').first().json.location_id }}&week_start_date=eq.{{ $('Condense Altos Data').first().json.weekStartDate }}
```

## Newsletter Dispatch

Workflow file: `workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json`

Node count: `15`

### Weekly Schedule

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.scheduleTrigger` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "rule": {
    "interval": [
      {
        "field": "weeks",
        "triggerAtDay": [
          1
        ],
        "triggerAtHour": 10
      }
    ]
  }
}
```

### Fetch Active Agents

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `filters.conditions[0].keyName`

```text
newsletter_enabled
```

### Get Newest Newsletter

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### Fetch Eligible Leads

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### Build HTML Email

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### Send Email via GHL

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `continueRegularOutput` |

#### `url`

```text
https://services.leadconnectorhq.com/conversations/messages
```

#### `specifyBody`

```text
json
```

#### `jsonBody`

```text
={
  "type": "Email",
  "contactId": "{{ $json.contact_id }}",
  "emailFrom": "{{ $json.coordinatorEmail }}",
  "html": {{ JSON.stringify($json.html) }},
  "subject": "{{ $json.subject }}"
}
```

### Log Delivery

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
newsletter_deliveries
```

#### `fieldsUi.fieldValues[0].fieldId`

```text
newsletter_id
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $('Build HTML Email').first().json.newsletterId }}
```

#### `fieldsUi.fieldValues[1].fieldId`

```text
lead_id
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $('Build HTML Email').first().json.id }}
```

#### `fieldsUi.fieldValues[2].fieldValue`

```text
={{ $('Build HTML Email').first().json.contact_id }}
```

#### `fieldsUi.fieldValues[3].fieldValue`

```text
={{ $('Get Newest Newsletter').first().json.location_id }}
```

#### `fieldsUi.fieldValues[4].fieldValue`

```text
={{ $('Build HTML Email').first().json.subject }}
```

#### `fieldsUi.fieldValues[6].fieldValue`

```text
={{ new Date().toISOString() }}
```

### Update Send Counts

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### Has Eligible Leads?

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.if` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `conditions.conditions[0].leftValue`

```text
={{ $json._skip }}
```

### Newsletter Found?

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.if` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `conditions.conditions[0].leftValue`

```text
={{ $json._skip }}
```

## SMRT Brain Engine

Workflow file: `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json`

Node count: `174`

### Schedule Outbound Check

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.scheduleTrigger` |
| Disabled | `True` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "rule": {
    "interval": [
      {
        "field": "hours",
        "hoursInterval": 3
      }
    ]
  }
}
```

### Fetch Outbound Candidates

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.postgres` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `query`

```sql
WITH eligible_splinter AS (
  SELECT
    cs.id AS splinter_id,
    cs.location_id,
    cs.content AS splinter_content,
    cs.topic AS splinter_topic,
    cs.data_point AS splinter_data_point,
    cs.splinter_title,
    cs.dominant_theme,
    cs.signal_type,
    cs.insight_core,
    cs.interpretation,
    cs.behavioral_implication,
    cs.audience_fit,
    cs.stage_fit,
    cs.embedding_text,
    cs.delivery_variants,
    cs.priority,
    cs.week_start_date,
    cs.created_at
  FROM content_spli…[TRUNCATED]
```

### Set Outbound Context

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.set` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `assignments.assignments[1].value`

```text
={{ $json.channel || 'sms' }}
```

#### `assignments.assignments[2].value`

```text
={{ $json.contact_id }}
```

#### `assignments.assignments[3].value`

```text
={{ $json.location_id }}
```

#### `assignments.assignments[4].value`

```text
={{ $json.first_name }}
```

#### `assignments.assignments[5].name`

```text
lead_temp
```

#### `assignments.assignments[5].value`

```text
={{ $json.pipeline_state || 'warm' }}
```

#### `assignments.assignments[6].name`

```text
message
```

#### `assignments.assignments[6].value`

```text
={{ (() => { const stage = ($json.pipeline_stage || 'MONTHLY').toLowerCase(); const dv = $json.delivery_variants || {}; const touchpoint = dv[stage + '_touchpoint'] || $json.splinter_content || ''; const firstName = $json.first_name || 'them'; const coordinatorName = $json.coordinator_name || 'a teammate'; const agentName = $json.agent_name || 'the team'; const marketName = $json.market_name || 'the local market'; const pref = ($json.contact_preference || '').toLowerCase(); const channel = (pref…[TRUNCATED]
```

#### `assignments.assignments[7].name`

```text
splinter_id
```

#### `assignments.assignments[7].value`

```text
={{ $json.splinter_id }}
```

#### `assignments.assignments[8].name`

```text
splinter_topic
```

#### `assignments.assignments[8].value`

```text
={{ $json.splinter_topic }}
```

#### `assignments.assignments[9].name`

```text
splinter_data_point
```

#### `assignments.assignments[9].value`

```text
={{ $json.splinter_data_point }}
```

#### `assignments.assignments[10].value`

```text
={{ $json.agent_name }}
```

#### `assignments.assignments[11].value`

```text
={{ $json.dominant_theme || 'none' }}
```

#### `assignments.assignments[12].value`

```text
={{ $json.insight_core || '' }}
```

#### `assignments.assignments[13].value`

```text
={{ $json.interpretation || '' }}
```

#### `assignments.assignments[14].name`

```text
behavioral_implication
```

#### `assignments.assignments[14].value`

```text
={{ $json.behavioral_implication || '' }}
```

#### `assignments.assignments[15].name`

```text
escalation_point
```

#### `assignments.assignments[15].value`

```text
={{ ($json.delivery_variants || {}).escalation_talking_point || '' }}
```

### Merge Outbound Context

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.merge` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "numberInputs": 4
}
```

### Get Outbound Agent Config

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `filters.conditions[0].keyValue`

```text
={{ $json.location_id }}
```

### Get Outbound Message History

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.postgres` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `query`

```sql
SELECT ml.*, (SELECT COUNT(*) FROM message_log WHERE contact_id = '{{ $json.contact_id }}') as interaction_count FROM message_log ml WHERE ml.contact_id = '{{ $json.contact_id }}' ORDER BY ml.timestamp DESC LIMIT 15
```

### Get Outbound Conversation Summary

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
conversation_context
```

#### `filters.conditions[0].keyValue`

```text
={{ $json.contact_id }}
```

### Get Outbound Lead Memory

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
leads
```

#### `filters.conditions[0].keyValue`

```text
={{ $json.contact_id }}
```

### Assemble System Prompt

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.code` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `parameters`

```text
{
  "jsCode": "[REDACTED]"
}
```

### AI Agent

| Field | Value |
| --- | --- |
| Type | `@n8n/n8n-nodes-langchain.agent` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `text`

```text
={{ $json.userMessage }}
```

#### `options.systemMessage`

```text
={{ $json.systemPrompt }}
```

### Log Outbound Message

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `tableId`

```text
message_log
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $('Assemble System Prompt').item.json.contactId }}
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $('Assemble System Prompt').item.json.locationId }}
```

#### `fieldsUi.fieldValues[3].fieldId`

```text
message_body
```

#### `fieldsUi.fieldValues[3].fieldValue`

```text
={{ $('Silence Gate').first().json.responseText || $('AI Agent').item.json.output }}
```

#### `fieldsUi.fieldValues[4].fieldValue`

```text
={{ $('Assemble System Prompt').item.json.channelType }}
```

#### `fieldsUi.fieldValues[7].fieldId`

```text
ghl_message_id
```

#### `fieldsUi.fieldValues[7].fieldValue`

```text
={{ $json.messageId }}
```

#### `fieldsUi.fieldValues[8].fieldId`

```text
ghl_conversation_id
```

#### `fieldsUi.fieldValues[8].fieldValue`

```text
={{ $json.conversationId }}
```

#### `fieldsUi.fieldValues[9].fieldValue`

```text
={{ $now.toUTC().toISO() }}
```

### Send SMS

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
https://services.leadconnectorhq.com/conversations/messages
```

#### `specifyBody`

```text
json
```

#### `jsonBody`

```text
={{ JSON.stringify({ type: 'SMS', contactId: $('Assemble System Prompt').first().json.contactId, message: $json.responseText || $('AI Agent').first().json.output }) }}
```

### Send Email

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.httpRequest` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `None` |

#### `url`

```text
https://services.leadconnectorhq.com/conversations/messages
```

#### `specifyBody`

```text
json
```

#### `jsonBody`

```text
={{ (() => { const raw = $json.responseText || $('AI Agent').first().json.output; const contactId = $('Assemble System Prompt').first().json.contactId; const coordinatorEmail = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_email } catch(e) { return $('Get Agent Config').first().json.coordinator_email } })(); const coordinatorName = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name } catch(e) { try { return $('Get Agent Config').fir…[TRUNCATED]
```

### Record Splinter Usage

| Field | Value |
| --- | --- |
| Type | `n8n-nodes-base.supabase` |
| Disabled | `False` |
| Retry on fail | `None` |
| On error | `continueRegularOutput` |

#### `tableId`

```text
splinter_usage
```

#### `fieldsUi.fieldValues[0].fieldId`

```text
splinter_id
```

#### `fieldsUi.fieldValues[0].fieldValue`

```text
={{ $json.splinter_id }}
```

#### `fieldsUi.fieldValues[1].fieldId`

```text
lead_id
```

#### `fieldsUi.fieldValues[1].fieldValue`

```text
={{ $json.lead_id || $json.id }}
```

#### `fieldsUi.fieldValues[2].fieldValue`

```text
={{ $json.channel || 'sms' }}
```

### Update Next Outbound Due

**Status:** Not found in export.

