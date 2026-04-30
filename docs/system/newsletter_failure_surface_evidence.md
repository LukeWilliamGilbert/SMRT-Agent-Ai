# Newsletter Failure-Surface Evidence

This evidence file is generated from versioned n8n workflow exports. It redacts credential-like fields and focuses on execution settings, gates, storage writes, and delivery ledgers.

## Workflow Counts

| Workflow | File | Node Count |
| --- | --- | ---: |
| `creation` | `workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json` | 37 |
| `dispatch` | `workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json` | 15 |
| `brain` | `workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json` | 174 |

## Target Node Settings

### Creation Workflow

#### Schedule Trigger

```json
_Node not found._
```

#### Fetch Agents

```json
_Node not found._
```

#### Prepare Agent Data

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Check Newsletter For Week`

#### Check Newsletter For Week

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "filterString": "=agent_id=eq.{{ $json.agent_id }}&week_start_date=eq.{{ $json.weekStartDate }}",
    "filterType": "string",
    "limit": 1,
    "operation": "getAll",
    "tableId": "newsletters"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Newsletter Exists For Week?`

#### Check Week Stats Exist

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "filterString": "=location_id=eq.{{ $('Condense Altos Data').first().json.location_id }}&week_start_date=eq.{{ $('Condense Altos Data').first().json.weekStartDate }}",
    "filterType": "string",
    "limit": 1,
    "operation": "getAll",
    "tableId": "altos_weekly_stats"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Week Already Processed?`

#### Altos Get Stats

```json
{
  "continueOnFail": true,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "const agentData = $('Prepare Agent Data').first().json;\nconst targetZips = agentData.target_zips || [];\nconst state = agentData.state;\nconst pai = agentData.pai;\n\nconst countyFips = agentData.county_fips || '16001';\n\nconst stats = [\n  'price_median', 'count', 'per_sqft_median', 'dom_median',\n  'new_price_median',\n  'price_decreased_percent', 'price_increased_percent',\n  'price_mean', 'dom_mean', 'mai'\n];\n\nconst allZipData = [];\nconst errors = [];\n\ntry {\n  const reportsResp = await globalThis.fet…[TRUNCATED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Condense Altos Data`

#### Condense Altos Data

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Check Week Stats Exist`

#### Grok National Context

```json
{
  "continueOnFail": true,
  "disabled": false,
  "onError": null,
  "parameters": {
    "authentication": "[REDACTED]",
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "jsonBody": "[REDACTED]",
    "method": "POST",
    "nodeCredentialType": "[REDACTED]",
    "options": {
      "timeout": 30000
    },
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://api.x.ai/v1/chat/completions"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Get Previous Newsletters`

#### Prep Data for AI

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "const condensedData = $('Condense Altos Data').first().json;\nconst grokResponse = $('Grok National Context').first().json;\n\nlet nationalContext = '';\nif (grokResponse.choices && grokResponse.choices[0]?.message?.content) {\n  nationalContext = grokResponse.choices[0].message.content;\n} else if (grokResponse.message?.content) {\n  nationalContext = grokResponse.message.content;\n} else if (grokResponse.content) {\n  nationalContext = grokResponse.content;\n}\n\n// Previous newsletters for week-over-week…[TRUNCATED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Generate Newsletter`

#### Generate Newsletter

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "messages": {
      "values": [
        {
          "content": "=## Agent Context\n\nYou are writing on behalf of **{{ $('Prepare Agent Data').first().json.agent.agent_name }}**{{ $('Prepare Agent Data').first().json.agent.business_name ? ', ' + $('Prepare Agent Data').first().json.agent.business_name : '' }}, serving the **{{ $json.market_name }}** real estate market.\n\n---\n\n## Who You Are\n\nYou are a trusted local advisor writing to real people -- buyers, sellers, homeowners, and curious neighbors. You are NOT a research analyst writing a market report. Your t…[TRUNCATED]",
          "role": "system"
        },
        {
          "content": "=Generate a weekly market newsletter for **{{ $json.market_name }}**.\n\n## Local Market Data (Altos Research)\n{{ JSON.stringify($json.altos_data, null, 2) }}\n\n## National/Global Context & Local Impact\n{{ JSON.stringify($json.perplexity_data, null, 2) }}\n\n## Previous Newsletters (last 2 weeks -- for continuity and week-over-week context)\n{{ $json.previous_newsletters && $json.previous_newsletters.length > 0 ? JSON.stringify($json.previous_newsletters, null, 2) : 'No previous newsletters available …[TRUNCATED]"
        }
      ]
    },
    "modelId": "gpt-4.1",
    "options": {
      "temperature": 0.7
    }
  },
  "retryOnFail": null,
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

Downstream nodes: `Get Altos Hash`

#### Extract Splinters

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "messages": {
      "values": [
        {
          "content": "SMRT NEWSLETTER SPLINTER LAYER - CANONICAL RECORD GENERATOR\n\nYou are a post-newsletter processing layer inside the SMRT system. Your job is to take a completed weekly real estate market newsletter and convert it into a small set of structured market splinter records.\n\nPRIMARY OBJECTIVE: Convert one completed newsletter into 3 to 5 canonical market splinter records.\n\nEach splinter record should:\n1. capture one distinct market shift, tension, or behavioral insight\n2. be semantically rich enough fo…[TRUNCATED]",
          "role": "system"
        },
        {
          "content": "=newsletter_id: pending\nmarket: {{ $('Prep Data for AI').first().json.market_name }}\nnewsletter_date: {{ $('Prep Data for AI').first().json.weekStartDate }}\n\nWeek-over-week market data:\n{{ $('Condense Altos Data').first().json.altosTextSummary }}\n\nRaw WoW changes:\n{{ JSON.stringify($('Condense Altos Data').first().json.wowChanges) }}\n\nFull newsletter text:\n{{ $('Generate Newsletter').first().json.message.content }}"
        }
      ]
    },
    "modelId": "gpt-4.1",
    "options": {
      "maxTokens": "[REDACTED]",
      "temperature": 0.3
    }
  },
  "retryOnFail": null,
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

Downstream nodes: `Prepare Storage Data`

#### Store Newsletter

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "fieldsUi": {
      "fieldValues": [
        {
          "fieldId": "agent_id",
          "fieldValue": "={{ $json.newsletter.agent_id }}"
        },
        {
          "fieldId": "location_id",
          "fieldValue": "={{ $json.newsletter.location_id }}"
        },
        {
          "fieldId": "week_start_date",
          "fieldValue": "={{ $json.newsletter.week_start_date }}"
        },
        {
          "fieldId": "full_content",
          "fieldValue": "={{ $json.newsletter.full_content }}"
        },
        {
          "fieldId": "subject_line",
          "fieldValue": "={{ $json.newsletter.subject_line }}"
        },
        {
          "fieldId": "raw_altos_data",
          "fieldValue": "={{ JSON.stringify($json.newsletter.raw_altos_data) }}"
        },
        {
          "fieldId": "raw_perplexity_data",
          "fieldValue": "={{ JSON.stringify($json.newsletter.raw_perplexity_data) }}"
        },
        {
          "fieldId": "image_url",
          "fieldValue": "={{ $json.newsletter.image_url }}"
        },
        {
          "fieldId": "active",
          "fieldValue": "=true"
        },
        {
          "fieldId": "generation_status",
          "fieldValue": "=completed"
        }
      ]
    },
    "tableId": "newsletters"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Create Newsletter Doc`

#### Delete Old Splinters

```json
{
  "continueOnFail": true,
  "disabled": false,
  "onError": null,
  "parameters": {
    "fieldsUi": {
      "fieldValues": [
        {
          "fieldId": "active",
          "fieldValue": "false"
        }
      ]
    },
    "filterString": "location_id=eq.{{ $json.location_id }}&active=eq.true",
    "filterType": "string",
    "operation": "update",
    "tableId": "content_splinters"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

#### Store Splinter

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "fieldsUi": {
      "fieldValues": [
        {
          "fieldId": "location_id",
          "fieldValue": "={{ $json.splinter.location_id }}"
        },
        {
          "fieldId": "content",
          "fieldValue": "={{ $json.splinter.content }}"
        },
        {
          "fieldId": "topic",
          "fieldValue": "={{ $json.splinter.topic }}"
        },
        {
          "fieldId": "data_point",
          "fieldValue": "={{ $json.splinter.data_point }}"
        },
        {
          "fieldId": "active",
          "fieldValue": "true"
        },
        {
          "fieldId": "priority",
          "fieldValue": "={{ $json.splinter.priority }}"
        },
        {
          "fieldId": "week_start_date",
          "fieldValue": "={{ $json.splinter.week_start_date }}"
        },
        {
          "fieldId": "splinter_title",
          "fieldValue": "={{ $json.splinter.splinter_title }}"
        },
        {
          "fieldId": "dominant_theme",
          "fieldValue": "={{ $json.splinter.dominant_theme }}"
        },
        {
          "fieldId": "signal_type",
          "fieldValue": "={{ $json.splinter.signal_type }}"
        },
        {
          "fieldId": "insight_core",
          "fieldValue": "={{ $json.splinter.insight_core }}"
        },
        {
          "fieldId": "interpretation",
          "fieldValue": "={{ $json.splinter.interpretation }}"
        },
        {
          "fieldId": "behavioral_implication",
          "fieldValue": "={{ $json.splinter.behavioral_implication }}"
        },
        {
          "fieldId": "audience_fit",
          "fieldValue": "={{ $json.splinter.audience_fit }}"
        },
        {
          "fieldId": "stage_fit",
          "fieldValue": "={{ $json.splinter.stage_fit }}"
        },
        {
          "fieldId": "relevance_tags",
          "fieldValue": "={{ $json.splinter.relevance_tags }}"
        },
        {
          "fieldId": "send_eligibility_note",
          "fieldValue": "={{ $json.splinter.send_eligibility_note }}"
        },
        {
          "fieldId": "rationale",
          "fieldValue": "={{ $json.splinter.rationale }}"
        },
        {
          "fieldId": "source_excerpt",
          "fieldValue": "={{ $json.splinter.source_excerpt }}"
        },
        {
          "fieldId": "embedding_text",
          "fieldValue": "={{ $json.splinter.embedding_text }}"
        },
        {
          "fieldId": "delivery_variants",
          "fieldValue": "={{ JSON.stringify($json.splinter.delivery_variants) }}"
        }
      ]
    },
    "tableId": "content_splinters"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Back to Agent Loop`

#### Store Weekly Stats

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "fieldsUi": {
      "fieldValues": [
        {
          "fieldId": "location_id",
          "fieldValue": "={{ $('Condense Altos Data').first().json.location_id }}"
        },
        {
          "fieldId": "week_start_date",
          "fieldValue": "={{ $('Condense Altos Data').first().json.weekStartDate }}"
        },
        {
          "fieldId": "zips_processed",
          "fieldValue": "={{ $('Condense Altos Data').first().json.zipsProcessed }}"
        },
        {
          "fieldId": "total_zips",
          "fieldValue": "={{ $('Condense Altos Data').first().json.totalZips }}"
        },
        {
          "fieldId": "price_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.price_median?.current }}"
        },
        {
          "fieldId": "count",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.count?.current }}"
        },
        {
          "fieldId": "per_sqft_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.per_sqft_median?.current }}"
        },
        {
          "fieldId": "dom_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.dom_median?.current }}"
        },
        {
          "fieldId": "absorbed_price_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.absorbed_price_median?.current }}"
        },
        {
          "fieldId": "absorbed_dom_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.absorbed_dom_median?.current }}"
        },
        {
          "fieldId": "median_ppsqft_absorbed",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.median_ppsqft_of_listings_absorbed?.current }}"
        },
        {
          "fieldId": "new_price_median",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.new_price_median?.current }}"
        },
        {
          "fieldId": "price_decreased_percent",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.price_decreased_percent?.current }}"
        },
        {
          "fieldId": "price_increased_percent",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.price_increased_percent?.current }}"
        },
        {
          "fieldId": "price_mean",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.price_mean?.current }}"
        },
        {
          "fieldId": "dom_mean",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.dom_mean?.current }}"
        },
        {
          "fieldId": "mai",
          "fieldValue": "={{ $('Condense Altos Data').first().json.altosSummary.mai?.current }}"
        },
        {
          "fieldId": "raw_summary",
          "fieldValue": "={{ JSON.stringify($('Condense Altos Data').first().json.altosSummary) }}"
        }
      ]
    },
    "tableId": "altos_weekly_stats"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Grok National Context`

#### Generate Embedding

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "authentication": "[REDACTED]",
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "jsonBody": "={{ JSON.stringify({ model: 'text-embedding-3-small', input: $json.market_doc.content }) }}",
    "method": "POST",
    "nodeCredentialType": "[REDACTED]",
    "options": {},
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://api.openai.com/v1/embeddings"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Store Embedded Doc`

#### Store Embedded Doc

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "authentication": "[REDACTED]",
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        },
        {
          "name": "Prefer",
          "value": "return=representation"
        }
      ]
    },
    "jsonBody": "={{ (() => { const doc = $('Prepare Storage Data').item.json.market_doc; const emb = $json.data[0].embedding; return JSON.stringify({ content: doc.content, metadata: doc.metadata, embedding: '[' + emb.join(',') + ']', location_id: doc.location_id, document_type: 'market_weekly', week_start_date: doc.week_start_date }); })() }}",
    "method": "POST",
    "nodeCredentialType": "[REDACTED]",
    "options": {},
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://kfoijgcbkjeizxxyiwxv.supabase.co/rest/v1/documents"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Back to Agent Loop`

