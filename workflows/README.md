# SMRT n8n Workflow Exports

This directory contains **sanitized n8n workflow JSON exports** copied into the repository after the read-only SMRT audit. They are intended to make workflow review, diffing, handoff tickets, and future Git-first workflow development possible.

These files are not yet an automated deployment source. Before any workflow is pushed back into the active Hostinger/n8n instance, the project still needs a verified pull/deploy pipeline, deployment credentials stored outside the repo, a staging or dry-run procedure, and post-deployment verification.

| Directory | Meaning |
| --- | --- |
| `active/` | Workflows that were active in the captured n8n inventory. These are the likely production-impacting workflows. |
| `inactive/` | Disabled, test, onboarding, replay, backfill, or archived workflows from the captured inventory. |
| `manifest.json` | Maps workflow names, n8n IDs, active state, node counts, and repo paths. |

The current safest operating model is **Git-first but not auto-deploy yet**: make proposed edits in a branch, review diffs, test against a controlled instance or manual import, then promote only after verification.
