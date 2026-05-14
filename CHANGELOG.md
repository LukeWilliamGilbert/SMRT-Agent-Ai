# SMRT Agent AI Change Log
Author: **Manus AI**

## 2026-05-14 — End-to-End Onboarding Wiring

**Goal:** Admin pastes transcript → Portrait Builder runs → admin clicks Send Homework → agent receives email with clickable button → agent opens homework form to review portrait, approve characteristics, and complete their profile.

### Portrait Builder (`MUewekoBJkI5z4Zv`) — Stage 5 patch
- Stage 5 now reads `anchor.submission_id` from the incoming webhook payload
- `portrait_versions` rows are now inserted using `smrt_saas_submissions.id` as the FK (not `onboarding_requests.id`)
- `portrait_versions_submission_id` returned in Stage 5 response so admin dashboard can use it without a separate lookup
- Workflow redeployed and active

### Admin Dashboard (`agent-connect-dashboard`) — Onboarding tab rewrite
- Added `@supabase/supabase-js` client with persistent session (`storageKey: smrt_sb_auth`) — shares auth state with `admin.smrtagent.ai`
- Added **Submission ID** input field (UUID from `smrt_saas_submissions` — required for homework-send)
- Auto-populated from Portrait Builder response (`portrait_versions_submission_id`) when available
- **Send Homework** button now calls `POST /functions/v1/homework-send` with admin JWT + `{ submission_id }`
  - Creates `agent_homework_packets` row with secure token
  - Sends agent a clean HTML email with a prominent "Finish onboarding" button
  - Link expires in 24 hours
- Removed old `homework-email` n8n webhook call entirely
- Admin auth status indicator in header (green dot = signed in, amber warning = not signed in)
- Friendly error messages for all `homework-send` error codes
- Committed to `LukeWilliamGilbert/agent-connect-dashboard` (commit `6901f8d`)

### What the agent receives
The `homework-send` edge function sends a clean, minimal HTML email:
- Subject: `{FirstName}, finish your SMRT onboarding (5 min)`
- Body: brief intro + prominent blue "Finish onboarding" button
- Button opens `https://admin.smrtagent.ai/h/{token}`
- The homework form (`h/index.html`) lets the agent:
  1. Review and approve (or request revisions to) their portrait
  2. Review and approve (or request revisions to) their characteristics brief
  3. Fill in contact info, scheduling preferences, A2P registration
  4. Submit — writes back to `smrt_saas_submissions.payload` and `agents` table

### Remaining gap
- The `smrt_saas_submissions` record must have `payload.agent_info.agent_email` populated before `homework-send` is called. If the email is blank, the send will fail with `missing_agent_email`. Admin should verify the email in the Submissions tab before clicking Send Homework.

---

## 2026-05-14 — Portrait Builder v2: Full Agent Review Loop + portrait_versions Integration

### Updated — Portrait Builder Workflow (`MUewekoBJkI5z4Zv`) — v2

Redeployed the Portrait Builder with a revised portrait tone and an additional Stage 5 write to `portrait_versions`. The workflow now seeds two v1 draft rows (section: `portrait` and section: `characteristics`) immediately after generating content, so the homework form can load the agent's portrait without any additional REST calls.

**Portrait tone change:** Autobiography style — personal, honest, grounded. No metaphors, no "journey", no inspirational framing, no Hallmark card language. The compiler prompt now enforces a strict anti-metaphor rule and matches prose energy to the individual agent's character (reserved → measured prose; high-energy → shorter sentences; no-nonsense → plain direct language).

**Stage 5 additions:**
- After inserting to `onboarding_requests.bio_template`, Stage 5 now inserts two rows into `portrait_versions` (`section: 'portrait'`, `section: 'characteristics'`, both `version: 1`, `status: 'draft'`).
- Non-fatal: if `portrait_versions` insert fails, the main record is already saved and a warning is logged.
- Output now includes `portrait_versions_seeded: true` and `pipeline_version: 'portrait_builder_v2'`.

Workflow JSON updated in `workflows/active/Portrait_Builder__MUewekoBJkI5z4Zv.json`.

### Added — Revise Section Workflow (`9VT3BXntmB1DhpHF`)