### Dispatch Workflow

#### Weekly Schedule

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
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
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.scheduleTrigger"
}
```

Downstream nodes: `Fetch Active Agents`

#### Fetch Active Agents

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "filters": {
      "conditions": [
        {
          "condition": "eq",
          "keyName": "newsletter_enabled",
          "keyValue": "true"
        }
      ]
    },
    "matchType": "allFilters",
    "operation": "getAll",
    "returnAll": true,
    "tableId": "agents"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Stamp Supabase Key`

#### Get Newest Newsletter

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Newsletter Found?`

#### Fetch Eligible Leads

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Has Eligible Leads?`

#### Build HTML Email

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Send Email via GHL`

#### Send Email via GHL

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": "continueRegularOutput",
  "parameters": {
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
    "jsonBody": "={\n  \"type\": \"Email\",\n  \"contactId\": \"{{ $json.contact_id }}\",\n  \"emailFrom\": \"{{ $json.coordinatorEmail }}\",\n  \"html\": {{ JSON.stringify($json.html) }},\n  \"subject\": \"{{ $json.subject }}\"\n}",
    "method": "POST",
    "options": {},
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://services.leadconnectorhq.com/conversations/messages"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Log Delivery`

#### Log Delivery

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "fieldsUi": {
      "fieldValues": [
        {
          "fieldId": "newsletter_id",
          "fieldValue": "={{ $('Build HTML Email').first().json.newsletterId }}"
        },
        {
          "fieldId": "lead_id",
          "fieldValue": "={{ $('Build HTML Email').first().json.id }}"
        },
        {
          "fieldId": "contact_id",
          "fieldValue": "={{ $('Build HTML Email').first().json.contact_id }}"
        },
        {
          "fieldId": "location_id",
          "fieldValue": "={{ $('Get Newest Newsletter').first().json.location_id }}"
        },
        {
          "fieldId": "subject_line",
          "fieldValue": "={{ $('Build HTML Email').first().json.subject }}"
        },
        {
          "fieldId": "status",
          "fieldValue": "sent"
        },
        {
          "fieldId": "sent_at",
          "fieldValue": "={{ new Date().toISOString() }}"
        }
      ]
    },
    "tableId": "newsletter_deliveries"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.supabase"
}
```

Downstream nodes: `Update Send Counts`

#### Update Send Counts

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "jsCode": "[REDACTED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.code"
}
```

