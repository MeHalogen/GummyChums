/* ============ GummyChums brand interactions — cursor, ripple/splash, reveals ============ */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FLAV = ['#DE1D61', '#8DAA31', '#F9740D'];

  /* ---------- fixed flavour background (coming-soon look, zero scroll cost) ---------- */
  function initBackground() {
    if (document.querySelector('.gc-bg')) return;
    var bg = document.createElement('div');
    bg.className = 'gc-bg';
    bg.setAttribute('aria-hidden', 'true');

    // The three blurred flavour gummies from the coming-soon page, at the size
    // they are there. They were 4 blobs of a FIXED 200-250px here, which on
    // anything bigger than a phone read as small smudges rather than the big
    // soft washes of colour that page has — 52vw is 749px on a 1440 screen,
    // where 230px is a third of that.
    //
    // Sizes, positions, blur and opacity all match deploy/index.html. The one
    // thing deliberately NOT carried over is its drift animation: a blur this
    // large has to be re-rasterised on every frame it moves, and four of them
    // animating was the single biggest cause of scroll jank on this site.
    // Static, they rasterise once and cost nothing after that.
    // Phones take the same three gummies measured against the long side, for the
    // reason the washes in gc-brand.css do: a vw size tuned for a 1440 screen is
    // a smudge on a 393px one. Same proportions, desktop untouched.
    var gummies = innerWidth <= 749 ? [
      { css: 'left:-14vw;top:-4vh;width:52vmax;height:52vmax',    c: 'var(--c-cherry)' },
      { css: 'right:-14vw;top:14vh;width:46vmax;height:46vmax',   c: 'var(--c-mango)' },
      { css: 'left:-4vw;bottom:-8vh;width:50vmax;height:50vmax',  c: 'var(--c-orange)' }
    ] : [
      { css: 'left:-6vw;top:-4vw;width:52vw;height:52vw',   c: 'var(--c-cherry)' },
      { css: 'right:-6vw;top:8vw;width:46vw;height:46vw',   c: 'var(--c-mango)' },
      { css: 'left:20vw;bottom:-10vw;width:50vw;height:50vw', c: 'var(--c-orange)' }
    ];
    gummies.forEach(function (g) {
      var el = document.createElement('i');
      el.style.cssText = g.css + ';background:' + g.c + ';';
      bg.appendChild(el);
    });

    document.body.insertBefore(bg, document.body.firstChild);
  }

  /* ---------- gummy cursor ---------- */
  function initCursor() {
    if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
    document.documentElement.classList.add('gc-cursor');
    var c = document.createElement('div');
    c.id = 'gc-cursor';
    c.setAttribute('aria-hidden', 'true');
    // The blob is drawn entirely in CSS now (see gc-brand.css) — no SVG, no
    // filter. The wrapper carries the hover scale so the outer element's
    // transform stays reserved for position.
    c.innerHTML = '<div class="gc-cursor__in"></div>';
    document.body.appendChild(c);

    /* ---- the three gummies trailing behind ---- */
    /* Chained lerp, straight out of index31: dot 1 chases the pointer, dot 2
       chases dot 1, dot 3 chases dot 2, each with a smaller step, so they
       string out behind and swing wide on a fast flick.

       Two departures from the original, both deliberate.

       It wrote style.left/top every frame, which is layout on every frame.
       These are transform:translate3d, which the compositor handles.

       And it ran its rAF loop forever. This one STOPS: when every dot has
       caught up to within half a pixel and the pointer is not moving, there is
       nothing left to animate, so the loop ends and the next pointermove
       restarts it. A still mouse costs nothing.

       Decorative motion, so reduced motion skips it entirely — the cursor
       itself stays. */
    var trail = [];
    if (!reduce) {
      [0.30, 0.23, 0.16].forEach(function (k, i) {
        // A SPAN, not a div, on purpose. base.css carries
        // `div:empty{display:none}` and these dots are empty by design — pure
        // colour, no content. As divs all three were hidden while their width,
        // colour and transforms applied perfectly, so they were being
        // positioned every frame and never painted. `div:empty` is (0,1,1) and
        // beats a plain class, so .gc-trail{display:block} does not win it;
        // span is simply not in Dawn's list.
        var el = document.createElement('span');
        el.className = 'gc-trail gc-trail--' + (i + 1);
        el.setAttribute('aria-hidden', 'true');
        document.body.appendChild(el);
        trail.push({ el: el, x: innerWidth / 2, y: innerHeight / 2, k: k });
      });
    }
    var tx = innerWidth / 2, ty = innerHeight / 2, raf = null;

    function step() {
      var px = tx, py = ty, moving = false;
      for (var i = 0; i < trail.length; i++) {
        var t = trail[i];
        t.x += (px - t.x) * t.k;
        t.y += (py - t.y) * t.k;
        if (Math.abs(px - t.x) > 0.5 || Math.abs(py - t.y) > 0.5) moving = true;
        t.el.style.transform = 'translate3d(' + t.x + 'px,' + t.y + 'px,0) translate(-50%,-50%)';
        px = t.x; py = t.y;
      }
      raf = moving ? requestAnimationFrame(step) : null;
    }
    function wake() { if (raf == null && trail.length) raf = requestAnimationFrame(step); }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && raf != null) { cancelAnimationFrame(raf); raf = null; }
    });

    // Set the transform directly in the handler. Browsers already coalesce
    // pointermove to one event per frame, so a rAF loop only adds latency and
    // burns the main thread while idle.
    //
    // The hover test is throttled separately: closest() walks every ancestor of
    // the target, and running that on each of 60-120 events per second was
    // making the cursor itself feel laggy. Position stays per-frame smooth;
    // only the grow-on-hover check is sampled.
    var lastHotCheck = 0, HOT_MS = 100;
    addEventListener('pointermove', function (e) {
      c.style.transform = 'translate3d(' + e.clientX + 'px,' + e.clientY + 'px,0) translate(-50%,-50%)';
      if (!c.classList.contains('on')) c.classList.add('on');
      tx = e.clientX; ty = e.clientY;
      for (var n = 0; n < trail.length; n++) {
        if (!trail[n].el.classList.contains('on')) trail[n].el.classList.add('on');
      }
      wake();
      var now = e.timeStamp || performance.now();
      if (now - lastHotCheck < HOT_MS) return;
      lastHotCheck = now;
      var hot = e.target.closest && e.target.closest('a,button,input,summary,[role="button"],.gc-card');
      c.classList.toggle('big', !!hot);
    }, { passive: true });
    document.addEventListener('mouseleave', function () {
      c.classList.remove('on');
      for (var n = 0; n < trail.length; n++) trail[n].el.classList.remove('on');
    });
  }

  /* ---------- click ripple + gummy splash + colour flash ---------- */
  function initRipple() {
    if (reduce) return;
    var flash = document.createElement('div');
    flash.className = 'gc-flash';
    document.body.appendChild(flash);
    var ft = null, ci = 0;

    addEventListener('pointerdown', function (e) {
      var col = FLAV[ci++ % FLAV.length];

      // 1. expanding ring
      var r = document.createElement('span');
      r.className = 'gc-ripple';
      r.style.left = e.clientX + 'px';
      r.style.top = e.clientY + 'px';
      r.style.borderColor = col;
      document.body.appendChild(r);
      setTimeout(function () { r.remove(); }, 780);

      // 2. gummy splash blob
      var s = document.createElement('span');
      s.className = 'gc-splash';
      s.style.cssText += 'left:' + e.clientX + 'px;top:' + e.clientY + 'px;width:34px;height:34px;background:' + col + ';opacity:.75;';
      document.body.appendChild(s);
      s.animate(
        [{ transform: 'translate(-50%,-50%) scale(.25)', opacity: .7 },
         { transform: 'translate(-50%,-50%) scale(14)', opacity: 0 }],
        { duration: 700, easing: 'cubic-bezier(.22,.7,.2,1)' }
      ).onfinish = function () { s.remove(); };

      // 3. little flavour specks flying out
      for (var i = 0; i < 3; i++) {
        (function () {
          var p = document.createElement('span');
          var sz = 5 + Math.random() * 8;
          p.className = 'gc-splash';
          p.style.cssText += 'left:' + e.clientX + 'px;top:' + e.clientY + 'px;width:' + sz + 'px;height:' + sz + 'px;background:' + FLAV[(Math.random() * 3) | 0] + ';opacity:.9;';
          document.body.appendChild(p);
          var a = Math.random() * 6.283, d = 40 + Math.random() * 80;
          p.animate(
            [{ transform: 'translate(-50%,-50%) translate(0,0) scale(1)', opacity: .9 },
             { transform: 'translate(-50%,-50%) translate(' + Math.cos(a) * d + 'px,' + Math.sin(a) * d + 'px) scale(.3)', opacity: 0 }],
            { duration: 640, easing: 'cubic-bezier(.2,.7,.2,1)' }
          ).onfinish = function () { p.remove(); };
        })();
      }

      // 4. whole-screen flavour flash
      flash.style.background = col;
      flash.style.opacity = '.10';
      clearTimeout(ft);
      ft = setTimeout(function () { flash.style.opacity = '0'; }, 130);
    }, { passive: true });
  }

  /* ---------- reveal on scroll ---------- */
  function initReveal() {
    var els = document.querySelectorAll('.gc-rise,.gc-pop');
    if (!els.length) return;
    if (!('IntersectionObserver' in window) || reduce) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0, rootMargin: '0px 0px 18% 0px' });
    els.forEach(function (el) { io.observe(el); });
    // failsafe: never leave content hidden
    addEventListener('load', function () {
      setTimeout(function () { els.forEach(function (el) {
        if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in');
      }); }, 600);
    });
  }

  function boot() { initBackground(); initCursor(); initRipple(); initReveal(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

  /* pause always-on decorative animation while it is off screen */
  (function () {
    var targets = document.querySelectorAll('[data-idle-pause]');
    if (!targets.length || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.target.classList.toggle('gc-paused', !e.isIntersecting); });
    }, { rootMargin: '150px' });
    targets.forEach(function (el) { io.observe(el); });
  })();


  /* Warm a page the moment someone shows intent — hover on a mouse, the first
     touch on a phone — so the tap that follows lands on an already-fetched
     page. This is what makes "open the bag" feel instant; the navigation is
     still a normal one, we just start it earlier.

     Never prefetches /cart/change or /cart/add: those CHANGE the cart, and a
     prefetch would fire them for real. Skips slow connections and Save-Data. */
  (function () {
    if (!('fetch' in window)) return;
    var c = navigator.connection;
    if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ''))) return;
    var done = Object.create(null);
    function warm(url) {
      if (done[url]) return;
      done[url] = 1;
      var l = document.createElement('link');
      l.rel = 'prefetch';
      l.href = url;
      document.head.appendChild(l);
    }
    function intent(e) {
      var t = e.target;
      var a = t && t.closest ? t.closest('a') : null;
      if (!a || a.hasAttribute('download')) return;
      if (a.target && a.target !== '_self') return;
      var href = a.getAttribute('href') || '';
      if (href.charAt(0) !== '/') return;                 /* same-origin paths only */
      if (href.indexOf('/cart/change') === 0) return;     /* mutating */
      if (href.indexOf('/cart/add') === 0) return;        /* mutating */
      warm(a.href);
    }
    addEventListener('pointerover', intent, { passive: true });
    addEventListener('touchstart', intent, { passive: true });
  })();
