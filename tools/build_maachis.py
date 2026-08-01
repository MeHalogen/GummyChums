#!/usr/bin/env python3
"""build_maachis.py — Maachis Collection generator.

Four hyper-Indian pages riffing on index26 (matchbox), on the FINALIZED palette,
sharing a strike-to-ignite hero animation. index26 is the donor for the shared
kit / kinetic manifesto / Chum Box / bill-checkout (extracted, palette-remapped,
reused verbatim). Each vibe supplies its own skin CSS + nav/hero/boxes + how the
strike resolves.

    python3 tools/build_maachis.py            # writes the 4 maachis-*.html files

Built HTML is the source of truth; this script reproduces them.
"""
import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(REPO, "index26.html")

# ---------------------------------------------------------------- palette remap
BG="#f1e7da"; SURF="#ffffff"; INK="#1f1c1a"; CORAL="#e8503a"; SAFFRON="#f4c84f"
PURPLE="#6b2f6a"; GREEN="#234225"; PINK="#e8a0b2"; TEAL="#477971"
MANGO="#98c64b"; SINDOOR="#ff7a2f"; LIME="#d4e53b"; IMLI="#7b4726"
GULMOHAR="#d72638"; MAROON="#6b1e21"

HEXMAP = {
 # shared neon kit
 "#261236":INK, "#006d36":GREEN,
 "#38bdf8":TEAL, "#8b5cf6":PURPLE, "#7c6cf6":PURPLE,
 "#e44bd3":GULMOHAR, "#ff5c8a":PINK, "#39c98e":MANGO,
 "#ffb02e":SAFFRON, "#fecf34":SAFFRON, "#ffd23f":SAFFRON, "#b80865":MAROON,
 # maachis warm tones
 "#2b1608":INK, "#b3261e":CORAL, "#d4a017":SAFFRON, "#e8641b":SINDOOR,
 "#3e2a1c":IMLI, "#5c4030":IMLI,
 # paper / near-white tints
 "#f3e6c9":BG, "#fdf3da":BG, "#f7e9c6":BG, "#fff8e6":BG, "#e9d7a8":BG,
 "#f4f2f3":SURF, "#fcfafa":SURF, "#fdfdfd":SURF,
}
RGBMAP = {
 "179,38,30":"232,80,58",     # b3261e -> coral
 "212,160,23":"244,200,79",   # d4a017 -> saffron
 "40,20,50":"31,28,26", "43,22,8":"31,28,26",
}

def remap(s):
    for a,b in sorted(HEXMAP.items(), key=lambda kv:-len(kv[0])):
        s = re.sub(re.escape(a), b, s, flags=re.I)
    for a,b in RGBMAP.items():
        r,g,bl = a.split(",")
        s = re.sub(r"(?<![0-9.])%s\s*,\s*%s\s*,\s*%s(?![0-9.])"%(r,g,bl), b, s)
    return s

# ---------------------------------------------------------------- extract donor
raw = open(SRC, encoding="utf-8").read()

head_css_full = raw.split("<style>",1)[1].split("</style>",1)[0]
HEAD_SHARED = head_css_full.split("  body.mb-mx{",1)[0]                     # kit + reveal
KCBB        = "  /* ===== kinetic manifesto ===== */" + \
              head_css_full.split("  /* ===== kinetic manifesto ===== */",1)[1]
HEAD_SHARED = remap(HEAD_SHARED); KCBB = remap(KCBB)

body_part   = raw.split('<body class="mb-mx">',1)[1]
SHARED_TAIL = '<section class="kc" id="kc-manifesto"' + \
              body_part.split('<section class="kc" id="kc-manifesto"',1)[1]
SHARED_TAIL = remap(SHARED_TAIL)   # manifesto + Chum Box + footer + bill + all JS + </body></html>

GCJS = ('<script>(function(){var h=document.documentElement;h.classList.add("gcjs");'
        'window.addEventListener("load",function(){setTimeout(function(){'
        'if(!h.classList.contains("gcready")){document.querySelectorAll(".gc-reveal").forEach('
        'function(e){e.classList.add("in");});}},700);});})();</script>')

# ---------------------------------------------------------------- products
PRODUCTS = [
 ("neon-violet","Neon Violet","Brain Booster","Mango",
  "Bacopa monnieri (Brahmi) 60 mg","₹899",MAROON,"product-neon-violet.html"),
 ("dreamy-sleep","Dreamy Sleep","Melatonin Sleep","Cherry",
  "Melatonin 5 mg + Ashwagandha + Chamomile + Valerian + Passion flower + Magnesium",
  "₹699",PURPLE,"product-dreamy-sleep.html"),
 ("electric-blue","Electric Blue","Eye Care","Orange",
  "Lutein 5 mg + Zeaxanthin + Bilberry 100 mg + Grape seed + Vit A·C·E·B1·B2·B6 + Lycopene",
  "₹749",TEAL,"product-electric-blue.html"),
]
def gummy(c, w="74%"):
    return ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:%s">'
      '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="%s"/>'
      '<ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/>'
      '<ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>')%(w,c)

