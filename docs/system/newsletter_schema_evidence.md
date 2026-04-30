# Newsletter Schema Evidence

This local evidence extract summarizes database structures that interact with newsletter generation, dispatch, and splinter delivery.

## agents

| Field | Value |
| --- | --- |
| estimated_rows | `-1` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `market` | `text` | `YES` | `` |
| `active` | `boolean` | `YES` | `true` |
| `market_area` | `text` | `YES` | `` |
| `agent_email` | `text` | `YES` | `` |
| `target_zips` | `ARRAY` | `YES` | `` |
| `market_name` | `text` | `YES` | `` |
| `altos_location_hashes` | `jsonb` | `YES` | `'{}'::jsonb` |
| `newsletter_enabled` | `boolean` | `YES` | `true` |
| `newsletter_day` | `integer` | `YES` | `0` |
| `newsletter_time` | `time without time zone` | `YES` | `'03:00:00'::time without time zone` |
| `newsletters_sent_total` | `integer` | `YES` | `0` |
| `coordinator_email` | `text` | `YES` | `` |
| `county_fips` | `text` | `YES` | `` |
| `altos_pai` | `text` | `YES` | `` |
| `altos_user_id` | `text` | `YES` | `` |
| `altos_account_id` | `text` | `YES` | `` |
| `agent_funnel_active` | `boolean` | `YES` | `true` |
| `agent_website_active` | `boolean` | `YES` | `true` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_26325_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_26325_2_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_26325_3_not_null", "constraint_type": "CHECK"}` |
| `{"columns": ["id"], "constraint_name": "agents_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["location_id"], "constraint_name": "agents_location_id_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE UNIQUE INDEX agents_location_id_key ON public.agents USING btree (location_id)", "indexname": "agents_location_id_key"}` |
| `{"indexdef": "CREATE UNIQUE INDEX agents_pkey ON public.agents USING btree (id)", "indexname": "agents_pkey"}` |
| `{"indexdef": "CREATE INDEX idx_agents_location_id ON public.agents USING btree (location_id)", "indexname": "idx_agents_location_id"}` |
| `{"indexdef": "CREATE INDEX idx_agents_state ON public.agents USING btree (state)", "indexname": "idx_agents_state"}` |

## newsletters

| Field | Value |
| --- | --- |
| estimated_rows | `-1` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `id` | `uuid` | `NO` | `gen_random_uuid()` |
| `agent_id` | `uuid` | `YES` | `` |
| `location_id` | `text` | `NO` | `` |
| `week_start_date` | `date` | `NO` | `` |
| `week_number` | `integer` | `YES` | `` |
| `year` | `integer` | `YES` | `` |
| `full_content` | `text` | `YES` | `` |
| `subject_line` | `text` | `YES` | `` |
| `raw_altos_data` | `jsonb` | `YES` | `` |
| `raw_perplexity_data` | `jsonb` | `YES` | `` |
| `active` | `boolean` | `YES` | `true` |
| `generation_status` | `text` | `YES` | `'pending'::text` |
| `generation_error` | `text` | `YES` | `` |
| `gdrive_file_id` | `text` | `YES` | `` |
| `gdrive_file_url` | `text` | `YES` | `` |
| `created_at` | `timestamp with time zone` | `YES` | `now()` |
| `updated_at` | `timestamp with time zone` | `YES` | `now()` |
| `image_url` | `text` | `YES` | `` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_67365_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_67365_3_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_67365_4_not_null", "constraint_type": "CHECK"}` |
| `{"columns": ["agent_id"], "constraint_name": "newsletters_agent_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "newsletters_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["agent_id", "week_start_date"], "constraint_name": "newsletters_agent_id_week_start_date_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE INDEX idx_newsletters_active ON public.newsletters USING btree (agent_id, active) WHERE (active = true)", "indexname": "idx_newsletters_active"}` |
| `{"indexdef": "CREATE UNIQUE INDEX newsletters_agent_id_week_start_date_key ON public.newsletters USING btree (agent_id, week_start_date)", "indexname": "newsletters_agent_id_week_start_date_key"}` |
| `{"indexdef": "CREATE UNIQUE INDEX newsletters_pkey ON public.newsletters USING btree (id)", "indexname": "newsletters_pkey"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["agent_id"], "constraint_name": "newsletters_agent_id_fkey", "delete_rule": "RESTRICT", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "agents", "update_rule": "NO ACTION"}` |

