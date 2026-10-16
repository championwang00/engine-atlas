#!/usr/bin/env python3
"""Build the standalone Engine Atlas. Stable IDs live in catalog.json."""
from pathlib import Path
from urllib.parse import quote
import json, html, re, os, posixpath

ROOT = Path(__file__).resolve().parent
ERAS = [('e0','1769–1860','蒸汽与雏形','Steam and origins',0,1860),('e1','1861–1900','内燃机诞生','Birth of combustion',1861,1900),('e2','1901–1945','量产与多缸化','Production and cylinders',1901,1945),('e3','1946–1970','增压与大排量','Boost and displacement',1946,1970),('e4','1971–1990','排放与电喷','Emissions and electronics',1971,1990),('e5','1991–2010','精确控制','Precision control',1991,2010),('e6','2011–2020','小型化与混动','Downsizing and hybrids',2011,2020),('e7','2021–今','燃料与效率','Fuels and efficiency',2021,2100)]
TYPES = [('ext','外燃机','External combustion'),('proto','雏形与循环','Origins and cycles'),('layout','气缸布局','Cylinder layouts'),('unconv','非常规机型','Unconventional'),('boost','增压','Forced induction'),('valve','配气机构','Valvetrain'),('control','供油·点火·电控','Fuel, spark and control'),('combustion','燃烧·排放·冷却','Combustion and emissions'),('diesel','柴油机','Diesel'),('fuel','替代燃料','Alternative fuels'),('hybrid','混动配套','Hybrid combustion'),('model','著名机型','Engine families')]
TL = {t:(zh,en) for t,zh,en in TYPES}
def read(name, default=None):
    p=ROOT/name
    return json.loads(p.read_text()) if p.exists() else ({} if default is None else default)
def write(path, text):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
def esc(s): return html.escape(str(s),quote=True)
def js(data): return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
E = read('catalog.json',[])
BY = {e['id']:e for e in E}
ORDER = sorted(E,key=lambda e:(e['year'],e['id']))
CONTENT = read('content.json')
INTRO={}; MENT={}
for p in sorted(ROOT.glob('intro-*.json')): INTRO.update(json.loads(p.read_text()))
for p in sorted(ROOT.glob('mentions-*.json')): MENT.update(json.loads(p.read_text()))
ENGLISH=read('english.json'); TERMS=read('terms.json',[]); TBY={t['id']:t for t in TERMS}
CARS=read('cars.json'); CARS2=read('cars2.json'); F1=read('f1-eras.json',[])
PREVIEWS=read('previews.json')
USED_CARDS={}
CARD_CONTEXT={}
SITE=os.environ.get('ATLAS_SITE_URL','').rstrip('/')
GENERATED=[]

def era(e): return next(x for x in ERAS if x[4]<=e['year']<=x[5])
def name(e,lang): return e['en'] if lang=='en' else e['cn']
def year_label(e,lang): return e.get('shown_year_en',str(e['year'])) if lang=='en' else e['shown_year']
def tx(zh,en,lang): return en if lang=='en' else zh
def type_name(t,lang): return TL.get(t,('F1 规则','F1 regulations'))[lang=='en']
def rel(current,target): return posixpath.relpath(target,posixpath.dirname(current) or '.')
def entry_path(pid,lang): return f'{lang}/e/{pid.lower()}.html'
def content_for(e,lang):
    d=dict(CONTENT.get(e['id'],{})); i=INTRO.get(e['id'],{})
    d['intro']=i.get('intro',''); d['verify']='pending' if d.get('verify')=='pending' or i.get('verify')=='pending' else 'ok'
    d['sources']=list(d.get('sources',[]))
    for s in i.get('sources',[]):
        if s['url'] not in [x['url'] for x in d['sources']]:d['sources'].append(s)
    if lang=='en':d.update(ENGLISH.get(e['id'],{}))
    return d

def term_entry(t):
    value=t.get('entry')
    return f'EA-{value:03d}' if isinstance(value,int) else value

