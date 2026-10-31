/* Ein Scroll-Takt für die Fassungen mit data-p: --p läuft von 0 (Block unten am Rand) bis 1 (Mitte im Bild). Nur sichtbare Blöcke rechnen. */
(function(){
var els=[].slice.call(document.querySelectorAll('[data-p]'));if(!els.length)return;
var sicht=new Set(),an=false;
function takt(){an=false;var vh=innerHeight;sicht.forEach(function(el){var r=el.getBoundingClientRect();
 var p=(vh-r.top)/(vh/2+r.height/2);p=Math.max(0,Math.min(1,p));el.style.setProperty('--p',p.toFixed(4))})}
function los(){if(!an){an=true;requestAnimationFrame(takt)}}
var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?sicht.add(e.target):sicht.delete(e.target)});los()},{rootMargin:'100px 0px'});
els.forEach(function(e){io.observe(e)});addEventListener('scroll',los,{passive:true});addEventListener('resize',los);
})();