# ---------------------------------------------------------------- strike engine (shared spine)
STRIKE_CSS = """
  /* ===== strike-to-ignite intro (shared spine) ===== */
  #mk{position:fixed;inset:0;z-index:300;background:#1f1c1a;overflow:hidden;
      transition:opacity .7s ease .9s;}
  #mk.done{opacity:0;pointer-events:none}
  #mk .mk-strip{position:absolute;left:0;right:0;top:50%;height:26px;transform:translateY(-50%);
      background:repeating-linear-gradient(90deg,#7b4726 0 7px,#5c3a20 7px 14px);
      box-shadow:0 1px 0 rgba(255,255,255,.06) inset, 0 -12px 40px rgba(0,0,0,.6);}
  #mk .mk-match{position:absolute;top:50%;left:-24%;width:30%;height:12px;transform:translateY(-50%);
      display:flex;align-items:center;filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))}
  #mk .mk-stick{flex:1;height:9px;border-radius:5px;background:linear-gradient(180deg,#e9d7a8,#c9a86b)}
  #mk .mk-head{width:26px;height:26px;border-radius:52% 48% 50% 50%/58% 58% 42% 42%;
      background:radial-gradient(circle at 40% 35%,#e8503a,#6b1e21 80%);margin-left:-4px;flex:0 0 auto}
  #mk .mk-flame{position:absolute;left:50%;top:50%;width:0;height:0;transform:translate(-50%,-60%);
      border-radius:50% 50% 50% 50%/60% 60% 40% 40%;opacity:0;
      background:radial-gradient(circle at 50% 70%,#fff6d8,#f4c84f 34%,#e8503a 66%,rgba(215,38,56,0) 78%);
      filter:blur(1px);mix-blend-mode:screen}
  #mk .mk-halo{position:absolute;left:50%;top:50%;width:10px;height:10px;border-radius:50%;
      transform:translate(-50%,-50%);opacity:0;background:radial-gradient(circle,#f4c84f,rgba(244,200,79,0) 70%)}
  #mk.go .mk-match{animation:mk-slide 1.15s cubic-bezier(.5,0,.2,1) forwards}
  #mk.go .mk-flame{animation:mk-burst .9s .95s cubic-bezier(.34,1.56,.64,1) forwards, mk-flick .32s 1.2s ease-in-out infinite}
  #mk.go .mk-halo{animation:mk-halo 1s .95s ease-out forwards}
  #mk .mk-spark{position:absolute;top:50%;width:4px;height:4px;border-radius:50%;background:#f4c84f;opacity:0}
  #mk.go .mk-spark{animation:mk-spark .5s .78s ease-out}
  @keyframes mk-slide{0%{left:-24%}62%{left:44%}100%{left:44%}}
  @keyframes mk-burst{0%{width:0;height:0;opacity:0}40%{opacity:1}100%{width:230px;height:340px;opacity:.96}}
  @keyframes mk-flick{0%,100%{transform:translate(-50%,-60%) scale(1) rotate(-1deg)}50%{transform:translate(-50%,-62%) scale(1.06,.95) rotate(1.5deg)}}
  @keyframes mk-halo{0%{opacity:0;width:10px;height:10px}45%{opacity:.9}100%{opacity:0;width:2200px;height:2200px}}
  @keyframes mk-spark{0%{opacity:1;transform:translate(0,-50%)}100%{opacity:0;transform:translate(var(--dx,40px),calc(-50% + var(--dy,-30px)))}}
  /* ignite target */
  .mk-ignite{transition:text-shadow .8s ease 1.15s, filter .8s ease 1.15s;}
  body.lit .mk-ignite{text-shadow:0 0 26px rgba(244,200,79,.65),0 0 60px rgba(232,80,58,.35)}
  .mx-foot{text-align:center;padding:3.2rem 1rem;opacity:.65;font-size:.9rem}
  .mk-ember{position:fixed;bottom:-10px;width:6px;height:6px;border-radius:50%;z-index:120;pointer-events:none;
      background:radial-gradient(circle,#f4c84f,rgba(232,80,58,0) 72%);opacity:0}
  body.lit .mk-ember{animation:mk-rise linear infinite}
  @keyframes mk-rise{0%{opacity:0;transform:translateY(0) scale(1)}12%{opacity:.9}100%{opacity:0;transform:translateY(-88vh) translateX(var(--ex,20px)) scale(.4)}}
  @media (prefers-reduced-motion:reduce){#mk{display:none}}
"""

STRIKE_HTML = ('<div id="mk" aria-hidden="true"><div class="mk-strip"></div>'
  '<div class="mk-halo"></div>'
  '<div class="mk-match"><div class="mk-stick"></div><div class="mk-head"></div>'
  '<div class="mk-flame"></div>'
  + "".join('<span class="mk-spark" style="left:44%%;--dx:%dpx;--dy:%dpx"></span>'%(dx,dy)
            for dx,dy in [(60,-40),(80,10),(50,-70),(90,-20),(40,40)]) +
  '</div></div>')

STRIKE_JS = """<script>(function(){
  var mk=document.getElementById('mk'), b=document.body;
  var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  // drifting embers
  for(var i=0;i<7;i++){var e=document.createElement('div');e.className='mk-ember';
    e.style.left=(6+i*13)+'%';e.style.setProperty('--ex',(i%2?24:-20)+'px');
    e.style.animationDuration=(7+i*1.4)+'s';e.style.animationDelay=(i*0.9)+'s';
    e.style.width=e.style.height=(4+ (i%3))+'px';b.appendChild(e);}
  function lit(){b.classList.add('lit');}
  if(reduce){lit();return;}
  requestAnimationFrame(function(){requestAnimationFrame(function(){
    mk.classList.add('go');
    setTimeout(lit,1150);
    setTimeout(function(){mk.classList.add('done');},1650);
    setTimeout(function(){if(mk&&mk.parentNode)mk.parentNode.removeChild(mk);},2600);
  });});
})();</script>"""

# ---------------------------------------------------------------- LABEL vibe
def label_boxes():
    cards=[]
    for pid,name,role,fl,ing,price,c,pdp in PRODUCTS:
        cards.append(f'''  <article class="lb-box" data-pdp="{pdp}" style="--c:{c}">
    <div class="lb-sun"></div>
    <div class="lb-tray"><div class="lb-inner">
      <div class="lb-role">{role}</div>
      <div class="lb-name">{name}</div>
      <div class="lb-medal">{gummy(c,"58%")}</div>
      <span class="lb-fl">{fl}</span>
      <p class="lb-ing">{ing}</p>
      <div class="lb-buy"><span class="lb-price">{price}</span>
      <button class="add-to-cart-btn lb-add" data-product-id="{pid}">STRIKE</button></div>
    </div></div>
  </article>''')
    return "\n".join(cards)

