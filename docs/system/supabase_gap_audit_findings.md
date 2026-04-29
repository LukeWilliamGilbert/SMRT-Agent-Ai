# SMRT Supabase Gap Audit Findings

This document summarizes a read-only data-integrity query focused on the live SMRT appointment, identity, memory, message, inbound capture, and agent configuration surfaces. It is intended to support a ranked hardening plan rather than to make direct production changes.

> **Read-only audit note:** The query used only `SELECT` statements through the configured Supabase connector. No rows, schema, workflows, prompts, credentials, or runtime configuration were modified.

Generated at: `2026-04-29T21:23:37.100326+00:00`

## Row Counts

| Surface | Count |
| --- | ---: |
| `leads` | 313 |
| `agents` | 1 |
| `message_log` | 376 |
| `appointments` | 0 |
| `active_agents` | 1 |
| `inbound_capture` | 179 |
| `conversation_context` | 25 |

## Appointment Health

| Check | Count / Value |
| --- | ---: |
| `total` | 0 |
| `by_status` | `{}` |
| `null_lead_id` | 0 |
| `null_agent_id` | 0 |
| `null_location_id` | 0 |
| `missing_lead_by_id` | 0 |
| `missing_agent_by_id` | 0 |
| `missing_agent_by_location` | 0 |
| `missing_lead_by_contact_location` | 0 |

The critical visibility signal is whether conversation contexts have `appointment_booked = true` while no matching row exists in `appointments` for the same contact/location pair.

| Context Booking Check | Count |
| --- | ---: |
| `total_contexts_booked_true` | 0 |
| `booked_contexts_without_appointment_row` | 0 |

## Recent Appointment Rows

| Created At | Contact ID | Location ID | Status | Lead ID Exists | Contact/Location Lead Exists | Agent ID Exists | Location Agent Exists |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Booked Context Sample

| Updated At | Contact ID | Location ID | Appointment Rows | Pending Slot | Summary Excerpt |
| --- | --- | --- | ---: | --- | --- |

## Orphan Summary

| Check | Count |
| --- | ---: |
| `message_log_without_lead` | 0 |
| `inbound_capture_unprocessed` | 31 |
| `conversation_context_without_lead` | 0 |

## Agent State

| Agent | Location ID | Active | Custom Personality Enabled | Has Personality Prompt | Has Agent Notes | Has Calendar ID | Has Calendar Link | Has GHL User ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Luke Gilbert | `kv1Af9i1qYK7KfIiT0U3` | True | False | False | True | True | True | True |
