#!/usr/bin/env python3.11
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF = ROOT / 'workflows' / 'active' / 'SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json'
OUT = ROOT / 'docs' / 'system' / 'brain_engine_prompt_assembly_full.md'
OUT_JSON = ROOT / 'data' / 'workflows' / 'brain_engine_prompt_assembly_nodes.json'
NODE_NAMES = [
    'Assemble System Prompt',
    'Gather Prompt Data',
    'Get Prompt Blocks (SMRT)',
    'Get Static Prompt Sections',
    'Get Default Personality',
    'Prepare Tier Response',
]


def main():
    wf = json.loads(WF.read_text())
    nodes = {n.get('name'): n for n in wf.get('nodes', []) if isinstance(n, dict)}
    selected = []
    for name in NODE_NAMES:
        n = nodes.get(name)
        if n:
            selected.append(n)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(selected, indent=2, ensure_ascii=False))

    lines = [
        '# Brain Engine Prompt Assembly Full Node Evidence',
        '',
        'Author: **Manus AI**',
        'Date: **2026-04-29**',
        '',
        'This evidence file extracts the complete parameters for the active Brain Engine nodes that retrieve, gather, and assemble prompt material before the `AI Agent` node. No production changes were made.',
        '',
    ]
    for n in selected:
        lines.append(f"## {n.get('name')}")
        lines.append('')
        lines.append(f"Type: `{n.get('type')}`")
        lines.append('')
        lines.append('```json')
        lines.append(json.dumps(n.get('parameters', {}), indent=2, ensure_ascii=False))
        lines.append('```')
        lines.append('')
    OUT.write_text('\n'.join(lines))
    print(f'Wrote {OUT}')
    print(f'Wrote {OUT_JSON}')

if __name__ == '__main__':
    main()