LABEL = dict(
 title="GummyChums — Maachis · Vintage Label",
 fonts='<link href="https://fonts.googleapis.com/css2?family=Bevan&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet"/>',
 bodyclass="mb-lb",
 cursor='<div id="pkc" style="background:#e8503a"></div>',
 skin_css=r"""
  body.mb-lb{background:#f1e7da;color:#1f1c1a;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:
      radial-gradient(circle at 50% -10%,rgba(244,200,79,.18),transparent 60%),
      repeating-linear-gradient(45deg,rgba(31,28,26,.028) 0 2px,transparent 2px 15px);}
  .lb-disp{font-family:Bevan,serif}
  .lb-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.85rem 1.4rem;background:#e8503a;color:#f1e7da;
    box-shadow:0 4px 14px -6px rgba(31,28,26,.5);border-bottom:3px solid #6b1e21}
  .lb-bag{border:2px solid #f1e7da;background:transparent;color:#f1e7da;border-radius:6px;
    padding:.5rem 1.1rem;font-weight:800;cursor:pointer;letter-spacing:.04em}
  /* hero = one giant matchbox label */
  .lb-hero{max-width:56rem;margin:3.2rem auto 0;padding:0 1.25rem}
  .lb-card{position:relative;background:radial-gradient(circle at 50% 20%,#ffffff,#f1e7da 78%);
    border:3px solid #e8503a;box-shadow:0 0 0 5px #6b1e21,10px 12px 0 -1px rgba(31,28,26,.22),0 30px 60px -30px rgba(31,28,26,.5);
    padding:2.6rem 1.5rem 2.2rem;text-align:center;overflow:hidden}
  .lb-card::before{content:"";position:absolute;inset:11px;border:2px dashed rgba(107,30,33,.5);pointer-events:none}
  .lb-rays{position:absolute;left:50%;top:44%;width:135%;aspect-ratio:1;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg,rgba(244,200,79,.35) 0 6deg,transparent 6deg 12deg);
    border-radius:50%;opacity:.55;pointer-events:none;-webkit-mask:radial-gradient(circle,#000 30%,transparent 62%);
            mask:radial-gradient(circle,#000 30%,transparent 62%)}
  body.lit .lb-rays{animation:lb-spin 60s linear infinite}
  @keyframes lb-spin{to{transform:translate(-50%,-50%) rotate(1turn)}}
  .lb-regd{position:relative;letter-spacing:.34em;font-size:.62rem;font-weight:700;color:#6b1e21;opacity:.8}
  .lb-banner{position:relative;display:inline-block;margin:.7rem 0 .2rem;background:#234225;color:#f1e7da;
    font-weight:800;letter-spacing:.12em;font-size:.72rem;padding:.32rem 1.1rem;border-radius:3px;
    box-shadow:2px 2px 0 rgba(31,28,26,.4)}
  .lb-title{position:relative;font-size:clamp(2.6rem,9vw,5.6rem);line-height:.92;color:#e8503a;
    text-shadow:2px 2px 0 rgba(107,30,33,.9),4px 4px 0 rgba(244,200,79,.5)}
  .lb-medallion{position:relative;width:min(46vw,190px);aspect-ratio:1;margin:1rem auto .4rem;
    border-radius:50%;background:radial-gradient(circle at 50% 38%,#ffffff,#f1e7da);
    border:3px solid #6b1e21;box-shadow:0 0 0 4px #f4c84f,0 12px 26px -14px rgba(31,28,26,.7);
    display:grid;place-items:center;overflow:hidden}
  .lb-medallion img{width:88%;filter:drop-shadow(0 4px 8px rgba(31,28,26,.3))}
  .lb-sub{position:relative;max-width:32rem;margin:1rem auto 0;line-height:1.7;font-weight:500;opacity:.85}
  .lb-seals{position:relative;display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap;margin-top:1.3rem}
  .lb-seal{border:2px solid #6b1e21;color:#6b1e21;border-radius:999px;padding:.32rem .95rem;
    font-weight:800;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase}
  .lb-cta{position:relative;display:inline-block;margin-top:1.5rem;background:#e8503a;color:#f1e7da;
    font-weight:800;letter-spacing:.04em;border:3px solid #6b1e21;box-shadow:4px 4px 0 #6b1e21;
    padding:.95rem 2rem;cursor:pointer}
  /* scrolling safety band */
  .lb-band{overflow:hidden;background:#1f1c1a;color:#f4c84f;padding:.8rem 0;margin-top:3.2rem}
  .lb-band>div{display:flex;white-space:nowrap;font-family:Bevan,serif;font-size:1rem;letter-spacing:.14em;animation:lb-mv 26s linear infinite}
  @keyframes lb-mv{to{transform:translateX(-50%)}}
  /* product matchbox labels */
  .lb-grid{max-width:74rem;margin:0 auto;padding:4rem 1.25rem 5rem;display:grid;gap:2.4rem;
    grid-template-columns:repeat(auto-fit,minmax(268px,1fr))}
  .lb-box{position:relative;transition:transform .4s cubic-bezier(.22,.8,.26,1)}
  .lb-box:hover{transform:translateY(-6px) rotate(-.6deg)}
  .lb-sun{position:absolute;left:50%;top:34%;width:150%;aspect-ratio:1;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg,rgba(244,200,79,.4) 0 5deg,transparent 5deg 10deg);
    border-radius:50%;opacity:0;transition:opacity .4s;pointer-events:none;
    -webkit-mask:radial-gradient(circle,#000 22%,transparent 55%);mask:radial-gradient(circle,#000 22%,transparent 55%)}
  .lb-box:hover .lb-sun{opacity:.7;animation:lb-spin 40s linear infinite}
  .lb-tray{position:relative;background:radial-gradient(circle at 50% 22%,#ffffff,#f1e7da 80%);
    border:3px solid var(--c);box-shadow:0 0 0 4px #6b1e21,6px 8px 0 rgba(31,28,26,.22),0 18px 30px -14px rgba(31,28,26,.5);
    padding:1.2rem;z-index:2}
  .lb-inner{border:2px dashed rgba(107,30,33,.4);padding:1.2rem 1rem;text-align:center}
  .lb-role{font-size:.7rem;font-weight:800;letter-spacing:.24em;text-transform:uppercase;color:var(--c)}
  .lb-name{font-family:Bevan,serif;font-size:1.45rem;margin:.3rem 0 .5rem;color:#1f1c1a}
  .lb-medal{width:74%;margin:auto}
  .lb-fl{display:inline-block;border:2px solid var(--c);color:var(--c);border-radius:4px;padding:.2rem .7rem;
    font-size:.72rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin:.5rem 0}
  .lb-ing{font-size:.78rem;line-height:1.55;opacity:.72;min-height:3.4em}
  .lb-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.5rem}
  .lb-price{font-family:Bevan,serif;font-size:1.35rem;color:#e8503a}
  .lb-add{border:2px solid #6b1e21;background:#f4c84f;color:#1f1c1a;border-radius:6px;padding:.55rem 1.1rem;
    font-weight:800;cursor:pointer;box-shadow:3px 3px 0 #6b1e21;transition:transform .15s,box-shadow .15s}
  .lb-add:active{transform:translate(3px,3px);box-shadow:0 0 0 #6b1e21}
  .lb-foot{text-align:center;padding:3.2rem 1rem;opacity:.65;font-size:.9rem}
""",
)

