#!/usr/bin/env python3
"""Merge reviewed research artifacts into stable content files; rerunnable by ID."""
from pathlib import Path
import json as _fjson, pathlib as _fpath
_fm=_fpath.Path(__file__).with_name('figures-map.json')
FIGURE_MAP=_fjson.loads(_fm.read_text()) if _fm.exists() else {}

import json,re
ROOT=Path(__file__).resolve().parent
load=lambda name:json.loads((ROOT/name).read_text())
def save(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sources(a,b):return list({x['url']:x for x in a+b}.values())
def verified(v):return 'ok' if v in ('ok','verified') else 'pending'
base=load('work/baseline/entries.json')
catalog={r['id']:{'id':r['id'],'n':r['n'],'cn':r['name'],'en':r['en'],'type':r['type'],'year':int(re.search(r'\d{4}',r['year'])[0]),'shown_year':r['year'],'description':r['desc'],'kind':'concept','year_basis':'代表性里程碑'} for r in base}
content={};intro={};english={};mentions={}
for p in sorted(ROOT.glob('mentions-[1-4].json')):mentions.update(json.loads(p.read_text()))
if (ROOT/'work/mentions-reconciled.json').exists():
 for pid,patch in load('work/mentions-reconciled.json').items():
  old=mentions.setdefault(pid,{'examples':[],'intro':[]})
  if isinstance(old,list):old=mentions[pid]={'examples':old,'intro':old}
  # Keep unrelated entities, while preferring the newly checked core-name records.
  for section,rows in patch.items():
   old[section]=rows+[row for row in old.get(section,[]) if not any(r['match'].casefold() in row['match'].casefold() or row['match'].casefold() in r['match'].casefold() for r in rows)]
existing=load('work/research-existing.json')
if len(existing)!=52:raise SystemExit(f'Existing research incomplete: {len(existing)}/52')
for pid,r in existing.items():
 catalog[pid].update(r.get('entry_patch',{}));content[pid]=r['content'];intro[pid]=r['intro'];english[pid]=r['english']
 content[pid]['verify']=verified(content[pid].get('verify'));intro[pid]['verify']=verified(intro[pid].get('verify'))

research_files=sorted({str(p.relative_to(ROOT)) for pattern in ['research-*.json','new*.json','primary-supplement*.json'] for p in (ROOT/'work').glob(pattern) if p.name!='research-existing.json'})
research_files.sort(key=lambda name:not Path(name).name.startswith('research-'))
for filename in research_files:
 if not (ROOT/filename).exists():continue
 research=load(filename)
 for r in research.get('entries',[]):
  pid=r['id'];catalog[pid]={k:v for k,v in r.items() if k not in ['content','intro','english','mentions','note']}
  catalog[pid]['n']=int(pid[3:]);content[pid]=r['content'];intro[pid]=r['intro'];english[pid]=r['english']
  content[pid]['verify']=verified(content[pid].get('verify'));intro[pid]['verify']=verified(intro[pid].get('verify'))
  mentions[pid]={'examples':r.get('mentions',[]),'intro':r.get('mentions',[])}
 merge_rows=research.get('merges',{})
 if isinstance(merge_rows,list):merge_rows={m.get('id',m.get('entry_id')):m for m in merge_rows}
 for pid,m in merge_rows.items():
  if pid not in catalog:continue
  # Research directions are notes; only explicit reader-facing publication prose is appended.
  zh=m.get('publication_text');en=m.get('publication_text_en')
  if m.get('sources'):
   content[pid]['sources']=sources(content[pid].get('sources',[]),m['sources'])
   intro[pid]['sources']=sources(intro[pid].get('sources',[]),m['sources'])
  if zh:
   intro[pid]['intro']+='\n\n'+zh;english[pid]['intro']+='\n\n'+(en or '')
   intro[pid]['sources']=sources(intro[pid].get('sources',[]),m.get('sources',[]))
   intro[pid]['note']=intro[pid].get('note','')+'；追加覆盖：'+m.get('action','research merge')
  if m.get('entry_patch'):catalog[pid].update(m['entry_patch'])
  if m.get('content_patch'):content[pid].update(m['content_patch'])
  if m.get('english_patch'):english[pid].update(m['english_patch'])
  if m.get('mentions'):
   old=mentions.setdefault(pid,{'examples':[],'intro':[]})
   if isinstance(old,list):old=mentions[pid]={'examples':old,'intro':old}
   old.setdefault('intro',[]).extend(m['mentions']);old.setdefault('examples',[]).extend(m['mentions'])
if (ROOT/'work/mentions-supplement.json').exists():
 for pid,rows in load('work/mentions-supplement.json').items():
  old=mentions.setdefault(pid,{'examples':[],'intro':[]})
  if isinstance(old,list):old=mentions[pid]={'examples':old,'intro':old}
  old.setdefault('intro',[]).extend(rows)
# Categories and conceptual levels are independent of chronology.
for pid,e in catalog.items():
 if e['type'] in ['cycle','support']:e['type']='combustion'
 if e.get('kind')=='model':e['type']='model'
 if pid in ['EA-034','EA-043','EA-047','EA-052']:e.update(kind='era',type='f1')
 if pid in ['EA-032','EA-035','EA-041']:e['type']='valve'
 if pid in ['EA-030','EA-038']:e['type']='control'
 if pid in ['EA-049','EA-050']:e['type']='combustion'
 if pid in ['EA-010','EA-039']:e['type']='diesel'
 if pid in ['EA-035','EA-041']:e.update(kind='variant',parent='EA-032')
 if pid in ['EA-049','EA-050']:
  e.update(kind='variant',parent_term='vcr' if pid=='EA-049' else 'hcci')
  matches=[v for v in catalog.values() if v['id']!=pid and v['kind']=='concept' and (bool(re.search(r'variable (?:geometric )?compression',v['en'].lower())) if pid=='EA-049' else ('hcci' in v['en'].lower() or 'homogeneous charge' in v['en'].lower()))]
  if matches:e['parent']=matches[0]['id'];e.pop('parent_term',None)
 if pid in ['EA-014','EA-015','EA-025']:e['figure']={'EA-014':'v8','EA-015':'v12','EA-025':'v6'}[pid]
 # figures-map.json: {"EA-nnn": "<figure key>"} for engine figures drawn later (assets/figures/<key>.html + .svg)
 if pid in FIGURE_MAP:e['figure']=FIGURE_MAP[pid]
 e.setdefault('year_basis','代表性里程碑');e.setdefault('kind','concept');e.setdefault('shown_year',str(e['year']))
 e['year']=int(e['year'])
 # The English date label is compact. Full context remains in translated examples and history.
 e.setdefault('shown_year_en',str(e['year']))
 e.setdefault('year_basis_en','Representative milestone; see the history and cited sources.')

terms={x['id']:x for x in load('work/baseline/terms.json')}
for filename in ['work/terms-additions.json','work/terms-expansion.json']:
 if not (ROOT/filename).exists():continue
 obj=load(filename)
 if isinstance(obj,list):new=obj;patches={}
 else:
  new=obj.get('terms',obj.get('additions',obj.get('new_terms',[])));patches=obj.get('patches',{})
 for t in new:terms[t['id']]=t
 if isinstance(patches,list):patches={t['id']:t for t in patches}
 for key,patch in patches.items():
  if key in terms:terms[key].update(patch)
for tid,pid in {'commonrail':'EA-039','gdi':'EA-038','vvt':'EA-032','vcr':'EA-049','ignition':'EA-010'}.items():
 if tid in terms:terms[tid]['entry']=pid
for e in catalog.values():
 if 'hcci' in e['en'].lower() and e['kind']=='concept' and 'hcci' in terms:terms['hcci']['entry']=e['id']
 if re.search(r'variable (?:geometric )?compression',e['en'].lower()) and e['kind']=='concept':terms['vcr']['entry']=e['id']
images=load('work/preview-images.json') if (ROOT/'work/preview-images.json').exists() else {}
for key,im in images.get('terms',{}).items():
 if key in terms:terms[key]['image']=im
for p in sorted((ROOT/'work').glob('term-images-*.json')):
 for key,im in json.loads(p.read_text()).get('terms',{}).items():
  if key in terms:terms[key]['image']=im
if terms.get('piston',{}).get('image'):
 terms['piston']['image']=dict(terms['piston']['image'])
 terms['piston']['image']['caption']='活塞—连杆—曲轴机构示意；图中的 P 表示活塞。'
 terms['piston']['image']['caption_en']='Piston, connecting-rod and crank mechanism; P marks the piston.'
for key,im in images.get('entries',{}).items():
 if key in catalog:catalog[key]['preview_image']=im
save('catalog.json',sorted(catalog.values(),key=lambda e:e['id']))
save('content.json',content);save('intro-current.json',intro);save('english.json',english);save('mentions-current.json',mentions);save('terms.json',list(terms.values()))
if (ROOT/'work/f1-timeline.json').exists():
 timeline=load('work/f1-timeline.json');save('f1-eras.json',timeline if isinstance(timeline,list) else timeline.get('eras',timeline.get('timeline',[])))
print(f'Merged {len(catalog)} stable entries, {len(terms)} terms.')
