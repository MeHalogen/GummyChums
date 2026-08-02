#!/usr/bin/env python3
"""add_motion.py — inject the shared "sick-motion" kit into index15-24.

Idempotent: removes any existing <!-- MO:START -->..<!-- MO:END --> block, then
re-injects a fresh <style id="mo-css"> + <script id="mo-js"> just before </body>.
Extends the existing engine (mini-Lenis smooth scroll, gc-reveal, blob cursor,
pk-light glows) — no second scroll loop, pinned/scrub heroes untouched.

    python3 tools/add_motion.py         # patch index15.html .. index24.html

Built HTML is the source of truth; re-run any time.
"""
import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [f"index{n}.html" for n in range(15, 25)]

GRAIN = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E"
         "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")

MO_CSS = """<style id="mo-css">
  /* ---- sick-motion kit (shared, injected) ---- */
  #mo-prog{position:fixed;top:0;left:0;height:3px;width:0;z-index:500;pointer-events:none;
    background:linear-gradient(90deg,#e8503a,#f4c84f,#98c64b,#477971,#6b2f6a);
    box-shadow:0 0 12px rgba(232,80,58,.55);transition:width .12s linear}
  #mo-grain{position:fixed;inset:-60px;z-index:90;pointer-events:none;opacity:.055;mix-blend-mode:overlay;
    background-image:url("%GRAIN%");background-size:140px;will-change:transform;animation:mo-grain 1.1s steps(3) infinite}
  @keyframes mo-grain{0%{transform:translate(0,0)}33%{transform:translate(-16px,10px)}66%{transform:translate(12px,-12px)}100%{transform:translate(0,0)}}
  .mo-trail{position:fixed;left:0;top:0;width:15px;height:15px;border-radius:50%;z-index:399;pointer-events:none;
    opacity:0;will-change:transform,left,top;transform:translate(-50%,-50%);filter:blur(.5px)}
  .mo-squish{animation:mo-squish .4s cubic-bezier(.34,1.56,.64,1)}
  @keyframes mo-squish{28%{transform:scale(.9,.88)}58%{transform:scale(1.05,.97)}100%{transform:scale(1)}}
  /* cinematic: blur->sharp added to the existing gc-reveal (opacity/translate kept) */
  html.gcjs .gc-reveal{filter:blur(7px);
    transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1),filter .7s ease}
  html.gcjs .gc-reveal.in{filter:blur(0)}
  .mo-word{display:inline-block;opacity:0;transform:translateY(.55em) rotate(2.5deg);
    transition:opacity .5s ease,transform .62s cubic-bezier(.2,.8,.2,1);will-change:transform,opacity}
  .mo-word.in{opacity:1;transform:none}
  @media (prefers-reduced-motion:reduce){
    #mo-grain,.mo-trail{display:none!important}
    html.gcjs .gc-reveal{filter:none!important}
    .mo-word{opacity:1!important;transform:none!important}
  }
</style>""".replace("%GRAIN%", GRAIN)

