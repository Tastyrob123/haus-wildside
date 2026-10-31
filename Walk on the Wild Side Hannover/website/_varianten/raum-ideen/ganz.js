const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const S='/private/tmp/claude-501/-Users-robertreff--claude-spares-spare-LXHy91/b6e6b044-3a33-421f-b8d9-8002880bc2bb/scratchpad/';
(async()=>{const b=await webkit.launch();const c=await b.newContext({viewport:{width:1440,height:900}});
for(const f of process.argv.slice(2)){const p=await c.newPage();await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/'+f,{waitUntil:'networkidle'});
const h=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<h;y+=400){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(120)}
await p.evaluate(()=>{scrollTo(0,0);const l=document.getElementById('leiste');if(l)l.style.position='absolute';document.querySelectorAll('[data-pin],.k1').forEach(e=>e.style.height='auto')});await p.waitForTimeout(1500);
await p.screenshot({path:S+'ganz-'+f.replace('.html','')+'.jpg',fullPage:true,type:'jpeg',quality:55});console.log(f,h);await p.close()}
await b.close()})();
