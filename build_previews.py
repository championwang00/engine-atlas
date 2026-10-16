"""Reconcile entity aliases, verified entry context and licensed image metadata."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent
load=lambda p:json.loads((ROOT/p).read_text())
entries=load('catalog.json');by={x['id']:x for x in entries};content=load('content.json');english=load('english.json') if (ROOT/'english.json').exists() else {}
intro={};mentions={}
for p in sorted(ROOT.glob('intro-*.json')):intro.update(json.loads(p.read_text()))
for p in sorted(ROOT.glob('mentions-*.json')):mentions.update(json.loads(p.read_text()))
images=[]
for fn in ['cars2.json','cars.json']:
 for pid,ls in load(fn).items():
  for row in ls:
   if row.get('image'):images.append(row)

def core(value):
 value=re.sub(r'\s*·\s*(装车示例|配图示例).*$','',value).strip()
 value=re.sub(r'[（(].*$','',value).strip()
 value=re.sub(r'\s*[：:].*$','',value).strip()
 return value.rstrip('，,；; ')
def sentence(text,aliases,english=False):
 clauses=re.split(r'(?<=[。！？])|(?<=[.!?])\s+(?=[A-Z])',text)
 hits=[x.strip() for x in clauses if any(a.lower() in x.lower() for a in aliases if len(a)>2)]
 if not hits:return ''
 hit=min(hits,key=len)
 if len(hit)>(220 if english else 110):
  cuts=re.split(r'[；;]|\n',hit);hit=next((c for c in cuts if any(a.lower() in c.lower() for a in aliases if len(a)>2)),hit)
 return hit if len(hit)<(320 if english else 180) else ''

out={}
for pid,m in mentions.items():
 if pid not in by:continue
 if isinstance(m,list):m={'examples':m,'intro':m}
 for row in m.get('examples',[])+m.get('intro',[]):
  label=core(row.get('name','') or row['match']);match=core(row['match'])
  if not label or len(label)<2:continue
  # Exact model identity remains explicit; aliases never collapse down to only a brand.
  aliases=sorted({label,match,row['match'],*row.get('aliases',[])},key=lambda x:-len(x))
  if label.endswith(' 发动机'):aliases.append(label[:-4])
  aliases=[a for a in aliases if a not in {'Subaru','Toyota','Honda','Nissan','BMW','Audi','Porsche','Ferrari'}]
  key='entity-'+hashlib.sha1(label.lower().encode()).hexdigest()[:12]
  item=out.setdefault(key,{'name':label,'aliases':[],'year':str(row.get('year') or ''),'kind':row.get('kind','car'),'brief':'','brief_en':'','image':{},'entries':[]})
  item['aliases']=list(dict.fromkeys(item['aliases']+aliases));item['entries']=list(dict.fromkeys(item['entries']+[pid]))
  verified=' '.join([intro.get(pid,{}).get('intro','')]+[content.get(pid,{}).get(k,'') for k in ['principle','examples','tradeoffs','status']])
  translated=' '.join(english.get(pid,{}).get(k,'') for k in ['intro','examples','principle'])
  fresh=sentence(verified,aliases);fresh_en=sentence(translated,aliases,True)
  if row.get('brief_en'):
   fresh=row.get('brief') or fresh;fresh_en=row['brief_en']
  if fresh and (not item['brief'] or len(fresh)<len(item['brief'])):item['brief']=fresh
  if fresh_en and (not item['brief_en'] or len(fresh_en)<len(item['brief_en'])):item['brief_en']=fresh_en
  im=row.get('image') or next((r['image'] for r in images if core(r.get('name','') or r['match']).lower()==label.lower() or core(r['match']).lower()==match.lower()),None)
  if im and not item['image']:
   item['image']=im.copy();item['image']['kind']='车型示例（非发动机本体）' if row.get('kind')=='engine' else '车型参考图';item['image']['kind_en']='Vehicle example, not a photograph of the engine' if row.get('kind')=='engine' else 'Vehicle reference image'
  # Prefer the known concise description only when the model is still present in revised copy.
  if not item['brief'] and fresh:item['brief']=row.get('brief','')
for item in out.values():
 e=by[item['entries'][0]]
 if not item['brief']:item['brief']=f'{item["name"]}：本条目所列的代表应用，技术背景见“{e["cn"]}”。'
 if not item['brief_en']:item['brief_en']=f'{item["name"]} is a referenced example of {e["en"].lower()}. See the entry for its technical context.'
english_names={'Achates Power 对置活塞柴油机':'Achates Power opposed-piston diesel','Bugatti 8.0 L 四涡轮 W16':'Bugatti 8.0 L quad-turbo W16','Cugnot 蒸汽炮车':'Cugnot steam vehicle','DLR 自由活塞线性发电机':'DLR free-piston linear generator','De Dion-Bouton 单缸机':'De Dion-Bouton single-cylinder engine','Honda J 系列':'Honda J series','Mod II 斯特林机':'Mod II Stirling engine','NASA 汽车斯特林机 Mod I':'NASA automotive Stirling engine Mod I','Renault RS 系列 V10':'Renault RS series V10','Selden 专利车':'Selden patent vehicle','第一代 Toyota Prius':'First-generation Toyota Prius'}
for item in out.values():
 item['name_en']=english_names.get(item['name'],item['name'])
 if re.search(r'[\u4e00-\u9fff]',item['name_en']):
  item['name_en']={'Spyker 60 HP 赛车':'Spyker 60 HP racing car','Audi 100 五缸汽油版':'Audi 100 five-cylinder gasoline model','大众 6.0 L W12':'Volkswagen 6.0 L W12'}.get(item['name'],next((a for a in item['aliases'] if not re.search(r'[\u4e00-\u9fff]',a)),item['name']))
 year=re.search(r'\d{4}(?:[–—-]\d{4})?',item['year']);item['year_en']=year[0] if year else ''
# Later research can provide an audited image/description without touching aliases.
for p in sorted((ROOT/'work').glob('entity-images-extra*.json')):
 for key,im in json.loads(p.read_text()).get('entities',{}).items():
  if key in out:out[key]['image']=im
# Only identity-checked aliases are merged. Related variants (e.g. Sport quattro)
# remain separate from their base models.
canonical={'第一代Prius':'第一代 Toyota Prius','Toyota Prius NHW10':'第一代 Toyota Prius','LS1':'Chevrolet LS1','M256':'Mercedes-Benz M256','Mercedes M256':'Mercedes-Benz M256','13B-MSP RENESIS':'Mazda RENESIS','Honda B16A · Integra XSi':'Honda B16A','大众 6.0 L W12':'VW W12'}
for key,item in list(out.items()):
 target=canonical.get(item['name'])
 if item['name']=='Integra' and item['entries']==['EA-084']:target='Honda Integra XSi'
 if not target:continue
 dest='entity-'+hashlib.sha1(target.lower().encode()).hexdigest()[:12]
 if dest==key or dest not in out:continue
 old=out[dest];old['aliases']=list(dict.fromkeys(old['aliases']+[item['name']]+item['aliases']));old['entries']=list(dict.fromkeys(old['entries']+item['entries']))
 if not old['image'] and item['image']:old['image']=item['image']
 del out[key]
overrides=load('preview-overrides.json') if (ROOT/'preview-overrides.json').exists() else {}
for item in out.values():
 if item['name'] in overrides:item.update(overrides[item['name']])
(ROOT/'previews.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
report={'entities':len(out),'with_images':sum(bool(x['image']) for x in out.values()),'without_images':[{'name':x['name'],'entries':x['entries']} for x in out.values() if not x['image']],'context_only_descriptions':[x['name'] for x in out.values() if '技术背景见' in x['brief']]}
(ROOT/'work/preview-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if isinstance(v,int)},ensure_ascii=False))
