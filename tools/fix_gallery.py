# -*- coding: utf-8 -*-
"""
Gallery fixes:
1) MOBILE BLANK-TAB FIX: the gallery loaded ~25 live iframes (each booting
   Tailwind CDN + fonts + canvas physics) which crashes/blanks mobile Chrome.
   Iframes become data-src; a loader promotes them to src ONLY on desktop
   (lazily, via IntersectionObserver). Mobile gets lightweight gradient
   placeholder tiles instead — instant load.
2) Adds the Moodboard Collection group (index25-29) after "Start here".
Idempotent. Run from repo root:  python3 tools/fix_gallery.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP = os.path.join(ROOT, 'index-gallery.html')

MOOD = [
 ('index25.html','Daak Ghar ✦✦✦','Indian postal stamps — perforated cards, postmarks, rani pink','#d81b60'),
 ('index26.html','Maachis ✦✦✦','Vintage matchbox labels — strike-strip hovers, deep red & gold','#b3261e'),
 ('index27.html','Kirana Pouch ✦✦✦','Pillow-pouch shelves, checkerboard, hand-tag prices','#e8641b'),
 ('index28.html','Kala Pop ✦✦✦','Spiced-soda label — arches, sunburst, royal blue & rani pink','#1a3fb3'),
 ('index29.html','Tin Bagh ✦✦✦','Biscuit-tin block prints — emerald florals, embossed tins','#0d6b45'),
]

LOADER = '''<script id="gal-loader">
(function(){
  var desk=matchMedia('(min-width:880px) and (hover:hover) and (pointer:fine)').matches;
  var frs=[].slice.call(document.querySelectorAll('.thumb iframe[data-src]'));
  if(desk&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){
      if(en.isIntersecting){var f=en.target;f.src=f.getAttribute('data-src');io.unobserve(f);}
    })},{rootMargin:'300px'});
    frs.forEach(function(f){io.observe(f);});
  }else{
    frs.forEach(function(f){
      var card=f.closest('.card'); if(!card)return;
      var dot=card.querySelector('.dot');
      var c=dot?getComputedStyle(dot).backgroundColor:'#b80865';
      var t=card.querySelector('h3');
      var th=f.parentElement; f.remove();
      th.style.background='linear-gradient(135deg,'+c+' 0%,#241233 140%)';
      var s=document.createElement('div');
      s.style.cssText='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;gap:6px;';
      s.innerHTML='<div style="font-family:Fraunces,serif;font-size:46px;line-height:1">'+(t?t.textContent.trim().charAt(0):'G')+
        '</div><div style="font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;opacity:.75">tap to open</div>';
      th.appendChild(s);
    });
  }
})();
</script>'''

def main():
    s = open(FP, encoding='utf-8').read()

    # 1) iframes -> data-src + loader
    s = s.replace('<iframe src="', '<iframe data-src="')
    if 'id="gal-loader"' not in s:
        s = s.replace('</body>', LOADER + '\n</body>')
    else:
        s = re.sub(r'<script id="gal-loader">.*?</script>', LOADER, s, flags=re.S)

    # 2) moodboard group after the "Start here" card (idempotent)
    if 'index25.html' not in s:
        cards = ''.join(
            '<a href="%s" target="_blank" class="card group">'
            '<div class="thumb"><iframe data-src="%s" loading="lazy" scrolling="no" tabindex="-1" title="%s"></iframe><span class="veil"></span></div>'
            '<div class="meta"><div class="row"><span class="dot" style="background:%s"></span>'
            '<span class="idx">%s</span><span class="open">Open ↗</span></div>'
            '<h3>%s</h3><p>%s</p></div></a>'
            % (f, f, n, a, f.replace('.html',''), n, d)
            for (f, n, d, a) in MOOD)
        head = ('<div class="ghead"><h2>Moodboard Collection ✦✦✦</h2>'
                '<p>Tailored to the founder&rsquo;s Pinterest board — Indian retro-pop packaging, real SKU data</p></div>')
        anchor = '<div class="ghead"><h2>Premium Motion Collection'
        assert anchor in s, 'premium ghead anchor missing'
        s = s.replace(anchor, head + cards + anchor, 1)

    open(FP, 'w', encoding='utf-8').write(s)
    print('gallery patched: mobile-safe thumbs + moodboard group')

if __name__ == '__main__':
    main()
