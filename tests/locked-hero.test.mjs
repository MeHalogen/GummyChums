/**
 * LOCKED: the pink gummy scroll sequence.
 *
 * Signed off 11 Sep 2026. Phone pacing re-opened by Mehal on 12 Sep 2026 —
 * it read as a jump on a real phone — and re-signed at the values below.
 *
 * 13 Sep 2026 — LOCK LIFTED AND RE-CUT, by Mehal, who asked for the sequence
 * from index31.html instead: "Look at index 31 in this repo. I wanted that
 * scroll, the big gummy coming in." Ported from that file's .tp-stage / .tp-pin
 * / .tp-gummy / .tp-title / .tp-inside, and the values below are now ITS values,
 * not the 11 Sep ones. What changed and why it reads calmer: the stage is 270vh
 * rather than 190-200, so the zoom advances far less per pixel scrolled; the
 * curve is z squared times 26 rather than 55; the gummy sits ON the fold with
 * transform-origin at its base, so it grows UP out of the bottom edge instead of
 * floating centred and rising into place; the headline fades at 2.6 rather than
 * 4.5; and the reveal waits until 62% through instead of 18%. If the 11 Sep
 * sequence is ever wanted back, it is in the history at c3c0533.
 *
 * SUPERSEDED — 13 Sep 2026, scope narrowed to desktop, by Mehal, after four rounds of
 * jitter on iOS. Below 750px the hero no longer pins and nothing is driven by
 * scroll: see the PHONE HERO block in sections/gc-home.liquid. The declarations
 * asserted below still exist and still drive every screen at 750px and up, so
 * these assertions still pass — but they no longer describe what a phone does.
 * Read them as the DESKTOP lock. If the phone sequence is ever restored, the
 * values to restore it to are the ones here.
 *
 * Original sign-off — "I like the pink Gummy thing that we did right now,
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
  ['stage height, desktop',        '.gh-stage{position:relative;height:270vh}'],
  ['stage height, phone',          '@media(max-width:749px){.gh-stage{height:270vh}}'],
  ['zoom and reveal timing',       '.gh-pin{--zoom-k:26;--rev-start:.38;--rev-ramp:4.5;--flood-start:.22;--flood-ramp:4.4;'],
  ['reveal timing, desktop',       '@media(min-width:750px){.gh-pin{--rev-start:.46;--rev-ramp:4.5;--flood-start:.30;--flood-ramp:3.9}}'],
  ['gummy is a CSS circle',        'width:min(32vw,190px);aspect-ratio:1;'],
  ['gummy sits on the fold',       'bottom:4%;'],
  ['gummy grows from its base',    'transform-origin:center bottom;'],
  ['gummy scale curve',            'scale(calc(1 + var(--z,0) * var(--z,0) * var(--zoom-k)))'],
  ['headline fade rate',           'opacity:calc(1 - var(--z,0) * 2.6)'],
  ['reveal fade curve',            'opacity:calc((var(--z,0) - var(--rev-start)) * var(--rev-ramp))'],
  ['reveal does not scale',        'pointer-events:none;transform:none;'],
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