def terms_payload(lang):
    return {t['id']:{'name':tx(t['name'],t['en'],lang),'en':t['en'],'def':t.get('def_en',t['def']) if lang=='en' else t['def'],'image':t.get('image',{}),'related':[r for r in t.get('related',[]) if r in TBY]} for t in TERMS}

def car_cards(pid):
    m=MENT.get(pid,{})
    if isinstance(m,list):m={'examples':m,'intro':m}
    cards={};aliases=[]
    images=[c for c in CARS2.get(pid,[])+CARS.get(pid,[]) if c.get('image')]
    for ix,c in enumerate(m.get('examples',[])+m.get('intro',[])):
        key=f'{pid}-{ix}';im=c.get('image')
        if not im:
            im=next((v['image'] for v in images if v.get('match') and (v['match'] in c['match'] or c['match'] in v['match'])),None)
        cards[key]={'name':c.get('name',c['match']),'year':str(c.get('year') or ''),'brief':c.get('brief',''),'brief_en':c.get('brief_en',''),'image':im or {}}
        for a in {c['match'],re.sub(r'[（(].*$','',c['match']).strip(),c.get('name','').split(' · ')[0]}:
            if len(a)>=2:aliases.append((a,key))
    return cards,aliases

ALIASES=sorted([(a,t['id']) for t in TERMS for a in t.get('aliases',[])],key=lambda x:-len(x[0]))
def link_text(text,current,lang,self_id=None,car_aliases=()):
    text=str(text);taken=[];used=set()
    if PREVIEWS:car_aliases=[(a,k) for k,v in PREVIEWS.items() for a in v.get('aliases',[])]
    candidates=[(a,('car',c)) for a,c in car_aliases]+[(a,('term',tid)) for a,tid in ALIASES]+[(a,('entry',e['id'])) for e in E if e['id']!=self_id for a in (e['cn'],e['en'],*e.get('aliases',[])) if len(a)>=2]
    if lang=='en':candidates += [(t['en'],('term',t['id'])) for t in TERMS if len(t['en'])>3]
    text_fold=text.casefold()
    ascii_word=lambda c:c.isascii() and (c.isalnum() or c=='_')
    for a,key in sorted(candidates,key=lambda x:(-len(x[0]),{'term':0,'entry':1,'car':2}[x[1][0]])):
        if a.casefold() not in text_fold:continue
        for m in re.finditer(re.escape(a),text,re.I if a.isascii() else 0):
            s,e=m.span()
            if a.isascii() and ((s>0 and ascii_word(text[s-1])) or (e<len(text) and ascii_word(text[e]))):continue
            if any(not(e<=x or s>=y) for x,y,_ in taken):continue
            taken.append((s,e,key));used.add(key)
    out=[];pos=0
    for s,e,key in sorted(taken):
        out.append(esc(text[pos:s]));label=esc(text[s:e]);kind,k=key
        if kind=='entry':out.append(f'<a class="term" data-entry="{k}" href="{rel(current,entry_path(k,lang))}">{label}</a>')
        elif kind=='car':
            USED_CARDS.setdefault(current,set()).add(k)
            # The sentence currently being read is a grounded fallback for a globally reused entity.
            sentences=re.split(r'(?<=[。！？；])|(?<=[.!?])\s+(?=[A-Z])',text)
            context=next((v.strip() for v in sentences if text[s:e] in v),text).strip()
            if context:CARD_CONTEXT.setdefault(current,{}).setdefault(k,{})['brief_en' if lang=='en' else 'brief']=context
            out.append(f'<button class="car" type="button" data-car="{k}" aria-expanded="false">{label}</button>')
        else:
            t=TBY[k];pid=term_entry(t);target=entry_path(pid,lang) if pid and pid in BY and pid!=self_id else f'{lang}/glossary.html#{k}'
            out.append(f'<a class="term" data-term="{k}" href="{rel(current,target)}">{label}</a>')
        pos=e
    out.append(esc(text[pos:]));return ''.join(out)

