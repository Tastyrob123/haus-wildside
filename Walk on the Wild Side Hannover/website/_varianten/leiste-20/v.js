/* Fassung 11: das goldene Feld gleitet unter das Wort, auf dem die Maus steht, und kehrt zur aktiven Seite zurück. */
(function(){
var nav=document.querySelector('.leiste.lv11 nav');if(!nav)return;
var s=nav.querySelector('.lv-schein'),akt=nav.querySelector('a.aktiv');
function zu(a){if(!a)return;s.style.setProperty('--x',a.offsetLeft+'px');s.style.setProperty('--w',a.offsetWidth+'px')}
zu(akt);addEventListener('load',function(){zu(akt)});
nav.querySelectorAll('a').forEach(function(a){a.addEventListener('mouseenter',function(){zu(a)})});
nav.addEventListener('mouseleave',function(){zu(akt)});
})();
