#!/usr/bin/env python3
"""Extract GoHighLevel boundary evidence from SMRT n8n workflow exports.

Read-only static analysis. Produces JSON and Markdown artifacts identifying GHL entry
points, exit calls, data domains, and Supabase mirror targets referenced by workflows.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu')
SANITIZED_DIR = ROOT / 'smrt_analysis' / 'sanitized_workflows'
RAW_ALL = ROOT / 'smrt_analysis' / 'raw_export' / 'root' / 'smrt_n8n_export_20260428_194357' / 'workflows' / 'smrt_workflows_all.json'
OUT_JSON = ROOT / 'SMRT-Agent-Ai' / 'data' / 'workflows' / 'ghl_boundary_inventory.json'
OUT_MD = ROOT / 'SMRT-Agent-Ai' / 'docs' / 'system' / 'ghl_boundary_map.md'

GHL_PATTERNS = [
    r'ghl', r'go\\s*high\\s*level', r'leadconnector',
    r'services\\.leadconnectorhq\\.com', r'oauth\\.leadconnectorhq\\.com',
    r'locationId', r'contactId', r'conversationId', r'messageId',
    r'calendar', r'appointment', r'webhook', r'inboundMessage',
]
GHL_RE = re.compile('|'.join(GHL_PATTERNS), re.I)
URL_RE = re.compile(r'https?://[^\s\"\']+')
TABLE_RE = re.compile(r'(?i)\b(agents|leads|message_log|message_send_errors|conversation_context|appointments|inbound_capture|contact_intake_queue|newsletter_deliveries|onboarding_requests|agent_rules|documents|system_errors|ai_output_errors)\b')

DOMAIN_KEYWORDS = {
    'contacts': re.compile(r'(?i)contacts?|contactId|phone|email|firstName|lastName'),
    'conversations_messages': re.compile(r'(?i)conversations?|messages?|messageId|conversationId|sms|email|direction|inbound|outbound'),
    'calendars_appointments': re.compile(r'(?i)calendars?|appointments?|availability|free-slots|slot|startTime|endTime'),
    'users_locations': re.compile(r'(?i)users?|locations?|locationId|assignedTo|ghl_user'),
    'opportunities_pipelines': re.compile(r'(?i)opportunit|pipeline|stage'),
    'webhooks': re.compile(r'(?i)webhook|trigger|headers|body'),
}


def load_workflows() -> list[dict[str, Any]]:
    workflows: list[dict[str, Any]] = []
    for p in sorted(SANITIZED_DIR.glob('*.json')):
        try:
            wf = json.loads(p.read_text())
            wf['_source_path'] = str(p)
            workflows.append(wf)
        except Exception as exc:
            print(f'WARN failed sanitized {p}: {exc}')
    return workflows


def compact(value: Any, limit: int = 900) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, default=str)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(Bearer\s+)[A-Za-z0-9._\-]+', r'\1[REDACTED]', text, flags=re.I)
    text = re.sub(r'(Authorization["\']?\s*[:=]\s*["\']?)[^,"\'\s}]+', r'\1[REDACTED]', text, flags=re.I)
    return text[:limit] + ('…' if len(text) > limit else '')


def walk(obj: Any, path: str = ''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f'{path}.{k}' if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f'{path}[{i}]')
    else:
        yield path, obj


def classify_node(node: dict[str, Any]) -> dict[str, Any] | None:
    blob = json.dumps(node, ensure_ascii=False, default=str)
    if not GHL_RE.search(blob):
        return None

    node_type = node.get('type', '')
    name = node.get('name', '')
    params = node.get('parameters', {})
    type_lower = node_type.lower()
    name_lower = name.lower()
    blob_lower = blob.lower()

    if 'webhook' in type_lower or 'webhook' in name_lower:
        direction = 'entry_from_ghl_or_external_webhook'
    elif any(term in blob_lower for term in ['post', 'patch', 'put', 'delete']) and ('leadconnector' in blob_lower or 'ghl' in blob_lower or 'calendar' in blob_lower):
        direction = 'exit_to_ghl_api'
    elif any(term in blob_lower for term in ['get', 'fetch']) and ('leadconnector' in blob_lower or 'ghl' in blob_lower or 'calendar' in blob_lower):
        direction = 'read_from_ghl_api'
    else:
        direction = 'ghl_reference_or_transform'

    domains = [name for name, rx in DOMAIN_KEYWORDS.items() if rx.search(blob)]
    tables = sorted(set(TABLE_RE.findall(blob)))
    urls = sorted(set(URL_RE.findall(blob)))[:10]

    evidence = []
    for path, value in walk(node):
        if isinstance(value, (str, int, float, bool)) and GHL_RE.search(str(value)):
            evidence.append({'path': path, 'excerpt': compact(value, 350)})
            if len(evidence) >= 12:
                break

    return {
        'node_name': name,
        'node_type': node_type,
        'direction': direction,
        'domains': domains,
        'tables': tables,
        'urls': urls,
        'evidence': evidence,
        'parameters_excerpt': compact(params, 1000),
    }


def workflow_name(wf: dict[str, Any]) -> str:
    return wf.get('name') or Path(wf.get('_source_path', '')).stem


def main():
    workflows = load_workflows()
    records = []
    workflow_summaries = []
    direction_counts = Counter()
    domain_counts = Counter()
    table_counts = Counter()

    for wf in workflows:
        wf_records = []
        for node in wf.get('nodes', []):
            rec = classify_node(node)
            if rec:
                rec['workflow_name'] = workflow_name(wf)
                rec['workflow_active'] = bool(wf.get('active'))
                wf_records.append(rec)
                records.append(rec)
                direction_counts[rec['direction']] += 1
                domain_counts.update(rec['domains'])
                table_counts.update(rec['tables'])
        if wf_records:
            workflow_summaries.append({
                'workflow_name': workflow_name(wf),
                'active': bool(wf.get('active')),
                'total_nodes': len(wf.get('nodes', [])),
                'ghl_nodes': len(wf_records),
                'directions': dict(Counter(r['direction'] for r in wf_records)),
                'domains': dict(Counter(d for r in wf_records for d in r['domains'])),
                'tables': dict(Counter(t for r in wf_records for t in r['tables'])),
            })

    out = {
        'summary': {
            'workflows_scanned': len(workflows),
            'workflows_with_ghl_refs': len(workflow_summaries),
            'ghl_relevant_nodes': len(records),
            'direction_counts': dict(direction_counts),
            'domain_counts': dict(domain_counts),
            'supabase_table_mentions_near_ghl': dict(table_counts),
        },
        'workflow_summaries': workflow_summaries,
        'node_records': records,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    lines = []
    lines.append('# GoHighLevel Boundary Map for SMRT\n')
    lines.append('**Author:** Manus AI  ')
    lines.append('**Date:** 2026-04-29  ')
    lines.append('**Scope:** Static, read-only extraction from sanitized n8n workflow exports. This map identifies observed GHL entry points, API exits, reads, and Supabase mirror surfaces.\n')
    lines.append('> This is a boundary map, not a production change. It does not prove which GHL records currently exist; it shows where the exported workflows appear to enter, exit, or mirror GoHighLevel data.\n')
    lines.append('## Summary\n')
    lines.append('| Metric | Count |')
    lines.append('| --- | ---: |')
    for k, v in out['summary'].items():
        if isinstance(v, int):
            lines.append(f'| {k.replace("_", " ").title()} | {v} |')
    lines.append('\n## Direction Counts\n')
    lines.append('| Direction | Nodes |')
    lines.append('| --- | ---: |')
    for k, v in direction_counts.most_common():
        lines.append(f'| `{k}` | {v} |')
    lines.append('\n## GHL Domain Counts\n')
    lines.append('| Domain | Nodes |')
    lines.append('| --- | ---: |')
    for k, v in domain_counts.most_common():
        lines.append(f'| `{k}` | {v} |')
    lines.append('\n## Supabase Tables Mentioned Near GHL Logic\n')
    lines.append('| Table | Mentions |')
    lines.append('| --- | ---: |')
    for k, v in table_counts.most_common():
        lines.append(f'| `{k}` | {v} |')
    lines.append('\n## Workflow-Level Boundary Summary\n')
    lines.append('| Workflow | Active | GHL Nodes | Directions | Domains | Supabase Tables Near GHL Logic |')
    lines.append('| --- | --- | ---: | --- | --- | --- |')
    for wf in sorted(workflow_summaries, key=lambda x: (-x['ghl_nodes'], x['workflow_name'])):
        dirs = '<br>'.join(f'`{k}`: {v}' for k, v in sorted(wf['directions'].items())) or 'none'
        doms = '<br>'.join(f'`{k}`: {v}' for k, v in sorted(wf['domains'].items())) or 'none'
        tabs = '<br>'.join(f'`{k}`: {v}' for k, v in sorted(wf['tables'].items())) or 'none'
        lines.append(f"| {wf['workflow_name']} | {wf['active']} | {wf['ghl_nodes']} | {dirs} | {doms} | {tabs} |")
    lines.append('\n## Node-Level Evidence\n')
    for rec in records:
        lines.append(f"### {rec['workflow_name']} / {rec['node_name']}\n")
        lines.append(f"- **Active workflow:** {rec['workflow_active']}")
        lines.append(f"- **Node type:** `{rec['node_type']}`")
        lines.append(f"- **Boundary direction:** `{rec['direction']}`")
        lines.append(f"- **GHL domains:** {', '.join('`'+d+'`' for d in rec['domains']) if rec['domains'] else 'none classified'}")
        lines.append(f"- **Nearby Supabase tables:** {', '.join('`'+t+'`' for t in rec['tables']) if rec['tables'] else 'none observed'}")
        if rec['urls']:
            lines.append(f"- **URLs:** {', '.join('`'+u+'`' for u in rec['urls'])}")
        if rec['evidence']:
            lines.append('\n| Parameter Path | Evidence Excerpt |')
            lines.append('| --- | --- |')
            for ev in rec['evidence']:
                safe = ev['excerpt'].replace('|', '\\|')
                lines.append(f"| `{ev['path']}` | `{safe}` |")
        lines.append('')
    lines.append('## References\n')
    lines.append('[1]: ./workflow_schema_relationship_map.md "SMRT Workflow-Schema Relationship Map"  ')
    lines.append('[2]: ./SMRT_SCHEMA_WORKFLOW_AUDIT.md "SMRT Schema-Workflow Audit and Hardening Plan"')
    OUT_MD.write_text('\n'.join(lines) + '\n')
    print(f'wrote {OUT_JSON}')
    print(f'wrote {OUT_MD}')

if __name__ == '__main__':
    main()
