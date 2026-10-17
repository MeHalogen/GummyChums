/**
 * The hero threshold — the kolam drawn across the dome the Chums stand on.
 *
 * Two different things are guarded here and they fail for different reasons.
 *
 * THE FLOOR. .gh-reveal looks like a text block and is not one: it is the ground
 * the Chums stand on, tucked under their feet by a negative margin, with a domed
 * top and bottom padding sized so .gh-edge's -128px pull does not drag the
 * stepped teeth up across the copy. Anyone reading the markup sees a div with a
 * heading in it and edits accordingly. These tests are the warning they will not
 * otherwise get.
 *
 * THE DRAWING. A kolam is placed dots-first, then looped in one unbroken line,
 * and it animates in that order. Three of them draw left to right so the hero
 * reads as one hand drawing across a doorway. That stagger lives in CSS
 * variables set per instance, so it can drift silently; the delays are asserted
 * by value.
 *
 * Nothing here is coupled to scroll position. That is the whole point — see
 * tests/locked-hero.test.mjs for why, and docs/superpowers/specs/
 * 2026-10-17-hero-threshold-design.md §6 for the measurement behind it.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const THEME = 'shopify-theme';
const BRAND = join(THEME, 'assets', 'gc-brand.css');
const read = (p) => readFileSync(p, 'utf8');

/* ---------- the drawing ---------- */

test('kolam delays are variables, not hard-coded', () => {
  const css = read(BRAND);
  const line = css.match(/\.gc2-kolam-line\{[^}]*\}/s);
  assert.ok(line, '.gc2-kolam-line rule not found');
  assert.match(
    line[0], /var\(--k-delay/,
    '.gc2-kolam-line must take its transition delay from var(--k-delay, …) so ' +
    'three instances can be staggered from the markup',
  );
  const dots = css.match(/\.gc2-kolam-dots\{[^}]*\}/s);
  assert.ok(dots, '.gc2-kolam-dots rule not found');
  assert.match(
    dots[0], /var\(--k-dot-delay/,
    '.gc2-kolam-dots must take its delay from var(--k-dot-delay, …)',
  );
});

test('kolam delay fallbacks match what the story teaser relies on', () => {
  const css = read(BRAND);
  assert.match(
    css, /var\(--k-delay,\s*\.38s\)/,
    'the --k-delay fallback must stay .38s — gc2-story-teaser renders this ' +
    'kolam with no delay set and must animate exactly as it does today',
  );
  assert.match(
    css, /var\(--k-dot-delay,\s*0s\)/,
    'the --k-dot-delay fallback must stay 0s for the same reason',
  );
});

test('reduced motion still cancels the kolam transition', () => {
  const css = read(BRAND);
  /* gc-brand.css carries more than one reduced-motion block; pick the kolam's
     by content rather than by position, or this passes against the wrong one. */
  const blocks = [...css.matchAll(/@media\s*\(prefers-reduced-motion:\s*reduce\)\{[^@]*?\n\}/gs)]
    .map((m) => m[0]).filter((b) => b.includes('gc2-kolam'));
  assert.equal(blocks.length, 1,
    `expected exactly one reduced-motion block covering the kolam, found ${blocks.length}`);
  const b = blocks[0];
  assert.match(b, /\.gc2-kolam-dots\s*,\s*\.gc2-kolam-line\{transition:none\}/,
    'reduced motion must set transition:none — a delay must never resurrect ' +
    'motion this branch disabled');
  assert.match(b, /\.gc2-kolam-line\{stroke-dashoffset:0\}/,
    'reduced motion must leave the line fully drawn');
});

test('the kolam is drawn even when scripting is off', () => {
  const css = read(BRAND);
  const block = css.match(/@media\s*\(scripting:\s*none\)\{.*?\n\}/s);
  assert.ok(
    block,
    'no @media (scripting: none) branch. The draw waits for gc-brand.js to add ' +
    '.in; without it the dots sit at opacity 0 and the line stays fully dashed, ' +
    'so the hero\'s centrepiece renders as an empty band on any page where the ' +
    'script is blocked or fails.',
  );
  assert.match(block[0], /\.gc2-kolam-line\{stroke-dashoffset:0\}/,
    'the no-scripting branch must leave the line fully drawn');
  assert.match(block[0], /\.gc2-kolam-dots\{opacity:\.55\}/,
    'the no-scripting branch must leave the dots at their final opacity');
});

/* ---------- the floor ----------
   The section plus any stylesheet it links. Reading only the .liquid would miss
   every one of these, since gc-home's CSS lives in assets/. */
const SECTION = join(THEME, 'sections', 'gc-home.liquid');
const homeSrc = (() => {
  const liquid = read(SECTION);
  let out = liquid;
  for (const m of liquid.matchAll(/'([a-z0-9-]+\.css)'\s*\|\s*asset_url/g)) {
    out += '\n' + read(join(THEME, 'assets', m[1]));
  }
  return out;
})();

