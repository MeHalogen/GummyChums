/* ============ GummyChums brand interactions — cursor, ripple/splash, reveals ============ */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FLAV = ['#DE1D61', '#8DAA31', '#F9740D'];
  var GPATH = 'M50 3C72 1 95 18 97 42C99 68 82 95 55 97C30 99 5 82 3 55C1 30 26 5 50 3Z';

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
    var gummies = [
      { css: 'left:-6vw;top:-4vw;width:52vw;height:52vw',   c: '#DE1D61' },
      { css: 'right:-6vw;top:8vw;width:46vw;height:46vw',   c: '#8DAA31' },
      { css: 'left:20vw;bottom:-10vw;width:50vw;height:50vw', c: '#F9740D' }
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
    c.innerHTML =
      '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="' + GPATH + '" fill="#DE1D61"/>' +
      '<ellipse cx="35" cy="28" rx="15" ry="9" fill="#fff" opacity=".75" transform="rotate(-25 35 28)"/></svg>';
    document.body.appendChild(c);

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
      var now = e.timeStamp || performance.now();
      if (now - lastHotCheck < HOT_MS) return;
      lastHotCheck = now;
      var hot = e.target.closest && e.target.closest('a,button,input,summary,[role="button"],.gc-card');
      c.classList.toggle('big', !!hot);
    }, { passive: true });
    document.addEventListener('mouseleave', function () { c.classList.remove('on'); });
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
