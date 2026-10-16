// Export the already-built Anatomy figures and their static skeleton posters.
import {chromium} from 'playwright';
import {mkdir,copyFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
const root=dirname(fileURLToPath(import.meta.url));
await mkdir(join(root,'assets/figures'),{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chrome'});
try {
  for(const key of ['v6','v8','v12']){
    const source=join(root,'../engines',key+'-light.html');
    await copyFile(source,join(root,'assets/figures',key+'.html'));
    const page=await browser.newPage({viewport:{width:720,height:440},reducedMotion:'reduce'});
    await page.goto('file://'+source+'?embed=1');
    await page.waitForFunction(()=>document.querySelector('.eng')?.children.length>10);
    const svg=await page.evaluate(()=>{
      const root=document.querySelector('.eng');
      const clone=root.cloneNode(true);const originals=[root,...root.querySelectorAll('*')],copies=[clone,...clone.querySelectorAll('*')];
      const attrs=['fill','stroke','stroke-width','stroke-linejoin','stroke-linecap','stroke-dasharray','opacity','fill-opacity','stroke-opacity'];
      for(let i=0;i<originals.length;i++)for(const attr of attrs){const v=getComputedStyle(originals[i]).getPropertyValue(attr);if(v)copies[i].setAttribute(attr,v);}
      clone.setAttribute('xmlns','http://www.w3.org/2000/svg');clone.setAttribute('width','720');clone.setAttribute('height','440');clone.setAttribute('viewBox','0 0 720 440');clone.setAttribute('role','img');
      return new XMLSerializer().serializeToString(clone);
    });
    await writeFile(join(root,'assets/figures',key+'.svg'),svg);
    console.log(`${key}: portable skeleton SVG and interactive HTML exported`);
    await page.close();
  }
} finally {await browser.close();}
