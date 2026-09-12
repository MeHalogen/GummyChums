/* Meet our Chums — the pinned sideways ride.
   Lifted out of gc-home.liquid verbatim: it is pure JS with no Liquid, the
   section is smaller for it, this is cacheable, and theme check's LiquidHTML
   parser stops reporting the section's inline <script> as never closed. */
(function(){
  var sec=document.getElementById('gh-hs'), pin=document.getElementById('gh-hs-pin'), track=document.getElementById('gh-hs-track');
  if(!sec||!pin||!track) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var travel=0, span=0, last='', live=false, tk=false, vhPx=0;
  /* One viewport, measured the only way that cannot move: ask the browser for
     100svh. iOS shifts innerHeight AND documentElement.clientHeight as its
     toolbar collapses, and the hero pin carries padding on top of its 100svh
     (nothing here sets border-box globally — Dawn scopes that to details > *),
     so neither of those is the ruler. A span, not a div: base.css hides empty
     divs. Read once per gauge; svh cannot change without a resize. */
  function svh(){
    var el=document.createElement('span');
    el.style.cssText='position:absolute;top:0;left:0;width:0;height:100svh;visibility:hidden;pointer-events:none';
    document.body.appendChild(el);
    var h=el.offsetHeight; el.parentNode.removeChild(el);
    return h||document.documentElement.clientHeight;
  }
  /* A phone flick covers a lot of page, so the ride is given more scroll than it
     has sideways travel — each Chum then holds the screen long enough to read.
     Desktop stays 1:1, which was signed off. */
  function ratio(){ return innerWidth <= 749 ? 1.7 : 1; }
  function place(force){
    tk=false;
    var r=sec.getBoundingClientRect();
    var on=r.bottom>0&&r.top<vhPx;
    on=on&&!!span;   /* no compositing layer on a phone, which no longer transforms */
    if(on!==live){live=on;sec.classList.toggle('gh-hs--live',on);}
    if(!span||(!on&&!force)) return;
    var p=span?Math.min(Math.max(-r.top/span,0),1):0;
    var x=(-p*travel).toFixed(1);
    if(x!==last){last=x;track.style.transform='translate3d('+x+'px,0,0)';}
  }
  /* one pinned screen plus the scroll distance the ride is given: the sideways
     travel on desktop, 1.7x it on a phone so each Chum holds the screen */
  function measure(){
    sec.classList.add('gh-hs--js');
    vhPx=svh();
    /* On a phone, travel is read off the LAST card itself. Track-width minus one
       screen ended the ride the moment that card's right edge met the screen's,
       so it could never reach where the other two sit: on screen a third as long
       as its neighbours, which is what read as unreachable. Measuring the card
       also keeps this clear of how an engine sizes a max-content box carrying
       padding. The phone ride now ends with the last Chum centred like the rest.
       Desktop keeps the original sum — it was signed off and its cards are half
       a screen wide, so they were never starved this way. */
    var contW=pin.clientWidth;
    if(innerWidth<=749){
      var kids=track.children, lastEl=kids[kids.length-1];
      travel=Math.max(0, lastEl.offsetLeft - Math.max(0,(contW-lastEl.offsetWidth)/2));
    }else{
      travel=Math.max(0, track.offsetWidth-contW);   /* desktop, exactly as signed off */
    }
    span=travel*ratio();
    sec.style.height=(pin.offsetHeight+span)+'px';
    last=''; place(true);
  }
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(function(){place(false);});}},{passive:true});
  /* iOS resizes on every toolbar show/hide; only a width change alters the travel */
  var w=innerWidth; addEventListener('resize',function(){if(innerWidth!==w){w=innerWidth;measure();}else{place(true);}});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(measure);
  measure();
})();
