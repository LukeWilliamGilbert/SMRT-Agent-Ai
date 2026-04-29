#!/usr/bin/env python3
"""Validate SMRT n8n workflow JSON working set.

This is intentionally a local/static validator. It does not call n8n, Hostinger,
Supabase, GoHighLevel, or any external service. Its purpose is to make Git-based
workflow review safer before live pull/deploy automation is added.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = REPO / 'workflows'
MANIFEST = WORKFLOWS_DIR / 'manifest.json'
REQUIRED_WORKFLOW_KEYS = {'nodes', 'connections'}
REQUIRED_NODE_KEYS = {'id', 'name', 'type', 'parameters'}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]):
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as exc:  # noqa: BLE001 - validator should collect all parse failures
        fail(errors, f'{path.relative_to(REPO)}: invalid JSON: {exc}')
        return None


def validate_manifest(errors: list[str]) -> list[dict]:
    manifest = load_json(MANIFEST, errors)
    if not isinstance(manifest, dict):
        fail(errors, 'workflows/manifest.json must be a JSON object')
        return []
    workflows = manifest.get('workflows')
    if not isinstance(workflows, list):
        fail(errors, 'workflows/manifest.json must contain a workflows array')
        return []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for entry in workflows:
        if not isinstance(entry, dict):
            fail(errors, 'manifest entry is not an object')
            continue
        for key in ('id', 'name', 'active', 'path'):
            if key not in entry:
                fail(errors, f'manifest entry missing {key}: {entry}')
        wf_id = entry.get('id')
        wf_path = entry.get('path')
        if wf_id in seen_ids:
            fail(errors, f'duplicate workflow id in manifest: {wf_id}')
        if wf_path in seen_paths:
            fail(errors, f'duplicate workflow path in manifest: {wf_path}')
        if wf_id:
            seen_ids.add(wf_id)
        if wf_path:
            seen_paths.add(wf_path)
        if wf_path and not (REPO / wf_path).exists():
            fail(errors, f'manifest path does not exist: {wf_path}')
    return workflows


def validate_workflow(path: Path, manifest_entry: dict | None, errors: list[str], warnings: list[str]) -> None:
    wf = load_json(path, errors)
    if not isinstance(wf, dict):
        return
    missing = REQUIRED_WORKFLOW_KEYS - set(wf)
    if missing:
        fail(errors, f'{path.relative_to(REPO)}: missing workflow keys: {sorted(missing)}')
    nodes = wf.get('nodes')
    if not isinstance(nodes, list):
        fail(errors, f'{path.relative_to(REPO)}: nodes must be an array')
        return
    if manifest_entry and manifest_entry.get('node_count') is not None:
        expected = manifest_entry.get('node_count')
        if expected != len(nodes):
            warnings.append(f'{path.relative_to(REPO)}: node count differs from captured inventory: manifest={expected}, file={len(nodes)}')
    node_names: set[str] = set()
    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            fail(errors, f'{path.relative_to(REPO)}: node {idx} is not an object')
            continue
        missing_node = REQUIRED_NODE_KEYS - set(node)
        if missing_node:
            fail(errors, f'{path.relative_to(REPO)}: node {idx} missing keys: {sorted(missing_node)}')
        name = node.get('name')
        if name in node_names:
            warnings.append(f'{path.relative_to(REPO)}: duplicate node name: {name}')
        if name:
            node_names.add(name)
    connections = wf.get('connections')
    if not isinstance(connections, dict):
        fail(errors, f'{path.relative_to(REPO)}: connections must be an object')
    if 'credentials' in wf and wf.get('credentials'):
        warnings.append(f'{path.relative_to(REPO)}: workflow contains top-level credentials metadata; verify it is sanitized before committing')


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    workflows = validate_manifest(errors)
    entries_by_path = {entry.get('path'): entry for entry in workflows if isinstance(entry, dict)}
    json_files = sorted((WORKFLOWS_DIR / 'active').glob('*.json')) + sorted((WORKFLOWS_DIR / 'inactive').glob('*.json'))
    manifest_paths = set(entries_by_path)
    actual_paths = {str(path.relative_to(REPO)) for path in json_files}
    for missing in sorted(actual_paths - manifest_paths):
        fail(errors, f'workflow JSON not present in manifest: {missing}')
    for missing in sorted(manifest_paths - actual_paths):
        fail(errors, f'manifest references missing workflow JSON: {missing}')
    for path in json_files:
        validate_workflow(path, entries_by_path.get(str(path.relative_to(REPO))), errors, warnings)

    print(f'Validated {len(json_files)} workflow JSON files.')
    if warnings:
        print('\nWarnings:')
        for warning in warnings:
            print(f'  - {warning}')
    if errors:
        print('\nErrors:')
        for error in errors:
            print(f'  - {error}')
        return 1
    print('Validation passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
