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

    // floating blurred gummies — fixed positions so it looks composed, not random
    // kept to the edges — the centre column stays clean for type
    // 4 (was 7) — each blurred layer costs compositor memory
    var gummies = [
      { l: '-4%', t: '10%', s: 230, c: '#DE1D61', o: .34, d: 20, dx: '26px',  dy: '-24px' },
      { l: '86%', t: '4%',  s: 200, c: '#8DAA31', o: .26, d: 24, dx: '-22px', dy: '26px'  },
      { l: '88%', t: '56%', s: 240, c: '#F9740D', o: .30, d: 22, dx: '-26px', dy: '-22px' },
      { l: '-6%', t: '64%', s: 250, c: '#F9740D', o: .24, d: 26, dx: '24px',  dy: '22px'  }
    ];
    gummies.forEach(function (g, i) {
      var el = document.createElement('i');
      el.style.cssText =
        'left:' + g.l + ';top:' + g.t + ';width:' + g.s + 'px;height:' + g.s + 'px;' +
        'background:' + g.c + ';opacity:' + g.o + ';' +
        'animation-duration:' + g.d + 's;animation-delay:' + (-i * 2.5) + 's;' +
        '--dx:' + g.dx + ';--dy:' + g.dy + ';';
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
    addEventListener('pointermove', function (e) {
      c.style.transform = 'translate3d(' + e.clientX + 'px,' + e.clientY + 'px,0) translate(-50%,-50%)';
      if (!c.classList.contains('on')) c.classList.add('on');
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
    var els = document.querySelectorAll('.gc-rise');
    if (!els.length) return;
    if (!('IntersectionObserver' in window) || reduce) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
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
