/**
 * LOCKED: the pink gummy scroll sequence.
 *
 * Signed off 11 Sep 2026 — "I like the pink Gummy thing that we did right now,
 * whatever you had to change in the diff is perfectly fine. Lock this diff, and
 * if I try to change it, flag me. If you try to change it, flag yourself."
 *
 * This file IS the flag. It asserts the exact values that produce the sequence
 * as approved. Any edit to them — by anyone, deliberate or accidental — fails
 * the suite with a message saying what changed and that it needs sign-off.
 *
 * To change one of these on purpose: change the expected value here in the same
 * commit, and say in the commit message that the lock was lifted and by whom.
 * Do not just edit the section and re-run until it passes.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../shopify-theme/sections/gc-home.liquid', import.meta.url), 'utf8');

const LOCKED = [
  ['stage height, desktop',        '.gh-stage{position:relative;height:200vh}'],
  ['stage height, phone',          '@media(max-width:749px){.gh-stage{height:130vh}}'],
  ['zoom + rise, phone',           '.gh-pin{--zoom-k:140;--rise-end:.18;'],
  ['zoom + rise, desktop',         '@media(min-width:750px){.gh-pin{--zoom-k:40;--rise-end:.30}}'],
  ['gummy is a CSS circle',        'width:11vmax;aspect-ratio:1;'],
  ['gummy scale curve and cap',    'scale(min(14, calc(1 + var(--z,0) * var(--z,0) * var(--zoom-k))))'],
  ['gummy rise curve',             'max(0px, (var(--rise-end) - var(--z,0)) / var(--rise-end) * 55vh)'],
  ['reveal fade, phone',           '.gh-reveal{--rev-start:.11;--rev-ramp:11;'],
  ['reveal fade, desktop',         '@media(min-width:750px){.gh-reveal{--rev-start:.13;--rev-ramp:9}}'],
  ['reveal grows out of the gummy','scale(min(1, calc((1 + var(--z,0) * var(--z,0) * var(--zoom-k)) / 14)))'],
];

for (const [what, needle] of LOCKED) {
  test(`LOCKED hero sequence — ${what}`, () => {
    assert.ok(
      src.includes(needle),
      `\n\n  The locked pink-gummy sequence changed: ${what}\n` +
      `  Expected to find in sections/gc-home.liquid:\n    ${needle}\n\n` +
      `  This was signed off on 11 Sep 2026 and locked deliberately.\n` +
      `  If the change is intended, update tests/locked-hero.test.mjs in the same\n` +
      `  commit and say in the message that the lock was lifted. Otherwise revert.\n`
    );
  });
}