MO_JS = """<script id="mo-js">
(function(){
  if(window.__moKit)return; window.__moKit=1;
  var R=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
  var d=document, b=d.body, de=d.documentElement;

  // progress bar (cheap, always on)
  var prog=d.createElement('div'); prog.id='mo-prog'; b.appendChild(prog);
  function maxS(){return de.scrollHeight-innerHeight;}
  function onScroll(){var m=maxS(); prog.style.width=(m>0?Math.min(100,scrollY/m*100):0)+'%';}
  addEventListener('scroll',onScroll,{passive:true}); onScroll();
  if(R) return;

  // grain
  var g=d.createElement('div'); g.id='mo-grain'; b.appendChild(g);

  // word-stagger on big headings (skip pk-chars + pinned/scrub + complex nodes)
  try{
    [].slice.call(d.querySelectorAll('h1,h2')).forEach(function(h){
      if(h.classList.contains('pk-chars')||h.dataset.moDone)return;
      if(h.closest('[data-scrub]'))return;
      var kids=[].slice.call(h.childNodes);
      if(kids.some(function(n){return n.nodeType===1 && n.tagName!=='BR';}))return;
      var txt=h.textContent.trim(); if(!txt||txt.length>90)return;
      h.dataset.moDone=1;
      h.innerHTML=txt.split('\\n').map(function(line){
        return line.replace(/(\\S+)/g,'<span class="mo-word">$1</span>');
      }).join('<br>');
    });
  }catch(e){}
  var words=[].slice.call(d.querySelectorAll('.mo-word'));
  var wio=new IntersectionObserver(function(es){es.forEach(function(en){
    if(en.isIntersecting){var el=en.target;
      var sib=[].slice.call(el.parentNode.querySelectorAll('.mo-word'));
      el.style.transitionDelay=(sib.indexOf(el)*0.045)+'s'; el.classList.add('in'); wio.unobserve(el);}
  })},{threshold:0});
  words.forEach(function(w){wio.observe(w);});
  function revealWordsInView(){words.forEach(function(w){if(!w.classList.contains('in')&&w.getBoundingClientRect().top<innerHeight*1.05)w.classList.add('in');});}
  revealWordsInView(); setTimeout(revealWordsInView,60);
  addEventListener('load',revealWordsInView);
  addEventListener('scroll',revealWordsInView,{passive:true});  // failsafe: never stay hidden

  // squish on press (delegated)
  addEventListener('pointerdown',function(e){
    var t=e.target.closest&&e.target.closest('button,.pk-btn,[data-hot],a[href]');
    if(!t)return; t.classList.remove('mo-squish'); void t.offsetWidth; t.classList.add('mo-squish');
  },{passive:true});

  var mx=innerWidth/2, my=innerHeight/2, trails=[];
  if(FINE){
    ['#e8503a','#f4c84f','#6b2f6a'].forEach(function(col,i){
      var s=d.createElement('div'); s.className='mo-trail'; s.style.background=col;
      s.style.width=s.style.height=(15-i*3)+'px'; b.appendChild(s);
      trails.push({el:s,x:mx,y:my,k:0.30-i*0.07});
    });
    addEventListener('pointermove',function(e){mx=e.clientX;my=e.clientY;
      trails.forEach(function(t){t.el.style.opacity=0.42;});},{passive:true});
    // tilt-to-cursor on known cards
    [].slice.call(d.querySelectorAll('.al-card,.sq-card,.ob-card,.sn-rim,.jb-card,.zv-card,.ve-card,.cf-slide,.ms-panel')).forEach(function(c){
      c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();
        var px=(e.clientX-r.left)/r.width-0.5, py=(e.clientY-r.top)/r.height-0.5;
        c.style.transition='transform .08s ease-out';
        c.style.transform='perspective(760px) rotateY('+(px*7).toFixed(2)+'deg) rotateX('+(-py*7).toFixed(2)+'deg)';
      });
      c.addEventListener('pointerleave',function(){
        c.style.transition='transform .55s cubic-bezier(.22,.8,.26,1)'; c.style.transform='';
      });
    });
  }
  var glows=[].slice.call(d.querySelectorAll('.pk-light'));

  // single rAF loop: trail lerp + glow parallax; paused when tab hidden
  var raf=null;
  function loop(){
    var px=mx,py=my;
    for(var i=0;i<trails.length;i++){var t=trails[i];
      t.x+=(px-t.x)*t.k; t.y+=(py-t.y)*t.k;
      t.el.style.left=t.x+'px'; t.el.style.top=t.y+'px'; px=t.x; py=t.y;}
    var y=scrollY;
    for(var j=0;j<glows.length;j++){glows[j].style.transform='translate3d(0,'+(y*(((j%3)+1)*-0.045)).toFixed(1)+'px,0)';}
    raf=requestAnimationFrame(loop);
  }
  function start(){if(raf==null&&!d.hidden)raf=requestAnimationFrame(loop);}
  function stop(){if(raf!=null){cancelAnimationFrame(raf);raf=null;}}
  d.addEventListener('visibilitychange',function(){d.hidden?stop():start();});
  if(FINE||glows.length) start();
})();
</script>"""

BLOCK = "<!-- MO:START -->\n" + MO_CSS + "\n" + MO_JS + "\n<!-- MO:END -->\n"

def patch(html):
    html = re.sub(r"<!-- MO:START -->.*?<!-- MO:END -->\s*", "", html, flags=re.S)
    if "</body>" not in html:
        raise SystemExit("no </body>")
    return html.replace("</body>", BLOCK + "</body>", 1)

def main():
    for f in PAGES:
        p = os.path.join(REPO, f)
        s = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(patch(s))
        print("patched", f)

if __name__ == "__main__":
    main()
