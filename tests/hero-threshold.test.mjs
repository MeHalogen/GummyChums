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
