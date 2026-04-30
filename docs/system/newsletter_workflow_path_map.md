# SMRT Newsletter Workflow Path Map

This interim map records the observed path of the newsletter system from the versioned workflow exports and schema evidence. It is not the final audit conclusion; it is the working architecture map used to identify likely failure surfaces.

## Executive Path Summary

The newsletter system is not a single workflow. It is implemented across three separate surfaces: an active 37-node newsletter creation workflow, an active 15-node newsletter dispatch workflow, and newsletter-derived SMS/email splinter delivery surfaces embedded inside the much larger 174-node Brain Engine. The generation workflow pulls agent configuration, fetches Altos market data, requests macro context from xAI/Grok, generates a full newsletter with OpenAI, extracts structured splinters with OpenAI, then persists newsletters, weekly stats, content splinters, a market document, embeddings, and storage images. The dispatch workflow separately sends the newest newsletter by email through GoHighLevel and logs delivery records. The small-message splinter path appears to be part of the Brain Engine outbound path, but its schedule trigger is disabled in the export, which means splinter delivery may depend on another trigger path or may not be actively scheduled from this export.[1] [2] [3]

| Business Expectation | Observed Implementation | Audit Implication |
| --- | --- | --- |
| Pull distinct local market data points. | The creation workflow calls Altos using agent-level `target_zips`, `county_fips`, `pai`, and related agent fields, then condenses data into weekly stats and newsletter inputs.[1] [4] | The basic local-data path exists, but its quality depends on agent configuration completeness and Altos fetch/condense error handling. |
| Layer in macroeconomic overview from xAI. | The workflow contains a `Grok National Context` HTTP request to `https://api.x.ai/v1/chat/completions`, then maps returned content into `nationalContext` and later into `raw_perplexity_data`/macro context fields.[1] | The macro layer exists, but naming drift remains: workflow evidence refers to Grok/xAI while downstream prompt/data names still use `perplexity_data` and `raw_perplexity_data`. |
| Build a complete newsletter. | OpenAI `Generate Newsletter` receives local Altos data, national/global context, and prior newsletters for continuity.[1] | The assembly path exists and is reasonably aligned with the intended product concept. |
| Store reusable market memory. | The workflow stores the newsletter, weekly stats, a `market_weekly` document, an embedding, and 3–5 content splinters.[1] [4] | The system is trying to make the newsletter reusable by the Brain Engine rather than treating it as one-off email copy. |
| Email the newsletter through GoHighLevel. | A separate weekly dispatch workflow sends `type: Email` to GoHighLevel conversations/messages and then inserts a row into `newsletter_deliveries`.[2] | The email delivery path exists, but success/failure handling must be audited carefully because the send node continues on error before logging. |
| Splinter the newsletter into small SMS-ready deliverables. | The generation workflow extracts canonical splinter records with `delivery_variants`; the Brain Engine outbound candidate query selects active splinters and turns a stage-specific variant into outbound context.[1] [3] | The data architecture supports this, but Brain Engine outbound scheduling is disabled in the export and therefore must be verified before assuming delivery is live. |

## Observed Data and Persistence Flow

The generation flow starts on a daily schedule at hour 3 and fetches all agents from `agents`, rather than only filtering newsletter-enabled agents at the first node. It then performs agent preparation, checks whether a newsletter and weekly Altos stats exist for the week, fetches Altos stats, condenses them, calls xAI/Grok for macro context, prepares AI input, generates a newsletter, extracts splinters, stores the newsletter, stores splinters, stores weekly stats, creates an embeddable market document, and uploads assets.[1]

| Storage Surface | What It Stores | Notable Constraint or Risk |
| --- | --- | --- |
| `newsletters` | Full content, subject line, raw Altos data, raw macro context, image URL, status, active flag. | Unique on `(agent_id, week_start_date)`, so duplicate generation attempts can fail or skip depending on branch behavior.[4] |
| `altos_weekly_stats` | Condensed weekly market metrics by location and week. | Unique on `(location_id, week_start_date)`, so location-level collisions matter when multiple agents share a location.[4] |
| `content_splinters` | SMS/email micro-insights, structured market signal fields, delivery variants, and stage/audience fit. | Has active-location index but no uniqueness constraint on newsletter or content; old active splinters are marked inactive by location.[4] |
| `documents` | Embedded `market_weekly` document for retrieval. | Stored through an HTTP request to Supabase REST after embedding generation, making this a separate persistence path from native Supabase nodes.[1] [4] |
| `newsletter_deliveries` | Per-lead newsletter send ledger. | Unique on `(newsletter_id, lead_id)`; false positive logging can suppress later valid sends.[2] [4] |
| `splinter_usage` | Per-lead splinter-use ledger. | Unique on `(splinter_id, lead_id)`, which is useful for anti-repeat behavior if writes are correctly sequenced.[4] |

## Observed Email Dispatch Flow

The email dispatch flow runs weekly on Monday at 10, fetches agents where `newsletter_enabled = true`, selects the newest newsletter for each agent, filters eligible leads by newsletter opt-in and cadence, builds HTML email, sends the email through GoHighLevel, logs a `newsletter_deliveries` row, and updates send counts.[2] The workflow notes explicitly describe cadence behavior: weekly for `WEEKLY`, `APPT_SET`, and `APPT_OFFERED`; biweekly for `BIWEEKLY`; and monthly for `MONTHLY` or cold leads.[2]

The strongest structural concern in this path is that the `Send Email via GHL` node has `onError: continueRegularOutput`, while `Log Delivery` is immediately downstream and writes the send ledger. Unless the code inspects the actual GoHighLevel response and writes `status=failed` on failure, this can create a false delivery record.[2] Because `newsletter_deliveries` has a unique `(newsletter_id, lead_id)` constraint, one false positive can also block a later resend attempt for the same newsletter and lead.[4]

## Observed SMS and Splinter Delivery Flow

The SMS splinter concept is present but less cleanly bounded than email dispatch. The creation workflow produces `content_splinters` with `delivery_variants`, `stage_fit`, `audience_fit`, `send_eligibility_note`, `rationale`, and other fields.[1] The Brain Engine contains a `Fetch Outbound Candidates` SQL node that selects active splinters and eligible leads, a `Set Outbound Context` node that chooses a stage-specific delivery variant or falls back to splinter content, and downstream GHL `Send SMS` / `Send Email` nodes.[3]

However, the Brain Engine `Schedule Outbound Check` trigger is disabled in the export. That does not prove SMS splinters never send, because another trigger or manual execution may feed the path. It does mean the audit should not treat the SMS splinter delivery path as proven live until the development team confirms the runtime trigger strategy or enables a dedicated outbound-splinter workflow.[3]

## Key Open Questions for Failure Analysis

The next phase should validate whether agent filtering, Altos failures, xAI/Grok failures, JSON parsing of generated splinters, duplicate constraints, dispatch success logging, and disabled outbound scheduling are currently producing broken or misleading runtime behavior. The highest-value question is not whether the newsletter idea exists in the workflow; it does. The highest-value question is whether the workflow has enough guards and ledgers to prove that each stage succeeded before downstream delivery or suppression state is written.

## References

[1]: workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json "Data Source & Newsletter Creation workflow export"
[2]: workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json "Newsletter Dispatch workflow export"
[3]: workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json "SMRT Brain Engine workflow export"
[4]: data/supabase/schema_inventory_clean.json "Supabase schema inventory"