def label_body():
    band = ('SAFETY GUMMIES ✦ MADE IN INDIA ✦ STRIKES EVERY TIME ✦ 100% VEG ✦ '
            'NO ADDED SUGAR ✦ SUPERIOR QUALITY ✦ ')
    return f'''{LABEL["cursor"]}
<nav class="lb-nav"><b class="lb-disp" style="font-size:1.15rem">GUMMYCHUMS MAACHIS CO.</b>
  <button class="cart-trigger lb-bag" data-hot>BAG <span class="cart-count" style="display:none;background:#f4c84f;color:#1f1c1a;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="lb-hero"><div class="lb-card">
  <div class="lb-rays"></div>
  <p class="lb-regd">REGD. No. 2026 · AVERAGE CONTENTS 15 / 30 / 45</p>
  <div class="lb-banner">SAFETY GUMMIES · सुरक्षित सेहत</div>
  <h1 class="lb-disp lb-title mk-ignite pk-chars">GUMMYCHUMS</h1>
  <div class="lb-medallion"><img src="mascot.png" alt="GummyChums mascot"/></div>
  <p class="lb-sub">Vintage matchbox spirit, modern lab science. Slide a box open — brain, sleep or eyes — and <b>strike up your daily routine.</b></p>
  <div class="lb-seals"><span class="lb-seal">★ Superior Quality</span><span class="lb-seal">Trade Mark</span><span class="lb-seal">100% Veg</span></div>
  <a href="#boxes" data-hot class="lb-cta">OPEN A BOX ↓</a>
</div></header>
<div class="lb-band"><div><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span></div></div>
<section id="boxes" class="lb-grid">
{label_boxes()}
</section>'''

# ---------------------------------------------------------------- generic product card
def pcard(p, cta):
    out=[]
    for pid,name,role,fl,ing,price,c,pdp in PRODUCTS:
        out.append(f'''  <article class="{p}-box" data-pdp="{pdp}" style="--c:{c}">
    <div class="{p}-tray">
      <div class="{p}-role">{role}</div>
      <div class="{p}-name">{name}</div>
      <div class="{p}-art">{gummy(c,"62%")}</div>
      <span class="{p}-fl">{fl}</span>
      <p class="{p}-ing">{ing}</p>
      <div class="{p}-buy"><span class="{p}-price">{price}</span>
      <button class="add-to-cart-btn {p}-add" data-product-id="{pid}">{cta}</button></div>
    </div>
  </article>''')
    return "\n".join(out)

