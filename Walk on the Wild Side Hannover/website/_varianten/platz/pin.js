const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const S='/private/tmp/claude-501/-Users-robertreff--claude-spares-spare-LXHy91/b6e6b044-3a33-421f-b8d9-8002880bc2bb/scratchpad/';
(async()=>{const b=await webkit.launch();const W=+(process.argv[2]||1440),H=W>700?900:812;const c=await b.newContext({viewport:{width:W,height:H}});
for(const nr of ['05','09']){const p=await c.newPage();await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/platz/'+nr+'.html',{waitUntil:'networkidle'});
 const el=await p.evaluate(()=>{const s=document.querySelector('[data-pin]');return [s.getBoundingClientRect().top+scrollY,s.offsetHeight]});
 for(const f of [0.1,0.55,0.95]){const y=el[0]+f*(el[1]-H);for(let d=y-1200;d<=y;d+=300){await p.evaluate(v=>scrollTo(0,v),d);await p.waitForTimeout(120)}
  await p.evaluate(v=>{scrollTo(0,v);document.getElementById('leiste').style.visibility='hidden';document.querySelector('.vschild').style.display='none'},y);await p.waitForTimeout(1600);
  await p.screenshot({path:S+'pin'+W+'-'+nr+'-'+f+'.jpg',type:'jpeg',quality:55,scale:'css'})}
 await p.close()}
await b.close()})();