LOGO='<span class="mk" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span>engines</span>'
def header(current,lang,index=False,active=''):
    home=rel(current,f'{lang}/index.html');other='en' if lang=='zh' else 'zh';suffix=current.split('/',1)[1] if current.startswith(('en/','zh/')) else current
    if suffix.startswith('e/') or suffix in ['index.html','glossary.html','f1.html','about.html']:other_path=f'{other}/{suffix}'
    else:other_path=f'{other}/index.html'
    types=(f'<button data-type="all" aria-pressed="true">{tx("全部","All",lang)}</button>' if index else f'<a href="{home}">{tx("全部","All",lang)}</a>')
    for t,zh,en in TYPES:
        label=esc(tx(zh,en,lang))
        types+=f'<button data-type="{t}" aria-pressed="false">{label}</button>' if index else f'<a href="{home}?type={t}"'+(' aria-current="true"' if t==active else '')+f'>{label}</a>'
    zoom=(f'<div class="zoom" role="group" aria-label="{tx("视图缩放","View scale",lang)}"><div class="zoom-row"><button data-zoom="out" aria-label="{tx("缩小","Zoom out",lang)}">−</button><button data-zoom="reset" class="pct" title="{tx("恢复100%","Reset to 100%",lang)}">100%</button><button data-zoom="in" aria-label="{tx("放大","Zoom in",lang)}">+</button></div><div class="zoom-slide"><input type="range" min="0" max="11" step="1" value="4" data-zoom="range" aria-label="{tx("缩放比例","Scale",lang)}"></div></div>') if index else ''
    return f'''<a class="skip" href="#main">{tx('跳至内容','Skip to content',lang)}</a><header class="bar"><a class="logo" href="{home}" aria-label="Engine Atlas">{LOGO}</a><div class="types-wrap"><nav class="types" aria-label="{tx('类型','Types',lang)}">{types}</nav><button class="types-more" aria-label="{tx('滚动查看更多类型','Scroll to more categories',lang)}" hidden>›</button></div><div class="tools"><button class="search-toggle" aria-expanded="false" aria-controls="search-panel">{tx('搜索','Search',lang)}</button><a href="{rel(current,f'{lang}/glossary.html')}">{tx('术语','Terms',lang)}</a><a href="{rel(current,f'{lang}/f1.html')}">F1</a><a href="{rel(current,other_path)}" lang="{other}" hreflang="{other}">{tx('EN','中文',lang)}</a></div>{zoom}<form class="search-panel" id="search-panel" role="search" action="{home}" hidden><label for="search">{tx('搜索图谱','Search the atlas',lang)}</label><input id="search" name="q" type="search" placeholder="{tx('名称、原理、车型或 EA 编号','Name, principle, vehicle or EA ID',lang)}" autocomplete="off"><button type="submit">{tx('查找','Find',lang)}</button><button type="button" class="search-close" aria-label="{tx('关闭搜索','Close search',lang)}">×</button></form></header>'''

def rail(current,lang,selected='',index=False):
    rows=[]
    for k,label,zh,en,*_ in ERAS:
        label=label.replace('今','present') if lang=='en' else label
        href='#'+k if index else rel(current,f'{lang}/index.html')+'#'+k
        rows.append(f'<li><a href="{href}" data-era="{k}"'+(' aria-current="true"' if selected==k else '')+f'><span>{label}</span><em>{tx(zh,en,lang)}</em></a></li>')
    return f'<aside class="rail"><nav aria-label="{tx("年代","Eras",lang)}"><ol>{"".join(rows)}</ol></nav></aside>'