## newsletter_deliveries

| Field | Value |
| --- | --- |
| estimated_rows | `-1` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `id` | `uuid` | `NO` | `gen_random_uuid()` |
| `newsletter_id` | `uuid` | `YES` | `` |
| `lead_id` | `uuid` | `YES` | `` |
| `contact_id` | `text` | `NO` | `` |
| `location_id` | `text` | `NO` | `` |
| `ghl_message_id` | `text` | `YES` | `` |
| `subject_line` | `text` | `YES` | `` |
| `status` | `text` | `YES` | `'pending'::text` |
| `error_message` | `text` | `YES` | `` |
| `sent_at` | `timestamp with time zone` | `YES` | `` |
| `created_at` | `timestamp with time zone` | `YES` | `now()` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_104922_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_104922_4_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_104922_5_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "valid_delivery_status", "constraint_type": "CHECK"}` |
| `{"columns": ["lead_id"], "constraint_name": "newsletter_deliveries_lead_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["newsletter_id"], "constraint_name": "newsletter_deliveries_newsletter_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "newsletter_deliveries_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["newsletter_id", "lead_id"], "constraint_name": "newsletter_deliveries_newsletter_id_lead_id_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE INDEX idx_newsletter_deliveries_status ON public.newsletter_deliveries USING btree (status)", "indexname": "idx_newsletter_deliveries_status"}` |
| `{"indexdef": "CREATE UNIQUE INDEX newsletter_deliveries_newsletter_id_lead_id_key ON public.newsletter_deliveries USING btree (newsletter_id, lead_id)", "indexname": "newsletter_deliveries_newsletter_id_lead_id_key"}` |
| `{"indexdef": "CREATE UNIQUE INDEX newsletter_deliveries_pkey ON public.newsletter_deliveries USING btree (id)", "indexname": "newsletter_deliveries_pkey"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["lead_id"], "constraint_name": "newsletter_deliveries_lead_id_fkey", "delete_rule": "NO ACTION", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "leads", "update_rule": "NO ACTION"}` |
| `{"columns": ["newsletter_id"], "constraint_name": "newsletter_deliveries_newsletter_id_fkey", "delete_rule": "NO ACTION", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "newsletters", "update_rule": "NO ACTION"}` |

## content_splinters

| Field | Value |
| --- | --- |
| estimated_rows | `34` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `id` | `uuid` | `NO` | `gen_random_uuid()` |
| `newsletter_id` | `uuid` | `YES` | `` |
| `agent_id` | `uuid` | `YES` | `` |
| `content` | `text` | `YES` | `` |
| `topic` | `text` | `YES` | `` |
| `data_point` | `text` | `YES` | `` |
| `active` | `boolean` | `YES` | `true` |
| `priority` | `integer` | `YES` | `0` |
| `created_at` | `timestamp with time zone` | `YES` | `now()` |
| `location_id` | `text` | `YES` | `` |
| `week_start_date` | `date` | `YES` | `` |
| `splinter_title` | `text` | `YES` | `` |
| `dominant_theme` | `text` | `YES` | `` |
| `signal_type` | `text` | `YES` | `` |
| `insight_core` | `text` | `YES` | `` |
| `interpretation` | `text` | `YES` | `` |
| `behavioral_implication` | `text` | `YES` | `` |
| `audience_fit` | `ARRAY` | `YES` | `` |
| `stage_fit` | `ARRAY` | `YES` | `` |
| `relevance_tags` | `ARRAY` | `YES` | `` |
| `send_eligibility_note` | `text` | `YES` | `` |
| `rationale` | `text` | `YES` | `` |
| `source_excerpt` | `text` | `YES` | `` |
| `embedding_text` | `text` | `YES` | `` |
| `delivery_variants` | `jsonb` | `YES` | `` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_67387_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "valid_topic", "constraint_type": "CHECK"}` |
| `{"columns": ["agent_id"], "constraint_name": "content_splinters_agent_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["newsletter_id"], "constraint_name": "content_splinters_newsletter_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "content_splinters_pkey", "constraint_type": "PRIMARY KEY"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE UNIQUE INDEX content_splinters_pkey ON public.content_splinters USING btree (id)", "indexname": "content_splinters_pkey"}` |
| `{"indexdef": "CREATE INDEX idx_content_splinters_location_id ON public.content_splinters USING btree (location_id)", "indexname": "idx_content_splinters_location_id"}` |
| `{"indexdef": "CREATE INDEX idx_splinters_active_location ON public.content_splinters USING btree (location_id, active) WHERE (active = true)", "indexname": "idx_splinters_active_location"}` |
| `{"indexdef": "CREATE INDEX idx_splinters_stage_fit ON public.content_splinters USING gin (stage_fit) WHERE (active = true)", "indexname": "idx_splinters_stage_fit"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["agent_id"], "constraint_name": "content_splinters_agent_id_fkey", "delete_rule": "RESTRICT", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "agents", "update_rule": "NO ACTION"}` |
| `{"columns": ["newsletter_id"], "constraint_name": "content_splinters_newsletter_id_fkey", "delete_rule": "CASCADE", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "newsletters", "update_rule": "NO ACTION"}` |

## splinter_usage

| Field | Value |
| --- | --- |
| estimated_rows | `-1` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `id` | `uuid` | `NO` | `gen_random_uuid()` |
| `splinter_id` | `uuid` | `YES` | `` |
| `lead_id` | `uuid` | `YES` | `` |
| `channel` | `text` | `YES` | `` |
| `message_id` | `uuid` | `YES` | `` |
| `used_at` | `timestamp with time zone` | `YES` | `now()` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_113689_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": ["lead_id"], "constraint_name": "splinter_usage_lead_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["splinter_id"], "constraint_name": "splinter_usage_splinter_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "splinter_usage_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["splinter_id", "lead_id"], "constraint_name": "splinter_usage_splinter_id_lead_id_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE INDEX idx_splinter_usage_lead ON public.splinter_usage USING btree (lead_id)", "indexname": "idx_splinter_usage_lead"}` |
| `{"indexdef": "CREATE INDEX idx_splinter_usage_splinter ON public.splinter_usage USING btree (splinter_id)", "indexname": "idx_splinter_usage_splinter"}` |
| `{"indexdef": "CREATE UNIQUE INDEX splinter_usage_pkey ON public.splinter_usage USING btree (id)", "indexname": "splinter_usage_pkey"}` |
| `{"indexdef": "CREATE UNIQUE INDEX splinter_usage_splinter_id_lead_id_key ON public.splinter_usage USING btree (splinter_id, lead_id)", "indexname": "splinter_usage_splinter_id_lead_id_key"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["lead_id"], "constraint_name": "splinter_usage_lead_id_fkey", "delete_rule": "NO ACTION", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "leads", "update_rule": "NO ACTION"}` |
| `{"columns": ["splinter_id"], "constraint_name": "splinter_usage_splinter_id_fkey", "delete_rule": "NO ACTION", "foreign_column": "id", "foreign_schema": "public", "foreign_table": "content_splinters", "update_rule": "NO ACTION"}` |

## altos_weekly_stats

| Field | Value |
| --- | --- |
| estimated_rows | `-1` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `id` | `uuid` | `NO` | `gen_random_uuid()` |
| `location_id` | `text` | `NO` | `` |
| `week_start_date` | `date` | `NO` | `` |
| `zips_processed` | `integer` | `YES` | `` |
| `total_zips` | `integer` | `YES` | `` |
| `price_median` | `numeric` | `YES` | `` |
| `count` | `integer` | `YES` | `` |
| `per_sqft_median` | `numeric` | `YES` | `` |
| `dom_median` | `numeric` | `YES` | `` |
| `absorbed_price_median` | `numeric` | `YES` | `` |
| `median_ppsqft_absorbed` | `numeric` | `YES` | `` |
| `price_mean` | `numeric` | `YES` | `` |
| `dom_mean` | `numeric` | `YES` | `` |
| `mai` | `numeric` | `YES` | `` |
| `raw_summary` | `jsonb` | `YES` | `` |
| `created_at` | `timestamp with time zone` | `YES` | `now()` |
| `new_price_median` | `numeric` | `YES` | `` |
| `absorbed_dom_median` | `numeric` | `YES` | `` |
| `price_decreased_percent` | `numeric` | `YES` | `` |
| `price_increased_percent` | `numeric` | `YES` | `` |
| `agent_name` | `text` | `YES` | `` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_85558_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_85558_2_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_85558_3_not_null", "constraint_type": "CHECK"}` |
| `{"columns": ["location_id"], "constraint_name": "altos_weekly_stats_location_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "altos_weekly_stats_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["location_id", "week_start_date"], "constraint_name": "altos_weekly_stats_location_id_week_start_date_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE UNIQUE INDEX altos_weekly_stats_location_id_week_start_date_key ON public.altos_weekly_stats USING btree (location_id, week_start_date)", "indexname": "altos_weekly_stats_location_id_week_start_date_key"}` |
| `{"indexdef": "CREATE UNIQUE INDEX altos_weekly_stats_pkey ON public.altos_weekly_stats USING btree (id)", "indexname": "altos_weekly_stats_pkey"}` |
| `{"indexdef": "CREATE INDEX idx_altos_weekly_stats_location ON public.altos_weekly_stats USING btree (location_id)", "indexname": "idx_altos_weekly_stats_location"}` |
| `{"indexdef": "CREATE INDEX idx_altos_weekly_stats_week ON public.altos_weekly_stats USING btree (week_start_date DESC)", "indexname": "idx_altos_weekly_stats_week"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["location_id"], "constraint_name": "altos_weekly_stats_location_id_fkey", "delete_rule": "NO ACTION", "foreign_column": "location_id", "foreign_schema": "public", "foreign_table": "agents", "update_rule": "NO ACTION"}` |

