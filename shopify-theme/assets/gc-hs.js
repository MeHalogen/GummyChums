/* Meet our Chums — the pinned sideways ride.
   Lifted out of gc-home.liquid verbatim: it is pure JS with no Liquid, the
   section is smaller for it, this is cacheable, and theme check's LiquidHTML
   parser stops reporting the section's inline <script> as never closed. */
(function(){
  var sec=document.getElementById('gh-hs'), pin=document.getElementById('gh-hs-pin'), track=document.getElementById('gh-hs-track');
  if(!sec||!pin||!track) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  sec.classList.add('gh-hs--js');
  var travel=0, span=0, last='', live=false, tk=false;
  /* A phone flick covers roughly a thousand pixels, which at 1:1 is the entire
     ride — you never actually see the third Chum. On phones the section is made
     longer than the sideways travel, so the same flick moves the track less far
     and each Chum gets time on screen. Desktop keeps 1:1, which was right. */
  function ratio(){ return innerWidth <= 749 ? 1.7 : 1; }
  function place(force){
    tk=false;
    var r=sec.getBoundingClientRect();
    var on=r.bottom>0&&r.top<innerHeight;
    if(on!==live){live=on;sec.classList.toggle('gh-hs--live',on);}
    if(!on&&!force) return;
    var p=span?Math.min(Math.max(-r.top/span,0),1):0;
    var x=(-p*travel).toFixed(1);
    if(x!==last){last=x;track.style.transform='translate3d('+x+'px,0,0)';}
  }
  /* one pinned screen plus the scroll distance the ride is given — equal to the
     sideways travel on desktop, 1.7x it on a phone */
  function measure(){
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
