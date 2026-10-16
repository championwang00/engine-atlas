#!/usr/bin/env python3
"""Merge figures-map-*.json (one per drawing agent) into figures-map.json, keep only entries whose
assets/figures/<key>.html and .svg both exist, attach to catalog.json, then rebuild the site."""
import json,glob,pathlib,subprocess,sys
root=pathlib.Path(__file__).parent
merged={}
base=root/'figures-map.json'
if base.exists(): merged.update(json.loads(base.read_text()))
for f in sorted(glob.glob(str(root/'figures-map-*.json'))):
    try: merged.update(json.loads(pathlib.Path(f).read_text()))
    except Exception as e: print('skip',f,e)
ok={k:v for k,v in merged.items() if (root/'assets/figures'/f'{v}.html').exists() and (root/'assets/figures'/f'{v}.svg').exists()}
bad={k:v for k,v in merged.items() if k not in ok}
base.write_text(json.dumps(dict(sorted(ok.items())),ensure_ascii=False,indent=1))
print('figures attached:',len(ok),'| missing files:',bad)
subprocess.run([sys.executable,str(root/'apply_figures.py')],check=True)
subprocess.run([sys.executable,str(root/'atlas.py')],check=True)
