#!/usr/bin/env python3
import json
from pathlib import Path

schema_path = Path('/home/ubuntu/SMRT-Agent-Ai/data/supabase/schema_inventory_clean.json')
data = json.loads(schema_path.read_text())

tables = ['message_log','inbound_capture','message_send_errors','system_errors','conversation_context','leads','appointments']

# The parser output stores table details in a JSON payload returned by Supabase. Be tolerant of either
# top-level lists or nested dictionaries because future inventory parsers may shape the artifact differently.
def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item)

table_objects = [row for row in walk(data) if row.get('table') in tables and isinstance(row.get('columns'), list)]

for table in tables:
    print(f"\n## {table}")
    table_obj = next((row for row in table_objects if row.get('table') == table), None)
    columns = table_obj.get('columns', []) if table_obj else []
    columns.sort(key=lambda c: (c.get('ordinal_position') is None, c.get('ordinal_position') or 9999, c.get('column_name') or ''))
    if not columns:
        print('(no columns found)')
        continue
    for c in columns:
        print(f"{c.get('column_name')} | {c.get('data_type')} | nullable={c.get('is_nullable')} | default={c.get('column_default')}")
