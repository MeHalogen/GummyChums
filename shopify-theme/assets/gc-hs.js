/* Meet our Chums — the pinned sideways ride.
   Lifted out of gc-home.liquid verbatim: it is pure JS with no Liquid, the
   section is smaller for it, this is cacheable, and theme check's LiquidHTML
   parser stops reporting the section's inline <script> as never closed. */
(function(){
  var sec=document.getElementById('gh-hs'), pin=document.getElementById('gh-hs-pin'), track=document.getElementById('gh-hs-track');
  if(!sec||!pin||!track) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  sec.classList.add('gh-hs--js');
  var travel=0, last='', live=false, tk=false;
  function place(force){
    tk=false;
    var r=sec.getBoundingClientRect();
    var on=r.bottom>0&&r.top<innerHeight;
    if(on!==live){live=on;sec.classList.toggle('gh-hs--live',on);}
    if(!on&&!force) return;
    var p=travel?Math.min(Math.max(-r.top/travel,0),1):0;
    var x=(-p*travel).toFixed(1);
    if(x!==last){last=x;track.style.transform='translate3d('+x+'px,0,0)';}
  }
  /* the section is exactly one pinned screen plus the sideways travel, so
     vertical and horizontal distance match 1:1 */
  function measure(){
    travel=Math.max(0,track.offsetWidth-pin.clientWidth);
    sec.style.height=(pin.offsetHeight+travel)+'px';
    last=''; place(true);
  }
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(function(){place(false);});}},{passive:true});
  /* iOS resizes on every toolbar show/hide; only a width change alters the travel */
  var w=innerWidth; addEventListener('resize',function(){if(innerWidth!==w){w=innerWidth;measure();}else{place(true);}});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(measure);
  measure();
})();