test('the dome keeps the floor the Chums stand on', () => {
  const rule = homeSrc.match(/\.gh-reveal\{[^}]*\}/s);
  assert.ok(rule, '.gh-reveal rule not found');
  const r = rule[0];
  assert.match(
    r, /calc\(var\(--gh-chum-h\)\s*\*\s*-0\.14\)/,
    '.gh-reveal must keep its negative top margin. It is not spacing: it tucks ' +
    'the dome under the Chums\' feet so they stand ON the pink. Without it they ' +
    'float above a band.',
  );
  assert.match(
    r, /border-radius:50% 50% 0 0/,
    '.gh-reveal must keep its domed top — the threshold the Chums stand at',
  );
  assert.match(
    r, /padding:[^;]*128px/,
    '.gh-reveal\'s bottom padding must still clear 128px. .gh-edge pulls itself ' +
    'up by exactly that, and without the clearance the stepped teeth ride up ' +
    'across the copy.',
  );
});

test('the threshold renders exactly three kolams', () => {
  const n = [...read(SECTION).matchAll(/render\s+'gc2-kolam'/g)].length;
  assert.equal(n, 3, `expected 3 kolams in the hero, found ${n} — spec §6 caps it at three`);
});

test('each kolam carries its own stagger delays', () => {
  const liquid = read(SECTION);
  const line = [...liquid.matchAll(/--k-delay:\s*([0-9.]+s)/g)].map((m) => m[1]);
  const dot = [...liquid.matchAll(/--k-dot-delay:\s*([0-9.]+s)/g)].map((m) => m[1]);
  assert.deepEqual(line, ['.38s', '.92s', '1.46s'],
    'the three line delays must stagger left to right so the row reads as one ' +
    'hand drawing across the doorway');
  assert.deepEqual(dot, ['0s', '.54s', '1.08s'],
    'each kolam places its dots before its own line — the order a kolam is ' +
    'actually made in');
});

test('threshold copy is omitted when blank, not rendered empty', () => {
  const liquid = read(SECTION);
  for (const id of ['reveal_title', 'reveal_sub']) {
    assert.match(
      liquid, new RegExp(`s\\.${id}\\s*!=\\s*blank`),
      `${id} must be guarded with != blank. Priyal clearing it in the theme ` +
      'editor would otherwise leave an empty element holding its margins open.',
    );
  }
});

test('the kolam row narrows before it overflows', () => {
  assert.match(
    homeSrc, /@media\s*\(max-width:\s*348px\)\{[^}]*\.gh-thresh__kolams[^}]*\}/s,
    'the row must drop its third kolam before it overflows the gutter. 348px is ' +
    'measured: at 19vw three kolams plus their gaps stop fitting just below ' +
    'that, which keeps all three on every common phone (360px and up).',
  );
});

/* ---------- where the displaced copy went ---------- */

const QUALITY = join(THEME, 'sections', 'gc-quality.liquid');

test('the no-sugar claim survives either quality layout', () => {
  const liquid = read(QUALITY);
  const [badges, full] = liquid.split(/\{%-?\s*else\s*-?%\}/s);
  assert.ok(full, 'gc-quality no longer has two layout branches');
  for (const [name, branch] of [['badges', badges], ['full', full]]) {
    assert.match(
      branch, /No added sugar/i,
      `the no-sugar claim is missing from the ${name} branch. The homepage ` +
      'saves layout:"badges" while the schema default is "full", so a claim ' +
      'living in only one branch disappears the moment that setting changes.',
    );
  }
});

test('the actives are listed on the certifications strip', () => {
  const liquid = read(QUALITY);
  for (const active of ['Bacopa', 'Melatonin', 'Lutein']) {
    assert.match(liquid, new RegExp(active),
      `${active} is missing — it was displaced from the hero and the ` +
      'certifications strip is where it was meant to land');
  }
});

/* ---------- one Chum per SKU ----------
   The hero shipped with two Chums while the section directly below it announced
   "three chums · one a day". The brand has three SKUs and three characters; the
   sleep Chum was missing from her own homepage and nothing caught it. */

test('the hero shows one Chum per product, not two', () => {
  const liquid = read(SECTION);
  for (const chum of ['gc2-chum-brain.svg', 'gc2-chum-sleep.svg', 'gc2-chum-eye.svg']) {
    assert.match(liquid, new RegExp(chum.replace('.', '\\.')),
      `${chum} is missing from the hero — the page would claim three Chums and show fewer`);
  }
});

test('every Chum is sized at every breakpoint', () => {
  /* The middle Chum was added without an entry in the two media tiers that size
     her neighbours, so she computed to 159px against their 249px and 236px. A
     figure a head shorter than the others reads as a bug, not as depth. */
  for (const tier of ['max-width:1100px', 'max-width:749px']) {
    for (const chum of ['--l', '--c', '--r']) {
      const re = new RegExp(`@media\\(${tier.replace(/[-:]/g, '\\$&')}\\)\\{\\.gh-chum${chum}\\{height:`);
      assert.match(homeSrc, re,
        `.gh-chum${chum} has no height at ${tier} — it will fall back and stand out of scale`);
    }
  }
});
