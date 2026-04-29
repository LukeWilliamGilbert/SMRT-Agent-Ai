#!/usr/bin/env python3.11
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
SCHEMA = ROOT / 'data' / 'supabase' / 'schema_inventory_clean.json'
OUT = ROOT / 'data' / 'supabase' / 'prompt_schema_columns.txt'
TABLES = [
    'agents',
    'prompt_blocks',
    'static_prompt_sections',
    'system_defaults',
    'conversation_context',
    'leads',
    'message_log',
    'ai_output_errors',
    'agent_rules',
]

def get_tables(data):
    if isinstance(data, dict) and 'tables' in data:
        tables = data['tables']
        if isinstance(tables, list):
            return {t.get('table_name') or t.get('name'): t for t in tables if isinstance(t, dict)}
        if isinstance(tables, dict):
            return tables
    if isinstance(data, list):
        return {t.get('table') or t.get('table_name') or t.get('name'): t for t in data if isinstance(t, dict)}
    return {}

def main():
    data = json.loads(SCHEMA.read_text())
    tables = get_tables(data)
    lines = []
    for table in TABLES:
        t = tables.get(table)
        lines.append(f'## {table}')
        if not t:
            lines.append('NOT FOUND')
            lines.append('')
            continue
        columns = t.get('columns') or []
        for c in columns:
            if isinstance(c, dict):
                lines.append(f"- {c.get('column_name') or c.get('name')}: {c.get('data_type') or c.get('type')} nullable={c.get('is_nullable') or c.get('nullable')} default={c.get('column_default') or c.get('default')}")
        lines.append('')
    OUT.write_text('\n'.join(lines))
    print(OUT)

if __name__ == '__main__':
    main()
