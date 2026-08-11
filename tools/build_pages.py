#!/usr/bin/env python3
"""build_pages.py — Shopify-lean content pages (story / about / contact).

Plain CSS (no Tailwind runtime), self-contained, section-ready — each page's
<style>+markup+<script> pastes into a Liquid section with near-zero rework.
All the experience is kept: scroll-reveal, blob cursor, film grain, the
fall-in gummy takeover, tapri sticker-bomb, marquee — pure CSS + vanilla JS.

    python3 tools/build_pages.py     # writes story.html, about.html, contact.html
"""
import os
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GRAIN=("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E"
 "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E"
 "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")

def gummy(c,w="100%"):
    return ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:%s;display:block">'
     '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="%s"/>'
     '<ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/>'
     '<ellipse cx="52" cy="62" rx="30" ry="22" fill="#000" opacity=".07"/></svg>')%(w,c)

CSS=r"""
:root{--coral:#e8503a;--saffron:#f4c84f;--pink:#e8a0b2;--mango:#98c64b;--teal:#477971;
  --green:#234225;--maroon:#6b1e21;--sindoor:#ff7a2f;--ink:#1f1c1a;--cream:#f1e7da;--white:#fff}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Baloo 2',system-ui,-apple-system,sans-serif;background:var(--cream);color:var(--ink);
  overflow-x:hidden;-webkit-font-smoothing:antialiased;line-height:1.5}
.anton{font-family:'Anton',sans-serif;letter-spacing:.01em;font-weight:400}
a{color:inherit;text-decoration:none}
img,svg{max-width:100%}
.wrap{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.halftone{background-image:radial-gradient(rgba(31,28,26,.13) 1.5px,transparent 1.6px);background-size:15px 15px}
/* nav */
.nav{position:sticky;top:0;z-index:60;display:flex;align-items:center;justify-content:space-between;
  padding:.85rem 1.5rem;background:rgba(241,231,218,.92);backdrop-filter:blur(8px);border-bottom:3px solid var(--ink)}
.nav .brand{font-weight:800;font-size:1.35rem}
.nav .links{display:flex;gap:1.5rem;font-weight:700;font-size:.95rem;align-items:center}
.nav .links a{transition:color .2s}
.nav .links a:hover,.nav .links a[aria-current]{color:var(--coral)}
.nav .bag{border:2px solid var(--ink);background:var(--saffron);border-radius:999px;padding:.4rem 1.1rem;
  font-weight:800;box-shadow:3px 3px 0 var(--ink);font-size:.9rem}
@media(max-width:760px){.nav .links a:not(.bag){display:none}}
/* stickers + chips + buttons */
.sticker{position:absolute;font-weight:800;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;
  border:2px solid var(--ink);border-radius:999px;padding:.32rem .85rem;box-shadow:3px 3px 0 var(--ink);white-space:nowrap}
.chip{display:inline-block;font-weight:800;border:2px solid var(--ink);border-radius:999px;padding:.5rem 1.15rem;
  margin:.3rem;box-shadow:3px 3px 0 var(--ink);background:var(--white)}
.btn{display:inline-block;border:2px solid var(--ink);background:var(--coral);color:var(--cream);font-weight:800;
  border-radius:12px;padding:.9rem 2rem;box-shadow:4px 4px 0 var(--ink);cursor:pointer;
  transition:transform .14s,box-shadow .14s}
.btn:active{transform:translate(4px,4px);box-shadow:0 0 0 var(--ink)}
.eyebrow{font-weight:800;letter-spacing:.22em;text-transform:uppercase;font-size:.8rem;color:var(--coral)}
.hi{color:var(--coral)}
/* reveal */
.reveal{opacity:0;transform:translateY(38px);filter:blur(6px);
  transition:opacity .8s cubic-bezier(.2,.8,.2,1),transform .8s cubic-bezier(.2,.8,.2,1),filter .7s ease}
.reveal.in{opacity:1;transform:none;filter:none}
.reveal.d1{transition-delay:.08s}.reveal.d2{transition-delay:.16s}.reveal.d3{transition-delay:.24s}
/* grain + cursor */
#grain{position:fixed;inset:-60px;z-index:92;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
  background-image:url("%GRAIN%");background-size:140px;will-change:transform;animation:grain 1.1s steps(3) infinite}
@keyframes grain{0%{transform:translate(0,0)}33%{transform:translate(-14px,9px)}66%{transform:translate(11px,-11px)}100%{transform:translate(0,0)}}
#cur{position:fixed;left:0;top:0;width:26px;height:26px;border-radius:46% 54% 52% 48%/48% 46% 54% 52%;z-index:400;
  pointer-events:none;transform:translate(-50%,-50%);mix-blend-mode:multiply;background:var(--coral);opacity:0;
  transition:width .2s,height .2s,opacity .3s;box-shadow:inset -3px -4px 7px rgba(0,0,0,.18),inset 3px 4px 7px rgba(255,255,255,.4)}
#cur.on{opacity:.9}
@media(hover:none),(pointer:coarse){#cur{display:none}}
/* progress bar */
#prog{position:fixed;top:0;left:0;height:3px;width:0;z-index:500;pointer-events:none;
  background:linear-gradient(90deg,var(--coral),var(--saffron),var(--mango),var(--teal),var(--maroon))}
/* sections + colour-blocks */
.sec{padding:6rem 0;position:relative}
.block{border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);border-radius:20px;padding:2.4rem}
.grid3{display:grid;gap:1.6rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.card{background:var(--white);border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);border-radius:18px;
  padding:1.8rem;transition:transform .3s cubic-bezier(.22,.8,.26,1),box-shadow .3s cubic-bezier(.22,.8,.26,1)}
.card:hover{transform:translate(-2px,-5px);box-shadow:12px 15px 0 var(--ink)}
h1.big{font-family:'Anton',sans-serif;font-size:clamp(2.8rem,10vw,7rem);line-height:.9}
h2.big{font-family:'Anton',sans-serif;font-size:clamp(2.2rem,7vw,5rem);line-height:.92}
.lead{font-size:clamp(1.1rem,2.4vw,1.4rem);font-weight:600;max-width:42rem}
.strike{position:relative;white-space:nowrap;opacity:.6}
.strike::after{content:"";position:absolute;left:-2%;right:-2%;top:52%;height:.12em;background:var(--coral);border-radius:9px;
  transform:scaleX(0);transform-origin:left;transition:transform .6s cubic-bezier(.77,0,.18,1)}
.reveal.in .strike::after{transform:scaleX(1)}
/* footer */
.footer{border-top:3px solid var(--ink);padding:3.4rem 1.5rem;text-align:center}
.footer .flinks{display:flex;gap:1.4rem;justify-content:center;margin-bottom:1rem;flex-wrap:wrap;font-weight:800}
.footer .flinks a:hover{color:var(--coral)}
.footer small{opacity:.6;font-weight:600}
/* marquee */
.marq{overflow:hidden;background:var(--coral);color:var(--cream);padding:.75rem 0;border-block:3px solid var(--ink)}
.marq>div{display:flex;white-space:nowrap;font-family:'Anton',sans-serif;font-size:1.2rem;letter-spacing:.06em;
  animation:marq 24s linear infinite}
@keyframes marq{to{transform:translateX(-50%)}}
/* FALL-IN takeover (story) */
.fallin{position:relative;height:250vh}
.fallin .pin{position:sticky;top:0;height:100vh;overflow:hidden;display:grid;place-items:center;background:var(--cream)}
.fallin .fg{position:absolute;left:50%;bottom:4%;width:min(34vw,200px);transform-origin:center bottom;
  transform:translateX(-50%) scale(calc(1 + var(--z,0)*var(--z,0)*26));z-index:0}
.fallin .ftitle{position:relative;z-index:2;text-align:center;padding:0 1.25rem;opacity:calc(1 - var(--z,0)*2.6)}
.fallin .finside{position:absolute;inset:0;z-index:3;display:grid;place-items:center;text-align:center;padding:0 1.25rem;
  color:var(--cream);opacity:calc((var(--z,0) - .6)*3.4);pointer-events:none}
@media(prefers-reduced-motion:reduce){
  .reveal{opacity:1!important;transform:none!important;filter:none!important}
  #grain{display:none}
  .fallin{height:auto}.fallin .pin{position:static;height:auto;padding:5rem 0}
  .fallin .fg{position:static;transform:none;width:160px;margin:2rem auto}
  .fallin .ftitle{opacity:1}.fallin .finside{position:static;opacity:1;color:var(--ink);padding:3rem 1.25rem}
}
""".replace("%GRAIN%",GRAIN)

