#!/usr/bin/env python3
import json
from pathlib import Path
schema=json.loads(Path('/home/ubuntu/SMRT-Agent-Ai/data/supabase/schema_inventory_clean.json').read_text())
for table in ['appointments','leads','conversation_context','message_log','inbound_capture','agents','onboarding_requests','audit_log']:
    item=next((x for x in schema if x['table']==table), None)
    if not item:
        continue
    print('\n##', table)
    for col in item['columns']:
        print(col['column_name'], col['data_type'], col.get('is_nullable'))
