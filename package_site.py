#!/usr/bin/env python3
"""Build and package only public files. No research/workspace files are published."""
from pathlib import Path
import json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(ROOT/'atlas.py')],check=True)
manifest=json.loads((ROOT/'build-manifest.json').read_text())
dist=ROOT/'dist'
if dist.exists():shutil.rmtree(dist)
dist.mkdir()
files=list(manifest['pages'])+['assets/atlas.css','assets/atlas.js']
figure_keys=['v6','v8','v12']+sorted(set(json.loads((ROOT/'figures-map.json').read_text()).values())) if (ROOT/'figures-map.json').exists() else ['v6','v8','v12']
files += [f'assets/figures/{engine}.{ext}' for engine in figure_keys for ext in ('html','svg')]
files += ['assets/figures/_embed-lite.js']
files += ['assets/figures/LICENSE-anatomy.txt']
for name in files:
 target=dist/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
site=os.environ.get('ATLAS_SITE_URL','').rstrip('/')
robots='User-agent: *\nAllow: /\n'
if site:
 if not site.startswith('https://'):raise SystemExit('ATLAS_SITE_URL must be an https:// public origin.')
 canonical=[p for p in manifest['pages'] if p.startswith(('zh/','en/'))]
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{site}/{p}</loc></url>' for p in canonical)+'</urlset>\n'
 (dist/'sitemap.xml').write_text(sitemap);robots+=f'Sitemap: {site}/sitemap.xml\n'
(dist/'robots.txt').write_text(robots)
(dist/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>404 · Engine Atlas</title><style>body{font:16px monospace;background:#ebebea;margin:4rem;line-height:1.8}a{color:inherit}</style><h1>404</h1><p>此页不存在 / Page not found.</p><a href="/zh/index.html">中文图谱</a> · <a href="/en/index.html">English atlas</a></html>')
print(f'Packaged {len(files)} explicitly allowed files in {dist}. Private records excluded.')
