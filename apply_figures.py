#!/usr/bin/env python3
"""Attach drawn figures to catalog.json without re-running the whole research merge.
figures-map.json: {"EA-009": "single", ...}. A figure counts only if assets/figures/<key>.html and .svg both exist."""
import json,pathlib
root=pathlib.Path(__file__).parent
fm=json.loads((root/'figures-map.json').read_text()) if (root/'figures-map.json').exists() else {}
cat=json.loads((root/'catalog.json').read_text())
ok=0;miss=[]
for e in cat:
    key=fm.get(e['id'])
    if not key: continue
    if (root/'assets/figures'/f'{key}.html').exists() and (root/'assets/figures'/f'{key}.svg').exists():
        e['figure']=key; ok+=1
    else: miss.append((e['id'],key))
(root/'catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=1))
print('attached',ok,'missing files',miss)