New webhook-triggered n8n workflow that accepts agent revision notes and regenerates a single section (portrait or characteristics) without re-running the full pipeline.

**Webhook:** `POST https://twodegreesnorth.tech/webhook/portrait-revise`

**Payload:** `{ section: 'portrait'|'characteristics', current_content, agent_notes, submission_id }`

**Pipeline:**
1. Validate input — checks required fields, computes `current_version` from `portrait_versions` table
2. Build OpenAI request — runs only the relevant compiler (Stage 4A or 4B) with agent notes injected into the prompt
3. Parse + persist — inserts new row into `portrait_versions` with `version: current_version + 1`, `status: 'draft'`, `agent_notes` stored for audit trail

Response: `{ success, submission_id, section, version, content, record_id }`

### Added — Homework Form Biography + Characteristics Review Steps (`h/index.html`)

Committed to `SmrtGuys/smrt-command-centre` (commit `ff29cd3`).

**Step 4 — Biography Review (replaces bio bucket fields):**
- Displays the AI-generated portrait in a read-only panel
- Agent can click **This is me** (approve) or write revision notes and click **Regenerate**
- Regenerate calls `POST /webhook/portrait-revise` → updates panel with new version
- Loop continues until agent approves
- Approval guard: wizard Next button is blocked until Step 4 is approved

**Step 5 — Characteristics Review (replaces read-only persona textarea):**
- Same approve/revise loop as Step 4, but for the characteristics brief
- Approval guard: wizard Next button blocked until Step 5 is approved

**Technical changes:**
- `loadPortraitContent(packet, portraitData, characteristicsData)` — uses data returned directly from `smrt_homework_verify` RPC (no extra Supabase REST calls)
- `renderForm(packet, portraitData, characteristicsData)` — passes portrait/characteristics data through from verify response
- `buildPayload()` — includes `portrait_approved`, `portrait_version_id`, `characteristics_approved`, `characteristics_version_id`
- `REVISE_WEBHOOK` constant set to `https://twodegreesnorth.tech/webhook/portrait-revise`

### Added — Supabase Schema Migrations (SMRT Page project `kfoijgcbkjeizxxyiwxv`)

Committed to `SmrtGuys/smrt-command-centre`.

**Migration 019 — `portrait_versions` table:**
- Stores versioned portrait and characteristics content
- Columns: `id`, `submission_id` (FK → `smrt_saas_submissions`), `section`, `version`, `content`, `agent_notes`, `status`, `approved_at`, `created_at`
- Unique partial index: one approved version per `(submission_id, section)`
- RLS disabled (service role writes from n8n HTTP nodes)

**Migration 020 — `agent_homework_packets` approval columns:**
- Added: `portrait_approved` (bool), `portrait_version_id` (uuid FK), `characteristics_approved` (bool), `characteristics_version_id` (uuid FK)

**RPC patches (applied directly to SMRT Page Supabase):**
- `smrt_homework_submit` — whitelists new approval fields; writes approved portrait to `agents.agent_bio.full_bio` and approved characteristics to `agents.personality_prompt`
- `smrt_homework_verify` — returns `portrait` and `characteristics` version data (latest draft row from `portrait_versions`) alongside packet data

---

## 2026-05-14 — Homework Email Workflow + Onboarding Tab

### Added — Homework Email Workflow (`W1IcIn6NDN9H8vRm`)

New webhook-triggered n8n workflow (`📬 Onboarding — Homework Email`) that receives an approved portrait and characteristics brief from the admin dashboard and sends a formatted HTML email to the agent for review before launch.

**Webhook:** `POST https://twodegreesnorth.tech/webhook/homework-email`

**Pipeline (3 nodes):**
1. Webhook — receives `agent_email`, `agent_full_name`, `agent_portrait`, `agent_characteristics`, `record_id`
2. Build Email HTML (Code) — renders a clean two-section HTML email (portrait + characteristics) with SMRT branding
3. Send Homework Email (Gmail) — sends via `SMRT - Gmail OAuth Credential`; reply-to `luke@twodegreesnorth.tech`

Workflow JSON added to `workflows/active/Homework_Email__W1IcIn6NDN9H8vRm.json`. Manifest updated.

### Added — Onboarding Tab in `agent-connect-dashboard`

