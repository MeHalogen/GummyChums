# -*- coding: utf-8 -*-
"""
GummyChums themed-PDP factory.

Generates one product-detail page per (premium theme x product) so that
opening a product from any premium design keeps that design's UI:
  p15-dreamy-sleep.html ... p24-neon-violet.html   (10 themes x 3 products)

Also patches index15-24 in place so the WHOLE product card is clickable
(-> that theme's own PDP) instead of a small "View product page" link.

Shared pieces (bill/checkout HTML+JS, premium motion kit CSS/JS, reveal
failsafe) are EXTRACTED from the existing built product-dreamy-sleep.html,
so the receipt stays byte-identical everywhere. Run from repo root:
  python3 tools/build_pdps.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- data
PDP_DATA = [
 dict(id='dreamy-sleep', name='Dreamy Sleep Gummies', color='#8b5cf6', soft='#efe6ff',
   tag='Sleep &amp; Calm · 30 gummies · Blueberry Lavender', price='₹699', mrp='₹899', off='22% off',
   rating='4.8', ratings='1,284', line='For nights when your brain won&rsquo;t log off.',
   ing=[('Melatonin','5 mg','Signals your body clock that it&rsquo;s time to wind down'),
        ('Chamomile extract','120 mg','The classic calming herb, in one soft chew'),
        ('L-Theanine','50 mg','Smooths the racing 3am thoughts')],
   moments=['after a long workday','before a red-eye flight','when tomorrow is a big day','to build a consistent sleep ritual'],
   faq=[('When should I take it?','One gummy, 30–45 minutes before you want to sleep. No water needed.'),
        ('Will it make me groggy?','It is formulated for a gentle wind-down, not sedation. Most chums wake up feeling refreshed.'),
        ('Is it vegetarian?','Yes — 100% vegetarian, pectin-based, no gelatin. No artificial colours either.')],
   reviews=[('Ananya K. · Mumbai','Tastes like a treat, works like a ritual. I actually look forward to bedtime now.'),
            ('Rahul V. · Bengaluru','Replaced my alarm-scroll-anxiety loop with one gummy. Three weeks consistent — a record.'),
            ('Ishita R. · Pune','The blueberry lavender flavour is genuinely good. Not medicine-y at all.')]),
 dict(id='electric-blue', name='Electric Blue Gummies', color='#38bdf8', soft='#e0f3ff',
   tag='Eyes &amp; Focus · 30 gummies · Blue Raspberry', price='₹749', mrp='₹949', off='21% off',
   rating='4.7', ratings='976', line='For the 10-hour screen marathon.',
   ing=[('Lutein','10 mg','The screen-day carotenoid your eyes love'),
        ('Zeaxanthin','2 mg','Lutein&rsquo;s partner for blue-light-heavy days'),
        ('Vitamin B12','2.2 mcg','Steady, jitter-free energy support')],
   moments=['exam-prep marathons','back-to-back meetings','long coding or design sprints','gaming nights'],
   faq=[('When should I take it?','One gummy with breakfast, or before your longest screen stretch.'),
        ('Does it replace glasses/breaks?','No — it supports eye comfort. Keep taking screen breaks; we&rsquo;ll handle the snack part.'),
        ('Is it vegetarian?','Yes — 100% vegetarian and made in an FSSAI-certified facility.')],
   reviews=[('Karan M. · Hyderabad','I stare at terminals 12 hours a day. These are now part of the desk setup.'),
            ('Sneha T. · Delhi','Bought for my UPSC prep. The one supplement I have not forgotten to take.'),
            ('Aditya B. · Gurgaon','Blue raspberry that does not taste artificial. Impressive.')]),
 dict(id='neon-violet', name='Neon Violet Gummies', color='#e44bd3', soft='#ffe3f8',
   tag='Calm &amp; Clarity · 30 gummies · Jamun Grape', price='₹899', mrp='₹1,099', off='18% off',
   rating='4.9', ratings='1,502', line='For a quieter mind in a louder day.',
   ing=[('Ashwagandha (KSM-66)','300 mg','The studied adaptogen for everyday stress'),
        ('Brahmi extract','150 mg','Traditional clarity herb, modern format'),
        ('Vitamin D3','400 IU','Mood-supporting sunshine, chewable')],
   moments=['before a big presentation','deadline weeks','daily anxiety-prone commutes','building a calm evening routine'],
   faq=[('When should I take it?','One gummy daily, any time. Consistency matters more than timing.'),
        ('How soon will I feel it?','Adaptogens build gently — most chums report a calmer baseline in 2–3 weeks.'),
        ('Is it vegetarian?','Yes — 100% vegetarian, no gelatin, no artificial colours.')],
   reviews=[('Neha S. · Jaipur','My whole team calls it the meeting gummy. Calmer without feeling slow.'),
            ('Vikram P. · Chennai','Was sceptical about ashwagandha in gummy form. Three weeks in, I get it.'),
            ('Mahi D. · Indore','Jamun grape is such an Indian flavour choice and I love it.')]),
]
IDS = [d['id'] for d in PDP_DATA]

def GUMMY(color, cls='', style=''):
    return ('<svg class="' + cls + '" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"'
            + (' style="' + style + '"' if style else '') + '>'
            '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="' + color + '"/>'
            '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>'
            '<ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/>'
            '<ellipse cx="63" cy="76" rx="9" ry="5" fill="#fff" opacity=".18" transform="rotate(-20 63 76)"/>'
            '<ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>')

def _shot_jar(d):
    c=d['color']
    return ('<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
      '<rect width="400" height="400" fill="'+d['soft']+'"/>'
      '<ellipse cx="200" cy="345" rx="120" ry="16" fill="#000" opacity=".08"/>'
      '<rect x="120" y="120" width="160" height="220" rx="26" fill="#fff" stroke="'+c+'" stroke-width="3"/>'
      '<rect x="112" y="92" width="176" height="40" rx="14" fill="'+c+'"/>'
      '<rect x="138" y="196" width="124" height="88" rx="12" fill="'+d['soft']+'"/>'
      '<text x="200" y="230" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="17" fill="#241233">GummyChums</text>'
      '<text x="200" y="254" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="13" fill="'+c+'">'+d['name'].replace(' Gummies','')+'</text>'
      + ''.join('<g transform="translate('+str(x)+','+str(y)+') scale(.34)">'+GUMMY(c)+'</g>' for x,y in [(140,296),(186,304),(232,296)]) +
      '<text x="200" y="368" text-anchor="middle" font-family="Arial" font-size="12" fill="#241233" opacity=".55">30 gummies · 100% vegetarian</text></svg>')

def _shot_macro(d):
    c=d['color']
    pos=[(96,150,30,120,26,112,'start'),(320,180,376,140,378,132,'end'),(210,330,300,368,304,362,'start')]
    return ('<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
      '<defs><radialGradient id="mg'+d['id']+'" cx="35%" cy="30%"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="'+d['soft']+'"/></radialGradient></defs>'
      '<rect width="400" height="400" fill="url(#mg'+d['id']+')"/>'
      '<g transform="translate(70,70) scale(2.6)">'+GUMMY(c)+'</g>'
      '<g font-family="Arial" font-size="13" fill="#241233">'
      + ''.join('<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" stroke="#241233" stroke-width="1.4" opacity=".5"/>'
                '<text x="'+str(tx)+'" y="'+str(ty)+'" font-weight="bold" text-anchor="'+an+'">'+ing+'</text>'
                '<text x="'+str(tx)+'" y="'+str(ty+16)+'" opacity=".6" text-anchor="'+an+'">'+dose+'</text>'
        for (ing,dose,_w),(x1,y1,x2,y2,tx,ty,an) in zip(d['ing'],pos))
      +'</g><text x="20" y="34" font-family="Arial" font-weight="bold" font-size="16" fill="'+c+'">WHAT&rsquo;S INSIDE</text></svg>')

def _shot_podium(d):
    c=d['color']
    return ('<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
      '<defs><linearGradient id="pd'+d['id']+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="'+c+'"/><stop offset="55%" stop-color="#241233"/><stop offset="100%" stop-color="#0d0714"/></linearGradient></defs>'
      '<rect width="400" height="400" fill="url(#pd'+d['id']+')"/>'
      '<circle cx="200" cy="170" r="120" fill="'+c+'" opacity=".25"/>'
      '<circle cx="200" cy="170" r="80" fill="'+c+'" opacity=".2"/>'
      '<ellipse cx="200" cy="298" rx="92" ry="14" fill="#000" opacity=".4"/>'
      '<rect x="130" y="240" width="140" height="56" rx="10" fill="#1a1024" stroke="'+c+'" stroke-opacity=".5"/>'
      '<g transform="translate(128,96) scale(1.44)">'+GUMMY(c)+'</g>'
      '<text x="200" y="352" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="15" fill="#fff">'+d['name'].replace(' Gummies','')+'</text>'
      '<text x="200" y="374" text-anchor="middle" font-family="Arial" font-size="12" fill="#fff" opacity=".55">'+d['tag'].split(' · ')[0].replace('&amp;','&')+'</text></svg>')

def _shot_daily(d):
    c=d['color']
    return ('<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">'
      '<rect width="400" height="400" fill="#fffdf6"/>'
      '<text x="200" y="52" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="18" fill="#241233">ONE A DAY. THAT&rsquo;S IT.</text>'
      + ''.join('<g transform="translate('+str(30+i*52)+',96) scale(.4)">'+GUMMY(c if i<5 else '#ddd3e6')+'</g>' for i in range(7)) +
      '<text x="200" y="182" text-anchor="middle" font-family="Arial" font-size="13" fill="#241233" opacity=".6">Mon — Sun · with or without food</text>'
      '<rect x="52" y="216" width="296" height="130" rx="18" fill="'+d['soft']+'"/>'
      '<text x="200" y="252" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="14" fill="#241233">100% VEGETARIAN · FSSAI CERTIFIED</text>'
      '<text x="200" y="278" text-anchor="middle" font-family="Arial" font-size="13" fill="#241233" opacity=".65">Third-party lab tested</text>'
      '<text x="200" y="300" text-anchor="middle" font-family="Arial" font-size="13" fill="#241233" opacity=".65">No artificial colours · no gelatin</text>'
      '<text x="200" y="322" text-anchor="middle" font-family="Arial" font-size="13" fill="'+c+'" font-weight="bold">Made with joy in India</text></svg>')

# --------------------------------------------------- shared extraction
def extract_shared():
    src=open(os.path.join(ROOT,'product-dreamy-sleep.html'),encoding='utf-8').read()
    fail=re.search(r'<script>\s*/\* enable reveal-hiding.*?</script>', src, re.S).group(0)
    style=re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    kit_css=style[:style.index('.pd-band{')]
    co_i=src.index('<!-- ===================== SHARED BILL / CHECKOUT')
    sc_i=src.index('<script>', co_i)
    checkout_html=src[co_i:sc_i]
    js=src[sc_i+len('<script>'):src.rindex('</script>')]
    core_js=js[:js.index('/* ===== premium motion kit ===== */')]
    prem_js=js[js.index('/* ===== premium motion kit ===== */'):js.index('(function(){ // gallery thumb switcher')]
    return fail,kit_css,checkout_html,core_js,prem_js

# --------------------------------------------------------------- skins
# ACC is replaced by the product colour; each skin mirrors its theme's UI.
SKINS = {
 15: dict(home='index15.html', dark=1,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet"/>',
   body='bg-[#0b0714] text-[#f6f1ff] font-[Outfit] overflow-x-hidden',
   lights=['ACC55','#ff2d8740','#38bdf838'],
   css='''.pd-head{font-weight:800}
  .pd-acc{background:linear-gradient(100deg,ACC,#ff2d87,#38bdf8,ACC);background-size:280% 280%;animation:pk-aurora 12s ease infinite;-webkit-background-clip:text;background-clip:text;color:transparent}
  .pd-panel{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:1.5rem}
  .pd-sub{color:rgba(246,241,255,.55)}
  .pd-btn1{background:linear-gradient(100deg,#ff2d87,#8b5cf6,#38bdf8,#39c98e,#ff2d87);background-size:280% 280%;animation:pk-aurora 12s ease infinite;color:#0b0714;border-radius:9999px}
  .pd-btn2{border:1px solid rgba(255,255,255,.25);border-radius:9999px}
  .pd-nav{background:rgba(11,7,20,.55);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}'''),
 16: dict(home='index16.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;700;900&display=swap" rel="stylesheet"/>',
   body='bg-[#fff6ea] text-[#2a1637] font-[Nunito] overflow-x-hidden',
   lights=['#ffd9a8','#ffc2d8','ACC33'],
   css='''.pd-head{font-weight:900;letter-spacing:-.02em}
  .pd-acc{color:ACC}
  .pd-panel{background:#fff;border:1px solid rgba(42,22,55,.08);border-radius:2rem;box-shadow:0 12px 28px -18px rgba(42,22,55,.35)}
  .pd-sub{color:rgba(42,22,55,.55)}
  .pd-btn1{background:ACC;color:#fff;border-radius:9999px;box-shadow:0 8px 0 rgba(42,22,55,.25)}
  .pd-btn1:active{transform:translateY(4px);box-shadow:0 2px 0 rgba(42,22,55,.25)}
  .pd-btn2{background:#2a1637;color:#fff;border-radius:9999px;box-shadow:0 8px 0 rgba(42,22,55,.25)}
  .pd-nav{background:rgba(255,246,234,.85);backdrop-filter:blur(10px)}'''),
 17: dict(home='index17.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;600;800&family=Gloock&display=swap" rel="stylesheet"/>',
   body='bg-[#f3edff] text-[#231133] font-[Albert_Sans] overflow-x-hidden',
   lights=['#c9b2ff','#ffc9e5','#b7e6ff'],
   css='''.pd-head{font-family:'Gloock',serif;font-weight:400}
  .pd-acc{color:ACC}
  .pd-panel{background:rgba(255,255,255,.72);backdrop-filter:blur(8px);border:1px solid rgba(35,17,51,.06);border-radius:2.5rem}
  .pd-sub{color:rgba(35,17,51,.55)}
  .pd-btn1{background:#231133;color:#fff;border-radius:9999px;text-transform:uppercase;letter-spacing:.06em}
  .pd-btn2{border:1.5px solid #231133;border-radius:9999px;text-transform:uppercase;letter-spacing:.06em}
  .pd-nav{background:transparent}'''),
 18: dict(home='index18.html', dark=1,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet"/>',
   body='bg-[#060b2e] text-[#eef1ff] font-[Space_Grotesk] overflow-x-hidden',
   lights=['#1b2a8f99','#7c6cf64d','ACC40'],
   css='''.pd-head{font-weight:700}
  .pd-acc{background:linear-gradient(90deg,#7c6cf6,#38bdf8,#39c98e);-webkit-background-clip:text;background-clip:text;color:transparent}
  .pd-panel{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:1.5rem}
  .pd-sub{color:rgba(238,241,255,.55)}
  .pd-btn1{background:linear-gradient(90deg,#7c6cf6,#38bdf8);color:#060b2e;border-radius:9999px}
  .pd-btn2{border:1px solid rgba(255,255,255,.25);border-radius:9999px}
  .pd-nav{background:rgba(6,11,46,.55);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}'''),
 19: dict(home='index19.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&display=swap" rel="stylesheet"/>',
   body='bg-[#f4ebff] text-[#1d1030] font-[Sora] overflow-x-hidden',
   lights=['ACC33','#ffd6ef','#d8ecff'],
   css='''.pd-head{font-weight:800}
  .pd-acc{color:ACC}
  .pd-panel{background:#fff;border:1px solid rgba(29,16,48,.08);border-radius:1.75rem}
  .pd-sub{color:rgba(29,16,48,.55)}
  .pd-btn1{background:#1d1030;color:#fff;border-radius:9999px}
  .pd-btn2{border:2px solid #1d1030;border-radius:9999px}
  .pd-nav{background:rgba(244,235,255,.85);backdrop-filter:blur(10px)}'''),
 20: dict(home='index20.html', dark=1,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&family=Gloock&display=swap" rel="stylesheet"/>',
   body='bg-[#08060a] text-[#f5eefc] font-[Manrope] overflow-x-hidden',
   lights=['#ff7ab826','ACC22','#8b5cf622'],
   css='''.pd-head{font-family:'Gloock',serif;font-weight:400}
  .pd-acc{color:#ff7ab8}
  .pd-panel{background:#100a16;border:1px solid #2a1f36;border-radius:1.75rem}
  .pd-sub{color:rgba(245,238,252,.5)}
  .pd-btn1{background:#ff7ab8;color:#08060a;border-radius:9999px}
  .pd-btn2{border:1px solid rgba(255,255,255,.25);border-radius:9999px}
  .pd-nav{background:rgba(8,6,10,.6);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}'''),
 21: dict(home='index21.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&display=swap" rel="stylesheet"/>',
   body='bg-[#ffe8f2] text-[#33104a] font-[Baloo_2] overflow-x-hidden',
   lights=['ACC33','#ffd23f4d','#8b5cf62e'],
   css='''.pd-head{font-weight:800}
  .pd-acc{color:ACC}
  .pd-panel{background:#fff;border:3px solid #33104a;border-radius:2.25rem;box-shadow:0 8px 0 #33104a}
  .pd-sub{color:rgba(51,16,74,.55)}
  .pd-btn1{background:#ffd23f;color:#33104a;border:3px solid #33104a;border-radius:9999px;box-shadow:0 6px 0 #33104a}
  .pd-btn1:active{transform:translateY(5px);box-shadow:0 1px 0 #33104a}
  .pd-btn2{background:ACC;color:#fff;border:3px solid #33104a;border-radius:9999px;box-shadow:0 6px 0 #33104a}
  .pd-btn2:active{transform:translateY(5px);box-shadow:0 1px 0 #33104a}
  .pd-nav{background:rgba(255,232,242,.85);backdrop-filter:blur(10px);border-bottom:3px solid #33104a}'''),
 22: dict(home='index22.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap" rel="stylesheet"/>',
   body='bg-[#fdf3e7] text-[#2c1230] font-[Bricolage_Grotesque] overflow-x-hidden',
   lights=['ACC30','#f265dd33','#ffd9a8'],
   css='''.pd-head{font-weight:800}
  .pd-acc{color:ACC}
  .pd-panel{background:#fff;border:1px solid rgba(44,18,48,.07);border-radius:1.75rem;box-shadow:0 16px 36px -22px rgba(44,18,48,.4)}
  .pd-sub{color:rgba(44,18,48,.55)}
  .pd-btn1{background:#2c1230;color:#fff;border-radius:9999px}
  .pd-btn2{background:ACC;color:#fff;border-radius:9999px}
  .pd-nav{background:rgba(253,243,231,.85);backdrop-filter:blur(10px)}'''),
 23: dict(home='index23.html', dark=0,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet"/>',
   body='bg-[#f6f2ea] text-[#191410] font-[Instrument_Sans] overflow-x-hidden',
   lights=['ACC22','#1a43ff14','#ff5a3c14'],
   css='''.pd-head{font-family:'Instrument Serif',serif;font-weight:400}
  .pd-acc{font-style:italic}
  .pd-panel{background:transparent;border:1px solid rgba(25,20,16,.18);border-radius:0}
  .pd-sub{color:rgba(25,20,16,.55)}
  .pd-btn1{background:#191410;color:#f6f2ea;border:1px solid #191410;text-transform:uppercase;letter-spacing:.18em;font-size:.85rem}
  .pd-btn2{border:1px solid #191410;text-transform:uppercase;letter-spacing:.18em;font-size:.85rem}
  .pd-btn2:hover{background:#191410;color:#f6f2ea}
  .pd-nav{background:rgba(246,242,234,.88);backdrop-filter:blur(8px);border-bottom:1px solid rgba(25,20,16,.15)}'''),
 24: dict(home='index24.html', dark=1,
   fonts='<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;800;900&display=swap" rel="stylesheet"/>',
   body='bg-[#0e0a18] text-[#fff5fb] font-[Figtree] overflow-x-hidden',
   lights=['ACC40','#ff2d8733','#38bdf82e'],
   css='''.pd-head{font-weight:900}
  .pd-acc{background:linear-gradient(90deg,#ff2d87,#ffd23f,#38bdf8,ACC);background-size:250% 250%;animation:pk-aurora 9s ease infinite;-webkit-background-clip:text;background-clip:text;color:transparent}
  .pd-panel{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:2rem}
  .pd-sub{color:rgba(255,245,251,.5)}
  .pd-btn1{background:#fff;color:#0e0a18;border-radius:9999px}
  .pd-btn2{background:linear-gradient(90deg,#ff2d87,#8b5cf6);color:#fff;border-radius:9999px}
  .pd-nav{background:rgba(14,10,24,.55);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}'''),
}

# Tailwind's arbitrary font-[X] class silently fails on the CDN build, so
# every page also gets an explicit body font-family rule.
STACKS={15:"'Outfit',sans-serif",16:"'Nunito',sans-serif",17:"'Albert Sans',sans-serif",
        18:"'Space Grotesk',sans-serif",19:"'Sora',sans-serif",20:"'Manrope',sans-serif",
        21:"'Baloo 2',cursive",22:"'Bricolage Grotesque',sans-serif",
        23:"'Instrument Sans',sans-serif",24:"'Figtree',sans-serif"}

THUMBJS=r'''
(function(){ var shots=document.querySelectorAll('.pdp-shot'),thumbs=document.querySelectorAll('.pdp-thumb');
  thumbs.forEach(function(t){t.addEventListener('click',function(){var i=t.getAttribute('data-i');
    shots.forEach(function(s){s.classList.toggle('on',s.getAttribute('data-i')===i)});
    thumbs.forEach(function(x){x.classList.toggle('on',x===t)});});});
})();
'''

def pdp_body(d, num, skin):
    acc=d['color']
    pref='p%d-'%num
    shots=[('Jar',_shot_jar(d)),('Inside',_shot_macro(d)),('Studio',_shot_podium(d)),('Daily',_shot_daily(d))]
    gal_main=''.join('<div class="pdp-shot'+(' on' if i==0 else '')+'" data-i="'+str(i)+'">'+svg+'</div>' for i,(_,svg) in enumerate(shots))
    gal_thumb=''.join('<button class="pdp-thumb'+(' on' if i==0 else '')+'" data-i="'+str(i)+'" aria-label="'+l+'">'+svg+'</button>' for i,(l,svg) in enumerate(shots))
    ing=''.join('<div class="pd-panel flex items-start gap-4 p-5"><div class="w-2.5 h-2.5 rounded-full mt-2" style="background:'+acc+';box-shadow:0 0 12px '+acc+'"></div><div><div class="font-extrabold">'+n+' <span class="pd-sub font-semibold text-sm">· '+ds+'</span></div><p class="pd-sub text-sm mt-0.5">'+w+'</p></div></div>' for n,ds,w in d['ing'])
    chips=''.join('<span class="pd-panel px-4 py-2 text-sm font-semibold" style="border-radius:9999px">'+m+'</span>' for m in d['moments'])
    faqs=''.join('<details class="pd-panel p-5 group"><summary class="font-extrabold cursor-pointer list-none flex justify-between items-center">'+q+'<span class="transition-transform group-open:rotate-45 text-xl" style="color:'+acc+'">+</span></summary><p class="pd-sub text-sm mt-3 leading-relaxed">'+a+'</p></details>' for q,a in d['faq'])
    revs=''.join('<figure class="pd-panel p-6"><div class="text-sm mb-2" style="color:'+acc+'">★★★★★</div><blockquote class="pd-sub text-sm leading-relaxed">&ldquo;'+t+'&rdquo;</blockquote><figcaption class="pd-sub text-xs font-bold mt-3">'+n+'</figcaption></figure>' for n,t in d['reviews'])
    rel=''.join('<a href="'+pref+o['id']+'.html" class="pd-panel rel-card p-6 text-center block" data-hot><div class="grid place-items-center py-3">'+GUMMY(o['color'],'pk-gummy pk-float','width:96px')+'</div><div class="font-extrabold pd-head">'+o['name'].replace(' Gummies','')+'</div><p class="pd-sub text-xs mt-1">'+o['tag'].split(' · ')[0]+'</p><div class="font-extrabold mt-2" style="color:'+o['color']+'">'+o['price']+'</div></a>' for o in PDP_DATA if o['id']!=d['id'])
    L=skin['lights']; light=lambda i,pos,delay: '<span class="pk-light w-[42vw] h-[42vw] '+pos+'" style="background:'+L[i].replace('ACC',acc)+(';animation-delay:'+delay if delay else '')+'"></span>'
    return ('''
<div id="pkc" '''+('class="blend-screen" ' if skin['dark'] else '')+'''style="background:'''+acc+'''"></div>
<div class="fixed inset-0 -z-10 overflow-hidden">'''
  +light(0,'-top-[10vw] -left-[8vw]','')+light(1,'top-[36vh] right-[-6vw]','2.5s')+light(2,'bottom-[-10vw] left-[24vw]','5s')+'''
</div>
<nav class="pd-nav sticky top-0 z-50 px-5 md:px-10 py-4 flex items-center justify-between">
  <a href="'''+skin['home']+'''" class="pd-head text-xl pd-acc" data-hot>GummyChums</a>
  <div class="hidden md:flex gap-7 text-sm font-semibold pd-sub">
    <a href="'''+pref+'''dreamy-sleep.html" data-hot>Sleep</a><a href="'''+pref+'''electric-blue.html" data-hot>Focus</a><a href="'''+pref+'''neon-violet.html" data-hot>Calm</a>
  </div>
  <button class="cart-trigger pk-btn pk-mag pd-btn2 relative px-4 py-2 text-sm font-bold" data-hot>Bag <span class="cart-count hidden ml-1 text-[11px] px-1.5 rounded-full" style="background:'''+acc+''';color:#fff">0</span></button>
</nav>
<div class="max-w-6xl mx-auto px-5 md:px-10">
  <p class="pd-sub text-xs font-semibold pt-6"><a href="'''+skin['home']+'''" data-hot class="underline underline-offset-4">← Back to shop</a> &nbsp;/&nbsp; <span style="color:'''+acc+'''">'''+d['name']+'''</span></p>
  <div class="grid md:grid-cols-2 gap-10 py-8">
    <div data-scrub>
      <div class="pd-panel overflow-hidden" style="transform:translateY(calc((1 - var(--p)) * 24px))">'''+gal_main+'''</div>
      <div class="grid grid-cols-4 gap-3 mt-3">'''+gal_thumb+'''</div>
    </div>
    <div>
      <h1 class="pd-head text-3xl md:text-5xl leading-tight">'''+d['name']+'''</h1>
      <p class="mt-2 text-lg font-semibold pd-sub">'''+d['line']+'''</p>
      <p class="text-sm font-semibold pd-sub mt-1">'''+d['tag']+'''</p>
      <div class="flex items-center gap-3 mt-4">
        <span class="bg-[#1f7a4d] text-white text-sm font-bold rounded-lg px-2.5 py-1">'''+d['rating']+''' ★</span>
        <span class="pd-sub text-sm font-semibold">'''+d['ratings']+''' ratings · 96% would repurchase</span>
      </div>
      <div class="flex items-end gap-3 mt-6">
        <span class="pd-head text-4xl pd-acc">'''+d['price']+'''</span>
        <span class="text-lg line-through pd-sub mb-1">'''+d['mrp']+'''</span>
        <span class="text-lg font-extrabold mb-1" style="color:'''+acc+'''">'''+d['off']+'''</span>
      </div>
      <p class="pd-sub text-xs mt-1">Inclusive of all taxes · Free shipping over ₹999</p>
      <div class="flex gap-3 mt-7">
        <button class="add-to-cart-btn pk-btn pk-mag pd-btn1 flex-1 font-extrabold py-4 text-lg" data-product-id="'''+d['id']+'''" data-hot>Add to bag</button>
        <button class="add-to-cart-btn pk-btn pk-mag pd-btn2 flex-1 font-extrabold py-4 text-lg" data-product-id="'''+d['id']+'''" data-hot>Buy now</button>
      </div>
      <div class="grid grid-cols-3 gap-3 mt-7 text-center text-xs font-bold">
        <div class="pd-panel p-3">🌱<br/>100% vegetarian</div><div class="pd-panel p-3">🧪<br/>Third-party tested</div><div class="pd-panel p-3">🇮🇳<br/>FSSAI certified</div>
      </div>
      <div class="mt-8 space-y-3">'''+ing+'''</div>
    </div>
  </div>
  <section class="py-10" style="border-top:1px solid rgba(128,128,128,.18)" data-scrub>
    <div style="opacity:calc(.25 + var(--p) * .75);transform:translateY(calc((1 - var(--p)) * 30px))">
    <h2 class="pd-head text-2xl md:text-3xl mb-3">Why you&rsquo;ll actually <span class="pd-acc">stay consistent</span></h2>
    <div class="grid md:grid-cols-2 gap-8 text-sm md:text-base leading-relaxed pd-sub">
      <p>The biggest problem in wellness isn&rsquo;t ingredients — it&rsquo;s consistency. People start supplements with the best intentions, then forget, lose motivation, or simply stop enjoying the experience. Pills feel clinical. Powders are inconvenient. Wellness starts feeling like work.</p>
      <p>'''+d['name'].replace(' Gummies','')+''' is designed to break that cycle: a precise, science-backed formula inside a genuinely delicious gummy, so the healthy habit is also the highlight. It&rsquo;s not another task on your to-do list. It&rsquo;s the treat you look forward to.</p>
    </div>
    <h3 class="pd-head text-lg mt-8 mb-3">Reach for it&hellip;</h3>
    <div class="flex flex-wrap gap-3">'''+chips+'''</div></div>
  </section>
  <section class="py-10" style="border-top:1px solid rgba(128,128,128,.18)">
    <h2 class="pd-head text-2xl md:text-3xl mb-6">Questions, <span class="pd-acc">answered honestly</span></h2>
    <div class="space-y-3 max-w-3xl">'''+faqs+'''</div>
  </section>
  <section class="py-10" style="border-top:1px solid rgba(128,128,128,.18)">
    <h2 class="pd-head text-2xl md:text-3xl mb-6">What <span class="pd-acc">chums say</span></h2>
    <div class="grid md:grid-cols-3 gap-5">'''+revs+'''</div>
  </section>
  <section class="py-10" style="border-top:1px solid rgba(128,128,128,.18)">
    <h2 class="pd-head text-2xl md:text-3xl mb-6">Meet the <span class="pd-acc">other Chums</span></h2>
    <div class="grid sm:grid-cols-2 gap-5 max-w-xl">'''+rel+'''</div>
  </section>
</div>
<footer class="py-10 text-center text-sm pd-sub" style="border-top:1px solid rgba(128,128,128,.18)">GummyChums · wellness that feels like a treat, not a task · Made in India</footer>
''')

PDP_EXTRA_CSS='''
  .pdp-shot{display:none}.pdp-shot.on{display:block}
  .pdp-shot svg,.pdp-thumb svg{width:100%;height:auto;display:block}
  .pdp-thumb{border-radius:1rem;overflow:hidden;border:2px solid rgba(128,128,128,.25);transition:border-color .2s,transform .2s}
  .pdp-thumb.on{border-color:ACC;box-shadow:0 0 18px -6px ACC}
  .pdp-thumb:hover{transform:translateY(-3px)}
  .rel-card{transition:transform .25s,box-shadow .25s}
  .rel-card:hover{transform:translateY(-6px)}
  details summary::-webkit-details-marker{display:none}
'''

def build_all():
    fail,kit_css,checkout_html,core_js,prem_js=extract_shared()
    for num,skin in SKINS.items():
        for d in PDP_DATA:
            acc=d['color']
            css=kit_css+'\nbody{font-family:'+STACKS[num]+'}\n'+PDP_EXTRA_CSS.replace('ACC',acc)+'\n'+skin['css'].replace('ACC',acc)
            html=('<!DOCTYPE html>\n<html lang="en" class="scroll-smooth">\n<head>\n'
              '<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
              '<title>GummyChums — '+d['name']+'</title>\n'
              '<script src="https://cdn.tailwindcss.com"></script>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,1,0&display=swap" rel="stylesheet"/>\n'
              +skin['fonts']+'\n'+fail+'\n<style>\n'+css+'\n</style>\n</head>\n'
              '<body class="'+skin['body']+'">\n'
              +pdp_body(d,num,skin)+'\n'+checkout_html+'<script>\n'+core_js+prem_js+THUMBJS+'\n</script>\n</body>\n</html>')
            fn='p%d-%s.html'%(num,d['id'])
            open(os.path.join(ROOT,fn),'w',encoding='utf-8').write(html)
            print('wrote',fn)

CARD_JS_TPL=r'''
(function(){var MAP={'dreamy-sleep':'PREF-dreamy-sleep.html','electric-blue':'PREF-electric-blue.html','neon-violet':'PREF-neon-violet.html'};
 var SEL='.al-card,.sq-card,.ob-card,.sn-rim,.jb-card,.zv-card,.ve-card,.cf-slide,.ms-panel,.ch-page .grid';
 document.querySelectorAll('.add-to-cart-btn').forEach(function(b){
   var id=b.getAttribute('data-product-id');if(!MAP[id])return;
   var card=b.closest(SEL)||b.parentElement.parentElement;if(!card||card.__pdp)return;card.__pdp=1;
   card.style.cursor='pointer';card.setAttribute('data-hot','');card.setAttribute('title','Open product page');
   card.addEventListener('click',function(e){if(e.target.closest('.add-to-cart-btn,a,button'))return;window.location.href=MAP[id];});
 });})();
'''

def patch_premium_pages():
    """Replace injected 'view product page' link JS with whole-card clicks."""
    link_re=re.compile(r"\(function\(\)\{ // \"view product page\" links under premium product cards.*?\}\)\(\);",re.S)
    for num in SKINS:
        fp=os.path.join(ROOT,'index%d.html'%num)
        s=open(fp,encoding='utf-8').read()
        s2,cnt=link_re.subn(CARD_JS_TPL.replace('PREF','p%d'%num).strip(),s)
        # index21 rain drops -> its own themed PDPs
        s2=s2.replace("var pdps=['product-dreamy-sleep.html','product-electric-blue.html','product-neon-violet.html'];",
                      "var pdps=['p21-dreamy-sleep.html','p21-electric-blue.html','p21-neon-violet.html'];")
        open(fp,'w',encoding='utf-8').write(s2)
        print('patched','index%d.html'%num,'(cardjs x%d)'%cnt)

if __name__=='__main__':
    build_all()
    patch_premium_pages()
