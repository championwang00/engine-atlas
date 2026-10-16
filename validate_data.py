#!/usr/bin/env python3
"""Check cross-file integrity, localisation and evidence bookkeeping before packaging."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parent
load=lambda p:json.loads((ROOT/p).read_text())
entries=load('catalog.json');terms=load('terms.json');content=load('content.json');english=load('english.json');intro=load('intro-current.json');timeline=load('f1-eras.json')
errors=[];warnings=[];by={e['id']:e for e in entries};tb={t['id']:t for t in terms}
if len(by)!=len(entries):errors.append('Duplicate entry IDs')
if len(tb)!=len(terms):errors.append('Duplicate term IDs')
for n in range(1,53):
 if f'EA-{n:03d}' not in by:errors.append(f'Lost legacy ID EA-{n:03d}')
expected={'ext','proto','layout','unconv','boost','valve','control','combustion','diesel','fuel','hybrid','model'}
actual={e['type'] for e in entries if e['kind']!='era'}
if actual!=expected:errors.append(f'Category mismatch {actual^expected}')
for e in entries:
 pid=e['id']
 for table,name in [(content,'content'),(english,'english'),(intro,'intro')]:
  if pid not in table:errors.append(f'{pid} missing {name}')
 for key in ['description','principle','examples','tradeoffs','status','intro']:
  value=english.get(pid,{}).get(key,'')
  if not value:errors.append(f'{pid} missing English {key}')
  if re.search(r'[\u4e00-\u9fff]',value):errors.append(f'{pid} Chinese fallback in English {key}')
 if not content.get(pid,{}).get('sources'):errors.append(f'{pid} missing sources')
 if e.get('parent') and e['parent'] not in by:errors.append(f'{pid} unknown parent')
 if e.get('parent_term') and e['parent_term'] not in tb:errors.append(f'{pid} unknown parent term')
 if e.get('parent')==pid:errors.append(f'{pid} self-parent')
 if e['kind']=='variant' and not (e.get('parent') or e.get('parent_term')):errors.append(f'{pid} variant lacks parent')
 visited=set();p=pid
 while p in by and by[p].get('parent'):
  if p in visited:errors.append(f'{pid} cyclic parent');break
  visited.add(p);p=by[p]['parent']
for t in terms:
 if not t.get('def_en'):errors.append(f'{t["id"]} missing English definition')
 if re.search(r'[\u4e00-\u9fff]',t.get('def_en','')):errors.append(f'{t["id"]} Chinese fallback in English definition')
 for r in t.get('related',[]):
  if r not in tb:errors.append(f'{t["id"]} unknown related term {r}')
 entry=t.get('entry');entry=f'EA-{entry:03d}' if isinstance(entry,int) else entry
 if entry and entry not in by:errors.append(f'{t["id"]} unknown entry {entry}')
for row in timeline:
 for key in ['year','title','summary','en_title','en_summary','sources']:
  if not row.get(key):errors.append(f'F1 {row.get("year")} missing {key}')
 for pid in row.get('entries',[]):
  if pid not in by:errors.append(f'F1 row unknown entry {pid}')
# Evidence logs contain source-specific review notes, not just HTTP status.
logs=[]
for p in (ROOT/'work').glob('source-log-*.json'):
 obj=json.loads(p.read_text());logs+=obj if isinstance(obj,list) else obj.get('sources',[])
known={x.get('url') for x in logs if x.get('opened_at')}
supported={x.get('url') for x in logs if x.get('opened_at') and x.get('result') in ['verified','qualified','opened_supported']}
missing=[]
cited=set()
for pid,c in content.items():
 for source in c.get('sources',[])+intro.get(pid,{}).get('sources',[]):
  cited.add(source['url'])
  if source['url'] not in known:missing.append({'id':pid,'url':source['url']})
  elif source['url'] not in supported:errors.append(f'{pid} cited source has no successful evidence review: {source["url"]}')
for row in terms+timeline:
 for source in row.get('sources',[]):
  cited.add(source['url'])
  if source['url'] not in supported:errors.append(f'{row.get("id",row.get("year"))} term/timeline source lacks a successful evidence review: {source["url"]}')
if missing:errors.append(f'{len(missing)} source references have no opened-source log')
report={'entries':len(entries),'catalog_entries':sum(e['kind']!='era' for e in entries),'categories':len(actual),'terms':len(terms),'f1_eras':len(timeline),'pending':[pid for pid,c in content.items() if c.get('verify')!='ok'],'source_log_urls':len(known),'cited_source_urls':len(cited),'reviewed_source_urls':len(supported),'missing_source_logs':missing,'errors':errors,'warnings':warnings}
(ROOT/'work/data-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
