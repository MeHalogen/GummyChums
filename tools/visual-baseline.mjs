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

const DRIVER = 'http://127.0.0.1:4712';
const SITE = 'http://127.0.0.1:9292';
const PAGES = [
  ['home', '/'],
  ['product', '/products/brain-booster-gummies'],
];
const WIDTHS = [[430, 900, 'phone'], [1280, 900, 'desktop']];

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
        await new Promise((r) => setTimeout(r, 2500));
        const shot = await api('GET', `/session/${id}/screenshot`);
        writeFileSync(join(dir, `${pname}-${wname}.png`), Buffer.from(shot.value, 'base64'));
        console.log(`  captured ${pname}-${wname}`);
      }
    }
  } finally {
    await api('DELETE', `/session/${id}`);
  }
}

function compare(a, b) {
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