# ================================================================ BOLLYWOOD vibe
BOLLYWOOD = dict(
 title="GummyChums — Maachis · Retro Bollywood",
 fonts='<link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet"/>',
 bodyclass="mb-bw",
 cursor='<div id="pkc" style="background:#f4c84f"></div>',
 skin_css=r"""
  body.mb-bw{background:#6b1e21;color:#f1e7da;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:
      radial-gradient(120% 80% at 50% 0%,rgba(232,80,58,.55),transparent 60%),
      radial-gradient(80% 60% at 50% 42%,rgba(244,200,79,.22),transparent 62%),
      repeating-linear-gradient(0deg,rgba(0,0,0,.05) 0 2px,transparent 2px 4px);}
  .bw-disp{font-family:'Rozha One',serif}
  .bw-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.85rem 1.4rem;background:rgba(31,28,26,.55);backdrop-filter:blur(6px);color:#f4c84f;
    border-bottom:2px solid rgba(244,200,79,.5)}
  .bw-bag{border:2px solid #f4c84f;background:transparent;color:#f4c84f;border-radius:6px;
    padding:.5rem 1.1rem;font-weight:800;cursor:pointer;letter-spacing:.04em}
  .bw-hero{max-width:60rem;margin:0 auto;padding:3.2rem 1.25rem 1rem;text-align:center;position:relative}
  .bw-spot{position:absolute;left:50%;top:8%;width:90%;height:120%;transform:translateX(-50%);pointer-events:none;
    background:radial-gradient(circle at 50% 30%,rgba(244,200,79,.4),transparent 55%);opacity:0;transition:opacity 1s ease 1.15s}
  body.lit .bw-spot{opacity:1}
  .bw-now{display:inline-block;position:relative;background:#e8503a;color:#f1e7da;font-weight:800;
    letter-spacing:.16em;font-size:.72rem;padding:.4rem 1.2rem;border-radius:999px;margin-bottom:1rem;
    box-shadow:0 0 0 3px #6b1e21,0 0 0 5px #f4c84f}
  .bw-star{position:relative;display:inline-block;margin-bottom:.6rem}
  .bw-star::before,.bw-star::after{content:"✦";color:#f4c84f;margin:0 .5rem;font-size:1rem}
  .bw-title{position:relative;font-size:clamp(3rem,11vw,7rem);line-height:.9;color:#f4c84f;
    text-shadow:0 2px 0 #e8503a,0 4px 0 #6b1e21,0 14px 34px rgba(0,0,0,.6)}
  .bw-tag{font-family:'Rozha One',serif;font-size:clamp(1.3rem,3.6vw,2.2rem);color:#e8a0b2;margin-top:.2rem}
  .bw-sub{max-width:34rem;margin:1.1rem auto 0;line-height:1.7;opacity:.9}
  .bw-cast{margin:1.4rem auto 0;max-width:36rem;font-size:.82rem;letter-spacing:.06em;opacity:.85;
    border-top:1px solid rgba(244,200,79,.35);border-bottom:1px solid rgba(244,200,79,.35);padding:.7rem 0}
  .bw-cast b{color:#f4c84f}
  .bw-cta{position:relative;display:inline-block;margin-top:1.5rem;background:#f4c84f;color:#6b1e21;
    font-weight:800;letter-spacing:.04em;border-radius:999px;padding:.95rem 2.2rem;cursor:pointer;
    box-shadow:0 10px 26px -10px rgba(0,0,0,.6)}
  .bw-band{overflow:hidden;background:#1f1c1a;color:#f4c84f;padding:.8rem 0;margin-top:3rem;
    border-top:2px solid rgba(244,200,79,.4);border-bottom:2px solid rgba(244,200,79,.4)}
  .bw-band>div{display:flex;white-space:nowrap;font-family:'Rozha One',serif;font-size:1.1rem;letter-spacing:.14em;animation:bw-mv 26s linear infinite}
  @keyframes bw-mv{to{transform:translateX(-50%)}}
  .bw-grid{max-width:74rem;margin:0 auto;padding:4rem 1.25rem 5rem;display:grid;gap:2.2rem;
    grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .bw-box{position:relative;transition:transform .4s cubic-bezier(.22,.8,.26,1)}
  .bw-box:hover{transform:translateY(-8px) scale(1.02)}
  .bw-tray{position:relative;background:linear-gradient(180deg,#7b2e2f,#6b1e21);
    border:2px solid #f4c84f;border-radius:10px;padding:1.4rem 1.2rem;text-align:center;overflow:hidden;
    box-shadow:0 20px 40px -20px rgba(0,0,0,.7)}
  .bw-tray::before{content:"NOW SHOWING";position:absolute;top:.7rem;left:50%;transform:translateX(-50%);
    font-size:.55rem;letter-spacing:.24em;color:#f4c84f;opacity:.7}
  .bw-role{margin-top:1.2rem;font-size:.7rem;font-weight:800;letter-spacing:.22em;text-transform:uppercase;color:#e8a0b2}
  .bw-name{font-family:'Rozha One',serif;font-size:1.7rem;margin:.2rem 0 .4rem;color:#f4c84f}
  .bw-art{width:62%;margin:.3rem auto}
  .bw-fl{display:inline-block;border:1px solid #f4c84f;color:#f4c84f;border-radius:999px;padding:.2rem .7rem;
    font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin:.4rem 0}
  .bw-ing{font-size:.78rem;line-height:1.55;opacity:.8;min-height:3.4em}
  .bw-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.5rem}
  .bw-price{font-family:'Rozha One',serif;font-size:1.5rem;color:#f4c84f}
  .bw-add{border:0;background:#e8503a;color:#f1e7da;border-radius:999px;padding:.55rem 1.2rem;font-weight:800;
    cursor:pointer;box-shadow:0 8px 18px -8px rgba(0,0,0,.7);transition:transform .2s}
  .bw-add:active{transform:scale(.93)}
  .bw-foot{text-align:center;padding:3.2rem 1rem;opacity:.7;font-size:.9rem}
""",
)
def bollywood_body():
    band='GUMMYCHUMS ✦ A WELLNESS BLOCKBUSTER ✦ HOUSEFULL SINCE 2026 ✦ NOW SHOWING ✦ '
    return f'''{BOLLYWOOD["cursor"]}
<nav class="bw-nav"><b class="bw-disp" style="font-size:1.3rem">GUMMYCHUMS</b>
  <button class="cart-trigger bw-bag" data-hot>BAG <span class="cart-count" style="display:none;background:#f4c84f;color:#6b1e21;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="bw-hero"><div class="bw-spot"></div>
  <span class="bw-now">★ NOW SHOWING ★</span>
  <div class="bw-star"><span style="letter-spacing:.3em;font-size:.7rem;opacity:.75">PRESENTS</span></div>
  <h1 class="bw-disp bw-title mk-ignite pk-chars">GUMMYCHUMS</h1>
  <p class="bw-tag">Rang-Birangi Sehat ka Blockbuster</p>
  <p class="bw-sub">Vintage matchbox spirit, hand-painted-poster heart, modern lab science. <b>Strike up your daily routine.</b></p>
  <div class="bw-cast"><b>STARRING</b> · Dreamy Sleep · Electric Blue · Neon Violet — <b>a GummyChums Production</b></div>
  <a href="#boxes" data-hot class="bw-cta">BOOK YOUR BOX ↓</a>
</header>
<div class="bw-band"><div><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span></div></div>
<section id="boxes" class="bw-grid">
{pcard("bw","BOOK NOW")}
</section>'''

