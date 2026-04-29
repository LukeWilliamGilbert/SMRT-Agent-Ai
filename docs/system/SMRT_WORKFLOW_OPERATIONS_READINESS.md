# SMRT Workflow Operations Readiness

Author: **Manus AI**  
Date: **2026-04-29**

## Executive Readiness Assessment

The SMRT repository is now **materially closer** to a working find-fix-push operating system, but it is **not yet safe to treat GitHub as an automatic deployment source for the active Hostinger/n8n instance**. Before this update, the repository contained audit evidence, schema evidence, and handoff documents, but it did not contain the actual n8n workflow JSON files as a visible working set. That gap is now partially closed: sanitized workflow JSON exports have been copied into `workflows/active/` and `workflows/inactive/`, with `workflows/manifest.json` documenting workflow IDs, names, active status, node counts, and repository paths.

The practical status is therefore: **we have a reviewable and diffable workflow repository, but not yet a verified deployment pipeline**. We can now inspect, compare, and propose changes against actual workflow JSON. We should not yet push workflow edits directly into production until we install and verify a controlled pull/deploy process, credential boundaries, rollback behavior, and post-deployment checks.

| Capability | Current Status | Meaning |
| --- | --- | --- |
| Durable audit documentation | **Ready** | Schema, workflow, GHL boundary, and handoff documents are committed. |
| Workflow JSON visibility | **Partially ready** | Sanitized exports are now in `workflows/active/` and `workflows/inactive/`. |
| Safe Git diffs for workflow review | **Ready for review** | We can now create branches and proposed JSON changes that your developer can review. |
| Static workflow validation | **Installed** | `scripts/validate_workflows.py` now validates the 21-file working set without touching production. |
| Validation-only GitHub guardrail | **Deferred** | A validation-only GitHub Action is recommended, but it could not be pushed through the current GitHub App permission because workflow-file updates require elevated workflow permissions. |
| Live pull from Hostinger/n8n | **Not installed** | We still need a verified API pull script pointed at the SMRT n8n base URL. |
| Live deploy to Hostinger/n8n | **Not installed** | We should not auto-deploy until credentials, manifest shape, webhook checks, and rollback are tested. |
| Production-safe fix workflow | **Not fully ready** | The missing piece is controlled live pull/deploy plus post-fix verification. |

## Why You Did Not See Workflow JSON Before

The earlier commits intentionally prioritized **system evidence and audit artifacts**. The raw and sanitized workflow exports existed in the sandbox audit workspace under `/home/ubuntu/smrt_analysis/`, but they had not yet been promoted into the `SMRT-Agent-Ai` repository as a maintained workflow working set. That is why the GitHub repo showed JSON evidence files such as Supabase audit outputs, but not the actual n8n workflow definitions.

That has now been corrected at the repository-structure level. The repo now includes:

| Path | Purpose |
| --- | --- |
| `workflows/active/` | Sanitized workflow JSON files that were active in the captured n8n inventory. |
| `workflows/inactive/` | Sanitized workflow JSON files that were inactive, test, onboarding, replay, or backfill workflows in the captured inventory. |
| `workflows/manifest.json` | A registry mapping workflow IDs, names, active status, node counts, update timestamps, and repo paths. |
| `workflows/README.md` | A plain-English warning that these files are a review/diff working set, not yet an automatic deployment source. |

## The Target Operating Model

The correct destination is a **Git-first workflow lifecycle**. This means that production-impacting changes should not be made ad hoc in the n8n editor and forgotten. Instead, the live system should be pulled into Git, fixes should be proposed and reviewed as diffs, changes should be deployed through a controlled script or CI job, and the result should be verified immediately after deployment.

> **Working principle:** GitHub should become the durable memory of the workflow system, while Hostinger/n8n remains the runtime. The runtime should not be the only place where truth exists.

| Step | Owner | Action | Required Evidence |
| --- | --- | --- | --- |
| 1. Pull live state | Manus/developer | Pull current n8n workflows from Hostinger/n8n into Git before editing. | Git diff showing exactly what changed since last known state. |
| 2. Diagnose | Manus + user | Link the bug to workflow node(s), Supabase table(s), GHL endpoint(s), and acceptance tests. | Handoff ticket or audit note. |
| 3. Patch in branch | Developer or Manus | Edit workflow JSON, scripts, or SQL migrations in a branch, not directly in production. | Pull request or reviewable commit. |
| 4. Dry-run/static validate | Developer or Manus | Validate JSON shape, manifest mapping, critical nodes, and no obvious secret leakage. | Validation output committed or attached. |
| 5. Deploy controlled | Developer initially | Push a single named workflow to n8n via API or manual import, with rollback ready. | Deployment log and workflow ID. |
| 6. Verify behavior | Manus + user | Run the exact post-fix test, such as booking an appointment and confirming Supabase ledger row creation. | Query output, webhook response, or execution evidence. |
| 7. Update changelog | Manus | Record the fix, test evidence, and any remaining risk. | `CHANGELOG.md` entry. |