Downstream nodes: `Loop Agents`

#### Newsletter Found?

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "conditions": {
      "combinator": "and",
      "conditions": [
        {
          "id": "nl-skip-check",
          "leftValue": "={{ $json._skip }}",
          "operator": {
            "operation": "false",
            "singleValue": true,
            "type": "boolean"
          },
          "rightValue": ""
        }
      ],
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "loose",
        "version": 2
      }
    },
    "options": {}
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.if"
}
```

Downstream nodes: `Fetch Eligible Leads`, `Loop Agents`

#### Has Eligible Leads?

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "conditions": {
      "combinator": "and",
      "conditions": [
        {
          "id": "eligible-check",
          "leftValue": "={{ $json._skip }}",
          "operator": {
            "operation": "false",
            "singleValue": true,
            "type": "boolean"
          },
          "rightValue": ""
        }
      ],
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "strict",
        "version": 2
      }
    },
    "options": {}
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.if"
}
```

Downstream nodes: `Build HTML Email`, `Loop Agents`

### Brain Workflow

#### Schedule Outbound Check

```json
{
  "continueOnFail": null,
  "disabled": true,
  "onError": null,
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 3
        }
      ]
    }
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.scheduleTrigger"
}
```

Downstream nodes: `Business Hours Check`

#### Fetch Outbound Candidates

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "operation": "executeQuery",
    "options": {},
    "query": "WITH eligible_splinter AS (\n  SELECT\n    cs.id AS splinter_id,\n    cs.location_id,\n    cs.content AS splinter_content,\n    cs.topic AS splinter_topic,\n    cs.data_point AS splinter_data_point,\n    cs.splinter_title,\n    cs.dominant_theme,\n    cs.signal_type,\n    cs.insight_core,\n    cs.interpretation,\n    cs.behavioral_implication,\n    cs.audience_fit,\n    cs.stage_fit,\n    cs.embedding_text,\n    cs.delivery_variants,\n    cs.priority,\n    cs.week_start_date,\n    cs.created_at\n  FROM content_spli…[TRUNCATED]"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.postgres"
}
```

Downstream nodes: `Set Outbound Context`

#### Set Outbound Context

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "1",
          "name": "direction",
          "type": "string",
          "value": "outbound"
        },
        {
          "id": "2",
          "name": "channel",
          "type": "string",
          "value": "={{ $json.channel || 'sms' }}"
        },
        {
          "id": "3",
          "name": "contact_id",
          "type": "string",
          "value": "={{ $json.contact_id }}"
        },
        {
          "id": "4",
          "name": "location_id",
          "type": "string",
          "value": "={{ $json.location_id }}"
        },
        {
          "id": "5",
          "name": "first_name",
          "type": "string",
          "value": "={{ $json.first_name }}"
        },
        {
          "id": "6",
          "name": "lead_temp",
          "type": "string",
          "value": "={{ $json.pipeline_state || 'warm' }}"
        },
        {
          "id": "7",
          "name": "message",
          "type": "string",
          "value": "={{ (() => { const stage = ($json.pipeline_stage || 'MONTHLY').toLowerCase(); const dv = $json.delivery_variants || {}; const touchpoint = dv[stage + '_touchpoint'] || $json.splinter_content || ''; const firstName = $json.first_name || 'them'; const coordinatorName = $json.coordinator_name || 'a teammate'; const agentName = $json.agent_name || 'the team'; const marketName = $json.market_name || 'the local market'; const pref = ($json.contact_preference || '').toLowerCase(); const channel = (pref…[TRUNCATED]"
        },
        {
          "id": "8",
          "name": "splinter_id",
          "type": "string",
          "value": "={{ $json.splinter_id }}"
        },
        {
          "id": "9",
          "name": "splinter_topic",
          "type": "string",
          "value": "={{ $json.splinter_topic }}"
        },
        {
          "id": "10",
          "name": "splinter_data_point",
          "type": "string",
          "value": "={{ $json.splinter_data_point }}"
        },
        {
          "id": "11",
          "name": "agent_name",
          "type": "string",
          "value": "={{ $json.agent_name }}"
        },
        {
          "id": "12",
          "name": "situation",
          "type": "string",
          "value": "={{ $json.dominant_theme || 'none' }}"
        },
        {
          "id": "13",
          "name": "insight_core",
          "type": "string",
          "value": "={{ $json.insight_core || '' }}"
        },
        {
          "id": "14",
          "name": "interpretation",
          "type": "string",
          "value": "={{ $json.interpretation || '' }}"
        },
        {
          "id": "15",
          "name": "behavioral_implication",
          "type": "string",
          "value": "={{ $json.behavioral_implication || '' }}"
        },
        {
          "id": "16",
          "name": "escalation_point",
          "type": "string",
          "value": "={{ ($json.delivery_variants || {}).escalation_talking_point || '' }}"
        }
      ]
    },
    "options": {}
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.set"
}
```