def nav(active):
    def a(href,label,key):
        cur=' aria-current="page"' if key==active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return ('<nav class="nav"><a href="index31.html" class="brand">GummyChums</a>'
      '<div class="links">'
      + a("story.html","Story","story") + a("about.html","About","about")
      + a("contact.html","Contact","contact")
      + '<a href="index31.html#shop">Shop</a>'
      + '<a href="index31.html#shop" class="bag">BAG</a>'
      '</div></nav>')

FOOTER=('<footer class="footer"><div class="flinks">'
  '<a href="story.html">Story</a><a href="about.html">About</a><a href="contact.html">Contact</a>'
  '<a href="index31.html#shop">Shop</a></div>'
  '<p class="anton" style="font-size:1.6rem">A treat, not a task.</p>'
  '<small>GummyChums · Make wellness feel like a treat, not a task · Made in India · © 2026</small></footer>')

JS=r"""<script>
(function(){
  // reveal
  var els=[].slice.call(document.querySelectorAll('.reveal'));
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:0,rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(e){io.observe(e);});
  function inview(){els.forEach(function(e){if(e.getBoundingClientRect().top<innerHeight*1.05)e.classList.add('in');});}
  inview();addEventListener('load',inview);
  // progress
  var pr=document.getElementById('prog');
  function onScroll(){var m=document.documentElement.scrollHeight-innerHeight;if(pr)pr.style.width=(m>0?Math.min(100,scrollY/m*100):0)+'%';}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  // blob cursor
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches, cur=document.getElementById('cur');
  if(fine&&cur){var cx=innerWidth/2,cy=innerHeight/2,x=cx,y=cy;
    addEventListener('mousemove',function(e){cx=e.clientX;cy=e.clientY;cur.classList.add('on');});
    document.querySelectorAll('a,button,.btn,.card').forEach(function(b){
      b.addEventListener('mouseenter',function(){cur.style.width='52px';cur.style.height='52px';});
      b.addEventListener('mouseleave',function(){cur.style.width='26px';cur.style.height='26px';});});
    (function loop(){x+=(cx-x)*.55;y+=(cy-y)*.55;cur.style.left=x+'px';cur.style.top=y+'px';requestAnimationFrame(loop);})();
  }
  // fall-in --z
  var stage=document.querySelector('.fallin'); if(stage){var tk=false;
    function up(){var r=stage.getBoundingClientRect();var d=r.height-innerHeight;var z=d>0?Math.min(Math.max(-r.top/d,0),1):0;stage.style.setProperty('--z',z.toFixed(4));}
    addEventListener('scroll',function(){if(!tk){requestAnimationFrame(function(){up();tk=false;});tk=true;}},{passive:true});
    addEventListener('resize',up);up();}
})();
</script>"""

