/**
 * Visual baseline — proves a refactor changed nothing on screen.
 *
 *   node tools/visual-baseline.mjs capture before
 *   ...refactor...
 *   node tools/visual-baseline.mjs capture after
 *   node tools/visual-baseline.mjs compare before after
 *
 * Drives real Safari through WebDriver because that is the engine the store's
 * customers use. Requires `shopify theme dev` on 9292 and safaridriver on 4712.
 */
import { mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

/* Safari paints a blank window when it is not frontmost, and a blank capture
   reads as a visual regression. Bring it forward before every shot rather than
   relying on whoever is running this to remember. */
const front = () => {
  try { execFileSync('osascript', ['-e', 'tell application "Safari" to activate']); } catch {}
};

const DRIVER = 'http://127.0.0.1:4712';
const SITE = 'http://127.0.0.1:9292';
const PAGES = [
  ['home', '/'],
  ['product', '/products/brain-booster-gummies'],
];
const WIDTHS = [[430, 900, 'phone'], [1280, 900, 'desktop']];

/* Injected before every screenshot: kill motion, force lazy images in, settle
   at the top. Everything that makes two captures of one page differ. */
const FREEZE = `
  var st = document.createElement('style');
  st.textContent = '*,*::before,*::after{animation:none!important;' +
    'transition:none!important;caret-color:transparent!important}' +
    'html{scroll-behavior:auto!important}';
  document.head.appendChild(st);
  document.querySelectorAll('img[loading="lazy"]').forEach(function(i){ i.loading='eager'; });
  window.scrollTo(0, document.body.scrollHeight);
  window.scrollTo(0, 0);
  return document.querySelectorAll('img').length;
`;

const api = async (method, path, body) => {
  const res = await fetch(DRIVER + path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return res.json();
};

async function capture(label) {
  const dir = join('.visual', label);
  mkdirSync(dir, { recursive: true });
  const sizes = {};
  const session = await api('POST', '/session', {
    capabilities: { alwaysMatch: { browserName: 'safari' } },
  });
  const id = session.value?.sessionId;
  if (!id) {
    console.error('  could not open a Safari session:', JSON.stringify(session).slice(0, 200));
    process.exit(1);
  }
  try {
    await api('POST', `/session/${id}/timeouts`, { script: 60000, pageLoad: 60000 });
    for (const [w, h, wname] of WIDTHS) {
      await api('POST', `/session/${id}/window/rect`, { width: w, height: h });
      for (const [pname, path] of PAGES) {
        await api('POST', `/session/${id}/url`, { url: SITE + path });
        await new Promise((r) => setTimeout(r, 2000));
        /* Freeze the page before looking at it. Without this the Chums' sway and
           the background drift put every capture on a different frame, and the
           harness reports a difference for an unchanged site — which it did,
           and which a control capture caught. */
        front();
        await new Promise((r) => setTimeout(r, 600));
        const frozen = await api('POST', `/session/${id}/execute/sync`, { script: FREEZE, args: [] });
        /* Did the page actually load? A blank Safari window screenshots happily
           and then reads as a visual regression, sending you after a bug that is
           not there. It happened; hence this. */
        if (typeof frozen.value !== 'number' || frozen.value < 1) {
          console.error(`  ABORT: ${pname} at ${wname} rendered no images — the page did not load.`);
          console.error('  Check the dev server, and quit Safari if it is wedged.');
          await api('DELETE', `/session/${id}`);
          process.exit(2);
        }
        await new Promise((r) => setTimeout(r, 1200));
        const real = await api('POST', `/session/${id}/execute/sync`,
          { script: 'return innerWidth + "x" + innerHeight;', args: [] });
        sizes[`${pname}-${wname}`] = real.value;
        const shot = await api('GET', `/session/${id}/screenshot`);
        writeFileSync(join(dir, `${pname}-${wname}.png`), Buffer.from(shot.value, 'base64'));
        console.log(`  captured ${pname}-${wname}`);
      }
    }
    /* Safari clamps the window to its own minimum, and that minimum is not the
       same across restarts — one session gave 573x1130 for the same 430x900
       request that another answered with 430x848. Captures taken at different
       widths are different renders, so comparing them reports a regression that
       is not there. Recording the real size is what lets compare() refuse. */
    writeFileSync(join(dir, 'viewport.json'), JSON.stringify(sizes, null, 2));
  } finally {
    await api('DELETE', `/session/${id}`);
  }
}

function compare(a, b) {
  const va = join('.visual', a, 'viewport.json');
  const vb = join('.visual', b, 'viewport.json');
  if (!existsSync(va) || !existsSync(vb)) {
    console.log('  WARNING: one of these captures predates viewport recording, so there is');
    console.log('  no way to tell whether both were taken at the same window size. Safari');
    console.log('  clamps to a minimum that varies between restarts, and a width change');
    console.log('  looks exactly like a regression. Recapture both before trusting a result.\n');
  }
  if (existsSync(va) && existsSync(vb)) {
    const sa = JSON.parse(readFileSync(va, 'utf8'));
    const sb = JSON.parse(readFileSync(vb, 'utf8'));
    const bad = Object.keys(sa).filter((k) => sb[k] && sa[k] !== sb[k]);
    if (bad.length) {
      console.log('  REFUSING to compare — these were captured at different viewport sizes:');
      for (const k of bad) console.log(`    ${k}: ${a}=${sa[k]}  ${b}=${sb[k]}`);
      console.log('\n  Safari clamps the window to a minimum that varies between restarts,');
      console.log('  so these are different renders. Recapture both in one session.');
      process.exit(3);
    }
  }
  let differed = false;
  for (const [, , wname] of WIDTHS) {
    for (const [pname] of PAGES) {
      const name = `${pname}-${wname}.png`;
      const pa = join('.visual', a, name);
      const pb = join('.visual', b, name);
      if (!existsSync(pa) || !existsSync(pb)) {
        console.log(`  MISSING ${name}`);
        differed = true;
        continue;
      }
      const ba = readFileSync(pa);
      const bb = readFileSync(pb);
      const identical = ba.length === bb.length && ba.equals(bb);
      if (!identical) differed = true;
      console.log(`  ${name}: ${identical ? 'identical' : 'DIFFERS'} (${ba.length} vs ${bb.length} bytes)`);
    }
  }
  if (differed) {
    console.log('\n  Images differ. Open both and look before assuming it is a regression —');
    console.log('  PNG bytes also change for innocuous reasons, so eyes decide, not this script.');
    process.exit(1);
  }
  console.log('\n  all images byte-identical');
}

const [cmd, ...rest] = process.argv.slice(2);
if (cmd === 'capture') await capture(rest[0] || 'baseline');
else if (cmd === 'compare') compare(rest[0], rest[1]);
else {
  console.log('usage: visual-baseline.mjs capture <label> | compare <a> <b>');
  process.exit(1);
}
