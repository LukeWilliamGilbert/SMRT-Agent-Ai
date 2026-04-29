#!/usr/bin/env python3
"""Bootstrap sanitized n8n workflow JSON exports into the SMRT repo.

This script intentionally uses sanitized workflow exports, not raw credential-bearing exports.
It creates a Git-first working tree compatible with later deploy/pull automation:

workflows/
  active/
  inactive/
  manifest.json
  README.md
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path('/home/ubuntu/SMRT-Agent-Ai')
SANITIZED_DIR = Path('/home/ubuntu/smrt_analysis/sanitized_workflows')
INVENTORY_PATH = Path('/home/ubuntu/smrt_analysis/raw_export/root/smrt_n8n_export_20260428_194357/workflow_inventory.json')
WORKFLOWS_DIR = REPO / 'workflows'
ACTIVE_DIR = WORKFLOWS_DIR / 'active'
INACTIVE_DIR = WORKFLOWS_DIR / 'inactive'


def slugify(name: str) -> str:
    name = re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')
    return re.sub(r'_+', '_', name) or 'workflow'


def load_inventory() -> dict[str, dict]:
    with INVENTORY_PATH.open('r', encoding='utf-8') as f:
        rows = json.load(f)
    return {row['id']: row for row in rows}


def workflow_id_from_filename(path: Path) -> str:
    return path.stem.rsplit('__', 1)[-1]


def main() -> None:
    inventory = load_inventory()
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    INACTIVE_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        'generated_from': 'sanitized n8n workflow exports captured during read-only SMRT audit',
        'source_inventory': str(INVENTORY_PATH),
        'warning': 'These JSON files are sanitized working exports for review and Git diffing. Do not assume they are deploy-ready until a live pull/deploy pipeline is installed and verified.',
        'workflows': []
    }

    for src in sorted(SANITIZED_DIR.glob('*.json')):
        workflow_id = workflow_id_from_filename(src)
        row = inventory.get(workflow_id, {})
        name = row.get('name') or src.stem.rsplit('__', 1)[0].replace('_', ' ')
        active = bool(row.get('active', False))
        target_dir = ACTIVE_DIR if active else INACTIVE_DIR
        target_name = f"{slugify(name)}__{workflow_id}.json"
        target = target_dir / target_name
        shutil.copy2(src, target)
        manifest['workflows'].append({
            'id': workflow_id,
            'name': name,
            'active': active,
            'path': str(target.relative_to(REPO)),
            'updatedAt': row.get('updatedAt'),
            'node_count': row.get('node_count')
        })

    manifest['workflows'].sort(key=lambda w: (not w['active'], w['name']))
    with (WORKFLOWS_DIR / 'manifest.json').open('w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')

    readme = """# SMRT n8n Workflow Exports

This directory contains **sanitized n8n workflow JSON exports** copied into the repository after the read-only SMRT audit. They are intended to make workflow review, diffing, handoff tickets, and future Git-first workflow development possible.

These files are not yet an automated deployment source. Before any workflow is pushed back into the active Hostinger/n8n instance, the project still needs a verified pull/deploy pipeline, deployment credentials stored outside the repo, a staging or dry-run procedure, and post-deployment verification.

| Directory | Meaning |
| --- | --- |
| `active/` | Workflows that were active in the captured n8n inventory. These are the likely production-impacting workflows. |
| `inactive/` | Disabled, test, onboarding, replay, backfill, or archived workflows from the captured inventory. |
| `manifest.json` | Maps workflow names, n8n IDs, active state, node counts, and repo paths. |

The current safest operating model is **Git-first but not auto-deploy yet**: make proposed edits in a branch, review diffs, test against a controlled instance or manual import, then promote only after verification.
"""
    (WORKFLOWS_DIR / 'README.md').write_text(readme, encoding='utf-8')
    print(f"Copied {len(manifest['workflows'])} sanitized workflows into {WORKFLOWS_DIR}")


if __name__ == '__main__':
    main()