def head(current,lang,title,description='',canonical=None):
    canonical=canonical or current
    suffix=canonical.split('/',1)[1] if canonical.startswith(('zh/','en/')) else canonical
    def alternate(locale):
        target=f'{locale}/{suffix}'
        return SITE+'/'+target if SITE else rel(current,target)
    canonical_url=SITE+'/'+canonical if SITE else rel(current,canonical)
    return f'''<!doctype html><html lang="{'zh-CN' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Engine Atlas</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{canonical_url}"><link rel="alternate" hreflang="zh-CN" href="{alternate('zh')}"><link rel="alternate" hreflang="en" href="{alternate('en')}"><link rel="alternate" hreflang="x-default" href="{alternate('zh')}"><link rel="stylesheet" href="{rel(current,'assets/atlas.css')}?v=figs-4"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet"><script>try{{const z=+localStorage.getItem('ea-zoom-pct');if(z>=50&&z<=300)document.documentElement.style.setProperty('--z',z/100)}}catch(e){{}}</script><script src="{rel(current,'assets/atlas.js')}?v=figs-4" defer blocking="render"></script></head><body data-lang="{lang}" data-page="{esc(suffix)}">'''

def entry_image(e,current):
    if e.get('figure'):return {'src':rel(current,'assets/figures/'+e['figure']+'.svg')+'?v=figs-4','caption':'教学几何模型，非特定机型复原。','caption_en':'Teaching geometry, not a specific engine reconstruction.'}
    if e.get('preview_image'):return e['preview_image']
    names={e['cn'].casefold(),e['en'].casefold(),*[x.casefold() for x in e.get('aliases',[])]}
    for entity in PREVIEWS.values():
        if entity.get('image') and any(a.casefold() in names for a in entity.get('aliases',[])):return entity['image']
    return {}

def finish(current,lang,body,payload=None):
    payload=payload or {}
    if PREVIEWS:payload['cars']={k:{**PREVIEWS[k],'href':rel(current,entry_path(PREVIEWS[k]['entries'][0],lang))} for k in USED_CARDS.get(current,set()) if k in PREVIEWS}
    for key,over in CARD_CONTEXT.get(current,{}).items():
        if key not in payload.get('cars',{}):continue
        car=payload['cars'][key]
        for field,value in over.items():
            if not car.get(field) or '技术背景见' in car[field] or 'is a referenced example of' in car[field]:car[field]=value
    payload.setdefault('terms',terms_payload(lang))
    for tid,t in payload['terms'].items():t['href']=rel(current,f'{lang}/glossary.html#{tid}')
    payload['entries']={e['id']:{'name':name(e,lang),'en':e['en'],'year':e['shown_year'],'brief':content_for(e,lang).get('description') or e['description'],'href':rel(current,entry_path(e['id'],lang)),'image':entry_image(e,current)} for e in E}
    if lang=='en':
        for c in payload.get('cars',{}).values():
            if not c.get('brief_en'):c['brief_en']='An automotive example discussed in this entry.'
    foot=f'<footer class="footer"><a href="{rel(current,f"{lang}/about.html")}">{tx("关于","About",lang)}</a><span>Engine Atlas · 2026</span></footer>'
    if payload:body+=f'<script id="page-data" type="application/json">{js(payload)}</script>'
    write(current,body+foot+'</body></html>');GENERATED.append(current)

def source_html(srcs):return '<br>'.join(f'<a class="src" href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a>' for s in srcs)
def figure(e,current,lang,detail=False):
    fig=e.get('figure');label=tx('发动机示意图','Engine illustration',lang)
    if not fig:return f'<div class="tile" data-embed="" aria-hidden="true"></div>'
    poster=rel(current,f'assets/figures/{fig}.svg')+'?v=figs-4'
    if not detail:return f'<div class="tile" data-embed="{fig}"><img src="{poster}" alt="{esc(name(e,lang))}" width="720" height="440" loading="lazy"></div>'
    src=rel(current,f'assets/figures/{fig}.html')+f'?embed=1&handoff=1&lang={lang}&v=figs-4'
    return f'<div class="tile" data-embed="{fig}"><div class="figure-viewport"><img class="figure-poster" src="{poster}" alt="{esc(name(e,lang))}" width="720" height="440" loading="eager"><iframe src="{src}" title="{esc(name(e,lang))} · {label}" loading="eager"></iframe></div></div>'