Downstream nodes: `Get Outbound Agent Config`, `Get Outbound Message History`, `Get Outbound Conversation Summary`, `Get Outbound Lead Memory`

#### Send SMS

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
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
    "jsonBody": "={{ JSON.stringify({ type: 'SMS', contactId: $('Assemble System Prompt').first().json.contactId, message: $json.responseText || $('AI Agent').first().json.output }) }}",
    "method": "POST",
    "options": {},
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://services.leadconnectorhq.com/conversations/messages"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Log Outbound Message`, `Post-Farewell DND Gate`

#### Send Email

```json
{
  "continueOnFail": null,
  "disabled": false,
  "onError": null,
  "parameters": {
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
    "jsonBody": "={{ (() => { const raw = $json.responseText || $('AI Agent').first().json.output; const contactId = $('Assemble System Prompt').first().json.contactId; const coordinatorEmail = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_email } catch(e) { return $('Get Agent Config').first().json.coordinator_email } })(); const coordinatorName = (() => { try { return $('Get Outbound Agent Config').first().json.coordinator_name } catch(e) { try { return $('Get Agent Config').fir…[TRUNCATED]",
    "method": "POST",
    "options": {},
    "sendBody": true,
    "sendHeaders": true,
    "specifyBody": "json",
    "url": "https://services.leadconnectorhq.com/conversations/messages"
  },
  "retryOnFail": null,
  "type": "n8n-nodes-base.httpRequest"
}
```

