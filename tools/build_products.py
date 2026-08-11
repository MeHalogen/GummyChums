#!/usr/bin/env python3
"""build_products.py — rich, Shopify-lean product pages for the 3 real gummies.

Reuses the plain-CSS shell from build_pages.py (nav / footer / css / motion),
adds a product layout + accurate label nutrition (from the founder's xlsx).
Writes brain-booster.html, deep-sleep.html, eye-care.html.

    python3 tools/build_products.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import CSS, nav, FOOTER, JS, gummy, REPO  # shared shell

# 1 gummy ~3.5g, ~13.2 kcal, 0 added sugar — shared basics (label-accurate)
BASE=dict(serving="1 gummy (approx. 3.5 g)", energy="13.2 kcal", carb="3.3 g",
          added="0 g", protein="0 g", fat="0 g")

PRODUCTS=[
 dict(slug="brain-booster", pid="neon-violet", name="Brain Booster", flavour="Mango",
   price="&#8377;899", color="#6b2f6a", cat="Focus &amp; memory",
   tag="Big brain energy.<br/>Tiny gummy.",
   blurb="One little gummy of Bacopa (Brahmi) &mdash; the herb your nani trusted, now in a mango chew you&rsquo;ll actually look forward to.",
   actives=[("Bacopa Monnieri Leaf Extract","60 mg","&mdash;")],
   love=[("Focus that shows up","A classic nootropic botanical &mdash; for the 9am exam and the 3-hour meeting."),
         ("No sugar crash","Zero added sugar, ~13 kcal. A treat that doesn&rsquo;t undo the point."),
         ("Actually tasty","Nature-identical mango &mdash; the kind you finish the pack of. Responsibly.")],
   contains="Bacopa Monnieri Leaf Extract, Pectin, FOS (INS-440), Citric Acid (INS-330), Trisodium Citrate (INS-331(iii)). Contains nature-identical Mango flavour."),
 dict(slug="deep-sleep", pid="dreamy-sleep", name="Deep Sleep", flavour="Cherry",
   price="&#8377;699", color="#6b1e21", cat="Sleep &amp; calm",
   tag="Sleep tight,<br/>Chum.",
   blurb="Melatonin, ashwagandha, chamomile &amp; valerian in one cherry gummy &mdash; the wind-down ritual you&rsquo;ll happily reach for.",
   actives=[("Melatonin","5 mg","50%"),("Ashwagandha Extract","2 mg","&mdash;"),("Lemon","2 mg","&mdash;"),
            ("Magnesium","0.2 mg","&mdash;"),("Valerian Root Extract","2 mg","&mdash;"),
            ("Passion Flower","2 mg","&mdash;"),("Chamomile","5 mg","&mdash;")],
   love=[("Wind down, not out","Melatonin 5mg (50% RDA) + calming botanicals for lights-out."),
         ("A ritual, not a pill","A cherry chew beats a bitter capsule at 11pm."),
         ("Clean &amp; simple","Zero added sugar, ~13 kcal, no fuss.")],
   contains="Melatonin, Ashwagandha Extract, Lemon, Magnesium, Valerian Root Extract, Passion Flower, Chamomile, Pectin, FOS (INS-440), Citric Acid (INS-330), Trisodium Citrate (INS-331(iii)). Contains nature-identical Cherry flavour."),
 dict(slug="eye-care", pid="electric-blue", name="Eye Care", flavour="Orange",
   price="&#8377;749", color="#477971", cat="Eyes &amp; screens",
   tag="Screen-tired eyes?<br/>New bestie.",
   blurb="Lutein, zeaxanthin, bilberry &amp; a full vitamin stack in an orange gummy &mdash; for eyes glued to screens all day.",
   actives=[("Vitamin A (as Palmitate)","250 IU","15%"),("Vitamin E (as Acetate)","5 IU","33%"),
            ("Vitamin C","35 mg","100%"),("Vitamin B1","0.5 mg","56%"),("Vitamin B2","0.6 mg","46%"),
            ("Vitamin B6","0.9 mg","75%"),("Bilberry Fruit Extract","100 mg","17%"),
            ("Grape Seed Extract","25 mg","&mdash;"),("Lutein","5 mg","&mdash;"),
            ("Zeaxanthin","1 mg","25%"),("Lycopene","2 mg","&mdash;")],
   love=[("Made for screen days","Lutein + zeaxanthin + bilberry, the eye-care trio &mdash; for laptop-to-phone-to-TV life."),
         ("100% RDA Vitamin C","A full day&rsquo;s C in one orange chew, plus A, E and B-complex."),
         ("Zero guilt","No added sugar, ~13 kcal.")],
   contains="Bilberry Fruit Extract, Grape Seed Extract, Lutein, Zeaxanthin, Lycopene, Vitamins (A, E, C, B1, B2, B6), Pectin (INS-440), Citric Acid (INS-330), FOS. Contains nature-identical Orange flavour."),
]
BY={p["slug"]:p for p in PRODUCTS}

PCSS="""<style>
  .p-hero{display:grid;gap:2.4rem;grid-template-columns:1.05fr .95fr;align-items:center;padding:4.5rem 0 3rem}
  @media(max-width:860px){.p-hero{grid-template-columns:1fr;text-align:center}}
  .p-gwrap{position:relative;display:grid;place-items:center;min-height:320px}
  .p-glow{position:absolute;width:80%;aspect-ratio:1;border-radius:50%;filter:blur(46px);opacity:.5}
  .p-gum{width:min(60vw,300px);animation:pfloat 6s ease-in-out infinite}
  @keyframes pfloat{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-16px) rotate(3deg)}}
  .p-stat{display:inline-flex;flex-wrap:wrap;gap:.5rem;margin:1.2rem 0}
  .p-buy{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;margin-top:1.4rem}
  @media(max-width:860px){.p-buy{justify-content:center}}
  .p-price{font-family:'Anton',sans-serif;font-size:2.4rem}
  .nutri{width:100%;max-width:520px;border:3px solid var(--ink);border-radius:16px;overflow:hidden;background:var(--white);box-shadow:8px 8px 0 var(--ink)}
  .nutri .hd{background:var(--ink);color:var(--cream);padding:.85rem 1.2rem;font-family:'Anton',sans-serif;font-size:1.35rem;letter-spacing:.02em}
  .nutri .rw{display:flex;justify-content:space-between;gap:1rem;padding:.62rem 1.2rem;border-top:1px solid rgba(31,28,26,.12);font-weight:600}
  .nutri .rw b{font-weight:800}
  .nutri .sec-h{background:rgba(31,28,26,.06);font-weight:800;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;padding:.5rem 1.2rem;border-top:2px solid var(--ink)}
  .nutri .sub{font-size:.78rem;opacity:.6;padding:.6rem 1.2rem;border-top:1px solid rgba(31,28,26,.12)}
