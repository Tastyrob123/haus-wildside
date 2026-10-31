const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const S='/private/tmp/claude-501/-Users-robertreff--claude-spares-spare-LXHy91/b6e6b044-3a33-421f-b8d9-8002880bc2bb/scratchpad/';
(async()=>{const b=await webkit.launch();
for(const W of [1440,1000,390]){const c=await b.newContext({viewport:{width:W,height:W>700?900:812}});const p=await c.newPage();
await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/haus.html',{waitUntil:'networkidle'});
const y=await p.evaluate(()=>document.getElementById('raum').getBoundingClientRect().top+scrollY);const hh=await p.evaluate(()=>document.getElementById('raum').offsetHeight);
for(let d=-400;d<hh+200;d+=250){await p.evaluate(v=>scrollTo(0,v),y+d);await p.waitForTimeout(140)}
await p.evaluate(v=>{scrollTo(0,v);document.getElementById('leiste').style.visibility='hidden'},y);await p.waitForTimeout(2200);
const m=await p.evaluate(()=>[document.documentElement.scrollWidth,[...document.querySelectorAll('#raum img')].map(i=>i.currentSrc.split('/').pop()+':'+i.naturalWidth).join(' ')]);
await p.locator('#raum').screenshot({path:S+'echt'+W+'.jpg',type:'jpeg',quality:60});console.log(W,m[0],m[1]);await c.close()}
await b.close()})();