Downstream nodes: `Log Outbound Message`

#### Log Splinter Usage

```json
_Node not found._
```

#### Update Lead After Outbound

```json
_Node not found._
```


## Cross-Cutting Search Evidence

| Needle | Workflows / Nodes Found |
| --- | --- |
| `raw_perplexity_data` | `creation`: `Store Newsletter` |
| `nationalContext` | `creation`: `Prep Data for AI` |
| `newsletter_enabled` | `dispatch`: `Fetch Active Agents`, `Sticky Note - Trigger` |
| `generation_status` | `creation`: `Store Newsletter` |
| `status` | `creation`: `Store Newsletter`; `dispatch`: `Log Delivery`, `Sticky Note - Send & Log`; `brain`: `Log Outbound Message`, `Apply Time Decay`, `Update Lead Escalation`, `Fetch Outbound Note`, `getContact`, `Turnaround: Clear State`, `Turnaround: Disable DND`, `Apply L1: Mark Lead`, `Apply L1: Enable DND`, `Apply L2: Mark Lead`, `Apply L2: Enable DND` |
| `sent` | `creation`: `Splinter Info`, `Store Embedded Doc`; `dispatch`: `Log Delivery`, `Sticky Note - Send & Log`; `brain`: `AI Sentiment Analysis`, `Update Lead Escalation`, `Update Conversation Context`, `Prepare Tier Response`, `Tier Sub-Router1`, `Insert Conversation Context`, `Block Level Router`, `Send Farewell?`, `Apply L1: Mark Lead`, `Apply L1: Post Note`, `Apply L2: Mark Lead`, `Apply L2: Post Note` |
| `content_splinters` | `creation`: `Store Splinter`, `Delete Old Splinters` |
| `splinter_usage` | `brain`: `Record Splinter Usage` |
| `delivery_variants` | `creation`: `Store Splinter`; `brain`: `Fetch Outbound Candidates`, `Set Outbound Context` |

