# -*- coding: utf-8 -*-
"""
Kinetic copy upgrade: replaces the (identical, flat) brand-story section on
index15-24 with a theme-voiced kinetic manifesto — animated strikethroughs,
marker-highlight sweeps, self-drawing squiggle underline, staggered word
reveals. Copy is short and campaign-style; the punchline differs per theme.
Run from repo root:  python3 tools/upgrade_story.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (dark?, accent, punchline) per premium page — punchline ties to its concept
SKIN = {
 15:(1,'#ff7ab8','We chose glow.'),
 16:(0,'#ff5c8a','We chose squish.'),
 17:(0,'#8b5cf6','We chose silk.'),
 18:(1,'#38bdf8','We chose orbit.'),
 19:(0,'#e44bd3','We chose joy.'),
 20:(1,'#ff7ab8','We chose the night shift.'),
 21:(0,'#ff5c8a','We chose bounce.'),
 22:(0,'#e44bd3','We chose the deep dive.'),
 23:(0,'#8a6d3b','We chose taste.'),
 24:(1,'#ffd23f','We chose every colour.'),
}

def rgba(hexc, a):
    h=hexc.lstrip('#')
    return 'rgba(%d,%d,%d,%s)'%(int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)

CHIPS=['that 9am exam','the 3-hour meeting','leg day','a road trip','another Monday','lights out']
WORDS=['Happy.','Confident.','Energized.','Comforted.','Curious.','Proud.']
NEVERS=['clinical','preachy','childish','complicated']
VALUES=[('Within reach','premium should never mean pricey.'),
        ('Joy, non-negotiable','if it doesn&rsquo;t make you smile, it doesn&rsquo;t ship.'),
        ('Trust you can read','the label says everything. Every time.')]

def kinetic_css(acc, dark):
    ink = '#ffffff' if dark else 'currentColor'
    panel = 'rgba(255,255,255,.06)' if dark else 'rgba(0,0,0,.05)'
    mark = rgba(acc,'.30')
    return '''
  /* ===== kinetic manifesto ===== */
  .kc-kick{letter-spacing:.35em;font-size:12px;text-transform:uppercase;opacity:.6;color:'''+acc+''';margin-bottom:20px;font-weight:700}
  .kc-big{font-size:clamp(2rem,6vw,4.4rem);line-height:1.08;font-weight:800;letter-spacing:-.01em}
  .kc-strike{position:relative;white-space:nowrap;opacity:.5}
  .kc-strike::after{content:"";position:absolute;left:-2%;right:-2%;top:52%;height:.09em;border-radius:99px;background:'''+acc+''';transform:scaleX(0);transform-origin:left center;transition:transform .7s cubic-bezier(.77,0,.18,1)}
  .kc.go .kc-strike:nth-of-type(1)::after{transform:scaleX(1);transition-delay:.15s}
  .kc.go .kc-strike:nth-of-type(2)::after{transform:scaleX(1);transition-delay:.5s}
  .kc-mark{background-image:linear-gradient('''+mark+''','''+mark+''');background-repeat:no-repeat;background-size:0% 82%;background-position:0 62%;transition:background-size .8s .85s cubic-bezier(.77,0,.18,1);padding:0 .1em}
  .kc.go .kc-mark{background-size:100% 82%}
  .kc-mission{font-size:clamp(1.7rem,4.6vw,3.2rem);font-weight:800;text-align:center;margin:70px 0 64px}
  .kc-treat{color:'''+acc+''';position:relative;display:inline-block;padding-bottom:.12em}
  .kc-squig{position:absolute;left:0;right:0;bottom:-.08em;width:100%;height:.32em}
  .kc-squig path{stroke:'''+acc+''';stroke-width:8;fill:none;stroke-linecap:round;stroke-dasharray:320;stroke-dashoffset:320;transition:stroke-dashoffset 1.1s 1.05s cubic-bezier(.5,0,.2,1)}
  .kc.go .kc-squig path{stroke-dashoffset:0}
  .kc-h3{font-weight:800;font-size:1.05rem;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin:56px 0 18px}
  .kc-chip{display:inline-block;background:'''+panel+''';border-radius:999px;padding:.55rem 1.1rem;font-weight:700;font-size:.92rem;margin:0 .5rem .6rem 0;opacity:0;transform:translateY(16px) scale(.9);transition:opacity .5s,transform .55s cubic-bezier(.34,1.56,.64,1)}
  .kc.go .kc-chip{opacity:1;transform:none}
  .kc-chip:hover{animation:kc-jig .4s ease}
  @keyframes kc-jig{25%{transform:rotate(-2.5deg) scale(1.05)}75%{transform:rotate(2.5deg) scale(1.05)}}
  .kc-word{display:inline-block;font-size:clamp(1.7rem,4.6vw,3.1rem);font-weight:800;margin:0 .55em .2em 0;opacity:0;transform:translateY(34px) rotate(3deg);transition:opacity .55s,transform .6s cubic-bezier(.2,.8,.2,1);cursor:default}
  .kc.go .kc-word{opacity:1;transform:none}
  .kc-word:nth-child(even){color:'''+acc+'''}
  .kc-word:hover{animation:kc-squi .45s ease}
  @keyframes kc-squi{35%{transform:scale(1.15,.85)}70%{transform:scale(.92,1.08)}}
  .kc-never{font-size:1.05rem;font-weight:600;opacity:.85;margin-top:60px;line-height:2.1}
  .kc-nv{position:relative;white-space:nowrap;margin:0 .18em;opacity:.55}
  .kc-nv::after{content:"";position:absolute;left:-3%;right:-3%;top:52%;height:.11em;border-radius:99px;background:'''+acc+''';transform:scaleX(0);transform-origin:left center;transition:transform .5s cubic-bezier(.77,0,.18,1)}
  .kc.go .kc-nv::after{transform:scaleX(1)}
  .kc-val{background:'''+panel+''';border-radius:1.4rem;padding:1.4rem 1.5rem}
  .kc-val b{color:'''+acc+''';font-size:1.15rem;display:block;margin-bottom:.3rem}
'''

def section_html(acc, punch):
    chips=''.join('<span class="kc-chip" style="transition-delay:%dms">%s</span>'%(150+i*90,c) for i,c in enumerate(CHIPS))
    words=''.join('<span class="kc-word" style="transition-delay:%dms">%s</span>'%(120+i*110,w) for i,w in enumerate(WORDS))
    nevers=' '.join('<span class="kc-nv" style="transition-delay:%sms">%s</span>'%(200+i*220,n) for i,n in enumerate(NEVERS))
    vals=''.join('<div class="kc-val"><b>%s</b><span style="opacity:.65">%s</span></div>'%(a,b) for a,b in VALUES)
    return ('<section class="kc" id="kc-manifesto" style="border-top:1px solid rgba(128,128,128,.18)">'
      '<div class="max-w-5xl mx-auto px-5 md:px-10 py-24 md:py-28">'
      '<p class="kc-kick">The why · straight from the founder</p>'
      '<h2 class="kc-big">Pills feel like <span class="kc-strike">homework.</span><br/>'
      'Powders feel like <span class="kc-strike">chemistry class.</span><br/>'
      '<span class="kc-mark">'+punch+'</span></h2>'
      '<p style="opacity:.65;max-width:34rem;margin-top:26px;font-size:1.05rem;line-height:1.7">Born in India, on a shelf crowded with bottles nobody finished. One question changed everything: '
      '<b style="opacity:1">why can&rsquo;t the healthiest thing you do all day be the tastiest?</b> &ldquo;Chums&rdquo; means friends. That&rsquo;s the whole plan.</p>'
      '<div class="kc-mission">wellness = <span class="kc-treat">a treat'
      '<svg class="kc-squig" viewBox="0 0 100 14" preserveAspectRatio="none"><path d="M2 8 Q 10 2, 20 8 T 40 8 T 60 8 T 80 8 T 98 8"/></svg>'
      '</span> <span style="opacity:.45">not a task.</span></div>'
      '<h3 class="kc-h3">Grab a Chum before&hellip;</h3><div>'+chips+'</div>'
      '<h3 class="kc-h3">One chew should make you feel</h3><div>'+words+'</div>'
      '<p class="kc-never">And the fine print, in big letters: we will never be '+nevers+' — pinky promise, in writing. '
      'Not a supplement company. Not a candy brand. A lifestyle brand India actually loves.</p>'
      '<div class="grid sm:grid-cols-3 gap-4 mt-12">'+vals+'</div>'
      '</div>'
      '<script>(function(){var k=document.getElementById("kc-manifesto");'
      'function go(){k.classList.add("go");}'
      'new IntersectionObserver(function(es,o){es.forEach(function(en){if(en.isIntersecting){go();o.disconnect();}})},{threshold:0,rootMargin:"0px 0px -12% 0px"}).observe(k);'
      'addEventListener("scroll",function f(){if(k.getBoundingClientRect().top<innerHeight*.85){go();removeEventListener("scroll",f);}},{passive:true});'
      'if(k.getBoundingClientRect().top<innerHeight)go();})();</script>'
      '</section>')

def upgrade(num):
    fp=os.path.join(ROOT,'index%d.html'%num)
    s=open(fp,encoding='utf-8').read()
    dark,acc,punch=SKIN[num]
    marker='The story behind GummyChums'
    if marker in s:
        i=s.index(marker)
        start=s.rindex('<section',0,i)
        end=s.index('</section>',i)+len('</section>')
        s=s[:start]+section_html(acc,punch)+s[end:]
    elif 'kc-manifesto' in s:
        i=s.index('kc-manifesto')
        start=s.rindex('<section',0,i)
        end=s.index('</section>',i)+len('</section>')
        s=s[:start]+section_html(acc,punch)+s[end:]
    else:
        print('!! no story section in index%d'%num); return
    if '.kc-kick{' not in s:
        s=s.replace('</style>', kinetic_css(acc,dark)+'\n</style>',1)
    else:
        s=re.sub(r'/\* ===== kinetic manifesto ===== \*/.*?(?=\n</style>)', kinetic_css(acc,dark).strip(), s, flags=re.S)
    open(fp,'w',encoding='utf-8').write(s)
    print('kinetic manifesto -> index%d.html'%num)

if __name__=='__main__':
    for n in SKIN: upgrade(n)
