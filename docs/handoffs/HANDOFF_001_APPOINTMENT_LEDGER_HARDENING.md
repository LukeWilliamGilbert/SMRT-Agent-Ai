# HANDOFF 001 — Appointment Ledger Hardening v1

**Prepared by:** Manus AI  
**Date:** 2026-04-29  
**Target implementer:** SMRT developer using Claude or equivalent coding agent  
**Scope:** Bounded n8n workflow hardening. Do not refactor the Brain Engine outside the booking persistence path.

## Problem statement

SMRT can create a confirmed GoHighLevel appointment while the local Supabase `appointments` table remains empty. The current Brain Engine `bookAppointment` tool creates the GHL appointment first and then attempts a best-effort Supabase insert. If the Supabase insert fails, the error is silently swallowed. This breaks local visibility, reminder workflows, analytics, and Brain Engine context.

## Primary evidence

The relevant workflow is `🧠 SMRT Brain Engine`, node `bookAppointment`. The node posts to `https://services.leadconnectorhq.com/calendars/events/appointments`, receives a GHL response, and then attempts to insert into Supabase `/rest/v1/appointments`. The local insert is wrapped in a nested `try/catch`; the catch block discards the Supabase error with the comment that the Supabase write is best-effort.

See: [`../system/book_appointment_node_full.md`](../system/book_appointment_node_full.md) and [`../system/GHL_BOUNDARY_AND_HANDOFF_PLAN.md`](../system/GHL_BOUNDARY_AND_HANDOFF_PLAN.md).

## Required change

Make the appointment local ledger **observable, idempotent, and failure-aware** without changing the agent’s conversation strategy or the GHL booking behavior.

| Requirement | Detail |
| --- | --- |
| Preserve GHL booking behavior | Do not change the external appointment creation payload except where required for correctness. |
| Capture GHL event ID | When GHL returns an appointment/event ID, persist it as `appointments.ghl_event_id`. |
| Make local write idempotent | Use a conflict-safe approach keyed on `ghl_event_id` if schema supports it, or otherwise check existing rows before inserting. |
| Do not swallow Supabase failures | If the local appointment insert/update fails, write a durable error record or route to a visible workflow error path. |
| Include correlation data | Error record must include `contact_id`, `location_id`, selected slot, `calendar_id`, GHL event ID if available, and the Supabase error body/status. |
| Keep rollback simple | If the patch fails, reverting should restore previous behavior without impacting GHL appointment creation. |

## Suggested implementation approach

First, preserve the current GHL `POST /calendars/events/appointments` call. Second, after a successful GHL response, perform a durable upsert or insert-check-write into `appointments`. Third, replace the silent Supabase catch block with explicit error persistence. If there is no existing appointment-sync error table, use the project’s established error table pattern such as `system_errors` if available, or add a small bounded error path agreed with the owner before schema changes.

The implementation should not broaden into qualification logic, prompt assembly, reminder schedules, lead routing, or conversation memory. This handoff is specifically about making appointment persistence reliable and observable.

## Acceptance tests

| Test | Expected result |
| --- | --- |
| Book one test appointment through the same path used in production. | GHL contains the appointment, and Supabase `appointments` contains a row with the same GHL event ID. |
| Repeat or replay the same GHL event response. | The local ledger does not create duplicate appointment rows. |
| Simulate a Supabase insert failure. | The workflow produces a durable error record with contact/location/slot/calendar/GHL event correlation data. |
| Run or inspect Appointment Reminders against the test appointment. | The reminder workflow can discover the appointment from Supabase without relying on a live GHL read. |
| Inspect logs after a successful booking. | There is enough evidence to prove whether failure occurred in GHL creation or local mirroring. |

## Out of scope

This ticket must not modify the full Brain Engine prompt, the lead qualification sequence, the appointment reminder cadence, the GHL account configuration model, or the broader conversation-memory pipeline.

## Completion evidence to return

The developer should return a short implementation note, before/after workflow export or node diff, screenshots or logs from the test execution, the created Supabase appointment row with sensitive values redacted, and evidence of the forced-failure path creating a durable error record.
