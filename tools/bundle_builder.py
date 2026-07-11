# -*- coding: utf-8 -*-
"""
"Build your own Chum Box" configurator.

Injects a self-contained bundle-builder section (pure CSS/vanilla JS, no
Tailwind classes, WAAPI transform-only animations) into every index page
(index2-index24), theme-tinted per page, wired into each page's existing
shared bill (pushes a single cart line describing the chosen gummies).
Also writes a standalone single-file demo: bundle-builder.html.

Idempotent — the section lives between <!-- BB:START --> / <!-- BB:END -->
markers and is replaced on re-run.   Run from repo root:
  python3 tools/bundle_builder.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GUMS = [
 ('dreamy-sleep','Dreamy Sleep','Sleep','#8b5cf6'),
 ('electric-blue','Electric Blue','Focus','#38bdf8'),
 ('neon-violet','Neon Violet','Calm','#e44bd3'),
 ('minty-fresh','Minty Fresh','Gut','#39c98e'),
 ('burnt-orange','Burnt Orange','Immunity','#ffb02e'),
 ('coral-sunrise','Coral Sunrise','Glow','#ff5c8a'),
]
SIZES = [(15,349),(30,549),(45,749)]

# (dark?, accent) per page
ACCENTS = {
 2:(0,'#e6007a'), 3:(0,'#ff7eb6'), 4:(0,'#0ea5e9'), 5:(0,'#e84620'), 6:(0,'#8a6d3b'),
 7:(0,'#ff4ec7'), 8:(1,'#ec48ff'), 9:(0,'#5c6b4a'), 10:(0,'#ff5a5f'), 11:(0,'#a78bff'),
 12:(0,'#ff2d87'), 13:(0,'#1a43ff'), 14:(0,'#e4177e'), 15:(1,'#ff7ab8'), 16:(0,'#ff5c8a'),
 17:(0,'#8b5cf6'), 18:(1,'#38bdf8'), 19:(0,'#e44bd3'), 20:(1,'#ff7ab8'), 21:(0,'#ff5c8a'),
 22:(0,'#e44bd3'), 23:(0,'#8a6d3b'), 24:(1,'#ffd23f'),
}

def gummy_svg(color, size=44):
    return ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:%dpx;height:%dpx;display:block">'
      '<path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="%s"/>'
      '<ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/>'
      '<ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>') % (size,size,color)

def bb_css(dark, acc):
    panel = 'rgba(255,255,255,.06)' if dark else 'rgba(0,0,0,.045)'
    line  = 'rgba(255,255,255,.16)' if dark else 'rgba(0,0,0,.14)'
    soft  = 'rgba(255,255,255,.55)' if dark else 'rgba(0,0,0,.55)'
    boxbg = 'rgba(255,255,255,.04)' if dark else '#ffffff'
    return '''
  /* ===== chum box builder (self-contained, no framework classes) ===== */
  #bb-builder{--bb-acc:'''+acc+''';--bb-panel:'''+panel+''';--bb-line:'''+line+''';--bb-soft:'''+soft+''';
    border-top:1px solid var(--bb-line);padding:6rem 1.25rem;}
  #bb-builder *{box-sizing:border-box}
  .bb-wrap{max-width:72rem;margin:0 auto}
  .bb-kick{letter-spacing:.35em;font-size:12px;text-transform:uppercase;color:var(--bb-acc);font-weight:700;margin:0 0 14px}
  .bb-title{font-size:clamp(2rem,5.5vw,3.8rem);font-weight:800;line-height:1.05;margin:0 0 10px}
  .bb-sub{color:var(--bb-soft);font-size:1.02rem;margin:0 0 42px;max-width:36rem}
  .bb-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:2.2rem}
  .bb-grid>*{min-width:0}
  @media(min-width:880px){.bb-grid{grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);align-items:start}}
  /* --- the box --- */
  .bb-boxcol{position:sticky;top:90px}
  @media(max-width:879px){.bb-boxcol{position:static}}
  .bb-box{position:relative;background:'''+boxbg+''';border:3px solid var(--bb-line);border-radius:20px;
    padding:1rem 1rem 1.2rem;box-shadow:0 18px 40px -22px rgba(0,0,0,.35)}
  .bb-lid{height:16px;border-radius:10px 10px 0 0;background:var(--bb-acc);opacity:.9;margin:-1rem -1rem 12px;border-bottom:3px solid var(--bb-line)}
  .bb-label{display:flex;justify-content:space-between;align-items:baseline;font-weight:800;margin-bottom:10px}
  .bb-label small{color:var(--bb-soft);font-weight:600}
  .bb-drop{min-height:172px;border:2px dashed var(--bb-line);border-radius:14px;display:flex;flex-wrap:wrap;
    align-content:flex-end;justify-content:center;gap:6px;padding:12px;transition:border-color .3s}
  .bb-drop.bb-has{border-style:solid;border-color:var(--bb-acc)}
  .bb-drop-empty{width:100%;text-align:center;color:var(--bb-soft);font-weight:600;font-size:.92rem;align-self:center;margin:auto 0}
  .bb-inbox{position:relative;animation:bb-settle .45s cubic-bezier(.34,1.56,.64,1)}
  .bb-inbox small{position:absolute;left:50%;bottom:-4px;transform:translateX(-50%);background:var(--bb-acc);color:#fff;
    font-size:9px;font-weight:800;border-radius:99px;padding:1px 6px;white-space:nowrap}
  @keyframes bb-settle{0%{transform:translateY(-26px) scale(1.15)}60%{transform:translateY(3px) scale(.94,1.05)}100%{transform:none}}
  .bb-box.bb-land{animation:bb-squash .4s cubic-bezier(.34,1.56,.64,1)}
  @keyframes bb-squash{35%{transform:scale(1.03,.96)}70%{transform:scale(.985,1.015)}100%{transform:scale(1)}}
  .bb-tabs{margin-top:12px;font-weight:700;font-size:.92rem;color:var(--bb-soft);text-align:center}
  /* --- summary + cta --- */
  .bb-sum{margin-top:1.1rem;background:var(--bb-panel);border-radius:16px;padding:1rem 1.15rem}
  .bb-sumline{display:flex;justify-content:space-between;font-weight:600;font-size:.95rem;padding:.28rem 0;color:var(--bb-soft)}
  .bb-sumline b{color:inherit}
  .bb-total{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--bb-line);
    margin-top:.6rem;padding-top:.7rem;font-weight:800}
  .bb-total span:last-child{font-size:1.7rem}
  .bb-cta{width:100%;margin-top:.9rem;border:0;border-radius:999px;padding:1.05rem;font-weight:800;font-size:1.05rem;
    background:var(--bb-acc);color:#fff;cursor:pointer;transition:transform .12s,opacity .2s,box-shadow .25s}
  .bb-cta:hover{box-shadow:0 12px 26px -10px var(--bb-acc)}
  .bb-cta:active{transform:scale(.96)}
  .bb-cta[disabled]{opacity:.45;cursor:not-allowed;box-shadow:none}
  /* --- pickers --- */
  .bb-row{display:flex;align-items:center;gap:.9rem;background:var(--bb-panel);border:2px solid transparent;
    border-radius:18px;padding:.85rem 1rem;margin-bottom:.7rem;transition:border-color .25s,transform .2s}
  .bb-row.bb-on{border-color:var(--bb-acc)}
  .bb-row:hover{transform:translateX(4px)}
  .bb-dot{flex:0 0 44px}
  .bb-meta{flex:1 1 auto;min-width:0}
  .bb-meta b{display:block;font-size:1.02rem}
  .bb-meta small{color:var(--bb-soft);font-weight:600}
  .bb-sizes{display:flex;gap:.35rem;margin:0 .2rem}
  .bb-size{border:1.5px solid var(--bb-line);background:transparent;color:inherit;border-radius:999px;
    padding:.32rem .6rem;font-weight:700;font-size:.8rem;cursor:pointer;transition:all .2s;white-space:nowrap}
  .bb-size.bb-sel{background:var(--bb-acc);border-color:var(--bb-acc);color:#fff}
  .bb-add{border:0;border-radius:999px;width:2.4rem;height:2.4rem;font-size:1.2rem;font-weight:800;cursor:pointer;
    background:var(--bb-acc);color:#fff;flex:0 0 auto;transition:transform .12s;line-height:1}
  .bb-add:active{transform:scale(.9)}
  .bb-row.bb-on .bb-add{background:transparent;border:2px solid var(--bb-acc);color:var(--bb-acc)}
  .bb-price{font-weight:800;min-width:3.6rem;text-align:right}
  .bb-fly{position:fixed;z-index:250;pointer-events:none;left:0;top:0;will-change:transform}
  @media(max-width:560px){
    .bb-row{flex-wrap:wrap}
    .bb-meta{flex:1 1 8rem}
    .bb-sizes{width:100%;order:5;margin:.5rem 0 0;justify-content:flex-start}
    .bb-size{padding:.3rem .55rem}
    .bb-price{margin-left:auto}
  }
'''

def bb_html():
    rows=''
    for gid,name,short,color in GUMS:
        sizes=''.join('<button class="bb-size%s" data-bb-size="%d" data-bb-price="%d">%d tabs</button>'
                      % (' bb-sel' if t==30 else '', t, p, t) for t,p in SIZES)
        rows+=('<div class="bb-row" data-bb-id="'+gid+'" data-bb-name="'+name+'" data-bb-color="'+color+'" data-bb-short="'+short+'">'
          '<span class="bb-dot">'+gummy_svg(color,44)+'</span>'
          '<span class="bb-meta"><b>'+name+'</b><small>'+short+'</small></span>'
          '<span class="bb-sizes">'+sizes+'</span>'
          '<span class="bb-price">₹549</span>'
          '<button class="bb-add" aria-label="Add '+name+' to box" data-hot>+</button>'
          '</div>')
    return ('<!-- BB:START -->\n<section id="bb-builder">'
      '<div class="bb-wrap">'
      '<p class="bb-kick">Build your own · mix any of the six</p>'
      '<h2 class="bb-title">Pack your Chum Box.</h2>'
      '<p class="bb-sub">Pick your gummies, pick your size — watch them drop into the box. '
      'One box, your rules: 15 tabs ₹349 · 30 tabs ₹549 · 45 tabs ₹749 per chum.</p>'
      '<div class="bb-grid">'
      '<div class="bb-boxcol">'
        '<div class="bb-box" id="bb-box">'
          '<div class="bb-lid"></div>'
          '<div class="bb-label"><span>GummyChums · MY CHUM BOX</span><small id="bb-count">empty</small></div>'
          '<div class="bb-drop" id="bb-drop"><span class="bb-drop-empty">Your box is waiting — add a chum →</span></div>'
          '<div class="bb-tabs" id="bb-tabs">0 tabs packed</div>'
        '</div>'
        '<div class="bb-sum">'
          '<div id="bb-lines"><div class="bb-sumline"><span>Nothing packed yet</span><span>—</span></div></div>'
          '<div class="bb-total"><span>Box total</span><span id="bb-total">₹0</span></div>'
          '<button class="bb-cta" id="bb-cta" disabled data-hot>Pack my box → add to bag</button>'
        '</div>'
      '</div>'
      '<div>'+rows+'</div>'
      '</div></div>'
      '</section>\n<!-- BB:END -->')

BB_JS = r'''
<script>
/* ===== Chum Box builder (self-contained, lag-proof: transform-only WAAPI) ===== */
(function(){
  var box={}, drop=document.getElementById('bb-drop'), boxEl=document.getElementById('bb-box');
  var builder=document.getElementById('bb-builder');
  if(!builder||!drop)return;
  var GSVG=function(c,s){return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:'+s+'px;height:'+s+'px;display:block"><path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="'+c+'"/><ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/><ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>';};
  function inr(n){return '₹'+n.toLocaleString('en-IN');}

  function render(){
    var ids=Object.keys(box), lines='', total=0, tabs=0;
    // box contents
    drop.innerHTML='';
    if(!ids.length){drop.innerHTML='<span class="bb-drop-empty">Your box is waiting — add a chum →</span>';drop.classList.remove('bb-has');}
    else drop.classList.add('bb-has');
    ids.forEach(function(id,i){var it=box[id];
      var g=document.createElement('span');g.className='bb-inbox';
      g.style.transform='rotate('+((i%2?1:-1)*(4+i*2))+'deg)';
      g.innerHTML=GSVG(it.color,46)+'<small>'+it.tabs+'</small>';
      drop.appendChild(g);
      lines+='<div class="bb-sumline"><span><b>'+it.name+'</b> · '+it.tabs+' tabs</span><span>'+inr(it.price)+'</span></div>';
      total+=it.price;tabs+=it.tabs;
    });
    document.getElementById('bb-lines').innerHTML=lines||'<div class="bb-sumline"><span>Nothing packed yet</span><span>—</span></div>';
    document.getElementById('bb-total').textContent=inr(total);
    document.getElementById('bb-tabs').textContent=tabs+' tabs packed';
    document.getElementById('bb-count').textContent=ids.length?ids.length+' of 6 chums':'empty';
    var cta=document.getElementById('bb-cta');
    cta.disabled=!ids.length;
    cta.textContent=ids.length?('Pack my box · '+ids.length+' chums · '+inr(total)):'Pack my box → add to bag';
    // row states
    builder.querySelectorAll('.bb-row').forEach(function(r){
      var id=r.getAttribute('data-bb-id'), on=!!box[id];
      r.classList.toggle('bb-on',on);
      r.querySelector('.bb-add').textContent=on?'–':'+';
    });
  }

  function fly(fromEl,color,cb){
    try{
      var f=fromEl.getBoundingClientRect(), t=drop.getBoundingClientRect();
      var el=document.createElement('div');el.className='bb-fly';el.innerHTML=GSVG(color,40);
      document.body.appendChild(el);
      var sx=f.left+f.width/2-20, sy=f.top+f.height/2-20;
      var ex=t.left+t.width/2-20,  ey=t.top+t.height/2-20;
      el.animate([
        {transform:'translate('+sx+'px,'+sy+'px) scale(1)'},
        {transform:'translate('+((sx+ex)/2)+'px,'+(Math.min(sy,ey)-110)+'px) scale(1.2) rotate(120deg)',offset:.55},
        {transform:'translate('+ex+'px,'+ey+'px) scale(.6) rotate(300deg)',opacity:.9}
      ],{duration:620,easing:'cubic-bezier(.45,-.15,.35,1)'}).onfinish=function(){
        el.remove();
        boxEl.classList.remove('bb-land');void boxEl.offsetWidth;boxEl.classList.add('bb-land');
      };
      setTimeout(function(){if(el.parentNode)el.remove();},1500); /* hidden-tab safety */
      cb();
    }catch(e){cb();}
  }

  builder.addEventListener('click',function(e){
    var sz=e.target.closest('.bb-size');
    if(sz){
      var row=sz.closest('.bb-row'), id=row.getAttribute('data-bb-id');
      row.querySelectorAll('.bb-size').forEach(function(b){b.classList.toggle('bb-sel',b===sz);});
      row.querySelector('.bb-price').textContent=inr(+sz.getAttribute('data-bb-price'));
      if(box[id]){box[id].tabs=+sz.getAttribute('data-bb-size');box[id].price=+sz.getAttribute('data-bb-price');render();}
      return;
    }
    var add=e.target.closest('.bb-add');
    if(add){
      var row=add.closest('.bb-row'), id=row.getAttribute('data-bb-id');
      if(box[id]){delete box[id];render();return;}
      var sel=row.querySelector('.bb-size.bb-sel');
      var item={name:row.getAttribute('data-bb-name'),color:row.getAttribute('data-bb-color'),
                short:row.getAttribute('data-bb-short'),tabs:+sel.getAttribute('data-bb-size'),price:+sel.getAttribute('data-bb-price')};
      box[id]=item;render();          /* state first — animation is decoration only */
      fly(add,item.color,function(){});
      return;
    }
    if(e.target.closest('#bb-cta')){
      var ids=Object.keys(box);if(!ids.length)return;
      var total=0,tabs=0,parts=[];
      ids.forEach(function(id){var it=box[id];total+=it.price;tabs+=it.tabs;parts.push(it.short.toUpperCase()+' '+it.tabs);});
      var img='data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="26" width="80" height="64" rx="10" fill="#fff" stroke="#241233" stroke-width="4"/><rect x="6" y="14" width="88" height="16" rx="6" fill="'+box[ids[0]].color+'"/><circle cx="34" cy="62" r="13" fill="'+box[ids[0]].color+'"/><circle cx="60" cy="66" r="11" fill="'+(box[ids[1]]?box[ids[1]].color:'#e44bd3')+'"/><circle cx="48" cy="50" r="10" fill="'+(box[ids[2]]?box[ids[2]].color:'#ffb02e')+'"/></svg>');
      try{
        cart.push({id:'chum-box-'+Date.now(),name:'My Chum Box ('+ids.length+' chums · '+tabs+' tabs)',
                   price:total,image:img,variant:parts.join(' · '),quantity:1});
        syncCart();openCart();
        box={};render();
      }catch(err){alert('Box packed: '+parts.join(', ')+' — total '+inr(total));}
    }
  });

  render();
})();
</script>'''

CHECKOUT_MARK = '<!-- ===================== SHARED BILL / CHECKOUT'

def inject(fp, dark, acc):
    s=open(fp,encoding='utf-8').read()
    block=bb_html()+'\n'+BB_JS
    # replace previous injection if present
    s=re.sub(r'<!-- BB:START -->.*?</script>', lambda m:'', s, flags=re.S) if '<!-- BB:START -->' in s else s
    s=s.replace('<!-- BB:END -->','')
    css=bb_css(dark,acc)
    if '#bb-builder{' in s:
        s=re.sub(r'/\* ===== chum box builder.*?(?=\n</style>)', css.strip(), s, flags=re.S)
    else:
        s=s.replace('</style>', css+'\n</style>', 1)
    # insert before footer (last <footer), else before checkout markup
    idx=s.rfind('<footer')
    if idx==-1: idx=s.find(CHECKOUT_MARK)
    s=s[:idx]+block+'\n'+s[idx:]
    open(fp,'w',encoding='utf-8').write(s)

def build_standalone():
    src=open(os.path.join(ROOT,'product-dreamy-sleep.html'),encoding='utf-8').read()
    co_i=src.index(CHECKOUT_MARK); sc_i=src.index('<script>',co_i)
    checkout_html=src[co_i:sc_i]
    js=src[sc_i+len('<script>'):src.rindex('</script>')]
    core_js=js[:js.index('/* ===== premium motion kit ===== */')]
    html=('<!DOCTYPE html>\n<html lang="en" class="scroll-smooth">\n<head>\n'
      '<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
      '<title>GummyChums — Build Your Chum Box</title>\n'
      '<script src="https://cdn.tailwindcss.com"></script>\n'
      '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,1,0&display=swap" rel="stylesheet"/>\n'
      '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;800&display=swap" rel="stylesheet"/>\n'
      '<style>\nbody{font-family:Figtree,sans-serif;background:#fffdf6;color:#241233}\n'
      +bb_css(0,'#e4177e')+'\n'
      '.sa-nav{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;'
      'padding:1rem 1.5rem;background:rgba(255,253,246,.9);backdrop-filter:blur(10px);border-bottom:1px solid rgba(36,18,51,.1)}\n'
      '.sa-bag{border:0;background:#241233;color:#fff;border-radius:999px;padding:.6rem 1.2rem;font-weight:800;cursor:pointer}\n'
      +src[src.index('<style>')+7:src.index('.pd-band{')]  # shared bill css + kit css
      +'\n</style>\n</head>\n<body>\n'
      '<nav class="sa-nav"><b style="font-size:1.2rem">Gummy<span style="color:#e4177e">Chums</span> · Box Builder</b>'
      '<button class="sa-bag cart-trigger">Bag <span class="cart-count" style="display:none;background:#e4177e;border-radius:99px;padding:0 .45rem;margin-left:.2rem">0</span></button></nav>\n'
      +bb_html()+'\n'
      +checkout_html+'<script>\n'+core_js+'\n</script>\n'+BB_JS+'\n'
      '<footer style="text-align:center;padding:2.2rem;opacity:.5;font-size:.9rem">GummyChums · single-file demo · Made in India</footer>\n'
      '</body>\n</html>')
    open(os.path.join(ROOT,'bundle-builder.html'),'w',encoding='utf-8').write(html)
    print('wrote bundle-builder.html (standalone demo)')

def patch_gallery():
    fp=os.path.join(ROOT,'index-gallery.html')
    s=open(fp,encoding='utf-8').read()
    if 'bundle-builder.html' in s: print('gallery already has builder'); return
    card=('<a href="bundle-builder.html" target="_blank" class="card group">'
      '<div class="thumb"><iframe src="bundle-builder.html" loading="lazy" scrolling="no" tabindex="-1" title="Chum Box Builder"></iframe><span class="veil"></span></div>'
      '<div class="meta"><div class="row"><span class="dot" style="background:#e4177e"></span><span class="idx">configurator</span><span class="open">Open ↗</span></div>'
      '<h3>Chum Box Builder</h3><p>Build-your-own bundle — gummies drop into the box live; 15/30/45 tabs per chum.</p></div></a>')
    anchor='<h2>Product Pages</h2>'
    i=s.index(anchor); j=s.index('</div>',i)+6  # end of ghead div
    s=s[:j]+card+s[j:]
    open(fp,'w',encoding='utf-8').write(s)
    print('gallery: builder card added')

if __name__=='__main__':
    for num,(dark,acc) in ACCENTS.items():
        fp=os.path.join(ROOT,'index%d.html'%num)
        if os.path.exists(fp):
            inject(fp,dark,acc); print('chum box -> index%d.html'%num)
    build_standalone()
    patch_gallery()
