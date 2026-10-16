// node poster.mjs <key> ... : export assets/figures/<key>.svg (static poster) from assets/figures/<key>.html (svg#fig)
import {chromium} from 'playwright';
import {writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
const root=dirname(fileURLToPath(import.meta.url));
const keys=process.argv.slice(2);
const browser=await chromium.launch({headless:true,channel:'chrome'});
try{
  for(const key of keys){
    const page=await browser.newPage({viewport:{width:720,height:440},reducedMotion:'reduce'});
    await page.goto('file://'+join(root,'assets/figures',key+'.html')+'?embed=1&still=1');
    await page.waitForSelector('#fig *');
    await page.waitForTimeout(400);
    const svg=await page.evaluate(()=>{
      const r=document.querySelector('#fig'),c=r.cloneNode(true),o=[r,...r.querySelectorAll('*')],k=[c,...c.querySelectorAll('*')];
      const attrs=['fill','stroke','stroke-width','stroke-linejoin','stroke-linecap','stroke-dasharray','opacity','fill-opacity','stroke-opacity','font-family','font-size','font-weight','letter-spacing','text-anchor','dominant-baseline'];
      const drop=[];
      for(let i=0;i<o.length;i++){const cs=getComputedStyle(o[i]);
        // elements hidden by the page's CSS would default to black fill in a standalone SVG: drop them
        if(i>0&&(cs.display==='none'||cs.visibility==='hidden'||cs.visibility==='collapse')){drop.push(k[i]);continue;}
        for(const a of attrs){const v=cs.getPropertyValue(a);if(v)k[i].setAttribute(a,v);}
        // inline styles that use the page's CSS variables would override these and turn black outside the page
        k[i].removeAttribute('style');}
      drop.forEach(n=>n.remove());
      c.setAttribute('xmlns','http://www.w3.org/2000/svg');c.setAttribute('width','720');c.setAttribute('height','440');
      if(!c.getAttribute('viewBox'))c.setAttribute('viewBox','0 0 720 440');c.setAttribute('role','img');c.removeAttribute('style');
      return new XMLSerializer().serializeToString(c);
    });
    await writeFile(join(root,'assets/figures',key+'.svg'),svg);
    console.log(key,'poster',svg.length);
    await page.close();
  }
}finally{await browser.close()}