def page(title, active, body):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\"/>\n"
      "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>\n"
      f"<title>{title}</title>\n"
      "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"/>\n"
      "<link href=\"https://fonts.googleapis.com/css2?family=Anton&family=Baloo+2:wght@500;600;700;800&display=swap\" rel=\"stylesheet\"/>\n"
      f"<style>{CSS}</style>\n</head>\n<body>\n"
      "<div id=\"grain\"></div><div id=\"cur\"></div><div id=\"prog\"></div>\n"
      + nav(active) + "\n" + body + "\n" + FOOTER + "\n" + JS + "\n</body>\n</html>")

# ------------------------------------------------------------------ STORY
def story_body():
    def chap(bg,fg,inner):
        return f'<section class="sec" style="background:{bg};color:{fg}"><div class="wrap">{inner}</div></section>'
    hero=('<header class="sec halftone" style="min-height:88vh;display:grid;place-items:center;text-align:center;position:relative">'
      '<span class="sticker" style="top:18%;left:8%;background:var(--saffron);transform:rotate(-8deg)">since 2026</span>'
      '<span class="sticker" style="top:24%;right:7%;background:var(--mango);transform:rotate(7deg)">100% Veg</span>'
      '<div class="wrap reveal"><p class="eyebrow">GummyChums · The Story</p>'
      '<h1 class="big" style="margin:1rem 0">It started with<br/>one question.</h1>'
      '<p class="lead" style="margin:0 auto">“Why does taking care of our health have to feel like taking <span class="hi">medicine</span>?”</p>'
      '<p style="margin-top:2.5rem;font-weight:800;letter-spacing:.2em;opacity:.5">SCROLL ↓</p></div></header>')
    c1=chap("var(--cream)","var(--ink)",
      '<div class="reveal"><h2 class="big">It got to be<br/>too much.</h2>'
      '<p class="lead" style="margin-top:1.4rem">Multiple bottles. Different capsules. Remembering which one, when — carrying them everywhere. '
      'Wellness had quietly become <span class="hi">another task on the to-do list.</span></p></div>')
    c2=chap("var(--saffron)","var(--ink)",
      '<div class="reveal"><h2 class="big">I wasn&rsquo;t alone.</h2>'
      '<p class="lead" style="margin-top:1.4rem">So many people give up on their supplements — not because they don’t care about their health, '
      'but because the <b>experience itself isn’t enjoyable.</b> Pills feel clinical. Powders are a chore.</p></div>')
    # THE SPARK — fall-in takeover
    spark=('<section class="fallin"><div class="pin halftone">'
      '<div class="fg">'+gummy("var(--coral)")+'</div>'
      '<div class="ftitle reveal in"><p class="eyebrow">The spark</p>'
      '<h2 class="big" style="max-width:16ch;margin:1rem auto">What if wellness<br/>felt like candy?</h2>'
      '<p class="lead" style="margin:0 auto">As enjoyable as your favourite childhood treat — that you actually look forward to.</p>'
      '<p style="margin-top:2rem;font-weight:800;letter-spacing:.2em;opacity:.5">SCROLL ↓</p></div>'
      '<div class="finside"><div><h2 class="big">That’s where<br/><span style="color:var(--saffron)">GummyChums</span> began.</h2></div></div>'
      '</div></section>')
    c4=chap("var(--teal)","var(--cream)",
      '<div class="reveal"><p class="eyebrow" style="color:var(--saffron)">This one’s personal</p>'
      '<h2 class="big" style="margin:.6rem 0 1.4rem">This one&rsquo;s personal.</h2>'
      '<p class="lead">Lactose-intolerant, so I rethought my supplements. I went from non-veg to <b>pure vegetarian</b>, '
      'swapping fish oil for plant-based. Later, a job change brought anxiety, and for a while, medication. '
      'It taught me how <b>intimidating</b> wellness can feel — and that everyday wellness shouldn’t.</p></div>')
    c5=chap("var(--cream)","var(--ink)",
      '<div class="reveal"><h2 class="big">“Chums” means <span class="hi">friends.</span></h2>'
      '<p class="lead" style="margin-top:1.4rem">Your daily wellness companion. The little friend you happily reach for every day — '
      '<b>not because you have to, but because you want to.</b></p></div>')
    finale=('<section class="sec halftone" style="min-height:80vh;display:grid;place-items:center;text-align:center;background:var(--maroon);color:var(--cream)">'
      '<div class="wrap reveal"><p class="eyebrow" style="color:var(--saffron)">Our mission</p>'
      '<h2 class="big" style="margin:1rem 0 2rem">A treat,<br/>not a task.</h2>'
      '<p class="lead" style="margin:0 auto 2.4rem">Make wellness feel like a <span style="color:var(--saffron)">treat</span>, not a task.</p>'
      '<a href="index31.html#shop" class="btn" style="background:var(--saffron);color:var(--ink)">Meet the Chums →</a></div></section>')
    return hero+c1+c2+spark+c4+c5+finale

