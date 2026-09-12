/* Meet our Chums — the pinned sideways ride.
   Lifted out of gc-home.liquid verbatim: it is pure JS with no Liquid, the
   section is smaller for it, this is cacheable, and theme check's LiquidHTML
   parser stops reporting the section's inline <script> as never closed. */
(function(){
  var sec=document.getElementById('gh-hs'), pin=document.getElementById('gh-hs-pin'), track=document.getElementById('gh-hs-track');
  if(!sec||!pin||!track) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var travel=0, span=0, last='', live=false, tk=false;
  /* iOS's toolbar collapses mid-scroll, which changes innerHeight but not the
     layout viewport the pin is sized against. Reading the layout viewport keeps
     every number here still while that happens. */
  function vh(){ return document.documentElement.clientHeight; }
  /* A phone flick covers a lot of page, so the ride is given more scroll than it
     has sideways travel — each Chum then holds the screen long enough to read.
     Desktop stays 1:1, which was signed off. */
  function ratio(){ return innerWidth <= 749 ? 1.7 : 1; }
  function place(force){
    tk=false;
    var r=sec.getBoundingClientRect();
    var on=r.bottom>0&&r.top<vh();
    on=on&&!!span;   /* no compositing layer on a phone, which no longer transforms */
    if(on!==live){live=on;sec.classList.toggle('gh-hs--live',on);}
    if(!span||(!on&&!force)) return;
    var p=span?Math.min(Math.max(-r.top/span,0),1):0;
    var x=(-p*travel).toFixed(1);
    if(x!==last){last=x;track.style.transform='translate3d('+x+'px,0,0)';}
  }
  /* one pinned screen plus the scroll distance the ride is given, which equals the
     sideways travel so the track keeps pace with the scroll exactly 1:1 */
  function measure(){
    sec.classList.add('gh-hs--js');
    /* The track carries trailing space equal to one screen minus one card, so
       this travel reaches the LAST card's own offset rather than stopping when
       its right edge hits the right edge. Without that the final Chum only ever
       slid flush against the edge, on screen for a third as long as the other
       two — which is why it read as unreachable, and why stretching the scroll
       distance could not fix it: that scaled the short window too. */
    travel=Math.max(0,track.offsetWidth-pin.clientWidth);
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
