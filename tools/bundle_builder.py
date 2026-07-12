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
  .bb-drop{position:relative;height:340px;border:2px dashed var(--bb-line);border-radius:14px;overflow:hidden;transition:border-color .3s}
  @media(max-width:560px){.bb-drop{height:260px}}
  .bb-drop canvas{display:block;width:100%;height:100%;touch-action:none}
  .bb-drop.bb-has canvas{cursor:grab}
  .bb-swirl{position:absolute;right:10px;bottom:8px;font-size:.72rem;font-weight:700;color:var(--bb-soft);opacity:0;
    pointer-events:none;transition:opacity .4s;letter-spacing:.06em;text-transform:uppercase}
  .bb-drop.bb-has .bb-swirl{opacity:.6}
  .bb-reset{border:0;background:transparent;color:var(--bb-soft);font-size:1.15rem;font-weight:800;cursor:pointer;
    line-height:1;padding:.1rem .3rem;transition:color .2s,transform .3s}
  .bb-reset:hover{color:var(--bb-acc);transform:rotate(-180deg)}
  .bb-drop.bb-has{border-style:solid;border-color:var(--bb-acc)}
  .bb-drop-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;
    color:var(--bb-soft);font-weight:600;font-size:.92rem;pointer-events:none;transition:opacity .3s}
  .bb-drop.bb-has .bb-drop-empty{opacity:0}
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
  .bb-qtywrap{display:flex;align-items:center;gap:.35rem;flex:0 0 auto}
  .bb-minus{border:2px solid var(--bb-acc);background:transparent;color:var(--bb-acc);border-radius:999px;width:2.4rem;height:2.4rem;
    font-size:1.2rem;font-weight:800;cursor:pointer;transition:transform .12s;line-height:1}
  .bb-minus:active{transform:scale(.9)}
  .bb-qty{font-weight:800;min-width:1.1rem;text-align:center}
  .bb-row:not(.bb-on) .bb-minus,.bb-row:not(.bb-on) .bb-qty{display:none}
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
          '<span class="bb-qtywrap">'
          '<button class="bb-minus" aria-label="Remove one '+name+'" data-hot>–</button>'
          '<span class="bb-qty">0</span>'
          '<button class="bb-add" aria-label="Add '+name+' to box" data-hot>+</button>'
          '</span>'
          '</div>')
    return ('<!-- BB:START -->\n<section id="bb-builder">'
      '<div class="bb-wrap">'
      '<p class="bb-kick">Build your own · mix any of the six</p>'
      '<h2 class="bb-title">Pack your Chum Box.</h2>'
      '<p class="bb-sub">Pick your gummies, pick your size — watch every single tab tumble in, one by one. '
      'One box, your rules: 15 tabs ₹349 · 30 tabs ₹549 · 45 tabs ₹749 per jar. Love one? Stack it twice. Or five times — your box.</p>'
      '<div class="bb-grid">'
      '<div class="bb-boxcol">'
        '<div class="bb-box" id="bb-box">'
          '<div class="bb-lid"></div>'
          '<div class="bb-label"><span>GummyChums · MY CHUM BOX</span><span style="display:flex;gap:.55rem;align-items:center"><small id="bb-count">empty</small><button class="bb-reset" id="bb-reset" title="Empty the box" aria-label="Empty the box" data-hot>&#8634;</button></span></div>'
          '<div class="bb-drop" id="bb-drop"><canvas id="bb-canvas"></canvas><span class="bb-drop-empty" id="bb-empty">Your box is waiting — add a chum →</span><span class="bb-swirl">drag inside to swirl</span></div>'
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

BB_JS = r"""
<script>
/* ===== Chum Box v4: adaptive-size physics jar, swirl, reset, per-jar cart ===== */
(function(){
  var builder=document.getElementById('bb-builder'); if(!builder)return;
  var drop=document.getElementById('bb-drop'), boxEl=document.getElementById('bb-box');
  var cv=document.getElementById('bb-canvas'), cx=cv.getContext('2d');
  var box=[];
  function inr(n){return '₹'+n.toLocaleString('en-IN');}

  /* ---------- physics (adaptive radius: few tabs = big juicy gummies) ---------- */
  var R=16, targetR=16, MAXB=300, GRAV=.42, REST=.34, W=520, H=340, DPR=Math.min(2,window.devicePixelRatio||1);
  var bodies=[], queue=[], raf=null, visible=true;
  var reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function calcR(){
    var tabs=0; box.forEach(function(it){tabs+=it.tabs;});
    targetR=Math.max(8,Math.min(17,Math.sqrt((W*H*.44)/(Math.max(tabs,14)*Math.PI))));
  }
  function sizeCanvas(){
    W=cv.clientWidth||520; H=cv.clientHeight||340;
    cv.width=Math.round(W*DPR); cv.height=Math.round(H*DPR);
    cx.setTransform(DPR,0,0,DPR,0,0);
    calcR();
    bodies.forEach(function(b){ b.x=Math.max(R+3,Math.min(W-R-3,b.x)); b.rest=0; });
    draw(); wake();
  }
  if(window.ResizeObserver) new ResizeObserver(sizeCanvas).observe(cv);
  sizeCanvas();
  if(window.IntersectionObserver) new IntersectionObserver(function(es){
    es.forEach(function(en){ visible=en.isIntersecting; if(visible)wake(); });
  },{threshold:0}).observe(cv);

  function spawn(c,g){
    if(bodies.length>=MAXB)return;
    bodies.push({x:R+6+Math.random()*(W-2*R-12), y:-R-4-Math.random()*30,
      vx:(Math.random()-.5)*2, vy:1+Math.random()*1.5, c:c, g:g,
      rot:Math.random()*6.28, sq:.92+Math.random()*.16, rest:0});
  }
  function settleInstant(c,g){
    if(bodies.length>=MAXB)return;
    var i=bodies.length, per=Math.max(3,Math.floor((W-14)/(2*R+2)));
    var row=Math.floor(i/per), col=i%per;
    bodies.push({x:7+R+col*(2*R+2)+(row%2?R:0), y:H-R-4-row*(2*R-3),
      vx:0,vy:0,c:c,g:g,rot:Math.random()*6.28,sq:.92+Math.random()*.16,rest:999});
  }
  function pourJar(gid,color,n){
    calcR();
    if(reduced){ for(var i=0;i<n;i++)settleInstant(color,gid); draw(); return; }
    var at=performance.now()+360;
    for(var i=0;i<n;i++) queue.push({c:color,g:gid,at:at+i*24});
    bodies.forEach(function(b){b.rest=0;});
    wake();
  }
  function removeJar(gid,n){
    for(var i=queue.length-1;i>=0&&n>0;i--){ if(queue[i].g===gid){queue.splice(i,1);n--;} }
    for(var j=bodies.length-1;j>=0&&n>0;j--){ if(bodies[j].g===gid){bodies.splice(j,1);n--;} }
    calcR(); bodies.forEach(function(b){b.rest=0;});
    draw(); wake();
  }
  function clearSim(){ bodies.length=0; queue.length=0; calcR(); draw(); }

  function sim(){
    var now=performance.now(), awake=0, i, b;
    while(queue.length&&queue[0].at<=now){ var q=queue.shift(); spawn(q.c,q.g); }
    if(Math.abs(targetR-R)>.12){ R+=(targetR-R)*.08; awake++; bodies.forEach(function(bb){bb.rest=0;}); }
    for(i=0;i<bodies.length;i++){
      b=bodies[i];
      if(b.rest>55) continue;
      awake++;
      b.vy+=GRAV; b.x+=b.vx; b.y+=b.vy; b.vx*=.994;
      if(b.x<R+3){b.x=R+3;b.vx*=-.42;} else if(b.x>W-R-3){b.x=W-R-3;b.vx*=-.42;}
      if(b.y>H-R-3){b.y=H-R-3;b.vy*=-REST;b.vx*=.9; if(Math.abs(b.vy)<.6)b.vy=0;}
      if(b.y<-200){b.y=-R;b.vy=1;}
    }
    var cell=2*R+2, cols=Math.max(1,Math.ceil(W/cell)), rows=Math.max(1,Math.ceil(H/cell)), grid={};
    for(i=0;i<bodies.length;i++){ b=bodies[i];
      var k=Math.max(0,Math.min(cols-1,(b.x/cell)|0))+','+Math.max(0,Math.min(rows-1,(b.y/cell)|0));
      (grid[k]||(grid[k]=[])).push(i);
    }
    function pair(a,c2){
      var A=bodies[a],B=bodies[c2];
      if(A.rest>55&&B.rest>55)return;
      var dx=B.x-A.x,dy=B.y-A.y,d2=dx*dx+dy*dy,min=2*R;
      if(d2>=min*min||d2===0)return;
      var d=Math.sqrt(d2),nx=dx/d,ny=dy/d,ov=(min-d)/2;
      if(A.rest<=55){A.x-=nx*ov;A.y-=ny*ov;} else {B.x+=nx*ov;B.y+=ny*ov;}
      if(B.rest<=55){B.x+=nx*ov;B.y+=ny*ov;} else {A.x-=nx*ov;A.y-=ny*ov;}
      var rvx=B.vx-A.vx,rvy=B.vy-A.vy,vn=rvx*nx+rvy*ny;
      if(vn<0){var jimp=-(1+REST*.8)*vn/2;
        if(A.rest<=55){A.vx-=jimp*nx;A.vy-=jimp*ny;}
        if(B.rest<=55){B.vx+=jimp*nx;B.vy+=jimp*ny;}
        if(ov>R*.45){A.rest=0;B.rest=0;}
      }
    }
    for(var key in grid){
      var listA=grid[key], parts=key.split(','), gx=+parts[0], gy=+parts[1];
      for(i=0;i<listA.length;i++){
        for(var j2=i+1;j2<listA.length;j2++)pair(listA[i],listA[j2]);
        var neigh=[(gx+1)+','+gy, gx+','+(gy+1), (gx+1)+','+(gy+1), (gx-1)+','+(gy+1)];
        for(var nn=0;nn<4;nn++){var lb=grid[neigh[nn]];if(!lb)continue;
          for(var m=0;m<lb.length;m++)pair(listA[i],lb[m]);}
      }
    }
    for(i=0;i<bodies.length;i++){ b=bodies[i];
      if(b.rest>55)continue;
      if(Math.abs(b.vx)+Math.abs(b.vy)<.35&&b.y>H*.35){b.rest++;}else b.rest=0;
      b.rot+=b.vx*.02;
    }
    return awake+queue.length;
  }
  function draw(){
    cx.clearRect(0,0,W,H);
    // glass-jar dressing: floor shadow + diagonal shine streaks
    var fg=cx.createLinearGradient(0,H-30,0,H);
    fg.addColorStop(0,'rgba(0,0,0,0)');fg.addColorStop(1,'rgba(0,0,0,.08)');
    cx.fillStyle=fg;cx.fillRect(0,H-30,W,30);
    cx.save();cx.globalAlpha=.05;cx.fillStyle='#fff';
    cx.beginPath();cx.moveTo(W*.14,0);cx.lineTo(W*.24,0);cx.lineTo(W*.06,H);cx.lineTo(W*-.04,H);cx.closePath();cx.fill();
    cx.beginPath();cx.moveTo(W*.30,0);cx.lineTo(W*.34,0);cx.lineTo(W*.16,H);cx.lineTo(W*.12,H);cx.closePath();cx.fill();
    cx.restore();
    for(var i=0;i<bodies.length;i++){var b=bodies[i];
      cx.save();cx.translate(b.x,b.y);cx.rotate(b.rot);cx.scale(b.sq,1/b.sq);
      cx.beginPath();cx.arc(0,0,R,0,6.2832);cx.fillStyle=b.c;cx.fill();
      cx.globalAlpha=.5;cx.beginPath();cx.arc(-R*.32,-R*.36,R*.42,0,6.2832);cx.fillStyle='#fff';cx.fill();
      cx.globalAlpha=.18;cx.beginPath();cx.arc(R*.3,R*.42,R*.28,0,6.2832);cx.fillStyle='#fff';cx.fill();
      cx.globalAlpha=.09;cx.beginPath();cx.arc(R*.14,R*.2,R*.8,0,6.2832);cx.fillStyle='#000';cx.fill();
      cx.restore();
    }
  }
  function step(){ raf=null; var active=sim(); draw(); if(visible&&active>0) raf=requestAnimationFrame(step); }
  function wake(){ if(raf===null&&!reduced&&visible) raf=requestAnimationFrame(step); }
  window.__bbFlush=function(){ while(queue.length){var q=queue.shift();settleInstant(q.c,q.g);} draw(); };

  // swirl: dragging (or moving) across the jar pushes gummies around
  var lastP=null;
  function swirl(e){
    var r=cv.getBoundingClientRect(), x=e.clientX-r.left, y=e.clientY-r.top;
    if(lastP){
      var dx=x-lastP.x, dy=y-lastP.y, reach=R*3.2;
      if(Math.abs(dx)+Math.abs(dy)>1){
        for(var i=0;i<bodies.length;i++){var b=bodies[i];
          var ddx=b.x-x, ddy=b.y-y;
          if(ddx*ddx+ddy*ddy<reach*reach){
            b.vx+=Math.max(-6,Math.min(6,dx*.28)); b.vy+=Math.max(-6,Math.min(6,dy*.28))-.6;
            b.rest=0;
          }
        }
        wake();
      }
    }
    lastP={x:x,y:y};
  }
  cv.addEventListener('pointermove',swirl,{passive:true});
  cv.addEventListener('pointerleave',function(){lastP=null;},{passive:true});

  /* ---------- decorative arc ---------- */
  var GSVG=function(c,sz){return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:'+sz+'px;height:'+sz+'px;display:block"><path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="'+c+'"/><ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/><ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>';};
  function fly(fromEl,color){
    try{
      var f=fromEl.getBoundingClientRect(), t=drop.getBoundingClientRect();
      var el=document.createElement('div');el.className='bb-fly';el.innerHTML=GSVG(color,40);
      document.body.appendChild(el);
      var sx=f.left+f.width/2-20, sy=f.top+f.height/2-20;
      var ex=t.left+t.width/2-20, ey=t.top+20;
      el.animate([
        {transform:'translate('+sx+'px,'+sy+'px) scale(1)'},
        {transform:'translate('+((sx+ex)/2)+'px,'+(Math.min(sy,ey)-110)+'px) scale(1.2) rotate(120deg)',offset:.55},
        {transform:'translate('+ex+'px,'+ey+'px) scale(.6) rotate(300deg)',opacity:.85}
      ],{duration:540,easing:'cubic-bezier(.45,-.15,.35,1)'}).onfinish=function(){
        el.remove();
        boxEl.classList.remove('bb-land');void boxEl.offsetWidth;boxEl.classList.add('bb-land');
      };
      setTimeout(function(){if(el.parentNode)el.remove();},1400);
    }catch(e){}
  }

  /* ---------- state / summary / per-jar cart ---------- */
  function groups(){
    var order=[],map={};
    box.forEach(function(it){var k=it.gid+'|'+it.tabs;
      if(!map[k]){map[k]={it:it,n:0};order.push(k);} map[k].n++;});
    return order.map(function(k){return map[k];});
  }
  function render(){
    var gs=groups(), total=0, tabs=0, lines='';
    gs.forEach(function(g){
      lines+='<div class="bb-sumline"><span><b>'+g.it.name+'</b> · '+g.it.tabs+' tabs'+(g.n>1?' ×'+g.n:'')+'</span><span>'+inr(g.it.price*g.n)+'</span></div>';
      total+=g.it.price*g.n; tabs+=g.it.tabs*g.n;
    });
    drop.classList.toggle('bb-has',box.length>0);
    document.getElementById('bb-lines').innerHTML=lines||'<div class="bb-sumline"><span>Nothing packed yet</span><span>—</span></div>';
    document.getElementById('bb-total').textContent=inr(total);
    document.getElementById('bb-tabs').textContent=tabs+' tabs packed'+(tabs?' · every gummy in the jar is one tab':'');
    document.getElementById('bb-count').textContent=box.length?(box.length+(box.length>1?' jars':' jar')):'empty';
    var cta=document.getElementById('bb-cta');
    cta.disabled=!box.length;
    cta.textContent=box.length?('Pack my box · '+box.length+(box.length>1?' jars':' jar')+' · '+inr(total)):'Pack my box → add to bag';
    builder.querySelectorAll('.bb-row').forEach(function(r){
      var id=r.getAttribute('data-bb-id');
      var q=box.filter(function(it){return it.gid===id;}).length;
      r.classList.toggle('bb-on',q>0);
      r.querySelector('.bb-qty').textContent=q;
    });
  }

  builder.addEventListener('click',function(e){
    var sz=e.target.closest('.bb-size');
    if(sz){
      var row=sz.closest('.bb-row');
      row.querySelectorAll('.bb-size').forEach(function(b){b.classList.toggle('bb-sel',b===sz);});
      row.querySelector('.bb-price').textContent=inr(+sz.getAttribute('data-bb-price'));
      return;
    }
    if(e.target.closest('#bb-reset')){ box=[]; clearSim(); render(); return; }
    var minus=e.target.closest('.bb-minus');
    if(minus){
      var rid=minus.closest('.bb-row').getAttribute('data-bb-id');
      for(var i=box.length-1;i>=0;i--){ if(box[i].gid===rid){ removeJar(rid,box[i].tabs); box.splice(i,1); break; } }
      render(); return;
    }
    var add=e.target.closest('.bb-add');
    if(add){
      var row2=add.closest('.bb-row'), sel=row2.querySelector('.bb-size.bb-sel');
      var it={gid:row2.getAttribute('data-bb-id'),name:row2.getAttribute('data-bb-name'),
        color:row2.getAttribute('data-bb-color'),short:row2.getAttribute('data-bb-short'),
        tabs:+sel.getAttribute('data-bb-size'),price:+sel.getAttribute('data-bb-price')};
      box.push(it); render();
      fly(add,it.color); pourJar(it.gid,it.color,it.tabs);
      return;
    }
    if(e.target.closest('#bb-cta')){
      if(!box.length)return;
      var gs=groups();
      try{
        gs.forEach(function(g){
          var id='jar-'+g.it.gid+'-'+g.it.tabs, ex=null;
          for(var i=0;i<cart.length;i++){ if(cart[i].id===id){ex=cart[i];break;} }
          if(ex){ ex.quantity+=g.n; }
          else cart.push({id:id,name:g.it.name+' — '+g.it.tabs+' tabs',price:g.it.price,
            image:'data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z" fill="'+g.it.color+'"/><ellipse cx="35" cy="27" rx="16" ry="10" fill="#fff" opacity=".5" transform="rotate(-25 35 27)"/><ellipse cx="52" cy="62" rx="32" ry="24" fill="#000" opacity=".07"/></svg>'),
            variant:g.it.short.toUpperCase()+' · '+g.it.tabs+' TABS',quantity:g.n});
        });
        syncCart();openCart();
        box=[];clearSim();render();
      }catch(err){alert('Packed! Total '+inr(gs.reduce(function(a,g){return a+g.it.price*g.n;},0)));}
    }
  });
  render();
})();
</script>"""

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