# ------------------------------------------------------------------ ABOUT
def about_body():
    hero=('<header class="sec halftone" style="min-height:72vh;display:grid;place-items:center;text-align:center;position:relative">'
      '<span class="sticker" style="top:22%;right:9%;background:var(--teal);color:var(--cream);transform:rotate(7deg)">not a supplement co.</span>'
      '<div class="wrap reveal"><p class="eyebrow">About GummyChums</p>'
      '<h1 class="big" style="margin:1rem 0">We&rsquo;re not another<br/>supplement brand.</h1>'
      '<p class="lead" style="margin:0 auto">We’re building a new way for India to experience wellness — '
      '<b>modern, playful, proudly Indian</b>, and impossible to ignore.</p></div></header>')
    solve=('<section class="sec" style="background:var(--coral);color:var(--cream)"><div class="wrap reveal">'
      '<h2 class="big">Wellness should be <span style="color:var(--saffron)">fun</span>, not a chore.</h2>'
      '<p class="lead" style="margin-top:1.4rem">The biggest problem in wellness isn’t the product — it’s <b>consistency.</b> '
      'People start with good intentions, then forget, lose motivation, or just don’t enjoy it. '
      'We make delicious, science-backed gummies you actually look forward to.</p></div></section>')
    who=('<section class="sec"><div class="wrap"><div class="reveal"><p class="eyebrow">Who it’s for</p>'
      '<h2 class="big" style="margin:.6rem 0 2rem">20–45, busy &amp; ambitious.</h2></div>'
      '<div class="grid3">'
      '<div class="card reveal"><div class="anton" style="font-size:2.2rem;color:var(--coral)">01</div><b style="font-size:1.3rem">Young professionals</b><p style="margin-top:.5rem;opacity:.75">Metro &amp; Tier 1/2, juggling work, fitness, travel &amp; family.</p></div>'
      '<div class="card reveal d1"><div class="anton" style="font-size:2.2rem;color:var(--teal)">02</div><b style="font-size:1.3rem">Students</b><p style="margin-top:.5rem;opacity:.75">Competitive &amp; govt-exam prep — long hours, real focus &amp; energy.</p></div>'
      '<div class="card reveal d2"><div class="anton" style="font-size:2.2rem;color:var(--mango)">03</div><b style="font-size:1.3rem">Fitness &amp; travel</b><p style="margin-top:.5rem;opacity:.75">Convenient hydration, recovery &amp; on-the-go wellness — no bottles to lug.</p></div>'
      '</div></div></section>')
    feel=('<section class="sec" style="background:var(--saffron)"><div class="wrap reveal"><p class="eyebrow">How we want you to feel</p>'
      '<h2 class="big" style="margin:.6rem 0 1.6rem">Wellness = the best part of your day.</h2>'
      '<div>'+''.join(f'<span class="chip">{w}</span>' for w in
        ["Happy","Confident","Energized","Comforted","Curious","Proud","Consistent"])+'</div></div></section>')
    persona=('<section class="sec"><div class="wrap reveal"><p class="eyebrow">If we were a person</p>'
      '<h2 class="big" style="margin:.6rem 0 1.6rem">That friend who makes<br/>self-care easy.</h2>'
      '<div>'+''.join(f'<span class="chip" style="background:var(--pink)">{w}</span>' for w in
        ["Playful","Honest","Confident","Curious","Modern","Inclusive"])+'</div>'
      '<p class="lead" style="margin-top:1.6rem">Playful without being childish. Confident without being arrogant. '
      'Informative without ever being preachy.</p></div></section>')
    never=('<section class="sec" style="background:var(--ink);color:var(--cream)"><div class="wrap reveal">'
      '<p class="eyebrow" style="color:var(--saffron)">What we’ll never be</p>'
      '<h2 class="big" style="margin:.6rem 0 1.6rem;line-height:1.15">We will never be '
      + ' '.join(f'<span class="strike">{w}</span>' for w in ["clinical","childish","preachy","complicated","just another supplement bottle"])
      + '.</h2><p class="lead">Not a supplement company. Not a candy brand. Not an Ayurvedic brand. '
      'A modern lifestyle brand that happens to make wellness — one India actually loves.</p></div></section>')
    values=('<section class="sec"><div class="wrap"><div class="reveal"><p class="eyebrow">Non-negotiables</p>'
      '<h2 class="big" style="margin:.6rem 0 2rem">Three things we stand for.</h2></div><div class="grid3">'
      '<div class="block reveal" style="background:var(--mango)"><div class="anton" style="font-size:1.8rem">Accessibility</div><p style="margin-top:.6rem">Premium experience, affordable price. Great wellness shouldn’t feel out of reach.</p></div>'
      '<div class="block reveal d1" style="background:var(--pink)"><div class="anton" style="font-size:1.8rem">Joy</div><p style="margin-top:.6rem">Every flavour, pack &amp; message should make you smile. Wellness you look forward to.</p></div>'
      '<div class="block reveal d2" style="background:var(--teal);color:var(--cream)"><div class="anton" style="font-size:1.8rem">Trust</div><p style="margin-top:.6rem">Honest labels, quality ingredients, certified facilities. No question marks.</p></div>'
      '</div><div class="reveal" style="text-align:center;margin-top:3rem"><a href="story.html" class="btn">Read our story →</a></div></div></section>')
    return hero+solve+who+feel+persona+never+values