</style>"""

def nutri(p):
    rows=('<div class="rw"><span>Energy</span><b>%s</b></div>'
          '<div class="rw"><span>Carbohydrate</span><b>%s</b></div>'
          '<div class="rw"><span>Added Sugars</span><b>%s</b></div>'
          '<div class="rw"><span>Protein</span><b>%s</b></div>'
          '<div class="rw"><span>Total Fat</span><b>%s</b></div>')%(BASE["energy"],BASE["carb"],BASE["added"],BASE["protein"],BASE["fat"])
    acts=''.join('<div class="rw"><span>%s</span><b>%s <span style="opacity:.5;font-weight:600">%s</span></b></div>'%(n,q,r) for n,q,r in p["actives"])
    return ('<div class="nutri"><div class="hd">Nutrition &amp; actives</div>'
      '<div class="rw" style="border-top:0"><span>Serving size</span><b>%s</b></div>'%BASE["serving"]
      + rows
      + '<div class="sec-h">Each gummy contains</div>' + acts
      + '<div class="sub">%%RDA per ICMR 2020 guidelines. Nutraceutical &mdash; not for medicinal use.</div></div>')

def body(p):
    others=[q for q in PRODUCTS if q["slug"]!=p["slug"]]
    hero=('<section class="wrap"><div class="p-hero">'
      '<div class="reveal">'
      '<p class="eyebrow">%s &middot; Nutraceutical</p>'
      '<h1 class="big" style="margin:.6rem 0">%s</h1>'
      '<p class="lead" style="margin:.2rem 0;max-width:34rem">%s</p>'
      '<div class="p-stat"><span class="chip">%s flavour</span><span class="chip">0 added sugar</span><span class="chip">~13 kcal</span></div>'
      '<div class="p-buy"><span class="p-price" style="color:%s">%s</span>'
      '<a href="index31.html#shop" class="btn">Add to bag &rarr;</a></div></div>'
      '<div class="p-gwrap reveal"><div class="p-glow" style="background:%s"></div><div class="p-gum">%s</div></div>'
      '</div></section>')%(p["cat"],p["tag"],p["blurb"],p["flavour"],
                           p["color"],p["price"],p["color"],gummy(p["color"]))
    inside=('<section class="wrap sec"><div style="display:grid;gap:2.4rem;grid-template-columns:1fr 1fr;align-items:start">'
      '<div class="reveal">%s</div>'
      '<div class="reveal"><p class="eyebrow">What&rsquo;s inside</p>'
      '<h2 class="big" style="font-size:clamp(1.8rem,5vw,3.2rem);margin:.4rem 0 1rem">Honest label,<br/>zero fine print.</h2>'
      '<p class="lead" style="font-size:1.05rem">%s</p></div>'
      '</div></section>')%(nutri(p),p["contains"])
    inside='<style>@media(max-width:860px){section.wrap.sec>div{grid-template-columns:1fr!important}}</style>'+inside
    love=('<section class="sec" style="background:%s;color:%s"><div class="wrap"><div class="reveal">'
      '<p class="eyebrow" style="color:var(--saffron)">Why you&rsquo;ll love it</p>'
      '<h2 class="big" style="margin:.4rem 0 2rem">Small habit.<br/>Big smile.</h2></div>'
      '<div class="grid3">%s</div></div></section>')%(
      p["color"], "#f1e7da",
      ''.join('<div class="card reveal" style="color:var(--ink)"><div class="anton" style="font-size:1.5rem;color:%s">%02d</div>'
              '<b style="font-size:1.15rem;display:block;margin-top:.3rem">%s</b>'
              '<p style="margin-top:.4rem;opacity:.75">%s</p></div>'%(p["color"],i+1,t,d) for i,(t,d) in enumerate(p["love"])))
    howto=('<section class="wrap sec reveal" style="text-align:center">'
      '<p class="eyebrow">How to enjoy</p>'
      '<h2 class="big" style="font-size:clamp(1.8rem,6vw,3.4rem);margin:.5rem 0 1rem">One a day. That&rsquo;s the whole plan.</h2>'
      '<p class="lead" style="margin:0 auto">Chew one gummy a day &mdash; %s. Keep the pack somewhere you&rsquo;ll see it. '
      'Consistency beats perfection, Chum.</p></section>')%(
        "before that 9am exam or long meeting" if p["slug"]=="brain-booster" else
        "about an hour before lights-out" if p["slug"]=="deep-sleep" else
        "on those laptop-to-phone-to-TV days")
    rel=('<section class="sec" style="background:var(--cream)"><div class="wrap"><div class="reveal">'
      '<p class="eyebrow">More Chums</p><h2 class="big" style="font-size:clamp(1.8rem,5vw,3rem);margin:.4rem 0 1.6rem">Meet the rest of the gang.</h2></div>'
      '<div class="grid3">%s</div></div></section>')%(
      ''.join('<a href="%s.html" class="card reveal" style="display:block;text-align:center">'
              '<div style="width:120px;margin:0 auto">%s</div>'
              '<b style="font-size:1.25rem;display:block;margin-top:.6rem">%s</b>'
              '<p style="opacity:.7;margin-top:.2rem">%s &middot; %s</p></a>'%(o["slug"],gummy(o["color"],"100%"),o["name"],o["flavour"],o["price"]) for o in others)
      + '<a href="index31.html#shop" class="card reveal" style="display:grid;place-items:center;text-align:center;background:var(--saffron)">'
        '<div><div class="anton" style="font-size:2rem">Shop all</div><p style="margin-top:.3rem;font-weight:700">&rarr; back to the shop</p></div></a>')
    return PCSS+hero+inside+love+howto+rel

def page_product(p):
    title="GummyChums &mdash; %s"%p["name"]
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\"/>\n"
      "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>\n"
      f"<title>{title}</title>\n"
      "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"/>\n"
      "<link href=\"https://fonts.googleapis.com/css2?family=Anton&family=Baloo+2:wght@500;600;700;800&display=swap\" rel=\"stylesheet\"/>\n"
      f"<style>{CSS}</style>\n</head>\n<body>\n"
      "<div id=\"grain\"></div><div id=\"cur\"></div><div id=\"prog\"></div>\n"
      + nav("shop") + "\n" + body(p) + "\n" + FOOTER + "\n" + JS + "\n</body>\n</html>")

def build():
    for p in PRODUCTS:
        html=page_product(p)
        open(os.path.join(REPO,p["slug"]+".html"),"w",encoding="utf-8").write(html)
        print("wrote",p["slug"]+".html",f"({len(html)//1024} KB)")

if __name__=="__main__": build()