New `/onboarding` route added to `LukeWilliamGilbert/agent-connect-dashboard` (commit `a75aa9d`).

**Flow:**
1. Staff pastes transcript + agent name/email → clicks **Build Portrait**
2. Portrait Builder runs (~50s) → portrait and characteristics appear side-by-side in editable panels
3. Staff reviews and edits if needed → clicks **Approve & Send Homework**
4. Homework Email workflow fires → agent receives formatted email

Top nav added to `DashboardShell` for Dashboard ↔ Onboarding switching.

---

## 2026-05-14

### Portrait Builder — new standalone onboarding workflow (ID: YPNy8brb5LMbD75r)

Built and deployed a new n8n workflow (`🎨 Portrait Builder`) that converts a raw onboarding transcript into two structured AI-generated assets: an **agent portrait** (Hero's Journey narrative) and an **agent characteristics brief** (behavioral/communication profile). Both are persisted to `onboarding_requests.bio_template` in Supabase.

**Webhook:** `POST https://twodegreesnorth.tech/webhook/portrait-builder`

**Pipeline (5 stages, fire-and-forget):**
1. Pre-processor (Code) — deterministic normalisation, anchor extraction, 4-window topic split
2. 4× parallel GPT-4o-mini extractors (Operational / Origin & Geography / Method & Character / FAQ & Personal)
3. Merge & Floor Check (Code) — appends extractor outputs, enforces floor values, flags low-confidence records
4. 2× parallel GPT-4o compilers (Hero's Journey portrait + behavioral characteristics brief)
5. Persist to Supabase (Code) — normalises phone/timezone, maps to `onboarding_requests`, inserts with `status = awaiting_launch`

**Live verification:** Execution 10524 — all 14 nodes `success`. Record `96fb5e6c-c465-408e-bf14-97efc8885ed1` created. Portrait: 3,547 chars. Characteristics: 2,090 chars. Pipeline time: ~47s.

Workflow JSON added to `workflows/active/Portrait_Builder__YPNy8brb5LMbD75r.json`. Manifest updated.

---

## 2026-04-29

Initialized the SMRT system audit repository structure. Added the audit protocol and directories for schema exports, workflow exports, system documentation, diagrams, audit artifacts, and future implementation notes. No production data, schema, workflow, prompt, or configuration changes were made.

Added the first deep schema-workflow audit deliverable set. This includes a live Supabase schema inventory, a static workflow-to-table relationship map, a read-only gap audit, focused appointment-path evidence, the full `bookAppointment` node evidence, and a durable system flow diagram. The audit identified the highest-priority gap as the empty local `appointments` ledger despite appointment-language conversation activity, with `bookAppointment` currently performing a GHL booking first and then attempting a best-effort Supabase insert whose failures are swallowed. The recommended first hardening sprint is appointment-ledger observability and GHL-to-Supabase reconciliation before broader Brain Engine or prompt refactoring. No production data, schema, workflow, prompt, credential, or runtime configuration changes were made.

Added the GoHighLevel boundary and handoff deliverable set. This includes a dedicated GHL boundary map, rendered GHL-to-n8n-to-Supabase flow diagram, a responsibility/risk matrix, and three developer-ready handoff packets for appointment-ledger hardening, GHL identity-contract validation, and conversation/inbound-message mirroring. The recommended operating model is for Manus and the user to own system mapping, contracts, prioritization, and verification while handing the developer bounded implementation tickets with explicit acceptance evidence. The first recommended implementation ticket is `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md`; no production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-04-29 — Workflow JSON Bootstrap and Operations Readiness

Promoted the sanitized n8n workflow exports into the SMRT repository as a reviewable working set. The repository now includes `workflows/active/`, `workflows/inactive/`, and `workflows/manifest.json`, covering 21 workflow JSON files from the captured SMRT n8n inventory. This closes the visibility gap where audit documents existed in GitHub but the actual workflow definitions were not yet present as diffable source files.

Added `scripts/bootstrap_workflow_exports.py` to reproduce the bootstrap from the sanitized export workspace and `scripts/validate_workflows.py` to statically validate workflow JSON and manifest coverage without touching production. A validation-only GitHub Action remains recommended, but it was not pushed because the current GitHub App integration cannot create or update `.github/workflows/*` files without elevated workflow permissions. No automatic deployment to Hostinger/n8n was enabled.

Created `docs/system/SMRT_WORKFLOW_OPERATIONS_READINESS.md`, `docs/runbooks/WORKFLOW_DEPLOYMENT_RUNBOOK.md`, and `docs/handoffs/HANDOFF_004_SMRT_WORKFLOW_CONTROL_PLANE.md`. These artifacts define the current readiness state and the next infrastructure handoff required before production workflow fixes should be pushed into the active n8n instance. Static validation was run locally and passed across all 21 workflow JSON files.

## 2026-04-29 — Consolidated developer-meeting game plan and communication-log audit

Created a single meeting-ready working document at `docs/system/SMRT_CONSOLIDATED_GAME_PLAN.md` that consolidates the schema/workflow audit, GoHighLevel boundary map, workflow operations readiness assessment, developer handoff sequence, and new communication-log evidence into one prioritized plan. The document frames the next developer conversation around a safe workflow control plane first, appointment-ledger hardening as the first bounded behavioral repair, and inbound capture replay/backfill as the next communication-log-driven sprint.

Added a read-only communication-log audit evidence set using exact Supabase schema columns. The audit generated `data/supabase/communication_log_audit_query_input.json`, `data/supabase/communication_log_audit_raw.json`, `data/supabase/communication_log_audit_clean.json`, and `docs/system/communication_log_audit_findings.md`. Key findings were that communication observability is partially mature, outbound delivery/send-error tracking is stronger than inbound provenance, 31 inbound captures remain unprocessed, and global `system_errors` logging is likely underpopulated.

Added `docs/system/smrt_sprint_priority_matrix.md` to rank repair candidates by impact, risk reduction, dependency readiness, and testability. The resulting sequence is: workflow control plane, appointment ledger hardening, inbound replay/backfill, GHL identity contract, error/mirror-failure ledger, conversation mirror/forward state, and later prompt/agent-state simplification. No production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-04-29 — LLM Injection Audit and Prompt Observability Handoff

Completed a focused read-only audit of the SMRT Brain Engine LLM injection path. The audit confirmed that the main AI Agent appears to receive the assembled `systemPrompt`, but identified high-priority risk around partial upstream injection, inactive static prompt sections, missing prompt-manifest telemetry, inconsistent conversation context, possible message-history parsing loss, and ambiguous ownership between static sections, prompt blocks, system defaults, agent notes, and agent personality fields.

Created the following durable artifacts:

| Artifact | Purpose |
|---|---|
| `docs/system/SMRT_LLM_INJECTION_AUDIT.md` | Meeting-ready audit report explaining the injection path, likely failure surfaces, and recommended next step. |
| `docs/system/llm_injection_defect_map.md` | Ranked defect map with validation tests for prompt assembly and injection reliability. |
| `docs/system/llm_injection_audit_findings.md` | Parsed read-only Supabase findings for prompt-feeding records and active/inactive prompt surfaces. |
| `docs/system/brain_engine_llm_chain.md` | Focused workflow evidence for LLM, prompt, model, memory, and tool connections. |
| `docs/system/brain_engine_prompt_assembly_full.md` | Prompt retrieval and assembly evidence from the Brain Engine workflow. |
| `docs/system/assemble_system_prompt_code.md` | Extracted `Assemble System Prompt` logic with secret redaction. |
| `docs/handoffs/HANDOFF_005_LLM_INJECTION_OBSERVABILITY.md` | Developer-ready ticket for adding non-sensitive prompt assembly telemetry before any large prompt rewrite. |

Recommended sequencing: treat LLM injection as **Sprint 1B or Sprint 2A**, after workflow control-plane discipline is confirmed. The first implementation should add **prompt assembly observability**, not rewrite prompt content. No production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-04-29 — Final Core Focus Document

Created `docs/system/SMRT_FINAL_CORE_FOCUS_DOCUMENT.md` as the single meeting-ready consolidation of the SMRT audits. The document highlights the core repair focuses, surrounding issues, recommended sequence, and developer handoff stance across workflow control plane, appointment ledger hardening, inbound replay/backfill, GoHighLevel identity contract, error/mirror-failure logging, LLM injection observability, and conversation forward state.

The final recommended sequence is: **Sprint 0 workflow control plane; Sprint 1 appointment ledger hardening; Sprint 1B LLM injection observability; Sprint 2 inbound replay/backfill; Sprint 3 GoHighLevel identity contract; Sprint 4 error and mirror-failure ledger; Sprint 5 conversation mirror and forward state**. No production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-04-30 — Prompt-System Forensic Audit and Memory-Routing Handoff

Completed a focused forensic audit of the SMRT prompting and memory architecture, centered on the single-agent tool-load concern, the existing hardwired conversation summary node, the `conversation_context` persistence path, and the question of whether full conversation strips should be injected into the final responder. The audit concluded that prompt prose should not be heavily rewritten yet; the stronger immediate diagnosis is excessive responder tool burden, opaque prompt/context assembly, stale or under-structured summary state, and insufficient route-specific separation between memory, tool execution, and final response composition.

Created `docs/system/SMRT_PROMPT_SYSTEM_FORENSIC_AUDIT.md` as the meeting-ready report and `docs/handoffs/HANDOFF_006_PROMPT_SYSTEM_FORENSICS_AND_MEMORY_ROUTING.md` as the developer implementation packet. Supporting artifacts include `docs/system/prompt_system_forensic_digest.md`, `data/workflows/raw_prompt_summary_surfaces_redacted.json`, and `data/workflows/external_tool_calling_findings.md`. The recommended next work is prompt assembly manifest logging, route-specific tool allowlists, event-triggered summary refresh, structured `conversation_context` state packets, and compact responder context using durable summary plus recent 3–5 turns rather than full conversation strips by default. No production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-04-30 — Newsletter Workflow Forensic Audit and Splinter Delivery Handoff

Completed a focused forensic audit of the SMRT data-driven newsletter architecture, including local market data ingestion, xAI/Grok macro-context generation, newsletter assembly, GoHighLevel email dispatch, and SMS splinter delivery through the Brain Engine. The audit concluded that the newsletter concept is materially present in the workflow set, but the current reliability risk is state and delivery confidence rather than copywriting prompt quality.

Created `docs/system/SMRT_NEWSLETTER_WORKFLOW_FORENSIC_AUDIT.md` as the meeting-ready report and `docs/handoffs/HANDOFF_007_NEWSLETTER_WORKFLOW_RELIABILITY_AND_SPLINTER_DELIVERY.md` as the developer implementation packet. Supporting artifacts include `docs/system/newsletter_workflow_forensic_inventory.md`, `docs/system/newsletter_workflow_node_details.md`, `docs/system/newsletter_schema_evidence.md`, `docs/system/newsletter_workflow_path_map.md`, `docs/system/newsletter_failure_surface_evidence.md`, and `docs/system/newsletter_failure_analysis_matrix.md`. The highest-priority findings are that GoHighLevel email failures may be logged as `sent`, SMS splinter dispatch is structurally present but not proven live because the reviewed outbound schedule trigger is disabled, and Altos/xAI failures can continue into generation without a sufficiently explicit degraded-state contract. No production workflow, schema, credential, prompt, or runtime changes were made.

## 2026-05-01 — Brain Engine Orchestrator-to-Responder Renovation Handoff

Completed a focused current-state inspection of the active SMRT Brain Engine topology for the considered orchestrator/responder revision. The review re-used the extracted `Assemble System Prompt` code evidence, prompt-assembly node inventory, and current workflow topology evidence to identify the exact existing node path from `Gather Prompt Data` through `Assemble System Prompt`, `AI Agent`, `Analyze Conversation`, summary persistence, `Determine Action`, channel routing, send nodes, and outbound logging.

Created `docs/handoffs/HANDOFF_008_ORCHESTRATOR_RESPONDER_RENOVATION.md` as a machine-ready developer implementation packet. The handoff specifies a minimally invasive renovation in which the existing tool-connected `AI Agent` remains the operational orchestrator, emits a strict JSON handoff packet, and passes through a validator and downstream tool-less responder LLM that owns the final customer-facing SMS/email language. It includes the packet schema, explicit scheduling-state contract, node-level rewiring instructions, unsafe fallback removals, observability requirements, acceptance tests, deployment discipline, and rollback rules. No production workflow, schema, credential, prompt, or runtime changes were made.