def detail(e,current,lang):
    c=content_for(e,lang);er=era(e);pid=e['id'];home=rel(current,f'{lang}/index.html');title=name(e,lang);cards,aliases=car_cards(pid)
    desc=c.get('description') or e['description'];paragraphs=[p.strip() for p in c.get('intro','').split('\n\n') if p.strip()]
    lead=''.join(f'<p>{link_text(p,current,lang,pid,aliases)}</p>' for p in paragraphs) or f'<p>{link_text(desc,current,lang,pid,aliases)}</p>'
    pending=f'<span class="pend">{tx("待核实","Verification pending",lang)}</span>' if c.get('verify')=='pending' else ''
    relation=''
    if e.get('parent') in BY:
        pe=BY[e['parent']];relation=f'<a href="{rel(current,entry_path(pe["id"],lang))}">{esc(name(pe,lang))}</a>'
    elif e.get('parent_term') in TBY:
        pt=TBY[e['parent_term']];relation=f'<a href="{rel(current,f"{lang}/glossary.html")}#{pt["id"]}">{esc(tx(pt["name"],pt["en"],lang))}</a>'
    facts=[(tx('代表年份','Milestone',lang),link_text(year_label(e,lang),current,lang,pid,aliases)),(tx('类别','Category',lang),esc(type_name(e['type'],lang)))]
    if relation:facts.append((tx('所属概念','Parent concept',lang),relation))
    for key,zh,en in [('principle','原理','Principle'),('examples','代表应用','Examples'),('tradeoffs','优点与代价','Trade-offs'),('status','应用现状','Applications')]:
        if c.get(key):facts.append((tx(zh,en,lang),link_text(c[key],current,lang,pid,aliases)))
    children=[x for x in E if x.get('parent')==pid]
    if children:facts.append((tx('下位变体','Variants',lang),' · '.join(f'<a href="{rel(current,entry_path(x["id"],lang))}">{esc(name(x,lang))}</a>' for x in children)))
    if e['kind']=='era':facts.append((tx('规则年表','Regulation timeline',lang),f'<a href="{rel(current,f"{lang}/f1.html")}">{tx("查看完整 F1 年表","View the full F1 timeline",lang)}</a>'))
    if c.get('sources'):facts.append((tx('来源','Sources',lang),source_html(c['sources'])))
    fx=''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label,value in facts)
    ordered=[x for x in ORDER if x['kind']!='era'];idx=next((i for i,x in enumerate(ordered) if x['id']==pid),None)
    pn=[]
    for offset,zh,en in [(-1,'上一条','Previous'),(1,'下一条','Next')]:
        if idx is not None and 0<=idx+offset<len(ordered):
            x=ordered[idx+offset];pn.append(f'<a href="{rel(current,entry_path(x["id"],lang))}"><small>{tx(zh,en,lang)}</small>{esc(name(x,lang))}</a>')
        else:pn.append('<span></span>')
    sub_en=(f'<p class="en">{esc(e["en"])}</p>' if lang=='zh' and e['en'].strip().lower()!=title.strip().lower() else '')
    body=head(current,lang,title,desc,f'{lang}/e/{pid.lower()}.html')+header(current,lang,active=e['type'])
    body+=f'<div class="app">{rail(current,lang,er[0])}<main class="main" id="main"><nav class="crumb" aria-label="{tx("面包屑","Breadcrumb",lang)}"><a class="bk" data-back href="{home}#{er[0]}">← {tx("返回","Back",lang)}</a><ol><li><a href="{home}">{tx("图谱","Atlas",lang)}</a></li><li><a href="{home}?type={e["type"]}">{esc(type_name(e["type"],lang))}</a></li><li aria-current="page">{esc(title)}</li></ol></nav><article class="detail"><div class="side"><span class="code">{pid}</span><h1>{esc(title)}</h1>{sub_en}<div class="lead long">{lead}{pending}</div></div><figure class="fig">{figure(e,current,lang,True)}</figure><dl class="facts">{fx}</dl><nav class="pn" aria-label="{tx("相邻条目","Adjacent entries",lang)}">{"".join(pn)}</nav></article></main></div>'
    finish(current,lang,body,{'terms':terms_payload(lang),'cars':cards})

