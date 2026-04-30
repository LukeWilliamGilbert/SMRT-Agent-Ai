#!/usr/bin/env python3
"""Build concrete failure-surface evidence for the SMRT newsletter audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF_DIR = ROOT / 'workflows/active'
OUT = ROOT / 'docs/system/newsletter_failure_surface_evidence.md'
FILES = {
    'creation': WF_DIR / 'Data_Source_Newsletter_Creation__gI097yamrw7gDU6C.json',
    'dispatch': WF_DIR / 'Newsletter_Dispatch__XDcom3gft8yqwa5O.json',
    'brain': WF_DIR / 'SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json',
}

TARGET_NODES = {
    'creation': [
        'Schedule Trigger', 'Fetch Agents', 'Prepare Agent Data', 'Check Newsletter For Week',
        'Check Week Stats Exist', 'Altos Get Stats', 'Condense Altos Data', 'Grok National Context',
        'Prep Data for AI', 'Generate Newsletter', 'Extract Splinters', 'Store Newsletter',
        'Delete Old Splinters', 'Store Splinter', 'Store Weekly Stats', 'Generate Embedding', 'Store Embedded Doc'
    ],
    'dispatch': [
        'Weekly Schedule', 'Fetch Active Agents', 'Get Newest Newsletter', 'Fetch Eligible Leads',
        'Build HTML Email', 'Send Email via GHL', 'Log Delivery', 'Update Send Counts',
        'Newsletter Found?', 'Has Eligible Leads?'
    ],
    'brain': [
        'Schedule Outbound Check', 'Fetch Outbound Candidates', 'Set Outbound Context',
        'Send SMS', 'Send Email', 'Log Splinter Usage', 'Update Lead After Outbound'
    ],
}

SENSITIVE = ['authorization', 'apikey', 'apiKey', 'password', 'secret', 'token', 'bearer', 'credential']


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def nodes(wf: dict[str, Any]) -> list[dict[str, Any]]:
    return wf.get('nodes', [])


def node_by_name(wf: dict[str, Any], name: str) -> dict[str, Any] | None:
    for n in nodes(wf):
        if n.get('name') == name:
            return n
    return None


def redact_value(key: str, value: Any) -> Any:
    k = key.lower()
    if any(s in k for s in SENSITIVE):
        return '[REDACTED]'
    if isinstance(value, dict):
        return {kk: redact_value(kk, vv) for kk, vv in value.items()}
    if isinstance(value, list):
        return [redact_value(key, v) for v in value]
    if isinstance(value, str):
        low = value.lower()
        if any(s in low for s in ['bearer ', 'apikey', 'authorization:', 'service_role']):
            return '[REDACTED]'
        if len(value) > 900:
            return value[:900] + ' …[TRUNCATED]'
    return value


def compact_params(n: dict[str, Any] | None) -> str:
    if not n:
        return '_Node not found._'
    subset = {
        'type': n.get('type'),
        'disabled': n.get('disabled', False),
        'continueOnFail': n.get('continueOnFail'),
        'onError': n.get('onError'),
        'retryOnFail': n.get('retryOnFail'),
        'parameters': redact_value('parameters', n.get('parameters', {})),
    }
    return json.dumps(subset, indent=2, ensure_ascii=False, sort_keys=True)


def downstream_names(wf: dict[str, Any], source_name: str) -> list[str]:
    conns = wf.get('connections', {})
    out = []
    for conn_group in conns.get(source_name, {}).values():
        for branch in conn_group:
            if isinstance(branch, list):
                for c in branch:
                    if isinstance(c, dict) and c.get('node'):
                        out.append(c['node'])
    return out


def find_nodes_containing(wf: dict[str, Any], needle: str) -> list[str]:
    found = []
    for n in nodes(wf):
        txt = json.dumps(n.get('parameters', {}), ensure_ascii=False, default=str).lower()
        if needle.lower() in txt:
            found.append(n.get('name', '(unnamed)'))
    return found


def main() -> None:
    workflows = {k: load(v) for k, v in FILES.items()}
    lines: list[str] = [
        '# Newsletter Failure-Surface Evidence',
        '',
        'This evidence file is generated from versioned n8n workflow exports. It redacts credential-like fields and focuses on execution settings, gates, storage writes, and delivery ledgers.',
        '',
        '## Workflow Counts',
        '',
        '| Workflow | File | Node Count |',
        '| --- | --- | ---: |',
    ]
    for key, wf in workflows.items():
        lines.append(f"| `{key}` | `{FILES[key].relative_to(ROOT)}` | {len(nodes(wf))} |")

    lines += ['', '## Target Node Settings', '']
    for key, names in TARGET_NODES.items():
        wf = workflows[key]
        lines += [f'### {key.title()} Workflow', '']
        for name in names:
            n = node_by_name(wf, name)
            lines += [f'#### {name}', '', '```json', compact_params(n), '```', '']
            if n:
                ds = downstream_names(wf, name)
                if ds:
                    lines += ['Downstream nodes: `' + '`, `'.join(ds) + '`', '']

    lines += ['', '## Cross-Cutting Search Evidence', '', '| Needle | Workflows / Nodes Found |', '| --- | --- |']
    needles = ['raw_perplexity_data', 'nationalContext', 'newsletter_enabled', 'generation_status', 'status', 'sent', 'content_splinters', 'splinter_usage', 'delivery_variants']
    for needle in needles:
        parts = []
        for key, wf in workflows.items():
            found = find_nodes_containing(wf, needle)
            if found:
                parts.append(f'`{key}`: ' + ', '.join(f'`{x}`' for x in found[:12]))
        lines.append(f"| `{needle}` | {'; '.join(parts) if parts else '_None_'} |")

    lines += ['', '## Initial Failure Hypotheses From Settings', '']
    dispatch_send = node_by_name(workflows['dispatch'], 'Send Email via GHL')
    dispatch_log = node_by_name(workflows['dispatch'], 'Log Delivery')
    brain_schedule = node_by_name(workflows['brain'], 'Schedule Outbound Check')
    altos = node_by_name(workflows['creation'], 'Altos Get Stats')
    lines += [
        '| Finding | Evidence | Why It Matters |',
        '| --- | --- | --- |',
        f"| GHL email send may continue after API failure. | `Send Email via GHL` has `onError={dispatch_send.get('onError') if dispatch_send else None}` and downstream `{downstream_names(workflows['dispatch'], 'Send Email via GHL')}`. | If downstream logging treats continued output as success, send ledgers can become false positives. |",
        f"| Delivery logging can be downstream of a failed send. | `Log Delivery` node exists with parameters `{json.dumps(redact_value('parameters', dispatch_log.get('parameters', {}) if dispatch_log else {}), ensure_ascii=False)[:350]}`. | A false `sent` row can suppress resends because `newsletter_deliveries` is a cadence ledger. |",
        f"| SMS splinter scheduler is disabled in the Brain Engine export. | `Schedule Outbound Check` has `disabled={brain_schedule.get('disabled') if brain_schedule else None}`. | The splinter path may exist structurally without being actively scheduled from this workflow. |",
        f"| Altos fetch is configured to continue on failure. | `Altos Get Stats` has `continueOnFail={altos.get('continueOnFail') if altos else None}` and downstream `{downstream_names(workflows['creation'], 'Altos Get Stats')}`. | Market data gaps may flow into newsletter generation unless downstream validation blocks bad inputs. |",
    ]
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
