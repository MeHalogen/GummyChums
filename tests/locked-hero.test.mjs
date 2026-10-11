/**
 * The hero is NOT scroll-driven. This file used to lock the pink-gummy scroll
 * sequence in place; on 11 Oct 2026 Mehal removed that sequence, so the lock is
 * inverted — it now guards the decision that replaced it.
 *
 * Why it went: on a phone it juddered through every tuning pass, and the cause
 * was structural rather than tunable. The gummy was a gradient-filled circle
 * scaled past 5000px square, re-rasterised at every step; the Chums rode a
 * sideways transform driven from vertical scroll, which fights the phone's own
 * scrolling. Both measured clean on a desktop GPU, which is why they survived
 * so long. See docs/LAUNCH-BLOCKERS.md and the commits around 3f29cc7.
 *
 * The sequence itself is not lost: it is in the history, and index31.html in
 * the repo root is the prototype it came from. If it is ever rebuilt, rebuild
 * it knowing a phone has to paint it.
 *
 * These assertions fail if scroll-coupling comes back by accident. If it comes
 * back on purpose, say so in the commit and rewrite this file in the same one.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

/* The section AND any stylesheet it links. When gc-home's CSS moved to
   assets/section-gc-home.css, reading only the .liquid left a hole: scroll
   coupling could return in the stylesheet and this lock would not see it. */
const SECTION = new URL('../shopify-theme/sections/gc-home.liquid', import.meta.url);
const src = (() => {
  let out = readFileSync(SECTION, 'utf8');
  for (const m of out.matchAll(/'([a-z0-9-]+\.css)'\s*\|\s*asset_url/g)) {
    const asset = new URL(`../shopify-theme/assets/${m[1]}`, import.meta.url);
    try { out += '\n' + readFileSync(asset, 'utf8'); } catch { /* not present yet */ }
  }
  return out;
})();

const BANNED = [
  ['no scroll-driven timelines', 'animation-timeline'],
  ['no --z scroll variable',     'var(--z,'],
  ['no scroll-derived ground',   '--gh-ground'],
  ['no pinned hero',             'position:sticky'],
  ['no ride state class',        'gh-hs--js'],
  ['no ride script',             'gc-hs.js'],
];

for (const [what, needle] of BANNED) {
  test(`hero stays off the scroll position — ${what}`, () => {
    assert.ok(
      !src.includes(needle),
      `\n\n  Scroll-coupling is back in sections/gc-home.liquid: ${what}\n` +
      `  Found: ${needle}\n\n` +
      `  The hero and the Chums grid were deliberately taken off scroll position\n` +
      `  on 11 Oct 2026 because they juddered on a phone. If this is intentional,\n` +
      `  rewrite this test in the same commit and say why. Otherwise revert.\n`
    );
  });
}

test('the hero still has its content', () => {
  for (const needed of ['gh-stage', 'gh-mid', 'gh-chum', 'gh-reveal', 'gh-hs-card']) {
    assert.ok(src.includes(needed), `hero lost ${needed}`);
  }
});

test('the Chums are a grid', () => {
  assert.ok(src.includes('grid-template-columns:repeat(3,1fr)'), 'three-up grid missing');
});