def index(current,lang):
    groups=[];search={};shown=[e for e in ORDER if e['kind']!='era']
    for k,label,zh,en,*_ in ERAS:
        items=[]
        for e in shown:
            if era(e)[0]!=k:continue
            if e.get('kind')=='variant' and e.get('parent') in BY:continue
            c=content_for(e,lang);pid=e['id'];desc=c.get('description') or e['description'];variant=e['kind']=='variant'
            parent=BY.get(e.get('parent'));term=TBY.get(e.get('parent_term'))
            parent_name=name(parent,lang) if parent else tx(term['name'],term['en'],lang) if term else ''
            hierarchy=f'<span class="hierarchy">↳ {tx("变体","Variant",lang)} · {esc(parent_name)}</span>' if variant else ''
            href=rel(current,entry_path(pid,lang))
            items.append(f'<article class="item{" variant" if variant else ""}" data-id="{pid}" data-type="{e["type"]}" data-era="{k}"><div class="hd"><h3><a data-open-entry href="{href}">{esc(name(e,lang))}</a></h3><span class="code">{pid[3:]}</span></div><dl class="spec"><div><dt>{tx("年份","Year",lang)}</dt><dd>{link_text(year_label(e,lang),current,lang,pid)}</dd></div><div><dt>{tx("类别","Type",lang)}</dt><dd>{esc(type_name(e["type"],lang))}</dd></div></dl><a class="figure-link" href="{href}" tabindex="-1" aria-hidden="true">{figure(e,current,lang)}</a>{hierarchy}<p>{link_text(desc,current,lang,pid)}</p></article>')
            children=[x for x in ORDER if x.get('parent')==pid and x.get('kind')=='variant'];kid_text=[]
            if children:
                variants=[]
                for child in children:
                    cd=content_for(child,lang);cid=child['id']
                    variants.append(f'<a class="item variant-link" href="{rel(current,entry_path(cid,lang))}" data-id="{cid}" data-type="{child["type"]}" data-era="{k}"><span class="tile" aria-hidden="true"></span><span><span class="code">{esc(year_label(child,lang))}</span><strong>{esc(name(child,lang))}</strong></span><span aria-hidden="true">↗</span></a>')
                    kid_text.append(' '.join([cid,child['cn'],child['en'],child['shown_year']]+[str(cd.get(f,'')) for f in ['description','principle','examples','intro']]))
                # variants live on the parent's detail page only; the list stays one card per entry
            search[pid]=' '.join([pid,e['cn'],e['en'],str(e['year']),e['shown_year'],str(e.get('description',''))]+[str(c.get(f,'')) for f in ['description','principle','examples','intro']]+kid_text)
        label=label.replace('今','present') if lang=='en' else label
        groups.append(f'<section class="group" id="{k}" data-era="{k}"><header><h2>{label}</h2><span class="code">{sum(1 for e in shown if era(e)[0]==k)}</span></header><div class="items">{"".join(items)}</div></section>')
    body=head(current,lang,tx('发动机图谱','Engine Atlas',lang),tx('按年代、技术与车型探索汽车发动机。','Explore automotive engines by era, technology and vehicle.',lang),f'{lang}/index.html')+header(current,lang,True)
    body+=f'<div class="app">{rail(current,lang,index=True)}<main class="main" id="main"><h1 class="sr-only">{tx("发动机图谱","Engine Atlas",lang)}</h1><div class="result-meta" hidden><span id="result-count" role="status" aria-live="polite"></span><button id="clear-filters">{tx("重置筛选","Clear filters",lang)}</button></div>{"".join(groups)}<p class="empty" id="empty" hidden>{tx("没有符合条件的条目。试试其他名称或清除筛选。","No matching entries. Try another name or clear the filters.",lang)}</p></main></div>'
    finish(current,lang,body,{'search':search,'total':len(shown),'terms':terms_payload(lang)})

