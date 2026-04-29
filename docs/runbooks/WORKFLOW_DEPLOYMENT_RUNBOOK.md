# SMRT Workflow Deployment Runbook

Author: **Manus AI**  
Date: **2026-04-29**

## Purpose

This runbook defines the safe operating procedure for moving SMRT workflow changes from GitHub into the active Hostinger/n8n runtime. It exists because the SMRT repository now contains sanitized n8n workflow JSON files, but it does **not** yet have a verified live pull/deploy pipeline.

The rule for now is simple: **GitHub is the working memory; Hostinger/n8n is the runtime; no production deployment should occur without explicit verification evidence.**

## Current Safety Status

| Area | Status | Rule |
| --- | --- | --- |
| Workflow JSON in repo | Present | Use `workflows/active/` and `workflows/inactive/` for review and diffs. |
| Static validation | Present | Run `python3.11 scripts/validate_workflows.py` before committing workflow edits. |
| Live pull from n8n | Not installed | Do not assume repo JSON is the current runtime truth until live pull is added. |
| Live deploy to n8n | Not installed | Do not auto-deploy from GitHub yet. |
| GitHub Actions deployment | Not installed | Add only after manual pull/deploy has been proven. |

## Manual Development Procedure

### 1. Start From a Branch

Create a branch for every workflow change. Avoid editing `main` directly when production-impacting workflow JSON is involved.

```bash
git checkout -b fix/appointment-ledger-hardening
```

### 2. Identify the Workflow and Node

Use the handoff documents and audit reports to identify the exact file and nodes. For the appointment-ledger work, the likely primary workflow is:

```text
workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json
```

### 3. Edit Workflow JSON Carefully

Workflow JSON should be changed with scripted or highly targeted edits where possible. Avoid broad manual reformatting that creates noisy diffs.

### 4. Validate Locally

Run the static workflow validator before committing.

```bash
python3.11 scripts/validate_workflows.py
```

The validator currently checks manifest coverage, JSON parsing, required n8n workflow keys, required node keys, node counts, duplicate node names, and unexpected top-level credential metadata.

### 5. Review the Diff

Review the exact JSON diff before handing work to another agent, developer, or production runtime.

```bash
git diff -- workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json
```

### 6. Deploy Manually Until Automation Is Proven

Until `scripts/deploy_n8n.py` and the required credentials are installed and tested, deployment should be manual and explicit. The person deploying must record:

| Evidence | Required Detail |
| --- | --- |
| Workflow name | Exact n8n workflow name. |
| Workflow ID | Exact n8n workflow ID. |
| Deployment method | Manual import, API PUT, or n8n editor change. |
| Timestamp | Date and time of deployment. |
| Rollback path | Prior workflow export or Git commit. |

### 7. Verify Immediately

Every workflow deployment must be followed by a behavior test. For appointment-ledger hardening, the minimum verification is:

| Test | Expected Result |
| --- | --- |
| Book one controlled test appointment through the SMRT path. | A GHL appointment/event is created or an explicit failure is captured. |
| Query Supabase `appointments`. | A local appointment ledger row exists for the GHL event or a structured error ledger row exists. |
| Check workflow execution logs. | The appointment persistence node does not silently swallow failure. |
| Check related lead/conversation IDs. | The row can be traced back to the relevant lead/contact/conversation context. |

### 8. Update the Changelog

Every change must end with an entry in `CHANGELOG.md` describing what changed, what was tested, and what remains unresolved.

## Rollback Rule

If verification fails after a production change, restore the previous known-good workflow version immediately and preserve the failed execution evidence for diagnosis. Do not stack a second speculative fix on top of the first failed fix.

## What To Build Next

The next infrastructure task is to add **manual-control n8n pull and deploy scripts**. These should require explicit command invocation and environment variables. They should not auto-deploy on push until the manual path has been proven.