# ------------------------------------------------------------------ CONTACT
def contact_body():
    # NOTE: placeholder contact details — swap for the real email + handles.
    hero=('<header class="sec halftone" style="min-height:60vh;display:grid;place-items:center;text-align:center;position:relative">'
      '<span class="sticker" style="top:20%;left:8%;background:var(--mango);transform:rotate(-7deg)">we’re all ears</span>'
      '<div class="wrap reveal"><p class="eyebrow">Contact</p>'
      '<h1 class="big" style="margin:1rem 0">Say hi.</h1>'
      '<p class="lead" style="margin:0 auto">Questions, collabs, or just wanna tell us your GummyChums story? '
      'Slide into any of these.</p></div></header>')
    def tile(bg,fg,label,val,href):
        return (f'<a href="{href}" class="card reveal" style="background:{bg};color:{fg};display:block">'
          f'<div class="eyebrow" style="color:{fg};opacity:.75">{label}</div>'
          f'<div class="anton" style="font-size:clamp(1.4rem,4vw,2rem);margin-top:.4rem;word-break:break-word">{val}</div></a>')
    tiles=('<section class="sec"><div class="wrap"><div class="grid3">'
      + tile("var(--coral)","var(--cream)","Email","hello@gummychums.in","mailto:hello@gummychums.in")
      + tile("var(--saffron)","var(--ink)","Instagram","@gummychums","https://instagram.com/gummychums")
      + tile("var(--mango)","var(--ink)","WhatsApp","+91 00000 00000","https://wa.me/910000000000")
      + '</div>'
      '<div class="block reveal" style="margin-top:2rem;background:var(--teal);color:var(--cream);text-align:center">'
      '<h2 class="big" style="font-size:clamp(1.6rem,5vw,3rem)">Run clubs, cafés, creators?</h2>'
      '<p class="lead" style="margin:1rem auto 0">We love a good collab. Tell us what you’re dreaming up — '
      '<a href="mailto:hello@gummychums.in" style="text-decoration:underline">hello@gummychums.in</a></p></div>'
      '<p class="reveal" style="text-align:center;margin-top:2rem;font-weight:800;opacity:.6">Made in India · FSSAI-certified facilities · No added sugar</p>'
      '</div></section>')
    return hero+tiles

PAGES={
 "story.html":   ("GummyChums — The Story", "story",   story_body),
 "about.html":   ("GummyChums — About",     "about",   about_body),
 "contact.html": ("GummyChums — Contact",   "contact", contact_body),
}
def build():
    for fn,(title,active,fn_body) in PAGES.items():
        html=page(title,active,fn_body())
        open(os.path.join(REPO,fn),"w",encoding="utf-8").write(html)
        print("wrote",fn,f"({len(html)//1024} KB)")
if __name__=="__main__": build()