def glossary(current,lang):
    cards=[]
    for t in TERMS:
        links=' · '.join(f'<a href="#{r}">{esc(tx(TBY[r]["name"],TBY[r]["en"],lang))}</a>' for r in t.get('related',[]) if r in TBY)
        pid=term_entry(t);goto=f'<a class="go" href="{rel(current,entry_path(pid,lang))}">→ {tx("查看条目","Explore entry",lang)}</a>' if pid in BY else ''
        variants=[e for e in E if e.get('parent_term')==t['id']]
        goto+=''.join(f'<a class="go" href="{rel(current,entry_path(e["id"],lang))}">↳ {esc(name(e,lang))}</a>' for e in variants)
        references=('<details class="term-sources"><summary>'+tx('来源','Sources',lang)+'</summary>'+source_html(t['sources'])+'</details>') if t.get('sources') else ''
        cards.append(f'<article class="tcard" id="{esc(t["id"])}"><span class="code">{esc(t["en"])}</span><h2>{esc(tx(t["name"],t["en"],lang))}</h2><p>{link_text(t.get("def_en",t["def"]) if lang=="en" else t["def"],current,lang,term_entry(t))}</p><div class="rel">{links}</div>{goto}{references}</article>')
    title=tx('术语表','Glossary',lang);body=head(current,lang,title,canonical=f'{lang}/glossary.html')+header(current,lang)
    body+=f'<main class="gloss" id="main"><nav class="crumb flat"><a class="bk" href="{rel(current,f"{lang}/index.html")}">← {tx("图谱","Atlas",lang)}</a><h1>{title} <span class="code">{len(TERMS)}</span></h1></nav><div class="tgrid">{"".join(cards)}</div></main>'
    finish(current,lang,body)

def f1(current,lang):
    blocks=[]
    for row in F1:
        links=' · '.join(f'<a href="{rel(current,entry_path(pid,lang))}">{esc(name(BY[pid],lang))}</a>' for pid in row.get('entries',[]) if pid in BY)
        blocks.append(f'<article class="timeline-row" id="f1-{row.get("id",str(row["year"])[:4])}"><span class="code">{esc(row["year"])}</span><div><h2>{esc(row.get("en_title",row["title"]) if lang=="en" else row["title"])}</h2><p>{link_text(row.get("en_summary",row["summary"]) if lang=="en" else row["summary"],current,lang)}</p><p class="related">{links}</p><div class="timeline-sources">{source_html(row.get("sources",[]))}</div></div></article>')
    title=tx('F1 发动机规则年表','F1 engine regulations',lang);body=head(current,lang,title,canonical=f'{lang}/f1.html')+header(current,lang)
    body+=f'<main class="document" id="main"><nav class="crumb flat"><a class="bk" href="{rel(current,f"{lang}/index.html")}">← {tx("图谱","Atlas",lang)}</a><span>F1</span></nav><header class="document-title"><h1>{title}</h1><p>{tx("规则时代独立于技术条目。年份表示规则适用期；同一时期可能存在例外和过渡许可。","Regulation eras are separate from technology entries. Dates show rule periods; exceptions and transitional allowances may apply.",lang)}</p></header>{"".join(blocks)}</main>'
    finish(current,lang,body)