## How Close We Are

We are approximately **60 percent of the way** to the working system you described. The difficult knowledge work has moved forward: we have the schema model, workflow-to-table map, GHL boundary, appointment-ledger ticket, and now the workflow JSON working set. The remaining 40 percent is operational plumbing and trust-building.

| Layer | Readiness | Explanation |
| --- | ---: | --- |
| System understanding | 75% | We have enough map coverage to avoid wandering through the rats nest blindly. |
| Workflow source control | 65% | JSON files are now present and statically validated, but the current set is based on sanitized exports rather than a live pull pipeline. |
| Deployment automation | 20% | No SMRT-specific live deploy script is installed yet, and no auto-deployment has been enabled. |
| Validation guardrails | 40% | Local validation now exists; GitHub Actions validation is deferred until workflow-file permissions are available, and live runtime validation still needs to be added. |
| Verification harness | 25% | We have acceptance-test definitions in handoff tickets, but not automated tests. |
| Production safety | 40% | We can propose bounded changes and validate JSON, but should avoid auto-deploy until rollback and live verification are proven. |

## What Must Be Built Next

The next infrastructure sprint should not be the appointment fix itself. It should be the **SMRT workflow control plane**: the small amount of tooling that lets us move safely between GitHub and Hostinger/n8n.

| Priority | Artifact | Why It Matters |
| --- | --- | --- |
| 1 | `scripts/pull_n8n.py` | Pulls live Hostinger/n8n workflows into `workflows/active/` so Git stays aligned with reality. |
| 2 | `scripts/validate_workflows.py` | Installed now; checks workflow JSON shape, manifest mapping, active workflow IDs, and obvious missing fields before deployment. |
| 3 | `scripts/deploy_n8n.py` | Still needed; deploys one selected active workflow by ID after review; initially manual, not auto-triggered. |
| 4 | `.github/workflows/validate-workflows.yml` | Still needed; validation-only workflow should be added by a user/developer token with GitHub workflow permissions. |
| 5 | Optional `.github/workflows/deploy-to-n8n.yml` | Still deferred; only after manual deploy has been proven; deploys changed active workflows using GitHub secrets. |
| 6 | `docs/runbooks/WORKFLOW_DEPLOYMENT_RUNBOOK.md` | Installed now; human-readable checklist for pull, patch, validate, deploy, verify, rollback, and changelog. |

## Recommended Immediate Decision

The immediate answer is: **we are close enough to start working like a real workflow engineering team, but not close enough to auto-push fixes into production yet**. I recommend that we first install a manual-control workflow pipeline, then use the appointment-ledger hardening ticket as the first real controlled change.

This keeps us from trying to fix too many things at once. The right sequence is:

| Sequence | Work Item | Result |
| --- | --- | --- |
| 1 | Commit sanitized workflow JSON into the repo. | Done in this update. |
| 2 | Add local validation scaffolding without enabling auto-deploy. | Done in this update. |
| 3 | Add live pull/manual deploy scripts after confirming Hostinger/n8n API details. | Next step. |
| 4 | Confirm Hostinger/n8n API base URL and credentials path. | Needed before live pull/deploy. |
| 5 | Pull live workflows and compare against sanitized exports. | Establishes current runtime truth. |
| 6 | Implement `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md`. | First bounded production fix. |
| 7 | Verify by booking test appointment and querying Supabase. | Confirms the loop actually works. |

## Developer Handoff Position

The developer should not receive a broad instruction like “fix the workflows” or “fix GHL.” That would recreate the rats nest. The developer should receive a tightly scoped operating assignment: help install the SMRT workflow control plane, then implement one bounded workflow change at a time.

The first developer assignment should be one of these two, depending on whether we want infrastructure first or feature fix first:

| Option | Handoff | When to Choose It |
| --- | --- | --- |
| A | Build pull/validate/manual-deploy scripts for SMRT n8n workflows. | Choose this if we want safety before production changes. This is my recommendation. |
| B | Implement `HANDOFF_001_APPOINTMENT_LEDGER_HARDENING.md` manually in n8n with evidence. | Choose this if appointment visibility is urgent and we accept more manual process. |

My recommendation is **Option A first**, immediately followed by the appointment-ledger ticket. That gives us the operating system we need so every future repair becomes less scary and more traceable.