## documents

| Field | Value |
| --- | --- |
| estimated_rows | `50` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `week_start_date` | `date` | `YES` | `` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_51410_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_51410_2_not_null", "constraint_type": "CHECK"}` |
| `{"columns": ["id"], "constraint_name": "documents_pkey", "constraint_type": "PRIMARY KEY"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE INDEX documents_embedding_idx ON public.documents USING ivfflat (embedding vector_cosine_ops) WITH (lists='100')", "indexname": "documents_embedding_idx"}` |
| `{"indexdef": "CREATE UNIQUE INDEX documents_pkey ON public.documents USING btree (id)", "indexname": "documents_pkey"}` |
| `{"indexdef": "CREATE INDEX idx_documents_location_type ON public.documents USING btree (location_id, document_type)", "indexname": "idx_documents_location_type"}` |

## leads

| Field | Value |
| --- | --- |
| estimated_rows | `313` |

### Relevant columns

| Column | Type | Nullable | Default |
| --- | --- | --- | --- |
| `contact_id` | `text` | `NO` | `` |
| `email` | `text` | `YES` | `` |
| `last_value_delivery_at` | `timestamp without time zone` | `YES` | `` |
| `status` | `character varying` | `YES` | `'active_conversation'::character varying` |
| `next_outbound_due_at` | `timestamp with time zone` | `YES` | `` |
| `escalation_status` | `text` | `YES` | `'none'::text` |
| `sms_paused_until` | `timestamp with time zone` | `YES` | `` |
| `market_role` | `text` | `YES` | `'unknown'::text` |
| `contact_preference` | `text` | `YES` | `'unknown'::text` |
| `agent_dormant` | `boolean` | `YES` | `false` |
| `newsletter_opted_in` | `boolean` | `YES` | `false` |
| `newsletter_opted_in_at` | `timestamp with time zone` | `YES` | `` |
| `newsletters_received` | `integer` | `YES` | `0` |
| `send_blocked` | `boolean` | `YES` | `false` |
| `send_blocked_at` | `timestamp with time zone` | `YES` | `` |