def about(current,lang):
    title=tx('关于图谱','About the atlas',lang)
    paragraphs=[tx('发动机图谱记录汽车中的外燃机、内燃机及相关燃料、控制与排放技术。混动只收录内燃机和直接配套技术，不收录纯电驱动。','Engine Atlas covers automotive external- and internal-combustion engines, fuels, controls and emissions technology. Hybrid entries focus on combustion and directly related systems; pure electric drives are outside its scope.',lang),tx('年份是条目所选的代表性里程碑，可能是专利、首次试验、亮相或量产节点；详情页注明口径。它不是对所有技术“全球首次”的统一断言。编号长期固定，不随年代排序变化。','Each date is a representative milestone: a patent, experiment, unveiling or production event. The detail page states its basis. Dates are not blanket claims of a worldwide first. Entry IDs remain stable when chronology changes.',lang),tx('概念、厂商变体与代表机型分层记录；F1 规则独立列成年表。每条详情保留可查来源，尚不能证实的内容标为“待核实”。本轮新增与改写文案仍待人工审阅。','Concepts, manufacturer variants and engine families are identified separately, with F1 rules in their own timeline. Sources are listed on each detail page. Unresolved material is marked “Verification pending”. Newly written and revised copy awaits human editorial review.',lang),tx('三张 V 型发动机图是简化的教学几何模型，不复原某一量产机或 F1 机型。尺寸、曲轴和点火安排用于演示运动关系。未绘制的条目保留灰色图位。','The three V-engine figures are simplified teaching models, not reconstructions of a production or F1 engine. Dimensions, crank geometry and firing sequences illustrate mechanical relationships. Other entries retain empty grey figure plates.',lang),tx('字体使用 IBM Plex Mono 与 Noto Sans SC。预览中的车型、发动机照片与技术示意图使用 Wikimedia Commons 的自由许可素材，各图单独显示作者、许可与原始页面链接。图片和网络字体由外部服务加载。','Typography uses IBM Plex Mono and Noto Sans SC. Vehicle and engine photographs and technical diagrams in previews use freely licensed Wikimedia Commons material, with individual author, licence and source links. Images and web fonts load from external services.',lang)]
    body=head(current,lang,title,canonical=f'{lang}/about.html')+header(current,lang)+f'<main class="document" id="main"><nav class="crumb flat"><a class="bk" href="{rel(current,f"{lang}/index.html")}">← {tx("图谱","Atlas",lang)}</a><span>{title}</span></nav><div class="document-title"><h1>{title}</h1>'+''.join(f'<p>{p}</p>' for p in paragraphs)+'</div></main>'
    finish(current,lang,body)

for lang in ('zh','en'):
    index(f'{lang}/index.html',lang);glossary(f'{lang}/glossary.html',lang);f1(f'{lang}/f1.html',lang);about(f'{lang}/about.html',lang)
    for e in E:detail(e,entry_path(e['id'],lang),lang)
# Root compatibility pages preserve old bookmarks, while canonical URLs use explicit locales.
index('index.html','zh');glossary('glossary.html','zh');f1('f1.html','zh');about('about.html','zh')
for e in E:detail(e,f'e/{e["id"].lower()}.html','zh')
write('entries.json',json.dumps([{'id':e['id'],'n':int(e['id'][3:]),'year':e['shown_year'],'type':e['type'],'name':e['cn'],'en':e['en'],'desc':e['description'],'kind':e['kind']} for e in E],ensure_ascii=False,indent=2)+'\n')
write('build-manifest.json',json.dumps({'pages':GENERATED,'entry_count':len(E),'catalog_count':sum(e['kind']!='era' for e in E),'categories':len(TYPES),'eras':len(ERAS),'terms':len(TERMS),'f1_eras':len(F1)},ensure_ascii=False,indent=2)+'\n')
active=set().union(*USED_CARDS.values()) if USED_CARDS else set()
usage={'active_entities':len(active),'with_images':sum(bool(PREVIEWS[k].get('image')) for k in active),'without_images':[{'id':k,'name':PREVIEWS[k]['name'],'pages':[page for page,ids in USED_CARDS.items() if k in ids and page.startswith('zh/')]} for k in sorted(active) if not PREVIEWS[k].get('image')],'contexts':CARD_CONTEXT,'inactive_library_entities':len(PREVIEWS)-len(active)}
write('work/preview-usage.json',json.dumps(usage,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(GENERATED)} pages; {len(E)} stable entries; {len(TERMS)} terms; {len(F1)} F1 eras.')
