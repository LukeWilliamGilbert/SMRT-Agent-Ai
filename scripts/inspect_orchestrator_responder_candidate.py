#!/usr/bin/env python3
"""Read-only Brain Engine inspector for orchestrator->responder renovation planning."""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path('/home/ubuntu/SMRT-Agent-Ai')
WF = ROOT / 'workflows/active/SMRT_Brain_Engine__mlR5dZuzXxP_JYGaqrqpu.json'
OUT = ROOT / 'docs/system/orchestrator_responder_current_state_evidence.md'

SECRET_PATTERNS = [
    re.compile(r'(Bearer\s+)[A-Za-z0-9._\-]+', re.I),
    re.compile(r'(apikey|api[_-]?key|authorization|token|secret|password)\s*[:=]\s*["\']?[^"\'\s,}]+', re.I),
]

def red(s):
    if s is None:
        return ''
    s = str(s)
    for p in SECRET_PATTERNS:
        s = p.sub(lambda m: (m.group(1) if m.lastindex else '') + '[REDACTED]', s)
    return s

def trunc(s, n=1600):
    s = red(s)
    return s if len(s) <= n else s[:n] + f"\n...[truncated {len(s)-n} chars]"

def flatten_text(obj):
    found=[]
    def walk(x, path=''):
        if isinstance(x, dict):
            for k,v in x.items():
                walk(v, f'{path}.{k}' if path else str(k))
        elif isinstance(x, list):
            for i,v in enumerate(x):
                walk(v, f'{path}[{i}]')
        elif isinstance(x, str):
            if len(x)>30 and any(w in x.lower() for w in ['prompt','respond','response','tool','appointment','schedule','conversation','summary','ghl','sms','message','system']):
                found.append((path, x))
    walk(obj)
    return found

wf=json.loads(WF.read_text())
nodes=wf.get('nodes',[])
node_by_name={n.get('name'): n for n in nodes}
connections=wf.get('connections',{})

# Reverse and outgoing maps by node name; include connection type labels.
out=defaultdict(list)
incoming=defaultdict(list)
for src, groups in connections.items():
    for ctype, arr in groups.items():
        # arr can be list of lists of edge dicts
        if isinstance(arr, list):
            for channel_i, channel in enumerate(arr):
                if isinstance(channel, list):
                    for edge in channel:
                        tgt=edge.get('node')
                        if tgt:
                            out[src].append((tgt, ctype, channel_i))
                            incoming[tgt].append((src, ctype, channel_i))

agent_nodes=[]
toolish=[]
for n in nodes:
    typ=n.get('type','')
    name=n.get('name','')
    params=n.get('parameters',{})
    if 'agent' in typ.lower() or 'lmChat' in typ or 'openAi' in typ or 'chain' in typ.lower():
        agent_nodes.append(n)
    if 'tool' in typ.lower() or 'Tool' in name or any(('tool' in str(k).lower()) for k in params.keys()):
        foolish=False
        toolish.append(n)

# Search terms relevant to response path.
terms=['Analyze Conversation','conversation_context','message_log','Send','GHL','Appointment','Availability','Book','newsletter','summary','prompt','AI Agent','agent','OpenAI','Tool']
matched=[]
for n in nodes:
    blob=json.dumps(n.get('parameters',{}), ensure_ascii=False)
    lname=n.get('name','')+' '+n.get('type','')+' '+blob
    if any(t.lower() in lname.lower() for t in terms):
        matched.append(n)

lines=[]
lines.append('# Orchestrator-to-Responder Current-State Evidence')
lines.append('')
lines.append(f'- Workflow file: `{WF.relative_to(ROOT)}`')
lines.append(f'- Workflow name: `{wf.get("name")}`')
lines.append(f'- Node count: **{len(nodes)}**')
lines.append(f'- Connection source count: **{len(connections)}**')
lines.append('')
lines.append('## Candidate LLM / Agent Nodes')
lines.append('')
lines.append('| Node | Type | Incoming | Outgoing | Key Parameters |')
lines.append('|---|---|---:|---:|---|')
for n in agent_nodes:
    name=n.get('name','')
    params=n.get('parameters',{})
    keys=', '.join(list(params.keys())[:12])
    lines.append(f'| `{name}` | `{n.get("type","")}` | {len(incoming[name])} | {len(out[name])} | {red(keys)} |')
lines.append('')
lines.append('## Candidate Tool / Operational Nodes')
lines.append('')
lines.append('| Node | Type | Incoming Types | Outgoing Targets |')
lines.append('|---|---|---|---|')
for n in toolish:
    name=n.get('name','')
    inc=', '.join(sorted(set(t for _,t,_ in incoming[name])))
    outs=', '.join([x[0] for x in out[name]][:8])
    lines.append(f'| `{name}` | `{n.get("type","")}` | `{inc}` | `{outs}` |')
lines.append('')
lines.append('## Matched Prompt / Summary / Delivery / Scheduling Nodes')
lines.append('')
lines.append('| Node | Type | Incoming | Outgoing |')
lines.append('|---|---|---:|---:|')
for n in matched:
    name=n.get('name','')
    lines.append(f'| `{name}` | `{n.get("type","")}` | {len(incoming[name])} | {len(out[name])} |')
lines.append('')

# Detailed selected nodes containing specific names/keywords.
important=[]
for n in matched:
    name=n.get('name','')
    typ=n.get('type','')
    blob=json.dumps(n.get('parameters',{}), ensure_ascii=False)
    if any(w in (name+' '+typ+' '+blob).lower() for w in ['agent','analyze conversation','send','appointment','availability','book','message_log','conversation_context','prompt','system prompt','ghl']):
        important.append(n)

lines.append('## Detailed Evidence Snippets')
for n in important:
    name=n.get('name','')
    lines.append('')
    lines.append(f'### `{name}`')
    lines.append('')
    lines.append(f'- Type: `{n.get("type","")}`')
    lines.append(f'- Incoming: `{incoming[name][:10]}`')
    lines.append(f'- Outgoing: `{out[name][:10]}`')
    lines.append('- Parameter keys: `' + ', '.join(n.get('parameters',{}).keys()) + '`')
    texts=flatten_text(n.get('parameters',{}))[:8]
    if texts:
        for path,txt in texts:
            lines.append(f'\n**Text at `{path}`:**')
            lines.append('')
            lines.append('```text')
            lines.append(trunc(txt, 2200))
            lines.append('```')
    else:
        lines.append('')
        lines.append('```json')
        lines.append(trunc(json.dumps(n.get('parameters',{}), indent=2, ensure_ascii=False), 1800))
        lines.append('```')

OUT.write_text('\n'.join(lines)+'\n')
print(OUT)
