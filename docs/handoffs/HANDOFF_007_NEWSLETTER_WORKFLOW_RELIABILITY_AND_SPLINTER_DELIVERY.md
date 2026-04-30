# HANDOFF 007: Newsletter Workflow Reliability and Splinter Delivery

**Author:** Manus AI  
**Date:** 2026-04-30  
**Related audit:** `docs/system/SMRT_NEWSLETTER_WORKFLOW_FORENSIC_AUDIT.md`  
**Primary workflows:** `Data Source & Newsletter Creation`, `Newsletter Dispatch`, and `SMRT Brain Engine`.[1] [2] [3]

## Objective

Harden the SMRT newsletter system so weekly newsletters, GoHighLevel email delivery, and SMS splinter delivery are observable, idempotent, and truthfully ledgered. The purpose of this handoff is not to rewrite the newsletter copy prompt. The purpose is to make the workflow prove source quality, generation state, delivery state, and splinter-dispatch state before the team tunes creative output.

## Current Diagnosis

The newsletter system already implements the intended concept at a high level. The creation workflow pulls local market data, requests macro context through xAI/Grok, generates a newsletter, stores weekly stats, extracts canonical splinters, and stores embedded market documents.[1] The dispatch workflow sends the newsletter through GoHighLevel and writes delivery rows.[2] The Brain Engine contains outbound splinter selection and delivery surfaces.[3]

The reliability concern is that several critical transitions are permissive or under-ledgered. The highest-risk issue is that `Send Email via GHL` can continue regular output after an error, while `Log Delivery` hardcodes `status=sent` downstream.[4] Another major issue is that the Brain Engine’s `Schedule Outbound Check` is disabled in the active export, so SMS splinter delivery is structurally present but not proven live.[4]

## Required Changes

| Priority | Change | Acceptance Standard |
| ---: | --- | --- |
| P0 | Split GoHighLevel email send into verified success and failure branches. | A simulated or real GHL failure must not create a `newsletter_deliveries.status='sent'` row. |
| P0 | Add delivery response validation before `Log Delivery`. | `sent` is written only when GHL returns a valid success status and message/conversation identifier. |
| P0 | Confirm or create the live trigger for SMS splinter dispatch. | The team can point to the exact active trigger that evaluates outbound splinter candidates on schedule. |
| P1 | Add a newsletter generation run ledger. | Every generation attempt records agent, location, week, data-quality status, macro-provider status, artifact IDs, and error state. |
| P1 | Add Altos and xAI/Grok quality gates. | Empty, failed, or below-threshold inputs block generation or mark the run as degraded. |
| P1 | Validate splinter JSON before activation. | Malformed or incomplete splinters cannot be inserted as `active=true`. |
| P2 | Normalize macro-provider metadata. | Stored newsletter records identify provider, model, prompt version, generated time, and failure/fallback state. |
| P2 | Scope old-splinter deactivation safely. | Deactivation cannot accidentally disable another agent’s active splinters when locations are shared. |

## Implementation Notes

### 1. Email dispatch must stop treating continued errors as success

The current dispatch path should be changed so the HTTP node can still avoid crashing the whole workflow, but the response is routed through an explicit response-classification node. That classifier should inspect status code, response body, and expected GoHighLevel identifiers. It should emit one of three states: `sent`, `failed_retryable`, or `failed_terminal`.

| State | Required Ledger Behavior |
| --- | --- |
| `sent` | Insert or upsert `newsletter_deliveries` with `status='sent'`, `sent_at`, GHL message ID, and response metadata. |
| `failed_retryable` | Insert or upsert a failed delivery attempt with error details and retry eligibility. |
| `failed_terminal` | Insert or upsert a failed delivery attempt with non-retryable reason and no suppression of future manual repair. |

### 2. Add a generation run ledger before changing prompts

A newsletter run ledger should be created before major prompt changes. The ledger should separate generation status from delivery status, because successful content generation does not prove successful delivery.

| Field Group | Suggested Fields |
| --- | --- |
| Identity | `run_id`, `agent_id`, `location_id`, `week_start_date` |
| Local data | `altos_status`, `zips_expected`, `zips_processed`, `missing_required_metrics` |
| Macro context | `macro_status`, `macro_provider`, `macro_model`, `macro_prompt_version`, `macro_error` |
| Artifacts | `newsletter_id`, `splinter_count`, `document_id`, `image_url` |
| Delivery | `email_dispatch_status`, `sms_splinter_dispatch_status` |
| Failure | `error_stage`, `error_message`, `retryable`, `completed_at` |

### 3. SMS splinter delivery should become its own bounded workflow

The Brain Engine is already a large, responsibility-dense workflow. Newsletter splinter dispatch is deterministic enough to extract into a smaller workflow. The dedicated workflow should fetch eligible active splinters, fetch eligible leads, select delivery variant by pipeline stage, send or queue messages, record `splinter_usage`, and update retry/error state.

This extraction should not change the final communication tone yet. It should first make the SMS splinter path observable and schedulable.

## Test Plan

| Test | Setup | Expected Result |
| --- | --- | --- |
| Failed GHL email send | Use invalid contact ID, invalid token in staging, or mocked 4xx/5xx response. | No `status='sent'` row is written. A failure row captures response details. |
| Empty Altos data | Force target zip failure or empty data response. | Generation blocks or run is marked `degraded`; no silent full-success state. |
| xAI/Grok timeout | Force macro HTTP timeout or response error. | Run records `macro_status='failed'` or fallback status with provider metadata. |
| Malformed splinter JSON | Make `Extract Splinters` return invalid or missing required fields. | Splinter activation is blocked and the run records validation failure. |
| Disabled outbound schedule | Inspect production trigger state and run history. | Team documents the active trigger or enables a dedicated scheduler with dry-run mode. |
| Shared location agents | Generate newsletters for two agents sharing one location. | One agent’s old-splinter cleanup does not deactivate the other agent’s active splinters. |

## Definition of Done

This work is done when newsletter generation, email dispatch, and SMS splinter delivery have separate, inspectable success states. A run should be explainable from the database alone: whether local data was sufficient, whether xAI/Grok macro context was present, which newsletter was generated, which leads were emailed, which emails actually succeeded, which splinters were activated, and whether SMS splinter delivery ran.

## References

[1]: ../../workflows/active/Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json "Data Source & Newsletter Creation workflow export"
[2]: ../../workflows/active/Newsletter_Dispatch__XDcom3gft8yqwa5O.json "Newsletter Dispatch workflow export"
[3]: ../../workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json "SMRT Brain Engine workflow export"
[4]: ../system/newsletter_failure_surface_evidence.md "Generated newsletter failure-surface evidence"