# ================================================================ BAZAAR vibe
BAZAAR = dict(
 title="GummyChums — Maachis · Bazaar Signboard",
 fonts='<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet"/>',
 bodyclass="mb-bz",
 cursor='<div id="pkc" style="background:#234225"></div>',
 skin_css=r"""
  body.mb-bz{background:#f1e7da;color:#1f1c1a;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:repeating-linear-gradient(90deg,rgba(31,28,26,.03) 0 1px,transparent 1px 26px),
                     repeating-linear-gradient(0deg,rgba(31,28,26,.03) 0 1px,transparent 1px 26px);}
  .bz-disp{font-family:'Baloo 2',cursive}
  .bz-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.7rem 1.4rem;background:#234225;color:#f4c84f;box-shadow:0 4px 14px -6px rgba(31,28,26,.5)}
  .bz-bag{border:2px solid #f4c84f;background:transparent;color:#f4c84f;border-radius:6px;
    padding:.5rem 1.1rem;font-weight:800;cursor:pointer}
  .bz-hero{max-width:58rem;margin:2.6rem auto 0;padding:0 1.25rem}
  /* hanging enamel board */
  .bz-hang{display:flex;justify-content:center;gap:22%;margin-bottom:-6px}
  .bz-hang span{width:4px;height:34px;background:linear-gradient(#7b4726,#5c3a20)}
  .bz-board{position:relative;background:#234225;color:#f1e7da;border-radius:16px;
    padding:2.4rem 1.5rem 2.2rem;text-align:center;
    box-shadow:0 0 0 4px #1f1c1a,0 0 0 9px #f4c84f,0 26px 44px -22px rgba(31,28,26,.7)}
  .bz-board::before{content:"";position:absolute;inset:14px;border:2px dotted rgba(241,231,218,.4);border-radius:8px;pointer-events:none}
  /* bulb marquee */
  .bz-bulbs{position:absolute;inset:-4px;border-radius:18px;pointer-events:none}
  .bz-bulbs i{position:absolute;width:9px;height:9px;border-radius:50%;background:#7b4726;
    box-shadow:0 0 0 1px rgba(0,0,0,.3)}
  body.lit .bz-bulbs i{background:#f4c84f;box-shadow:0 0 8px 2px rgba(244,200,79,.8);animation:bz-blink 1.4s steps(1) infinite}
  @keyframes bz-blink{0%,100%{opacity:1}50%{opacity:.45}}
  .bz-est{letter-spacing:.32em;font-size:.62rem;font-weight:700;color:#f4c84f;opacity:.85}
  .bz-title{position:relative;font-family:'Baloo 2',cursive;font-weight:800;font-size:clamp(2.6rem,10vw,6rem);
    line-height:.95;color:#f4c84f;text-shadow:3px 3px 0 #e8503a,6px 6px 0 rgba(31,28,26,.5)}
  .bz-line2{font-family:'Baloo 2',cursive;font-weight:800;font-size:clamp(1.1rem,3.6vw,2rem);color:#e8a0b2;margin-top:-.2rem}
  .bz-sub{max-width:32rem;margin:1rem auto 0;line-height:1.7;opacity:.9}
  .bz-tags{display:flex;gap:.7rem;justify-content:center;flex-wrap:wrap;margin-top:1.2rem}
  .bz-tag{background:#f4c84f;color:#1f1c1a;font-weight:800;font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;
    padding:.35rem .9rem;border-radius:4px;position:relative;box-shadow:2px 2px 0 rgba(31,28,26,.4)}
  .bz-cta{display:inline-block;margin-top:1.4rem;background:#e8503a;color:#f1e7da;font-weight:800;
    border-radius:8px;padding:.95rem 2rem;cursor:pointer;box-shadow:4px 4px 0 #1f1c1a}
  .bz-band{overflow:hidden;background:#e8503a;color:#f1e7da;padding:.75rem 0;margin-top:3.2rem}
  .bz-band>div{display:flex;white-space:nowrap;font-family:'Baloo 2',cursive;font-weight:800;font-size:1rem;letter-spacing:.1em;animation:bz-mv 24s linear infinite}
  @keyframes bz-mv{to{transform:translateX(-50%)}}
  .bz-grid{max-width:74rem;margin:0 auto;padding:4rem 1.25rem 5rem;display:grid;gap:2.2rem;
    grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
  .bz-box{position:relative;transition:transform .35s cubic-bezier(.22,.8,.26,1)}
  .bz-box:hover{transform:translateY(-6px)}
  .bz-tray{position:relative;background:#ffffff;border-radius:12px;padding:1.3rem 1.2rem;text-align:center;
    box-shadow:0 0 0 3px #1f1c1a,0 0 0 6px var(--c),0 16px 30px -16px rgba(31,28,26,.5)}
  .bz-role{font-size:.7rem;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:var(--c)}
  .bz-name{font-family:'Baloo 2',cursive;font-weight:800;font-size:1.55rem;margin:.1rem 0 .4rem;color:#1f1c1a}
  .bz-art{width:62%;margin:.2rem auto}
  .bz-fl{display:inline-block;background:var(--c);color:#fff;border-radius:4px;padding:.2rem .7rem;
    font-size:.7rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin:.4rem 0}
  .bz-ing{font-size:.78rem;line-height:1.55;opacity:.72;min-height:3.4em}
  .bz-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.5rem}
  .bz-price{position:relative;font-family:'Baloo 2',cursive;font-weight:800;font-size:1.4rem;color:#e8503a;
    background:#f4c84f;padding:.1rem .7rem;border-radius:4px;transform:rotate(-3deg);box-shadow:2px 2px 0 rgba(31,28,26,.35)}
  .bz-add{border:0;background:#234225;color:#f1e7da;border-radius:8px;padding:.55rem 1.1rem;font-weight:800;
    cursor:pointer;box-shadow:3px 3px 0 #1f1c1a;transition:transform .18s,box-shadow .18s}
  .bz-add:active{transform:translate(3px,3px);box-shadow:0 0 0 #1f1c1a}
  .bz-foot{text-align:center;padding:3.2rem 1rem;opacity:.65;font-size:.9rem}
""",
)
def bazaar_body():
    band='★ BEST QUALITY ★ TAAZA MAAL ★ WHOLESALE & RETAIL ★ NO. 1 GUMMY WELLNESS STORE ★ '
    bulbs="".join(
      f'<i style="{pos}"></i>' for pos in
      [f"left:{x}%;top:-4px" for x in range(4,97,9)] +
      [f"left:{x}%;bottom:-4px" for x in range(4,97,9)] +
      ["left:-4px;top:20%","left:-4px;top:50%","left:-4px;top:80%","right:-4px;top:20%","right:-4px;top:50%","right:-4px;top:80%"])
    return f'''{BAZAAR["cursor"]}
<nav class="bz-nav"><b class="bz-disp" style="font-size:1.4rem">GummyChums</b>
  <button class="cart-trigger bz-bag" data-hot>BAG <span class="cart-count" style="display:none;background:#f4c84f;color:#234225;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="bz-hero">
  <div class="bz-hang"><span></span><span></span></div>
  <div class="bz-board"><div class="bz-bulbs">{bulbs}</div>
    <p class="bz-est">✦ ESTD. 2026 · MADE IN INDIA ✦</p>
    <h1 class="bz-title mk-ignite pk-chars">GUMMYCHUMS</h1>
    <p class="bz-line2">Gummy Wellness Store · गमी सेहत भंडार</p>
    <p class="bz-sub">Vintage matchbox spirit, dukaan-board warmth, modern lab science. <b>Best quality, guaranteed.</b></p>
    <div class="bz-tags"><span class="bz-tag">★ Best Quality</span><span class="bz-tag">100% Veg</span><span class="bz-tag">No Added Sugar</span></div>
    <a href="#boxes" data-hot class="bz-cta">VISIT THE SHELF ↓</a>
  </div>
</header>
<div class="bz-band"><div><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span><span style="padding:0 1.6rem">{band}</span></div></div>
<section id="boxes" class="bz-grid">
{pcard("bz","BUY")}
</section>'''

