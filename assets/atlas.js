/* Engine Atlas: filtering, previews, navigation and accessible motion. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const lang = document.body.dataset.lang || 'zh';
  const text = (zh, en) => lang === 'en' ? en : zh;
  const data = JSON.parse($('#page-data')?.textContent || '{}');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  // A cached iframe may load before pagereveal. Keep the gate pending until
  // that event supplies its actual transition, including on a cold document.
  let enteringTransition;
  addEventListener('pagereveal', e => { enteringTransition=e.viewTransition; });
  const revealFinished = new Promise(resolve => {
    addEventListener('pagereveal', e => resolve(e.viewTransition?.finished), {once:true});
    if (!('onpagereveal' in window)) addEventListener('load', () => resolve(), {once:true});
  });
  const bar = $('.bar');
  new ResizeObserver(() => document.documentElement.style.setProperty('--bar-h', `${bar.getBoundingClientRect().height}px`)).observe(bar);
  const types=$('.types'), more=$('.types-more'), typeWrap=$('.types-wrap');
  const typeEdges=()=>{const next=types.scrollWidth-types.clientWidth-types.scrollLeft>3;more.hidden=!next;typeWrap.classList.toggle('can-next',next);typeWrap.classList.toggle('can-prev',types.scrollLeft>3);};
  types.addEventListener('scroll',typeEdges,{passive:true});new ResizeObserver(typeEdges).observe(types);
  more.addEventListener('click',()=>types.scrollBy({left:Math.max(140,types.clientWidth*.7),behavior:reduce.matches?'instant':'smooth'}));typeEdges();
  const searchPanel = $('.search-panel'), search = $('#search'), toggle = $('.search-toggle');
  const setSearch = open => {
    searchPanel.hidden = !open; toggle.setAttribute('aria-expanded', String(open));
    document.querySelector('.bar').classList.toggle('searching', open);
    if (!toggle.dataset.label) toggle.dataset.label = toggle.textContent;
    toggle.textContent = open ? '×' : toggle.dataset.label;
    toggle.setAttribute('aria-label', open ? ($('.search-close').getAttribute('aria-label') || 'Close') : toggle.dataset.label);
    if (open) search.focus();
  };
  toggle.addEventListener('click', () => setSearch(searchPanel.hidden));
  $('.search-close').addEventListener('click', () => { setSearch(false); toggle.focus(); });
  search.addEventListener('keydown', e => { if (e.key === 'Escape') { setSearch(false); toggle.focus(); } });
  const query = new URLSearchParams(location.search);
  search.value = query.get('q') || '';
  if (search.value) setSearch(true);

  const items = $$('.item'), groups = $$('.group'), rail = $$('.rail a[data-era]');
  const alignTitles=()=>groups.forEach(group=>{
    const cards=$$('.items > .item,.items > .catalog-block > .item',group).filter(c=>!c.hidden);
    cards.forEach(c=>$('.hd',c).style.minHeight='');
    const rows=new Map();cards.forEach(c=>{const key=Math.round(c.getBoundingClientRect().top),list=rows.get(key)||[];list.push($('.hd',c));rows.set(key,list);});
    rows.forEach(headers=>{if(headers.length<2)return;const h=Math.max(...headers.map(h=>h.offsetHeight));headers.forEach(el=>el.style.minHeight=`${h}px`);});
  });
  let titleFrame=0;const queueTitles=()=>{cancelAnimationFrame(titleFrame);titleFrame=requestAnimationFrame(alignTitles);};
  addEventListener('resize',queueTitles);document.fonts.ready.then(queueTitles);
  if (items.length) {
    const chips = $$('.types button[data-type]');
    let type = chips.some(b => b.dataset.type === query.get('type')) ? query.get('type') : 'all';
    const result = $('#result-count'), meta = $('.result-meta');
    const normalize = value => String(value).normalize('NFKC').toLocaleLowerCase().replace(/[-–—]/g, ' ').trim();
    const index = Object.fromEntries(Object.entries(data.search || {}).map(([k,v]) => [k, normalize(v)]));
    const spy = () => {
      const visible = groups.filter(g => !g.hidden);
      let current = visible[0]?.dataset.era;
      const threshold = bar.offsetHeight + (innerWidth <= 760 ? $('.rail').offsetHeight : 0) + 24;
      for (const g of visible) if (g.getBoundingClientRect().top <= threshold) current = g.dataset.era;
      rail.forEach(a => {
        if (a.dataset.era === current) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    };
    const apply = (updateURL = true) => {
      const words = normalize(search.value).split(/\s+/).filter(Boolean);
      let total = 0;
      for (const item of items) {
        const ok = (type === 'all' || item.dataset.type === type) && words.every(w => (index[item.dataset.id] || '').includes(w));
        item.hidden = !ok; if (ok) total++;
      }
      $$('.catalog-block').forEach(block=>{const children=$$('.item',block);block.hidden=children.every(x=>x.hidden);const variants=$('.variants',block);variants.hidden=$$('.variant-link',variants).every(x=>x.hidden);});
      groups.forEach(g => {
        const count = $$('.item:not([hidden])', g).length;
        g.hidden = count === 0; $('header .code', g).textContent = count;
        const a = rail.find(x => x.dataset.era === g.dataset.era);
        a.classList.toggle('off', !count); a.setAttribute('aria-disabled', String(!count)); a.tabIndex = count ? 0 : -1;
      });
      chips.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.type === type)));
      $('#empty').hidden = total !== 0;
      meta.hidden = type === 'all' && !words.length;
      result.textContent = text(`显示 ${total} / ${items.length}`, `${total} / ${items.length} entries`);
      if (updateURL) {
        const url = new URL(location.href);
        type === 'all' ? url.searchParams.delete('type') : url.searchParams.set('type', type);
        search.value.trim() ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
        history.replaceState(history.state, '', url);
      }
      spy();
      queueTitles();
    };
    chips.forEach(b => b.addEventListener('click', () => { type = b.dataset.type; apply(); }));
    search.addEventListener('input', () => apply());
    searchPanel.addEventListener('submit', e => { e.preventDefault(); apply(); $('#main').focus({preventScroll:true}); });
    $('#clear-filters').addEventListener('click', () => { type = 'all'; search.value = ''; apply(); });
    rail.forEach(a => a.addEventListener('click', e => {
      const group = document.getElementById(a.dataset.era); e.preventDefault();
      if (!group || group.hidden) return;
      group.scrollIntoView({block:'start', behavior:reduce.matches ? 'instant' : 'smooth'});
      history.replaceState(history.state, '', location.pathname + location.search + '#' + a.dataset.era);
    }));
    const scales = [50,67,80,90,100,110,125,150,175,200,250,300];
    let step = 4;
    try { const stored = scales.indexOf(+localStorage.getItem('ea-zoom-pct')); if (stored >= 0) step = stored; } catch (_) {}
    const zoom = value => {
      step = Math.max(0, Math.min(scales.length-1, value));
      const pct = scales[step]; document.documentElement.style.setProperty('--z', pct / 100);
      $('[data-zoom=reset]').textContent = `${pct}%`;
      const range = $('[data-zoom=range]'); if (range) { range.value = String(step); range.setAttribute('aria-valuetext', `${pct}%`); range.style.setProperty('--p', String(step / (scales.length - 1))); }
      $('[data-zoom=out]').disabled = step === 0; $('[data-zoom=in]').disabled = step === scales.length-1;
      try {localStorage.setItem('ea-zoom-pct', pct);} catch (_) {}
      requestAnimationFrame(spy);
      queueTitles();
    };
    $('[data-zoom=out]').addEventListener('click', () => zoom(step-1));
    $('[data-zoom=in]').addEventListener('click', () => zoom(step+1));
    $('[data-zoom=reset]').addEventListener('click', () => zoom(4));
    const rangeEl = $('[data-zoom=range]'); if (rangeEl) rangeEl.addEventListener('input', () => zoom(+rangeEl.value));
    addEventListener('keydown', e => {
      if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest('input,textarea,select,[contenteditable=true]')) return;
      if (e.key === '+' || e.key === '=') {e.preventDefault(); zoom(step+1);}
      else if (e.key === '-') {e.preventDefault(); zoom(step-1);}
      else if (e.key === '0') {e.preventDefault(); zoom(4);}
    });
    let accumulated = 0;
    addEventListener('wheel', e => {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault(); accumulated += e.deltaY;
      if (Math.abs(accumulated) >= 40) {zoom(step + (accumulated < 0 ? 1 : -1)); accumulated = 0;}
    }, {passive:false});
    addEventListener('scroll', spy, {passive:true});
    zoom(step); apply(false);
    // Browser history restores both URL-filtered content and its scroll position.
    const save = a => {
      try { sessionStorage.setItem('ea-return', JSON.stringify({url:location.href, y:scrollY, id:a.dataset.id})); } catch (_) {}
    };
    document.addEventListener('click', e => {
      const a = e.target.closest('.item');
      if(a && e.target.closest('.term,.car'))return;
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      const link=a.matches('a')?a:$('[data-open-entry]',a);
      const background=!e.target.closest('a,button');
      const navigate=()=>{if(background&&link)location.assign(link.href);};
      save(a); if (reduce.matches) {navigate();return;}
      $$('.item .tile,.item .tile img').forEach(t => t.style.viewTransitionName = '');
      const tile=$('.tile',a), poster=$('img',tile);
      tile.style.viewTransitionName=poster?'engine-plate':'engine';
      if(poster)poster.style.viewTransitionName='engine';
      navigate();
    });
    const returnEntry = () => {try{return JSON.parse(sessionStorage.getItem('ea-return') || 'null');}catch(_){return null;}};
    addEventListener('pagereveal', e => {
      if (!e.viewTransition || reduce.matches) return;
      const saved=returnEntry();const target=saved && items.find(x => x.dataset.id===saved.id && !x.hidden);
      if (target) {
        const tile=$('.tile',target),poster=$('img',tile);
        tile.style.viewTransitionName=poster?'engine-plate':'engine';
        if(poster)poster.style.viewTransitionName='engine';
      }
      // Restore layout and scroll before the inbound transition is captured.
      alignTitles();
      if(saved?.url===location.href)scrollTo({top:saved.y,behavior:'instant'});
      e.viewTransition.finished.finally(() => $$('[style*="view-transition-name"]').forEach(x=>x.style.viewTransitionName=''));
    });
    addEventListener('pageshow', e => {
      const nav=performance.getEntriesByType('navigation')[0];
      if (e.persisted || nav?.type==='back_forward') {
        const saved=returnEntry();
        if (saved?.url===location.href) {alignTitles();scrollTo({top:saved.y,behavior:'instant'});}
      }
      if (!e.persisted) return;
      // pageshow can precede pagereveal on a restored document. Do not remove
      // its shared target name until the inbound snapshot has finished.
      requestAnimationFrame(() => {
        const clear=()=>{ $$('[style*="view-transition-name"]').forEach(x=>x.style.viewTransitionName='');spy(); };
        if(enteringTransition)enteringTransition.finished.finally(clear);else clear();
      });
    });
  }
  $('#main')?.setAttribute('tabindex','-1');
  $$('[data-back]').forEach(a => a.addEventListener('click', e => {
    try {
      const from = new URL(document.referrer);
      if (from.origin === location.origin && history.length>1) {
        e.preventDefault(); history.back();
      }
    } catch (_) {}
  }));

  // Keep the cached poster until the frame has drawn phase zero and the
  // shared-element flight has finished. A ready-state check also covers a
  // cached iframe that loaded before this deferred script attached its listener.
  $$('.fig iframe').forEach(frame => {
    const tile=frame.closest('.tile');
    let handedOff=false;
    const handoff=async()=>{
      let engine;
      // V6/V8/V12 expose __engine; every other figure exposes the shared FIG {play,reset,playing} API.
      try {engine=frame.contentWindow.__engine||frame.contentWindow.FIG;} catch (_) {return;}
      if(!engine || handedOff)return;
      handedOff=true;
      await revealFinished;
      requestAnimationFrame(()=>{
        tile.classList.add('model-ready');
        engine.handoffComplete?.();
      });
    };
    frame.addEventListener('load',handoff);
    // Wait for pagereveal to supply its transition promise before checking.
    addEventListener('pagereveal',handoff,{once:true});
    if(document.readyState==='complete')handoff();
    else addEventListener('load',handoff,{once:true});
  });

  // One shared preview supports pointer, focus, touch and Escape.
  const tip = document.createElement('div');tip.id='atlas-preview';tip.className='tip';tip.hidden=true;document.body.append(tip);
  let active=null, timer=0, pinned=false, suppressFocus=false;
  const restoreFocus=el=>{suppressFocus=true;el?.focus();queueMicrotask(()=>suppressFocus=false);};
  $$('a[href]').forEach(a=>{if(a.matches('.item,.figure-link,[data-open-entry],[data-back],[hreflang]')||a.closest('.bar,.rail,.crumb,.footer'))return;const url=new URL(a.href);const tid=decodeURIComponent(url.hash.slice(1));if(url.origin===location.origin&&data.terms?.[tid])a.dataset.term=tid;const match=url.pathname.match(/\/e\/(ea-\d+)\.html$/i);if(url.origin===location.origin&&match&&data.entries?.[match[1].toUpperCase()])a.dataset.entry=match[1].toUpperCase();});
  const node=(tag, cls, value) => {const el=document.createElement(tag);if(cls)el.className=cls;if(value)el.textContent=value;return el;};
  const hide=() => {clearTimeout(timer);tip.hidden=true;pinned=false;if(active){active.removeAttribute('aria-describedby');active.setAttribute('aria-expanded','false');}active=null;};
  const place=() => {
    if(!active)return;
    const r=active.getBoundingClientRect(), w=tip.offsetWidth, h=tip.offsetHeight;
    tip.style.left=`${innerWidth<=760?(innerWidth-w)/2:Math.max(12,Math.min(r.left,innerWidth-w-12))}px`;
    tip.style.top=`${Math.max(12, r.bottom+8+h<=innerHeight-12?r.bottom+8:r.top-h-8)}px`;
    tip.style.maxHeight=`${innerHeight-24}px`;
  };
  const show=(el, pin=false, relatedId=null) => {
    clearTimeout(timer);const term=data.terms?.[relatedId||el.dataset.term], car=relatedId?null:data.cars?.[el.dataset.car], entry=relatedId?null:data.entries?.[el.dataset.entry];
    const item=term||car||entry;if(!item)return;const displayName=lang==='en'?(item.name_en||item.name):item.name;
    if(active && active!==el)hide();active=el;pinned=pin;tip.replaceChildren();
    tip.setAttribute('role','dialog');tip.setAttribute('aria-modal','false');tip.setAttribute('aria-label',displayName);
    const close=node('button','tip-close','×');close.type='button';close.setAttribute('aria-label',text('关闭预览','Close preview'));close.addEventListener('click',()=>{const old=active;hide();restoreFocus(old);});tip.append(close);
    const im=item.image || {};
    const src=im.thumb || im.src || item.thumb;
    if(src){const image=node('img');image.src=src;image.alt=displayName;image.loading='lazy';image.addEventListener('load',place);image.addEventListener('error',()=>{image.hidden=true;place();});tip.append(image);}
    if(item.en || item.year)tip.append(node('span','tip-en',item.en||(lang==='en'?item.year_en||item.year:item.year)));
    const title=node('b','tip-title',displayName);title.tabIndex=-1;title.setAttribute('role','heading');title.setAttribute('aria-level','3');tip.append(title);
    const description=term?.def || (lang==='en'?item.brief_en || item.brief:item.brief);
    if(description)tip.append(node('p','',description));
    const meta=node('div','tip-meta');
    if(src && (im.caption||im.caption_en))meta.append(node('span','tip-caption',lang==='en'?(im.caption_en||im.kind_en||'Illustrative reference'):im.caption));
    if(src && im.kind){const kinds={diagram:['示意图','Diagram'],engine:['发动机照片','Engine photograph'],car:['车型外观','Vehicle exterior'],photo:['参考照片','Reference photograph'],technology:['技术参考图','Technology reference']};meta.append(node('span','tip-credit',kinds[im.kind]?.[lang==='en'?1:0]||(lang==='en'?(im.kind_en||'Illustrative reference'):im.kind)));}
    if(im.page){const credit=node('span','tip-credit',`${im.author||''} · `);const link=node('a','',im.license||text('图片来源','Image source'));link.href=im.page;link.target='_blank';link.rel='noopener noreferrer';credit.append(link);meta.append(credit);}
    if(meta.children.length)tip.append(meta);
    if(term?.related?.length){const related=node('div','tip-rel');term.related.forEach((id,index)=>{const t=data.terms?.[id];if(!t)return;if(index)related.append(document.createTextNode(' · '));const a=node('a','',t.name);a.href=t.href;a.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();show(el,true,id);$('.tip-title',tip).focus({preventScroll:true});});related.append(a);});tip.append(related);}
    const href=relatedId?item.href:(el.href || item.href);
    if(href){const go=node('a','tip-go',text('→ 查看条目','→ Explore entry'));go.href=href;tip.append(go);}
    tip.hidden=false;el.setAttribute('aria-describedby',tip.id);el.setAttribute('aria-expanded','true');place();
  };
  $$('[data-term],[data-car],[data-entry]').forEach(el => {
    el.setAttribute('aria-haspopup','dialog');el.setAttribute('aria-expanded','false');
    el.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();show(el,true);$('button,a',tip)?.focus();}});
    el.addEventListener('mouseenter',()=>{if(matchMedia('(hover:hover)').matches)show(el);});
    el.addEventListener('mouseleave',()=>{if(!pinned)timer=setTimeout(hide,180);});
    el.addEventListener('focus',()=>{if(!suppressFocus)show(el,active===el&&pinned);});
    if(el.matches('a'))el.addEventListener('pointerup',e=>{if(e.pointerType==='touch'&&!(active===el&&pinned)){e.preventDefault();el.dataset.touchPreview='1';show(el,true);}});
    if(el.matches('a'))el.addEventListener('click',e=>{if(el.dataset.touchPreview){delete el.dataset.touchPreview;e.preventDefault();}});
    el.addEventListener('blur',()=>{timer=setTimeout(()=>{if(!tip.contains(document.activeElement)&&!pinned)hide();},100);});
    if(el.matches('button'))el.addEventListener('click',e=>{if(active===el&&pinned){hide();return;}show(el,true);if(e.detail===0)$('button',tip).focus();});
  });
  tip.addEventListener('mouseenter',()=>clearTimeout(timer));
  tip.addEventListener('mouseleave',()=>{if(!pinned)timer=setTimeout(hide,180);});
  tip.addEventListener('focusin',()=>clearTimeout(timer));
  tip.addEventListener('focusout',()=>{timer=setTimeout(()=>{if(!tip.contains(document.activeElement)&&document.activeElement!==active)hide();},100);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!tip.hidden){const old=active;hide();if(tip.contains(document.activeElement))restoreFocus(old);}});
  document.addEventListener('pointerdown',e=>{if(!tip.hidden&&!tip.contains(e.target)&&!active?.contains(e.target))hide();});
  addEventListener('scroll',()=>{if(!tip.hidden)hide();},{passive:true});
  addEventListener('resize',()=>{if(!tip.hidden)place();});
  const highlight=()=>{$$('.tcard.hit').forEach(x=>x.classList.remove('hit'));if(location.hash)document.getElementById(decodeURIComponent(location.hash.slice(1)))?.classList.add('hit');};
  addEventListener('hashchange',highlight);highlight();
})();