## Initial Failure Hypotheses From Settings

| Finding | Evidence | Why It Matters |
| --- | --- | --- |
| GHL email send may continue after API failure. | `Send Email via GHL` has `onError=continueRegularOutput` and downstream `['Log Delivery']`. | If downstream logging treats continued output as success, send ledgers can become false positives. |
| Delivery logging can be downstream of a failed send. | `Log Delivery` node exists with parameters `{"tableId": "newsletter_deliveries", "fieldsUi": {"fieldValues": [{"fieldId": "newsletter_id", "fieldValue": "={{ $('Build HTML Email').first().json.newsletterId }}"}, {"fieldId": "lead_id", "fieldValue": "={{ $('Build HTML Email').first().json.id }}"}, {"fieldId": "contact_id", "fieldValue": "={{ $('Build HTML Email').first().json.contact_id }}"},`. | A false `sent` row can suppress resends because `newsletter_deliveries` is a cadence ledger. |
| SMS splinter scheduler is disabled in the Brain Engine export. | `Schedule Outbound Check` has `disabled=True`. | The splinter path may exist structurally without being actively scheduled from this workflow. |
| Altos fetch is configured to continue on failure. | `Altos Get Stats` has `continueOnFail=True` and downstream `['Condense Altos Data']`. | Market data gaps may flow into newsletter generation unless downstream validation blocks bad inputs. |