# ================================================================ DOORDARSHAN vibe
DD = dict(
 title="GummyChums — Maachis · Doordarshan Retro",
 fonts='<link href="https://fonts.googleapis.com/css2?family=VT323&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet"/>',
 bodyclass="mb-dd",
 cursor='<div id="pkc" style="background:#f4c84f"></div>',
 skin_css=r"""
  body.mb-dd{background:#1f1c1a;color:#f1e7da;font-family:Poppins,sans-serif;overflow-x:hidden;}
  body.mb-dd::after{content:"";position:fixed;inset:0;z-index:200;pointer-events:none;opacity:.5;
    background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 1px,transparent 1px 3px)}
  .dd-mono{font-family:'VT323',monospace}
  .dd-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.7rem 1.4rem;background:#0f0d0c;color:#f4c84f;border-bottom:2px solid #477971}
  .dd-bag{border:2px solid #f4c84f;background:transparent;color:#f4c84f;border-radius:4px;
    padding:.4rem 1rem;font-weight:800;cursor:pointer;font-family:'VT323',monospace;font-size:1.15rem}
  .dd-hero{max-width:60rem;margin:0 auto;padding:2.4rem 1.25rem 1rem;text-align:center}
  /* CRT screen */
  .dd-crt{position:relative;background:#100e0d;border-radius:22px/16px;padding:2.4rem 1.6rem 2rem;overflow:hidden;
    box-shadow:0 0 0 6px #2a2320,0 0 0 10px #0f0d0c,0 30px 60px -26px #000,inset 0 0 90px rgba(0,0,0,.7)}
  .dd-crt::before{content:"";position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(120% 90% at 50% 50%,transparent 60%,rgba(0,0,0,.55) 100%)}
  .dd-bars{position:absolute;inset:0;display:flex;opacity:0;transition:opacity .5s ease .3s}
  body.lit .dd-bars{opacity:.16}
  .dd-bars i{flex:1}
  .dd-ident{width:88px;height:88px;margin:0 auto .8rem;border-radius:50%;position:relative;
    background:conic-gradient(#e8503a,#f4c84f,#98c64b,#477971,#6b2f6a,#e8a0b2,#e8503a);
    display:grid;place-items:center;box-shadow:0 0 24px rgba(244,200,79,.4)}
  body.lit .dd-ident{animation:pk-spin 12s linear infinite}
  @keyframes pk-spin{to{transform:rotate(1turn)}}
  .dd-ident b{width:64px;height:64px;border-radius:50%;background:#100e0d;color:#f4c84f;font-family:'VT323',monospace;
    font-size:2rem;display:grid;place-items:center}
  .dd-kick{font-family:'VT323',monospace;font-size:1.3rem;letter-spacing:.3em;color:#98c64b}
  .dd-title{position:relative;font-family:'VT323',monospace;font-size:clamp(3rem,12vw,7.5rem);line-height:.85;
    color:#f4c84f;text-shadow:3px 0 #e8503a,-3px 0 #477971}
  .dd-tag{font-size:clamp(1rem,3vw,1.5rem);color:#f1e7da;opacity:.9;margin-top:.2rem}
  .dd-sub{max-width:34rem;margin:1rem auto 0;line-height:1.7;opacity:.85;position:relative}
  .dd-cta{display:inline-block;margin-top:1.4rem;background:#e8503a;color:#f1e7da;font-family:'VT323',monospace;
    font-size:1.4rem;letter-spacing:.08em;border-radius:6px;padding:.6rem 1.8rem;cursor:pointer}
  .dd-ticker{overflow:hidden;background:#0f0d0c;color:#98c64b;padding:.6rem 0;margin-top:2.6rem;
    border-top:1px solid #477971;border-bottom:1px solid #477971;font-family:'VT323',monospace;font-size:1.25rem}
  .dd-ticker>div{display:flex;white-space:nowrap;letter-spacing:.14em;animation:dd-mv 22s linear infinite}
  @keyframes dd-mv{to{transform:translateX(-50%)}}
  .dd-grid{max-width:74rem;margin:0 auto;padding:4rem 1.25rem 5rem;display:grid;gap:2.2rem;
    grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
  .dd-box{position:relative;transition:transform .35s cubic-bezier(.22,.8,.26,1)}
  .dd-box:hover{transform:translateY(-6px)}
  .dd-tray{position:relative;background:#100e0d;border-radius:16px;padding:1.3rem 1.2rem;text-align:center;overflow:hidden;
    box-shadow:0 0 0 3px #2a2320,0 0 0 6px var(--c),inset 0 0 50px rgba(0,0,0,.6)}
  .dd-tray::before{content:"CH ●";position:absolute;top:.6rem;right:.9rem;font-family:'VT323',monospace;color:#98c64b;
    font-size:1rem;letter-spacing:.1em}
  .dd-role{font-family:'VT323',monospace;font-size:1.15rem;letter-spacing:.16em;text-transform:uppercase;color:#98c64b}
  .dd-name{font-family:'VT323',monospace;font-size:2rem;line-height:1;margin:.1rem 0 .4rem;color:#f4c84f}
  .dd-art{width:62%;margin:.2rem auto}
  .dd-fl{display:inline-block;border:1px solid #f4c84f;color:#f4c84f;border-radius:4px;
    padding:.15rem .6rem;font-family:'VT323',monospace;font-size:.95rem;letter-spacing:.1em;text-transform:uppercase;margin:.4rem 0}
  /* Chum Box + manifesto vals are light-mode components -> give them a light inset on the CRT page */
  body.mb-dd #bb-builder{background:#f1e7da;color:#1f1c1a;margin:2.4rem 1rem;border-radius:20px;
    box-shadow:0 0 0 3px #477971,0 0 0 7px #0f0d0c}
  body.mb-dd .kc-chip,body.mb-dd .kc-val{background:rgba(241,231,218,.08)}
  body.mb-dd .mx-foot{color:#f1e7da}
  .dd-ing{font-size:.78rem;line-height:1.55;opacity:.78;min-height:3.4em}
  .dd-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.5rem}
  .dd-price{font-family:'VT323',monospace;font-size:1.8rem;color:#98c64b}
  .dd-add{border:0;background:#e8503a;color:#f1e7da;border-radius:6px;padding:.5rem 1.1rem;font-family:'VT323',monospace;
    font-size:1.2rem;letter-spacing:.06em;cursor:pointer;transition:transform .2s}
  .dd-add:active{transform:scale(.92)}
  .dd-foot{text-align:center;padding:3.2rem 1rem;opacity:.7;font-size:.9rem}
""",
)
def dd_body():
    bars="".join('<i style="background:%s"></i>'%c for c in
        ["#e8503a","#f4c84f","#98c64b","#477971","#6b2f6a","#e8a0b2","#f1e7da"])
    tick='◄ TRANSMISSION BEGINS ✦ GUMMYCHUMS · RANG-BIRANGI SEHAT ✦ STAND BY ✦ MADE IN INDIA ✦ '
    return f'''{DD["cursor"]}
<nav class="dd-nav"><b class="dd-mono" style="font-size:1.5rem;letter-spacing:.1em">GUMMYCHUMS</b>
  <button class="cart-trigger dd-bag" data-hot>BAG <span class="cart-count" style="display:none;background:#f4c84f;color:#100e0d;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="dd-hero"><div class="dd-crt">
  <div class="dd-bars">{bars}</div>
  <div class="dd-ident"><b>GC</b></div>
  <p class="dd-kick">▶ NOW BROADCASTING</p>
  <h1 class="dd-title mk-ignite pk-chars">GUMMYCHUMS</h1>
  <p class="dd-tag">रंग-बिरंगी सेहत · Colour Your Wellness</p>
  <p class="dd-sub">Vintage matchbox spirit, Doordarshan-era warmth, modern lab science. <b>Please adjust your routine.</b></p>
  <a href="#boxes" data-hot class="dd-cta">TUNE IN ↓</a>
</div></header>
<div class="dd-ticker"><div><span style="padding:0 1.6rem">{tick}</span><span style="padding:0 1.6rem">{tick}</span><span style="padding:0 1.6rem">{tick}</span></div></div>
<section id="boxes" class="dd-grid">
{pcard("dd","TUNE IN")}
</section>'''

