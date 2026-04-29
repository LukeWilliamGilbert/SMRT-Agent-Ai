# HANDOFF 004: SMRT Workflow Control Plane

Author: **Manus AI**  
Date: **2026-04-29**  
Status: **Ready for Developer Scoping**  
Production Change: **No direct production behavior change intended**

## Objective

Build the minimum safe infrastructure required to move SMRT workflow fixes through a traceable lifecycle: **pull live Hostinger/n8n state, review and patch in Git, validate locally, deploy one selected workflow manually, verify behavior, and update the changelog**.

This handoff should be completed before broad workflow refactors and preferably before `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` is deployed into production.

## Current Repository State

The repository now contains sanitized n8n workflow JSON exports under:

| Path | Purpose |
| --- | --- |
| `workflows/active/` | Workflows that were active in the captured n8n inventory. |
| `workflows/inactive/` | Workflows that were inactive or non-production at capture time. |
| `workflows/manifest.json` | Workflow registry containing IDs, names, active flags, node counts, timestamps, and file paths. |
| `scripts/validate_workflows.py` | Static local validator; it does not touch production. |
| `docs/runbooks/WORKFLOW_DEPLOYMENT_RUNBOOK.md` | Manual safety process for workflow changes. |

The repository does **not** yet have a verified live pull script, deploy script, GitHub Action, or stored n8n secrets for the SMRT Hostinger runtime.

## Required Implementation

### 1. Confirm Runtime Coordinates

Identify and document the active SMRT n8n base URL and workflow API access method. Do not commit API keys or credentials to the repository.

| Required Value | Storage Rule |
| --- | --- |
| `N8N_BASE_URL` | GitHub secret or local environment variable only. |
| `N8N_API_KEY` | GitHub secret or local environment variable only. |
| Production n8n dashboard URL | Can be documented if not sensitive. |
| Staging n8n URL, if available | Strongly preferred before auto-deploy. |

### 2. Implement `scripts/pull_n8n.py`

The pull script should read `workflows/manifest.json`, call the n8n API for each known active workflow ID, write the returned JSON into the correct `workflows/active/` file, and then tell the operator to inspect `git diff`.

Acceptance behavior:

| Command | Expected Result |
| --- | --- |
| `N8N_API_KEY=... N8N_BASE_URL=... python3.11 scripts/pull_n8n.py` | Pulls active workflows and prints updated files. |
| Missing `N8N_API_KEY` | Exits safely with a clear error. |
| Missing workflow in n8n | Reports the workflow ID and exits non-zero. |
| Successful pull | Does not auto-commit or auto-push. |

### 3. Implement `scripts/deploy_n8n.py`

The deploy script should deploy exactly one selected workflow file unless an explicit `--all` flag is supplied. Manual single-workflow deployment should be the default. The script must fail if the selected file is not listed as active in the manifest.

Acceptance behavior:

| Command | Expected Result |
| --- | --- |
| `python3.11 scripts/deploy_n8n.py --file workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json` | Deploys only that workflow ID. |
| File not in manifest | Exits without calling n8n. |
| Missing credentials | Exits safely with a clear error. |
| API error | Prints status/body summary and exits non-zero. |

### 4. Extend Validation

Extend `scripts/validate_workflows.py` only if needed. The current validator already checks JSON shape, manifest coverage, node keys, node counts, and duplicate node names. Add checks for workflow ID consistency if live-pulled JSON includes stable IDs.

### 5. Add Validation-Only GitHub Action

Add `.github/workflows/validate-workflows.yml` to run static validation on pull requests and pushes that touch workflow files. This action must not deploy.

Suggested behavior:

| Trigger | Action |
| --- | --- |
| Pull request touching `workflows/**` or `scripts/validate_workflows.py` | Run static validation. |
| Push to `main` touching `workflows/**` | Run static validation. |
| Manual dispatch | Run static validation. |

### 6. Defer Auto-Deploy

Do not add automatic deployment on push until manual pull and manual deploy have both been tested against the SMRT runtime and a rollback path is documented.

## Acceptance Tests

The handoff is complete only when all of the following are true:

| Test | Required Evidence |
| --- | --- |
| Static validator passes. | Terminal output showing `Validation passed.` |
| Live pull works. | Git diff after live pull, reviewed and either committed or explicitly discarded. |
| Single-workflow manual deploy works. | Deployment log for one non-dangerous or controlled workflow. |
| Failed deploy is safe. | Demonstrated missing credential or invalid file failure without production mutation. |
| Runbook updated. | `docs/runbooks/WORKFLOW_DEPLOYMENT_RUNBOOK.md` reflects actual commands and runtime URL rules. |
| Changelog updated. | `CHANGELOG.md` records what was installed and what was tested. |

## Non-Goals

This ticket does not require fixing appointment persistence, refactoring the Brain Engine, changing Supabase schema, changing GHL credentials, or altering prompt behavior. Those should remain separate bounded tickets.

## Recommended Sequencing

Complete this ticket first. Then execute `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` using the new pull/validate/deploy/verify loop as the first real production fix.
