/* Wild Side · Haus, Raum 15 neue Fassungen (31.10.2026). (0) Pin-Takt: --q von 0 bis 1 über die gehaltene Strecke [data-pin]. (1) Ein Scroll-Takt: --p von 0 (Block unten am Rand) bis 1 (Mitte im Bild), nur sichtbare Blöcke rechnen.
   (2) Tauschen: Zeigen oder Tippen auf [data-t] macht das passende [data-z] sichtbar. (3) Wandern: der Satz in der Mitte des Schirms bestimmt das Bild. */
(function(){
var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var els=$$('[data-p]'),sicht=new Set(),an=false;
function takt(){an=false;var vh=innerHeight;sicht.forEach(function(el){var r=el.getBoundingClientRect();
 var p=(vh-r.top)/(vh/2+r.height/2);p=Math.max(0,Math.min(1,p));el.style.setProperty('--p',p.toFixed(4))})}
function los(){if(!an){an=true;requestAnimationFrame(takt)}}
var pins=$$('[data-pin]');function pin(){pins.forEach(function(el){var r=el.getBoundingClientRect(),d=r.height-innerHeight;var q=d>0?Math.max(0,Math.min(1,-r.top/d)):1;el.style.setProperty('--q',q.toFixed(4));
 if(el.hasAttribute('data-schritte')){var n=+el.getAttribute('data-schritte'),i=Math.max(0,Math.min(n-1,Math.floor(q*(n-1)-.55)+1));if(el._i!==i){el._i=i;setze(el,i)}}})}
if(pins.length){addEventListener('scroll',function(){requestAnimationFrame(pin)},{passive:true});addEventListener('resize',pin);pin()}
if(els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?sicht.add(e.target):sicht.delete(e.target)});los()},{rootMargin:'100px 0px'});
 els.forEach(function(e){io.observe(e)});addEventListener('scroll',los,{passive:true});addEventListener('resize',los)}

function setze(box,i){if(box._blick)box._blick(i);$$('[data-z],[data-t]',box).forEach(function(x){var v=x.getAttribute('data-z');if(v==null)v=x.getAttribute('data-t');x.classList.toggle('an',+v===i)})}
$$('[data-tausch]').forEach(function(box){setze(box,box.hasAttribute('data-frei')?-1:0);
 $$('[data-t]',box).forEach(function(t){var i=+t.getAttribute('data-t');
  t.addEventListener('mouseenter',function(){setze(box,i)});t.addEventListener('focus',function(){setze(box,i)});t.addEventListener('click',function(){setze(box,i)})});
 if(box.hasAttribute('data-frei'))box.addEventListener('mouseleave',function(){setze(box,-1)})});

$$('[data-wandern]').forEach(function(box){var sch=$$('[data-schritt]',box);
 var w=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var i=+e.target.getAttribute('data-schritt');setze(box,i);sch.forEach(function(s){s.classList.toggle('an',s===e.target)})}})},{rootMargin:'-45% 0px -45% 0px'});
 sch.forEach(function(s){w.observe(s)});sch[0]&&sch[0].classList.add('an')});
})();

/* Blicke (raum-20): [data-blicke]=[[bild,transform],…]. Das passende Foto steigt im Rahmen auf, sein Bild fährt an die Stelle. */
(function(){[].slice.call(document.querySelectorAll('[data-blicke]')).forEach(function(box){var L=JSON.parse(box.getAttribute('data-blicke'));
 var fs=[].slice.call(box.querySelectorAll('[data-bild]'));
 box._blick=function(i){if(i<0||!L[i])return;var b=L[i][0];fs.forEach(function(f){var on=+f.getAttribute('data-bild')===b;f.classList.toggle('oben',on);if(on){var im=f.querySelector('img');if(im)im.style.transform=L[i][1]}})};
 box._blick(0)})})();
/* Postkarte: Tippen dreht um */
[].slice.call(document.querySelectorAll('[data-wenden]')).forEach(function(k){k.addEventListener('click',function(){k.classList.toggle('gedreht')})});
