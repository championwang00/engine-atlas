// Open every detail page that has a figure in the real atlas page; report console errors, empty frames, clipping.
import {chromium} from 'playwright';
import {readFile,writeFile} from 'node:fs/promises';
const cat=JSON.parse(await readFile('catalog.json','utf8'));
const ids=cat.filter(e=>e.figure).map(e=>[e.id,e.figure]);
const browser=await chromium.launch({headless:true,channel:'chrome'});
const out=[];
for(const [id,fig] of ids){
  const page=await browser.newPage({viewport:{width:1280,height:800},reducedMotion:'no-preference'});
  const errs=[];
  page.on('pageerror',e=>errs.push('pageerror: '+e.message.slice(0,120)));
  page.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,120))});
  page.on('requestfailed',r=>errs.push('reqfail: '+r.url().slice(-60)));
  try{
    await page.goto(`http://localhost:8766/zh/e/${id.toLowerCase()}.html`,{waitUntil:'load',timeout:15000});
    await page.waitForTimeout(1200);
    const fr=page.frames().find(f=>f.url().includes('/assets/figures/'));
    let info={frame:!!fr};
    if(fr){
      info.nodes=await fr.evaluate(()=>document.querySelector('#fig, .eng, svg')?.querySelectorAll('*').length||0).catch(()=>-1);
      info.hasFIG=await fr.evaluate(()=>!!(window.FIG||window.__engine)).catch(()=>false);
    }
    await page.screenshot({path:`work/qa-figures/${id}.png`,clip:{x:0,y:0,width:1280,height:800}});
    out.push({id,fig,errs,...info});
  }catch(e){out.push({id,fig,errs:['load: '+e.message.slice(0,100)]})}
  await page.close();
}
await browser.close();
await writeFile('work/qa-figures/report.json',JSON.stringify(out,null,1));
const bad=out.filter(o=>o.errs.length||!o.frame||!(o.nodes>10));
console.log('checked',out.length,'problems',bad.length);
for(const b of bad)console.log(b.id,b.fig,JSON.stringify({frame:b.frame,nodes:b.nodes,hasFIG:b.hasFIG}),b.errs.slice(0,2).join(' | '));