### Constraints

| Evidence |
| --- |
| `{"columns": null, "constraint_name": "2200_26339_1_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_26339_2_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "2200_26339_3_not_null", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "chk_pipeline_state", "constraint_type": "CHECK"}` |
| `{"columns": null, "constraint_name": "leads_pipeline_stage_check", "constraint_type": "CHECK"}` |
| `{"columns": ["location_id"], "constraint_name": "leads_location_id_fkey", "constraint_type": "FOREIGN KEY"}` |
| `{"columns": ["id"], "constraint_name": "leads_pkey", "constraint_type": "PRIMARY KEY"}` |
| `{"columns": ["contact_id"], "constraint_name": "leads_contact_id_key", "constraint_type": "UNIQUE"}` |

### Indexes

| Evidence |
| --- |
| `{"indexdef": "CREATE INDEX idx_leads_contact_id ON public.leads USING btree (contact_id)", "indexname": "idx_leads_contact_id"}` |
| `{"indexdef": "CREATE INDEX idx_leads_dormancy_check ON public.leads USING btree (status, last_customer_message_at) WHERE ((status)::text = 'active_conversation'::text)", "indexname": "idx_leads_dormancy_check"}` |
| `{"indexdef": "CREATE INDEX idx_leads_email ON public.leads USING btree (email)", "indexname": "idx_leads_email"}` |
| `{"indexdef": "CREATE INDEX idx_leads_location_id ON public.leads USING btree (location_id)", "indexname": "idx_leads_location_id"}` |
| `{"indexdef": "CREATE INDEX idx_leads_newsletter ON public.leads USING btree (newsletter_opted_in) WHERE (newsletter_opted_in = true)", "indexname": "idx_leads_newsletter"}` |
| `{"indexdef": "CREATE INDEX idx_leads_opt_out_level ON public.leads USING btree (opt_out_level) WHERE (opt_out_level IS NOT NULL)", "indexname": "idx_leads_opt_out_level"}` |
| `{"indexdef": "CREATE INDEX idx_leads_outbound_candidates ON public.leads USING btree (location_id, status, next_outbound_due_at)", "indexname": "idx_leads_outbound_candidates"}` |
| `{"indexdef": "CREATE INDEX idx_leads_phone ON public.leads USING btree (phone)", "indexname": "idx_leads_phone"}` |
| `{"indexdef": "CREATE INDEX idx_leads_pipeline_stage ON public.leads USING btree (pipeline_stage)", "indexname": "idx_leads_pipeline_stage"}` |
| `{"indexdef": "CREATE INDEX idx_leads_sms_paused_until ON public.leads USING btree (sms_paused_until) WHERE (sms_paused_until IS NOT NULL)", "indexname": "idx_leads_sms_paused_until"}` |
| `{"indexdef": "CREATE INDEX idx_leads_status_outbound_due ON public.leads USING btree (status, next_outbound_due_at) WHERE ((status)::text = 'outbound_due'::text)", "indexname": "idx_leads_status_outbound_due"}` |
| `{"indexdef": "CREATE UNIQUE INDEX leads_contact_id_key ON public.leads USING btree (contact_id)", "indexname": "leads_contact_id_key"}` |
| `{"indexdef": "CREATE UNIQUE INDEX leads_pkey ON public.leads USING btree (id)", "indexname": "leads_pkey"}` |

### Foreign Keys

| Evidence |
| --- |
| `{"columns": ["location_id"], "constraint_name": "leads_location_id_fkey", "delete_rule": "RESTRICT", "foreign_column": "location_id", "foreign_schema": "public", "foreign_table": "agents", "update_rule": "NO ACTION"}` |
