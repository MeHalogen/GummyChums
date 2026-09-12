/* Meet our Chums — the pinned sideways ride.
   Lifted out of gc-home.liquid verbatim: it is pure JS with no Liquid, the
   section is smaller for it, this is cacheable, and theme check's LiquidHTML
   parser stops reporting the section's inline <script> as never closed. */
(function(){
  var sec=document.getElementById('gh-hs'), pin=document.getElementById('gh-hs-pin'), track=document.getElementById('gh-hs-track');
  if(!sec||!pin||!track) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var travel=0, span=0, last='', live=false, tk=false;
  /* Phones do not get the pinned ride at all. Slowing it down did not work:
     iOS collapses its toolbar mid-scroll, so a scroll-linked transform judders,
     and a flick still covers most of the track, which left the last Chum out of
     reach. A phone already has a gesture for this — swiping sideways — so the
     strip stays a plain swipeable, snapping row there. Desktop keeps the ride. */
  function pinned(){ return innerWidth > 749; }
  function place(force){
    tk=false;
    var r=sec.getBoundingClientRect();
    var on=r.bottom>0&&r.top<innerHeight;
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
    if(!pinned()){                       /* hand the section back to the browser */
      sec.classList.remove('gh-hs--js');
      sec.style.height=''; track.style.transform='';
      travel=0; span=0; last=''; return;
    }
    sec.classList.add('gh-hs--js');
    travel=Math.max(0,track.offsetWidth-pin.clientWidth);
    span=travel;
    sec.style.height=(pin.offsetHeight+span)+'px';
    last=''; place(true);
  }
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(function(){place(false);});}},{passive:true});
  /* iOS resizes on every toolbar show/hide; only a width change alters the travel */
  var w=innerWidth; addEventListener('resize',function(){if(innerWidth!==w){w=innerWidth;measure();}else{place(true);}});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(measure);
  measure();
})();
