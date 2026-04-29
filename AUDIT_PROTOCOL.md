# SMRT System Audit Protocol

Author: **Manus AI**  
Date: 2026-04-29

## Purpose

This repository is the working source of truth for the SMRT system-understanding and hardening audit. The immediate objective is not to change production behavior. The objective is to build a durable, navigable model of how SMRT tracks, processes, routes, and delivers information across Supabase tables and n8n workflows.

## Operating Constraints

Production Supabase access is treated as **read-only** unless the user explicitly approves a specific write operation. Production n8n workflows must not be edited directly during audit work. Workflow changes, when eventually approved, should be prepared as reviewed, versioned artifacts before deployment.

## Audit Priorities

The audit focuses on the following questions:

| Priority | Question |
| --- | --- |
| Information tracking | Which tables represent leads, contacts, messages, conversations, appointments, prompt state, routing state, memory, and delivery events? |
| Workflow alignment | Which n8n nodes read from or write to those tables, and what assumptions do they make about IDs, timestamps, and foreign keys? |
| Conversation continuity | Can an inbound/outbound interaction be traced from capture to response to CRM sync to appointment booking? |
| Appointment visibility | Why are booked appointments not visible in the appointments table, and where are they being recorded instead, if anywhere? |
| Missing identifiers | Which tables lack canonical identifiers needed to reconstruct conversation and booking timelines? |
| Hardening plan | Which gaps should be fixed first, and which should be deferred to avoid trying to fix too much at once? |

## Deliverables

The audit will produce a system model, schema inventory, workflow-to-table touchpoint map, information-flow diagrams, gap register, and prioritized intervention plan. A changelog will track every meaningful audit or implementation step performed in this repository.