VIBES = {
 "maachis-label.html":     (LABEL, label_body),
 "maachis-bollywood.html": (BOLLYWOOD, bollywood_body),
 "maachis-bazaar.html":    (BAZAAR, bazaar_body),
 "maachis-dd.html":        (DD, dd_body),
}

# ---------------------------------------------------------------- assemble
HEAD_TOP = ('<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
 '<script src="https://cdn.tailwindcss.com"></script>\n'
 '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,1,0&display=swap" rel="stylesheet"/>\n')

def build():
    for fname,(vibe,body_fn) in VIBES.items():
        html = ("<!DOCTYPE html>\n<html lang=\"en\" class=\"scroll-smooth\">\n<head>\n"
          + HEAD_TOP + vibe["fonts"] + "\n"
          + f'<title>{vibe["title"]}</title>\n'
          + GCJS + "\n<style>\n"
          + HEAD_SHARED + vibe["skin_css"] + KCBB + STRIKE_CSS
          + "\n</style>\n</head>\n"
          + f'<body class="{vibe["bodyclass"]}">\n'
          + STRIKE_HTML + "\n"
          + body_fn() + "\n"
          + SHARED_TAIL)
        # inject strike JS just before </body>
        html = html.replace("</body>", STRIKE_JS + "\n</body>", 1)
        open(os.path.join(REPO,fname),"w",encoding="utf-8").write(html)
        print("wrote", fname, f"({len(html)//1024} KB)")

if __name__ == "__main__":
    build()
