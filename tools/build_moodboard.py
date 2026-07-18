# -*- coding: utf-8 -*-
"""
Moodboard Collection (index25-29) — five sites tailored to the founder's
Pinterest board: modern Indian retro-pop packaging (stamps, matchboxes,
kirana pouches, spiced-soda labels, biscuit-tin block prints).

Product cards carry the REAL supplier SKU data (Brain Booster = Bacopa 60mg
mango / Melatonin blend cherry / Eye Care lutein+bilberry orange) while
keeping the established chum ids+names so the shared bill stays consistent.

Shared pieces (reveal failsafe, bill CSS+HTML, checkout JS, motion kit) are
extracted from the built product-dreamy-sleep.html — the receipt stays
byte-identical.  Run from repo root:  python3 tools/build_moodboard.py
Then: python3 tools/upgrade_story.py && python3 tools/bundle_builder.py
      && python3 tools/fix_gallery.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKOUT_MARK = '<!-- ===================== SHARED BILL / CHECKOUT'

# ---------------------------------------------------------------- real SKUs
REAL = [
 dict(id='neon-violet',  name='Neon Violet',  role='Brain Booster', flavour='Mango',
      color='#e44bd3', ing='Bacopa monnieri (Brahmi) 60 mg',
      extra='no added sugar · berry-shaped', price='₹899'),
 dict(id='dreamy-sleep', name='Dreamy Sleep', role='Melatonin Sleep', flavour='Cherry',
      color='#8b5cf6', ing='Melatonin 5 mg + Ashwagandha + Chamomile + Valerian + Passion flower + Magnesium',
      extra='berry-shaped · one before bed', price='₹699'),
 dict(id='electric-blue',name='Electric Blue',role='Eye Care', flavour='Orange',
      color='#38bdf8', ing='Lutein 5 mg + Zeaxanthin + Bilberry 100 mg + Grape seed + Vit A·C·E·B1·B2·B6 + Lycopene',
      extra='no added sugar · berry-shaped', price='₹749'),
]

def gummy(color, style=''):
    return ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"'
      + (' style="'+style+'"' if style else '') + '>'
      '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="'+color+'"/>'
      '<ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/>'
      '<ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>')

CARD_JS = ('<script>(function(){document.querySelectorAll("[data-pdp]").forEach(function(c){'
  'c.style.cursor="pointer";c.setAttribute("data-hot","");'
  'c.addEventListener("click",function(e){if(e.target.closest("button,a"))return;'
  'location.href=c.getAttribute("data-pdp");});});})();</script>')

def extract_shared():
    src = open(os.path.join(ROOT,'product-dreamy-sleep.html'), encoding='utf-8').read()
    fail = re.search(r'<script>\s*/\* enable reveal-hiding.*?</script>', src, re.S).group(0)
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    kit_css = style[:style.index('.pd-band{')]
    co = src.index(CHECKOUT_MARK); sc = src.index('<script>', co)
    checkout_html = src[co:sc]
    js = src[sc+len('<script>'):src.rindex('</script>')]
    core_js = js[:js.index('/* ===== premium motion kit ===== */')]
    prem_js = js[js.index('/* ===== premium motion kit ===== */'):js.index('(function(){ // gallery thumb switcher')]
    return fail, kit_css, checkout_html, core_js, prem_js

def page(theme, fail, kit_css, checkout_html, core_js, prem_js):
    return ('<!DOCTYPE html>\n<html lang="en" class="scroll-smooth">\n<head>\n'
      '<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
      '<title>'+theme['title']+'</title>\n'
      '<script src="https://cdn.tailwindcss.com"></script>\n'
      '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,1,0&display=swap" rel="stylesheet"/>\n'
      + theme['fonts'] + '\n' + fail + '\n<style>\n' + kit_css + '\n' + theme['css'] + '\n</style>\n</head>\n'
      '<body class="'+theme['body_class']+'">\n'
      + theme['body'] + '\n' + checkout_html
      + '<script>\n' + core_js + prem_js + '\n</script>\n'
      + CARD_JS + '\n' + theme.get('js','') + '\n</body>\n</html>')

def cards(tpl):
    return ''.join(tpl.format(
        id=d['id'], name=d['name'], role=d['role'], flavour=d['flavour'],
        color=d['color'], ing=d['ing'], extra=d['extra'], price=d['price'],
        pdp='product-'+d['id']+'.html',
        gum=gummy(d['color'],'width:74%;margin:auto'))
        for d in REAL)

THEMES = []

# ==================================================================== 25 DAAK GHAR
THEMES.append(dict(
 file='index25.html', title='GummyChums — Daak Ghar',
 body_class='mb-daak',
 fonts='<link href="https://fonts.googleapis.com/css2?family=Rozha+One&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet"/>',
 css='''
  body.mb-daak{background:#f7f0e1;color:#3a2418;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:radial-gradient(rgba(58,36,24,.045) 1px,transparent 1px);background-size:26px 26px}
  .dk-disp{font-family:'Rozha One',serif}
  .dk-acc{color:#d81b60}
  .dk-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.9rem 1.4rem;background:rgba(247,240,225,.92);backdrop-filter:blur(8px);box-shadow:0 1px 0 rgba(58,36,24,.12)}
  .dk-bag{border:0;background:#3a2418;color:#f7f0e1;border-radius:999px;padding:.55rem 1.2rem;font-weight:700;cursor:pointer}
  .dk-hero{max-width:72rem;margin:0 auto;padding:5rem 1.25rem 4rem;display:grid;gap:2.5rem;align-items:center;overflow:hidden}
  @media(max-width:560px){.dk-postmark{right:-4px;top:-16px;width:94px;height:94px}}
  @media(min-width:880px){.dk-hero{grid-template-columns:1.15fr 1fr}}
  .dk-big{font-size:clamp(2.6rem,7vw,5.6rem);line-height:1.02}
  .dk-hindi{font-size:clamp(1rem,2vw,1.3rem);color:#0e7490;font-weight:700;letter-spacing:.2em}
  .dk-stamp{position:relative;background:#fff;padding:14px;
    -webkit-mask:radial-gradient(9px at 9px 9px,#0000 97%,#000) -9px -9px/18px 18px, linear-gradient(#000 0 0) content-box;
    mask:radial-gradient(9px at 9px 9px,#0000 97%,#000) -9px -9px/18px 18px, linear-gradient(#000 0 0) content-box;
    filter:drop-shadow(0 14px 22px rgba(58,36,24,.28))}
  .dk-stamp-in{border:3px solid #0e7490;padding:1.4rem;text-align:center;background:linear-gradient(180deg,#fdfaf2,#f4ecd9)}
  .dk-postmark{position:absolute;top:-26px;right:-22px;width:118px;height:118px;border:2.5px solid #3a2418;border-radius:999px;
    display:flex;align-items:center;justify-content:center;text-align:center;font-size:.6rem;font-weight:700;line-height:1.3;
    letter-spacing:.14em;text-transform:uppercase;color:#3a2418;opacity:.75;transform:rotate(-14deg);mix-blend-mode:multiply;
    background:radial-gradient(circle,transparent 58%,rgba(58,36,24,.06) 60%);animation:dk-wob 6s ease-in-out infinite;z-index:5}
  @keyframes dk-wob{50%{transform:rotate(-9deg)}}
  .dk-cancel{position:absolute;left:-8%;top:38%;width:116%;opacity:.5;pointer-events:none;z-index:4}
  .dk-band{overflow:hidden;background:#d81b60;color:#f7f0e1;padding:.75rem 0;transform:rotate(-1deg) scale(1.03)}
  .dk-band>div{display:flex;white-space:nowrap;font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:.85rem;
    animation:dk-mv 22s linear infinite}
  @keyframes dk-mv{to{transform:translateX(-50%)}}
  .dk-grid{max-width:72rem;margin:0 auto;padding:4.5rem 1.25rem;display:grid;gap:2.6rem;grid-template-columns:repeat(auto-fit,minmax(255px,1fr))}
  .dk-card{background:#fff;padding:12px;
    -webkit-mask:radial-gradient(8px at 8px 8px,#0000 97%,#000) -8px -8px/16px 16px, linear-gradient(#000 0 0) content-box;
    mask:radial-gradient(8px at 8px 8px,#0000 97%,#000) -8px -8px/16px 16px, linear-gradient(#000 0 0) content-box;
    filter:drop-shadow(0 12px 20px rgba(58,36,24,.22));transition:transform .35s cubic-bezier(.22,.8,.26,1)}
  .dk-card:hover{transform:translateY(-6px) rotate(-.6deg)}
  .dk-card-in{border:2.5px solid var(--c);padding:1.2rem;text-align:center;height:100%;
    background:linear-gradient(180deg,#fdfaf2,#f6efdd)}
  .dk-den{display:flex;justify-content:space-between;font-weight:800;font-size:.8rem;letter-spacing:.1em;color:#3a2418;opacity:.75}
  .dk-role{font-size:.72rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--c);margin-top:.6rem}
  .dk-name{font-family:'Rozha One',serif;font-size:1.7rem;margin:.15rem 0 .4rem}
  .dk-ing{font-size:.8rem;line-height:1.55;color:#3a2418;opacity:.72;min-height:3.4em}
  .dk-fl{display:inline-block;background:var(--c);color:#fff;border-radius:999px;padding:.25rem .8rem;font-size:.75rem;font-weight:700;margin:.55rem 0}
  .dk-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.6rem}
  .dk-price{font-family:'Rozha One',serif;font-size:1.5rem}
  .dk-add{border:0;background:#3a2418;color:#f7f0e1;border-radius:999px;padding:.6rem 1.2rem;font-weight:700;cursor:pointer;
    transition:transform .2s}
  .dk-add:active{transform:scale(.94)}
  .dk-foot{text-align:center;padding:3.4rem 1rem;color:#3a2418;opacity:.65;font-size:.9rem}
 ''',
 body='''
<div id="pkc" style="background:#d81b60"></div>
<nav class="dk-nav"><b class="dk-disp" style="font-size:1.35rem">GummyChums <span class="dk-acc">डाक</span></b>
  <button class="cart-trigger dk-bag" data-hot>Bag <span class="cart-count" style="display:none;background:#d81b60;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="dk-hero">
  <div>
    <p class="dk-hindi">डाक घर · FIRST-CLASS WELLNESS</p>
    <h1 class="dk-disp dk-big pk-chars">Good health,<br/>hand-delivered.</h1>
    <p style="max-width:26rem;margin-top:1.2rem;opacity:.75;line-height:1.7">Three little stamps of science — brain, sleep and eyes — posted daily from an FSSAI-certified lab to your doorstep. No added sugar. Full added joy.</p>
    <a href="#shelf" data-hot style="display:inline-block;margin-top:1.6rem;background:#d81b60;color:#fff;font-weight:700;border-radius:999px;padding:1rem 2.1rem;box-shadow:0 12px 24px -10px rgba(216,27,96,.5)">Open the post ↓</a>
  </div>
  <div class="dk-stamp" data-scrub style="transform:rotate(2deg) translateY(calc((1 - var(--p)) * 26px))">
    <div class="dk-stamp-in">
      <div class="dk-den"><span>भारत</span><span>₹ prepaid</span></div>
      '''+gummy('#d81b60','width:56%;margin:1rem auto')+'''
      <div class="dk-disp" style="font-size:1.6rem">GummyChums</div>
      <div style="font-size:.75rem;letter-spacing:.25em;font-weight:700;opacity:.65">MADE IN INDIA · EST. 2026</div>
    </div>
    <svg class="dk-cancel" viewBox="0 0 300 40"><path d="M0 8 Q 40 0 80 8 T 160 8 T 240 8 T 320 8 M0 20 Q 40 12 80 20 T 160 20 T 240 20 T 320 20 M0 32 Q 40 24 80 32 T 160 32 T 240 32 T 320 32" stroke="#3a2418" stroke-width="2" fill="none" opacity=".55"/></svg>
    <div class="dk-postmark">GummyChums<br/>· daily post ·<br/>2026</div>
  </div>
</header>
<div style="overflow:hidden"><div class="dk-band"><div><span style="padding:0 2rem">Registered wellness ✦ No added sugar ✦ FSSAI certified ✦ 100% vegetarian ✦ डाक से सीधा ✦ Registered wellness ✦ No added sugar ✦ FSSAI certified ✦ 100% vegetarian ✦ डाक से सीधा ✦</span><span style="padding:0 2rem">Registered wellness ✦ No added sugar ✦ FSSAI certified ✦ 100% vegetarian ✦ डाक से सीधा ✦ Registered wellness ✦ No added sugar ✦ FSSAI certified ✦ 100% vegetarian ✦ डाक से सीधा ✦</span></div></div></div>
<section id="shelf" class="dk-grid">'''+cards('''
  <article class="dk-card" data-pdp="{pdp}" style="--c:{color}">
    <div class="dk-card-in">
      <div class="dk-den"><span>भारत</span><span>{price}</span></div>
      <div class="dk-role">{role}</div>
      <div class="dk-name">{name}</div>
      {gum}
      <span class="dk-fl">{flavour} flavour</span>
      <p class="dk-ing">{ing}</p>
      <div class="dk-buy"><span class="dk-price">{price}</span>
      <button class="add-to-cart-btn dk-add" data-product-id="{id}">Post it</button></div>
    </div>
  </article>''')+'''</section>
<footer class="dk-foot">GummyChums · sorted, stamped &amp; sent with love · Made in India</footer>
'''))

# ==================================================================== 26 MAACHIS
THEMES.append(dict(
 file='index26.html', title='GummyChums — Maachis',
 body_class='mb-mx',
 fonts='<link href="https://fonts.googleapis.com/css2?family=Bevan&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet"/>',
 css='''
  body.mb-mx{background:#f3e6c9;color:#2b1608;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:repeating-linear-gradient(45deg,rgba(43,22,8,.03) 0 2px,transparent 2px 14px)}
  .mx-disp{font-family:Bevan,serif}
  .mx-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
    padding:.9rem 1.4rem;background:#b3261e;color:#f3e6c9;box-shadow:0 4px 14px -6px rgba(43,22,8,.5)}
  .mx-bag{border:2px solid #f3e6c9;background:transparent;color:#f3e6c9;border-radius:6px;padding:.5rem 1.1rem;font-weight:700;cursor:pointer}
  .mx-hero{max-width:70rem;margin:0 auto;padding:5rem 1.25rem 4rem;text-align:center}
  .mx-big{font-size:clamp(2.4rem,7vw,5.4rem);line-height:1.05;color:#b3261e;text-shadow:2px 2px 0 rgba(212,160,23,.55)}
  .mx-sub{max-width:30rem;margin:1.2rem auto 0;opacity:.78;line-height:1.7}
  .mx-grid{max-width:74rem;margin:0 auto;padding:4rem 1.25rem 5rem;display:grid;gap:2.4rem;grid-template-columns:repeat(auto-fit,minmax(268px,1fr))}
  .mx-box{position:relative;perspective:900px}
  .mx-tray{position:relative;background:#fdf3da;border:3px solid #2b1608;box-shadow:6px 8px 0 #2b1608,0 18px 30px -14px rgba(43,22,8,.5);
    padding:1.1rem;z-index:2;transition:transform .5s cubic-bezier(.22,.8,.26,1)}
  .mx-label{border:2px solid var(--c);outline:2px dashed rgba(43,22,8,.35);outline-offset:-9px;padding:1.3rem 1rem;text-align:center;
    background:radial-gradient(circle at 50% 24%,#fff8e6,#f7e9c6)}
  .mx-strike{position:absolute;left:10px;right:10px;bottom:-12px;height:14px;z-index:1;border:2px solid #2b1608;
    background:repeating-linear-gradient(90deg,#5c4030 0 6px,#3e2a1c 6px 12px)}
  .mx-drawer{position:absolute;inset:12px;background:#e9d7a8;border:2px solid #2b1608;z-index:1;display:flex;align-items:center;
    justify-content:center;gap:8px;transform:translateX(0);transition:transform .55s cubic-bezier(.22,.8,.26,1)}
  .mx-box:hover .mx-drawer{transform:translateX(34%)}
  .mx-box:hover .mx-tray{transform:translateX(-6%) rotate(-1.2deg)}
  .mx-flare{position:absolute;right:-6px;top:34%;width:22px;height:22px;border-radius:999px;background:radial-gradient(circle,#ffd23f,#e8641b 70%,transparent 72%);
    opacity:0;transform:scale(.3);transition:opacity .3s,transform .45s cubic-bezier(.34,1.56,.64,1)}
  .mx-box:hover .mx-flare{opacity:1;transform:scale(1.25)}
  .mx-role{font-size:.7rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:var(--c)}
  .mx-name{font-family:Bevan,serif;font-size:1.45rem;margin:.3rem 0 .5rem;color:#2b1608}
  .mx-ing{font-size:.78rem;line-height:1.55;opacity:.72;min-height:3.4em}
  .mx-fl{display:inline-block;border:2px solid var(--c);color:var(--c);border-radius:4px;padding:.2rem .7rem;font-size:.72rem;
    font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin:.5rem 0}
  .mx-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.5rem}
  .mx-price{font-family:Bevan,serif;font-size:1.35rem;color:#b3261e}
  .mx-add{border:2px solid #2b1608;background:#d4a017;color:#2b1608;border-radius:6px;padding:.55rem 1.1rem;font-weight:800;
    cursor:pointer;box-shadow:3px 3px 0 #2b1608;transition:transform .15s,box-shadow .15s}
  .mx-add:active{transform:translate(3px,3px);box-shadow:0 0 0 #2b1608}
  .mx-band{overflow:hidden;background:#2b1608;color:#d4a017;padding:.8rem 0}
  .mx-band>div{display:flex;white-space:nowrap;font-family:Bevan,serif;font-size:1rem;letter-spacing:.14em;animation:mx-mv 24s linear infinite}
  @keyframes mx-mv{to{transform:translateX(-50%)}}
  .mx-foot{text-align:center;padding:3.2rem 1rem;opacity:.65;font-size:.9rem}
 ''',
 body='''
<div id="pkc" style="background:#b3261e"></div>
<nav class="mx-nav"><b class="mx-disp" style="font-size:1.2rem">GUMMYCHUMS MAACHIS CO.</b>
  <button class="cart-trigger mx-bag" data-hot>BAG <span class="cart-count" style="display:none;background:#d4a017;color:#2b1608;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="mx-hero">
  <p style="letter-spacing:.3em;font-weight:700;font-size:.8rem;opacity:.6">SINCE 2026 · AVERAGE CONTENTS 15/30/45</p>
  <h1 class="mx-disp mx-big pk-chars">STRIKE UP YOUR HEALTH</h1>
  <p class="mx-sub">Vintage matchbox spirit, modern lab science. Slide a box open — brain, sleep or eyes — and light up your daily routine. <b>No added sugar.</b></p>
  <a href="#boxes" data-hot style="display:inline-block;margin-top:1.5rem;background:#b3261e;color:#f3e6c9;font-weight:800;border:3px solid #2b1608;box-shadow:4px 4px 0 #2b1608;padding:.95rem 2rem">OPEN A BOX ↓</a>
</header>
<div class="mx-band"><div><span style="padding:0 1.6rem">SAFETY WELLNESS ✦ MADE IN INDIA ✦ STRIKES EVERY TIME ✦ 100% VEG ✦</span><span style="padding:0 1.6rem">SAFETY WELLNESS ✦ MADE IN INDIA ✦ STRIKES EVERY TIME ✦ 100% VEG ✦</span><span style="padding:0 1.6rem">SAFETY WELLNESS ✦ MADE IN INDIA ✦ STRIKES EVERY TIME ✦ 100% VEG ✦</span></div></div>
<section id="boxes" class="mx-grid">'''+cards('''
  <article class="mx-box" data-pdp="{pdp}" style="--c:{color}">
    <div class="mx-drawer">'''+gummy('{color}','width:34px')+gummy('{color}','width:34px')+gummy('{color}','width:34px')+'''</div>
    <div class="mx-tray"><div class="mx-label">
      <div class="mx-role">{role}</div>
      <div class="mx-name">{name}</div>
      {gum}
      <span class="mx-fl">{flavour}</span>
      <p class="mx-ing">{ing}</p>
      <div class="mx-buy"><span class="mx-price">{price}</span>
      <button class="add-to-cart-btn mx-add" data-product-id="{id}">STRIKE</button></div>
    </div></div>
    <div class="mx-strike"></div><div class="mx-flare"></div>
  </article>''')+'''</section>
<footer class="mx-foot">GummyChums Maachis Co. · keep away from boring routines · Made in India</footer>
'''))

# ==================================================================== 27 KIRANA
THEMES.append(dict(
 file='index27.html', title='GummyChums — Kirana',
 body_class='mb-ki',
 fonts='<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Kalam:wght@700&display=swap" rel="stylesheet"/>',
 css='''
  body.mb-ki{background:#fbf3e4;color:#4a2c14;font-family:'Baloo 2',cursive;overflow-x:hidden}
  .ki-hand{font-family:Kalam,cursive}
  .ki-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;padding:.9rem 1.4rem;
    background:rgba(251,243,228,.94);backdrop-filter:blur(8px);box-shadow:0 1px 0 rgba(74,44,20,.14)}
  .ki-bag{border:0;background:#e8641b;color:#fff;border-radius:999px;padding:.55rem 1.25rem;font-weight:800;cursor:pointer;
    box-shadow:0 8px 18px -8px rgba(232,100,27,.6)}
  .ki-check{height:26px;background:repeating-conic-gradient(#f3d9b1 0 25%,#e8641b 0 50%) 0 0/26px 26px;opacity:.85}
  .ki-hero{max-width:72rem;margin:0 auto;padding:4.6rem 1.25rem 3rem;text-align:center}
  .ki-big{font-size:clamp(2.5rem,7vw,5.2rem);line-height:1;font-weight:800;color:#e8641b}
  .ki-big span{color:#0d6b45}
  .ki-shelfwrap{max-width:74rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
  .ki-shelf{display:grid;gap:2.4rem;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));position:relative;padding-bottom:26px}
  .ki-shelf::after{content:"";position:absolute;left:-14px;right:-14px;bottom:0;height:16px;border-radius:8px;
    background:linear-gradient(180deg,#c98a4b,#a96f36);box-shadow:0 10px 18px -8px rgba(74,44,20,.5)}
  .ki-pouch{position:relative;background:linear-gradient(115deg,#fff 0%,var(--soft) 55%,#fff 100%);
    border-radius:18px;padding:2rem 1.2rem 1.4rem;text-align:center;
    box-shadow:0 16px 28px -16px rgba(74,44,20,.4), inset 0 0 0 1px rgba(74,44,20,.08);
    transition:transform .35s cubic-bezier(.34,1.56,.64,1)}
  .ki-pouch:hover{transform:translateY(-8px) rotate(-.8deg)}
  .ki-pouch::before,.ki-pouch::after{content:"";position:absolute;left:0;right:0;height:12px;
    background:repeating-linear-gradient(90deg,var(--c) 0 7px,transparent 7px 14px);opacity:.85}
  .ki-pouch::before{top:0;border-radius:18px 18px 0 0;clip-path:polygon(0 0,100% 0,100% 55%,0 55%)}
  .ki-pouch::after{bottom:0;border-radius:0 0 18px 18px;clip-path:polygon(0 45%,100% 45%,100% 100%,0 100%)}
  .ki-sheen{position:absolute;top:0;bottom:0;left:18%;width:14%;background:linear-gradient(105deg,transparent,rgba(255,255,255,.6),transparent);pointer-events:none}
  .ki-tag{position:absolute;top:-14px;right:-10px;background:#fffbe8;border-radius:6px;padding:.35rem .7rem;font-family:Kalam,cursive;
    font-size:1rem;color:#b3261e;transform:rotate(8deg);box-shadow:0 6px 12px -6px rgba(74,44,20,.45);z-index:3}
  .ki-tag::before{content:"";position:absolute;left:-7px;top:9px;width:8px;height:8px;border-radius:99px;background:#b3261e}
  .ki-role{font-size:.72rem;font-weight:800;letter-spacing:.22em;text-transform:uppercase;color:var(--c)}
  .ki-name{font-weight:800;font-size:1.5rem;margin:.15rem 0 .3rem}
  .ki-ing{font-size:.8rem;line-height:1.5;opacity:.72;min-height:3.2em;font-family:Poppins,system-ui,sans-serif}
  .ki-fl{display:inline-block;background:var(--c);color:#fff;border-radius:999px;padding:.22rem .8rem;font-size:.75rem;font-weight:800;margin:.45rem 0}
  .ki-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.55rem}
  .ki-price{font-weight:800;font-size:1.35rem;color:#0d6b45}
  .ki-add{border:0;background:#4a2c14;color:#fbf3e4;border-radius:999px;padding:.55rem 1.15rem;font-weight:800;cursor:pointer;transition:transform .18s}
  .ki-add:active{transform:scale(.93)}
  .ki-foot{text-align:center;padding:3.2rem 1rem;opacity:.65;font-size:.9rem}
 ''',
 body='''
<div id="pkc" style="background:#e8641b"></div>
<nav class="ki-nav"><b style="font-size:1.3rem;font-weight:800">GummyChums <span class="ki-hand" style="color:#e8641b">किराना</span></b>
  <button class="cart-trigger ki-bag" data-hot>Thela <span class="cart-count" style="display:none;background:#fff;color:#e8641b;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<div class="ki-check"></div>
<header class="ki-hero">
  <p class="ki-hand" style="font-size:1.15rem;color:#0d6b45">आपकी सेहत की दुकान</p>
  <h1 class="ki-big pk-chars">The corner shop <span>of wellness.</span></h1>
  <p style="max-width:28rem;margin:1rem auto 0;opacity:.75;line-height:1.7;font-family:Poppins,sans-serif">Fresh pillow pouches on the shelf — brain, sleep, eyes. Straight from the lab sheet, honest as your neighbourhood kirana. No added sugar.</p>
  <a href="#shelf" data-hot style="display:inline-block;margin-top:1.4rem;background:#e8641b;color:#fff;font-weight:800;border-radius:999px;padding:.95rem 2.1rem;box-shadow:0 12px 24px -10px rgba(232,100,27,.55)">Browse the shelf ↓</a>
</header>
<div class="ki-shelfwrap"><section id="shelf" class="ki-shelf">'''+cards('''
  <article class="ki-pouch" data-pdp="{pdp}" style="--c:{color};--soft:{color}22">
    <span class="ki-sheen"></span>
    <span class="ki-tag">{price}/-</span>
    <div class="ki-role">{role}</div>
    <div class="ki-name">{name}</div>
    {gum}
    <span class="ki-fl">{flavour} · pillow pouch</span>
    <p class="ki-ing">{ing}</p>
    <div class="ki-buy"><span class="ki-price">{price}</span>
    <button class="add-to-cart-btn ki-add" data-product-id="{id}">Add to thela</button></div>
  </article>''')+'''</section></div>
<div class="ki-check"></div>
<footer class="ki-foot">GummyChums Kirana · उधार बंद है, सेहत चालू है · Made in India</footer>
'''))

# ==================================================================== 28 KALA POP
THEMES.append(dict(
 file='index28.html', title='GummyChums — Kala Pop',
 body_class='mb-kp',
 fonts='<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Poppins:wght@400;600;700&family=Kalam:wght@700&display=swap" rel="stylesheet"/>',
 css='''
  body.mb-kp{background:#1a3fb3;color:#fdf6e3;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:radial-gradient(rgba(253,246,227,.06) 1.5px,transparent 1.5px);background-size:30px 30px}
  .kp-disp{font-family:'Alfa Slab One',serif;letter-spacing:.01em}
  .kp-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;padding:.9rem 1.4rem;
    background:rgba(26,63,179,.9);backdrop-filter:blur(8px);box-shadow:0 1px 0 rgba(253,246,227,.18)}
  .kp-bag{border:2px solid #fdf6e3;background:transparent;color:#fdf6e3;border-radius:999px;padding:.5rem 1.15rem;font-weight:700;cursor:pointer}
  .kp-hero{position:relative;max-width:72rem;margin:0 auto;padding:5rem 1.25rem 4rem;text-align:center;overflow:hidden}
  .kp-burst{position:absolute;left:50%;top:52%;width:130vmin;height:130vmin;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(rgba(253,246,227,.09) 0 7deg,transparent 7deg 14deg);border-radius:999px;
    animation:kp-spin 60s linear infinite;pointer-events:none}
  @keyframes kp-spin{to{transform:translate(-50%,-50%) rotate(360deg)}}
  .kp-arch{position:relative;display:inline-block;background:#e91e8c;border-radius:260px 260px 22px 22px;
    padding:3rem 2.4rem 2rem;box-shadow:0 0 0 6px #fdf6e3, 0 0 0 10px #e91e8c, 0 26px 46px -18px rgba(0,0,0,.55)}
  .kp-big{font-size:clamp(2rem,6vw,4rem);line-height:1.08;color:#fdf6e3;text-shadow:3px 3px 0 rgba(26,63,179,.6)}
  .kp-hindi{font-family:Kalam,cursive;color:#ffd23f;font-size:clamp(1rem,2.4vw,1.5rem);margin-top:.6rem}
  .kp-scal{height:22px;margin:3.2rem 0 0;background:radial-gradient(circle 14px at 14px 0,#e91e8c 98%,transparent) 0 0/28px 22px}
  .kp-grid{max-width:74rem;margin:0 auto;padding:4.2rem 1.25rem 5rem;display:grid;gap:2.4rem;grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
  .kp-label{position:relative;background:#fdf6e3;color:#22284a;border-radius:150px 150px 16px 16px;padding:2.4rem 1.3rem 1.4rem;
    text-align:center;box-shadow:inset 0 0 0 3px #1a3fb3, inset 0 0 0 7px #fdf6e3, inset 0 0 0 9px var(--c),
    0 20px 34px -18px rgba(0,0,0,.55);transition:transform .35s cubic-bezier(.22,.8,.26,1)}
  .kp-label:hover{transform:translateY(-8px) rotate(.6deg)}
  .kp-role{font-size:.7rem;font-weight:800;letter-spacing:.26em;text-transform:uppercase;color:var(--c)}
  .kp-name{font-family:'Alfa Slab One',serif;font-size:1.45rem;margin:.25rem 0 .45rem}
  .kp-ing{font-size:.78rem;line-height:1.55;opacity:.75;min-height:3.4em}
  .kp-fl{display:inline-block;background:var(--c);color:#fff;border-radius:999px;padding:.24rem .85rem;font-size:.74rem;font-weight:800;margin:.5rem 0}
  .kp-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.55rem}
  .kp-price{font-family:'Alfa Slab One',serif;font-size:1.3rem;color:#e91e8c}
  .kp-add{border:0;background:#1a3fb3;color:#fdf6e3;border-radius:999px;padding:.6rem 1.2rem;font-weight:800;cursor:pointer;transition:transform .18s}
  .kp-add:active{transform:scale(.93)}
  .kp-band{overflow:hidden;background:#e91e8c;color:#fdf6e3;padding:.75rem 0}
  .kp-band>div{display:flex;white-space:nowrap;font-family:'Alfa Slab One',serif;font-size:.95rem;letter-spacing:.12em;animation:kp-mv 22s linear infinite}
  @keyframes kp-mv{to{transform:translateX(-50%)}}
  .kp-foot{text-align:center;padding:3.2rem 1rem;opacity:.7;font-size:.9rem}
 ''',
 body='''
<div id="pkc" class="blend-screen" style="background:#ffd23f"></div>
<nav class="kp-nav"><b class="kp-disp" style="font-size:1.15rem">GUMMY<span style="color:#ffd23f">POP</span></b>
  <button class="cart-trigger kp-bag" data-hot>Bag <span class="cart-count" style="display:none;background:#ffd23f;color:#1a3fb3;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="kp-hero">
  <div class="kp-burst"></div>
  <div class="kp-arch" data-scrub style="transform:translateY(calc((1 - var(--p)) * 20px))">
    <h1 class="kp-disp kp-big pk-chars">ICONIC HEALTH POP</h1>
    <div class="kp-hindi">असली स्वाद · असली साइंस</div>
    <p style="max-width:24rem;margin:1rem auto 0;font-size:.95rem;opacity:.9">Three bottled-up benefits — brain, sleep, eyes — uncapped daily. Spiced with mango, cherry &amp; orange. Zero added sugar.</p>
    <a href="#labels" data-hot style="display:inline-block;margin-top:1.3rem;background:#fdf6e3;color:#e91e8c;font-weight:800;border-radius:999px;padding:.9rem 2rem">POP ONE OPEN ↓</a>
  </div>
  <div class="kp-scal"></div>
</header>
<div class="kp-band"><div><span style="padding:0 1.6rem">KALA POP ✦ देसी GUMMY ✦ NO ADDED SUGAR ✦ MADE IN INDIA ✦</span><span style="padding:0 1.6rem">KALA POP ✦ देसी GUMMY ✦ NO ADDED SUGAR ✦ MADE IN INDIA ✦</span><span style="padding:0 1.6rem">KALA POP ✦ देसी GUMMY ✦ NO ADDED SUGAR ✦ MADE IN INDIA ✦</span></div></div>
<section id="labels" class="kp-grid">'''+cards('''
  <article class="kp-label" data-pdp="{pdp}" style="--c:{color}">
    <div class="kp-role">{role}</div>
    <div class="kp-name">{name}</div>
    {gum}
    <span class="kp-fl">{flavour} POP</span>
    <p class="kp-ing">{ing}</p>
    <div class="kp-buy"><span class="kp-price">{price}</span>
    <button class="add-to-cart-btn kp-add" data-product-id="{id}">UNCAP</button></div>
  </article>''')+'''</section>
<footer class="kp-foot">GummyChums Kala Pop · bottled joy since 2026 · Made in India</footer>
'''))

# ==================================================================== 29 TIN BAGH
THEMES.append(dict(
 file='index29.html', title='GummyChums — Tin Bagh',
 body_class='mb-tb',
 fonts='<link href="https://fonts.googleapis.com/css2?family=Prata&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet"/>',
 css='''
  body.mb-tb{background:#0d6b45;color:#f5ecd7;font-family:Poppins,sans-serif;overflow-x:hidden;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='84' height='84'%3E%3Cg fill='none' stroke='%23f5ecd7' stroke-opacity='.12' stroke-width='2'%3E%3Cellipse cx='42' cy='24' rx='7' ry='13'/%3E%3Cellipse cx='42' cy='60' rx='7' ry='13'/%3E%3Cellipse cx='24' cy='42' rx='13' ry='7'/%3E%3Cellipse cx='60' cy='42' rx='13' ry='7'/%3E%3C/g%3E%3Ccircle cx='42' cy='42' r='4' fill='%23f5ecd7' fill-opacity='.16'/%3E%3Ccircle cx='0' cy='0' r='2.5' fill='%23f5ecd7' fill-opacity='.12'/%3E%3Ccircle cx='84' cy='0' r='2.5' fill='%23f5ecd7' fill-opacity='.12'/%3E%3Ccircle cx='0' cy='84' r='2.5' fill='%23f5ecd7' fill-opacity='.12'/%3E%3Ccircle cx='84' cy='84' r='2.5' fill='%23f5ecd7' fill-opacity='.12'/%3E%3C/svg%3E")}
  .tb-disp{font-family:Prata,serif}
  .tb-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;padding:.9rem 1.4rem;
    background:rgba(13,107,69,.92);backdrop-filter:blur(8px);box-shadow:0 1px 0 rgba(245,236,215,.2)}
  .tb-bag{border:1.5px solid #f5ecd7;background:transparent;color:#f5ecd7;border-radius:999px;padding:.5rem 1.15rem;font-weight:700;cursor:pointer}
  .tb-hero{max-width:72rem;margin:0 auto;padding:5rem 1.25rem 4rem;display:grid;gap:2.6rem;align-items:center}
  @media(min-width:880px){.tb-hero{grid-template-columns:1.1fr 1fr}}
  .tb-big{font-size:clamp(2.4rem,6.4vw,4.8rem);line-height:1.08}
  .tb-big i{color:#e8b64c;font-style:italic}
  .tb-ped{position:relative;text-align:center}
  .tb-cyl{width:min(64%,270px);margin:0 auto;height:74px;border-radius:50%/28px;
    background:linear-gradient(180deg,#f5ecd7,#d9c9a4);box-shadow:0 22px 34px -16px rgba(0,0,0,.55)}
  .tb-trio{display:flex;justify-content:center;gap:-10px;margin-bottom:-26px;position:relative;z-index:2}
  .tb-trio>div{width:96px;filter:drop-shadow(0 14px 16px rgba(0,0,0,.4));animation:tb-flo 6s ease-in-out infinite}
  .tb-trio>div:nth-child(2){animation-delay:.6s;margin:0 -14px;transform:translateY(-14px)}
  .tb-trio>div:nth-child(3){animation-delay:1.2s}
  @keyframes tb-flo{50%{transform:translateY(-12px)}}
  .tb-grid{max-width:74rem;margin:0 auto;padding:4.2rem 1.25rem 5rem;display:grid;gap:2.4rem;grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
  .tb-tin{position:relative;border-radius:20px;padding:5px;
    background:linear-gradient(135deg,#e8b64c 0%,#f7e5b5 22%,#b98a2e 48%,#f2dfae 74%,#cfa03c 100%);
    box-shadow:0 22px 36px -18px rgba(0,0,0,.6);transition:transform .4s cubic-bezier(.22,.8,.26,1)}
  .tb-tin:hover{transform:translateY(-8px)}
  .tb-tin-in{position:relative;border-radius:16px;background:#f5ecd7;color:#243a2d;padding:1.6rem 1.2rem 1.3rem;text-align:center;
    box-shadow:inset 0 2px 6px rgba(255,255,255,.8), inset 0 -8px 16px rgba(36,58,45,.14);overflow:hidden}
  .tb-shine{position:absolute;top:0;bottom:0;left:-40%;width:34%;transform:skewX(-18deg);
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);transition:left .8s cubic-bezier(.22,.8,.26,1)}
  .tb-tin:hover .tb-shine{left:118%}
  .tb-role{font-size:.7rem;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:#0d6b45}
  .tb-name{font-family:Prata,serif;font-size:1.5rem;margin:.25rem 0 .45rem}
  .tb-ing{font-size:.78rem;line-height:1.55;opacity:.75;min-height:3.4em}
  .tb-fl{display:inline-block;background:#c62828;color:#fff;border-radius:999px;padding:.22rem .8rem;font-size:.74rem;font-weight:700;margin:.5rem 0}
  .tb-buy{display:flex;justify-content:space-between;align-items:center;margin-top:.55rem}
  .tb-price{font-family:Prata,serif;font-size:1.35rem;color:#c62828}
  .tb-add{border:0;background:#0d6b45;color:#f5ecd7;border-radius:999px;padding:.6rem 1.2rem;font-weight:700;cursor:pointer;transition:transform .18s}
  .tb-add:active{transform:scale(.93)}
  .tb-foot{text-align:center;padding:3.2rem 1rem;opacity:.7;font-size:.9rem}
 ''',
 body='''
<div id="pkc" class="blend-screen" style="background:#e8b64c"></div>
<nav class="tb-nav"><b class="tb-disp" style="font-size:1.25rem">GummyChums · Tin Bagh</b>
  <button class="cart-trigger tb-bag" data-hot>Bag <span class="cart-count" style="display:none;background:#e8b64c;color:#243a2d;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>
<header class="tb-hero">
  <div>
    <p style="letter-spacing:.32em;font-weight:700;font-size:.78rem;color:#e8b64c">THE FAMILY TIN · EST. 2026</p>
    <h1 class="tb-disp tb-big pk-chars">Grandma&rsquo;s tin,<br/><i>reinvented.</i></h1>
    <p style="max-width:26rem;margin-top:1.2rem;opacity:.82;line-height:1.75">The biscuit tin every Indian home hides on the top shelf — now filled with lab-tested wellness. Brain, sleep and eye care in mango, cherry and orange. No added sugar, all added nostalgia.</p>
    <a href="#tins" data-hot style="display:inline-block;margin-top:1.6rem;background:#e8b64c;color:#243a2d;font-weight:800;border-radius:999px;padding:1rem 2.1rem;box-shadow:0 14px 26px -10px rgba(0,0,0,.5)">Open the tin ↓</a>
  </div>
  <div class="tb-ped" data-scrub style="transform:translateY(calc((1 - var(--p)) * 22px))">
    <div class="tb-trio"><div>'''+gummy('#e44bd3')+'''</div><div>'''+gummy('#8b5cf6')+'''</div><div>'''+gummy('#38bdf8')+'''</div></div>
    <div class="tb-cyl"></div>
  </div>
</header>
<section id="tins" class="tb-grid">'''+cards('''
  <article class="tb-tin" data-pdp="{pdp}">
    <div class="tb-tin-in"><span class="tb-shine"></span>
      <div class="tb-role">{role}</div>
      <div class="tb-name">{name}</div>
      {gum}
      <span class="tb-fl">{flavour} flavour</span>
      <p class="tb-ing">{ing}</p>
      <div class="tb-buy"><span class="tb-price">{price}</span>
      <button class="add-to-cart-btn tb-add" data-product-id="{id}">Keep the tin</button></div>
    </div>
  </article>''')+'''</section>
<footer class="tb-foot">GummyChums Tin Bagh · the tin you&rsquo;re actually allowed to open · Made in India</footer>
'''))

if __name__ == '__main__':
    shared = extract_shared()
    for t in THEMES:
        html = page(t, *shared)
        open(os.path.join(ROOT, t['file']), 'w', encoding='utf-8').write(html)
        print('wrote', t['file'], len(html), 'bytes')
