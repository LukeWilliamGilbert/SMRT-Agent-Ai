#!/usr/bin/env python3
"""Extract newsletter-related Supabase schema evidence for audit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
SRC = ROOT / 'data/supabase/schema_inventory_clean.json'
OUT = ROOT / 'docs/system/newsletter_schema_evidence.md'
TABLES = ['agents', 'newsletters', 'newsletter_deliveries', 'content_splinters', 'splinter_usage', 'altos_weekly_stats', 'documents', 'leads']
KEYWORDS = ['newsletter', 'splinter', 'altos', 'outbound', 'sms', 'paused', 'blocked', 'agent_dormant', 'next_outbound', 'market', 'zip', 'fips', 'pai', 'delivery', 'status', 'week_start', 'active', 'contact', 'email']

def table_name(obj):
    return obj.get('table_name') or obj.get('name') or obj.get('table')

def cols_for(t):
    cols = t.get('columns', [])
    out = []
    if isinstance(cols, dict):
        cols = [{'column_name': k, **(v if isinstance(v, dict) else {'type': str(v)})} for k, v in cols.items()]
    for c in cols:
        name = c.get('column_name') or c.get('name')
        if not name:
            continue
        if table_name(t) in ['newsletters','newsletter_deliveries','content_splinters','splinter_usage','altos_weekly_stats'] or any(k in name.lower() for k in KEYWORDS):
            out.append(c)
    return out

def compact(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True)

def main():
    data = json.loads(SRC.read_text())
    tables = data.get('tables') if isinstance(data, dict) else data
    if isinstance(tables, dict):
        table_map = tables
    else:
        table_map = {table_name(t): t for t in tables if table_name(t)}
    lines = ['# Newsletter Schema Evidence', '', 'This local evidence extract summarizes database structures that interact with newsletter generation, dispatch, and splinter delivery.', '']
    for name in TABLES:
        t = table_map.get(name)
        if not t:
            lines += [f'## {name}', '', '**Not found in schema inventory.**', '']
            continue
        lines += [f'## {name}', '', '| Field | Value |', '| --- | --- |']
        for meta_key in ['estimated_rows', 'row_count', 'description']:
            if meta_key in t:
                lines.append(f'| {meta_key} | `{t[meta_key]}` |')
        lines += ['', '### Relevant columns', '', '| Column | Type | Nullable | Default |', '| --- | --- | --- | --- |']
        for c in cols_for(t):
            cname = c.get('column_name') or c.get('name')
            ctype = c.get('data_type') or c.get('type') or c.get('udt_name') or ''
            nullable = c.get('is_nullable') or c.get('nullable') or ''
            default = c.get('column_default') or c.get('default') or ''
            default_s = str(default).replace('|', '\\|')
            lines.append(f'| `{cname}` | `{ctype}` | `{nullable}` | `{default_s}` |')
        for section in ['constraints', 'indexes', 'foreign_keys', 'policies']:
            vals = t.get(section) or []
            if vals:
                lines += ['', f'### {section.replace("_", " ").title()}', '', '| Evidence |', '| --- |']
                for v in vals:
                    evidence_s = compact(v).replace('|', '\\|')
                    lines.append(f'| `{evidence_s}` |')
        lines.append('')
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
