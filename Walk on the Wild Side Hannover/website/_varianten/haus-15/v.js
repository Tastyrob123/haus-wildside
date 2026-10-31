/* Wild Side · Haus 15 Fassungen. (1) Ein Scroll-Takt: --p von 0 (Block unten am Rand) bis 1 (Mitte im Bild), nur sichtbare Blöcke rechnen.
   (2) Tauschen: Zeigen oder Tippen auf [data-t] macht das passende [data-z] sichtbar. (3) Wandern: der Satz in der Mitte des Schirms bestimmt das Bild. */
(function(){
var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var els=$$('[data-p]'),sicht=new Set(),an=false;
function takt(){an=false;var vh=innerHeight;sicht.forEach(function(el){var r=el.getBoundingClientRect();
 var p=(vh-r.top)/(vh/2+r.height/2);p=Math.max(0,Math.min(1,p));el.style.setProperty('--p',p.toFixed(4))})}
function los(){if(!an){an=true;requestAnimationFrame(takt)}}
if(els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?sicht.add(e.target):sicht.delete(e.target)});los()},{rootMargin:'100px 0px'});
 els.forEach(function(e){io.observe(e)});addEventListener('scroll',los,{passive:true});addEventListener('resize',los)}

function setze(box,i){$$('[data-z],[data-t]',box).forEach(function(x){var v=x.getAttribute('data-z');if(v==null)v=x.getAttribute('data-t');x.classList.toggle('an',+v===i)})}
$$('[data-tausch]').forEach(function(box){setze(box,box.hasAttribute('data-frei')?-1:0);
 $$('[data-t]',box).forEach(function(t){var i=+t.getAttribute('data-t');
  t.addEventListener('mouseenter',function(){setze(box,i)});t.addEventListener('focus',function(){setze(box,i)});t.addEventListener('click',function(){setze(box,i)})});
 if(box.hasAttribute('data-frei'))box.addEventListener('mouseleave',function(){setze(box,-1)})});

$$('[data-wandern]').forEach(function(box){var sch=$$('[data-schritt]',box);
 var w=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var i=+e.target.getAttribute('data-schritt');setze(box,i);sch.forEach(function(s){s.classList.toggle('an',s===e.target)})}})},{rootMargin:'-45% 0px -45% 0px'});
 sch.forEach(function(s){w.observe(s)});sch[0]&&sch[0].classList.add('an')});
})();
