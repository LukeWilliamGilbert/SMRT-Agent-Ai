#!/usr/bin/env python3.11
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
SANITIZED = ROOT / 'workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json'
RAW_ALL = Path('/home/ubuntu/smrt_analysis/raw_export/root/smrt_n8n_export_20260428_194357/workflows/smrt_workflows_all.json')
OUT = ROOT / 'docs/system/assemble_system_prompt_code.md'

SECRET_PATTERNS = [
    (re.compile(r'(supabaseServiceKey\s*=\s*)[`\'\"][^`\'\"]+[`\'\"]', re.I), r'\1[REDACTED]'),
    (re.compile(r'(service[_-]?role[^\n:=]*[:=]\s*)[`\'\"][^`\'\"]+[`\'\"]', re.I), r'\1[REDACTED]'),
    (re.compile(r'(apikey|apiKey|authorization|Authorization|bearer|Bearer)\s*[:=]\s*[`\'\"][^`\'\"]+[`\'\"]', re.I), r'\1: [REDACTED]'),
    (re.compile(r'(Authorization["\']?\s*:\s*["\']Bearer\s+)[^"\']+', re.I), r'\1[REDACTED]'),
]

def redact(s: str) -> str:
    out = s
    for pat, repl in SECRET_PATTERNS:
        out = pat.sub(repl, out)
    # Redact likely JWT/service tokens if any remain.
    out = re.sub(r'eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}', '[REDACTED_JWT]', out)
    return out

def find_node_from_workflow(wf: dict):
    for n in wf.get('nodes', []) or []:
        if n.get('name') == 'Assemble System Prompt':
            return n
    return None

def load_node():
    wf = json.loads(SANITIZED.read_text())
    node = find_node_from_workflow(wf)
    code = (node or {}).get('parameters', {}).get('jsCode', '')
    if code and code != '[REDACTED]':
        return 'sanitized workflow', code
    raw = json.loads(RAW_ALL.read_text())
    for wf in raw:
        if wf.get('name') == '🧠 SMRT Brain Engine' or wf.get('id') == 'mlR5dZuzXxP_JYGaqrqpu':
            node = find_node_from_workflow(wf)
            code = (node or {}).get('parameters', {}).get('jsCode', '')
            return 'raw all-workflows export with secret redaction applied', code
    # fallback scan
    for wf in raw:
        node = find_node_from_workflow(wf)
        if node:
            return f"raw all-workflows export workflow={wf.get('name')}", node.get('parameters', {}).get('jsCode', '')
    raise SystemExit('Assemble System Prompt node not found')

source, code = load_node()
code = redact(code or '')
interesting = []
for i, line in enumerate(code.splitlines(), 1):
    low = line.lower()
    if any(k in low for k in ['static', 'prompt', 'block', 'section', 'fallback', 'systemmessage', 'system_prompt', 'conversation', 'summary', 'return', 'context', 'messagehistory', 'personality', 'included']):
        interesting.append((i, line))

lines = []
lines.append('# Assemble System Prompt Code Evidence')
lines.append('')
lines.append('Author: **Manus AI**')
lines.append('Date: **2026-04-29**')
lines.append('')
lines.append(f'Source: `{source}`.')
lines.append('')
lines.append('This file captures the `Assemble System Prompt` code node with basic secret redaction. It is evidence only; no production workflow was changed.')
lines.append('')
lines.append('## High-Signal Lines')
lines.append('')
lines.append('```text')
for i, line in interesting[:260]:
    lines.append(f'{i:04d}: {line}')
if len(interesting) > 260:
    lines.append(f'... {len(interesting)-260} additional matching lines omitted; full code below.')
lines.append('```')
lines.append('')
lines.append('## Full Code')
lines.append('')
lines.append('```javascript')
lines.append(code)
lines.append('```')
OUT.write_text('\n'.join(lines) + '\n')
print(OUT)
print(f'source={source}')
print(f'code_lines={len(code.splitlines())} high_signal_lines={len(interesting)}')
