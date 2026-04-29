#!/usr/bin/env python3
import json, re
from pathlib import Path
raw = Path('/home/ubuntu/SMRT-Agent-Ai/data/supabase/schema_inventory_raw.json').read_text()
outer = json.loads(raw.split('Tool execution result:\n', 1)[1]) if 'Tool execution result:\n' in raw else json.loads(raw)
result = outer.get('result','')
matches = re.findall(r'<untrusted-data-[^>]+>\s*(.*?)\s*</untrusted-data-[^>]+>', result, re.S)
print('match_count', len(matches))
for i,m in enumerate(matches):
    print('---', i, 'len', len(m))
    print(repr(m[:200]))
