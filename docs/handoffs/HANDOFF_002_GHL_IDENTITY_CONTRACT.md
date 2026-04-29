# HANDOFF 002 — GoHighLevel Identity Contract Audit

**Prepared by:** Manus AI  
**Date:** 2026-04-29  
**Target implementer:** SMRT developer using Claude or equivalent coding agent  
**Dependency:** Do this after `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` unless identity defects block that work.

## Problem statement

SMRT uses multiple identity layers at once: GoHighLevel `contactId`, `locationId`, `calendarId`, and `ghlUserId`; Supabase `lead_id` and `agent_id`; and lead profile fields such as phone, email, and name. The system needs a visible identity contract so the Brain Engine and supporting workflows always know which external GHL record corresponds to which local Supabase record.

## Workflows in scope

| Workflow | Reason it matters |
| --- | --- |
| `☀️ Contact Created -> Brain Engine` | Likely normalizes a GHL contact event into local lead/context state. |
| `🧠 SMRT Brain Engine` | Consumes GHL and Supabase identifiers for prompt assembly, message sending, appointment booking, and context updates. |
| `🎉 Onboarding — Part 1: DB Enrichment` | Captures setup data and may seed local records from incoming onboarding payloads. |
| `🏗️ Onboarding — Part 2: GHL Setup` | References GHL location/calendar/user setup and Supabase agent configuration, but is currently inactive in the exported workflows. |

## Required output

The developer should produce a concrete mapping table and apply only the smallest required workflow changes to enforce it.

| Identity item | Contract question to answer |
| --- | --- |
| `contactId` | Where does it first enter SMRT, and which Supabase row stores it? |
| `locationId` | Is this the canonical tenant/account boundary, and where is it stored locally? |
| `lead_id` | Is this always derivable from `contactId`, phone, email, or another local key? |
| `agent_id` | Is this always derivable from `locationId`, and is it available during booking? |
| `calendarId` | Is it stored in `agents`, passed from prompt context, or read live from GHL setup? |
| `ghlUserId` | Is it required for booking assignment, and what happens if it is missing? |

## Acceptance tests

| Test | Expected result |
| --- | --- |
| Given a GHL contact-created webhook payload. | The system deterministically identifies or creates exactly one Supabase lead. |
| Given a known Supabase lead row. | The system can retrieve or infer the correct `contactId` and `locationId`. |
| Given a booking attempt. | The system has non-empty `contactId`, `locationId`, `calendarId`, and `ghlUserId` before calling GHL, or creates a visible error. |
| Given conflicting identity data. | The workflow does not silently choose a fallback; it creates an explicit triage/error record. |

## Out of scope

Do not change broad prompt behavior, lead qualification strategy, appointment reminder timing, newsletter behavior, or document ingestion. This handoff is only about identity mapping and validation.

## Completion evidence to return

Return the identity contract table, any workflow/node changes, and at least one test trace showing a contact-created event moving into a local lead row and then into Brain Engine prompt context.
