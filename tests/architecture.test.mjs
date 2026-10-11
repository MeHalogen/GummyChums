/**
 * Architecture contract — the layering that makes a re-skin cheap.
 *
 *   primitives  (--c-*, --sp-*)   the palette and scales
 *   roles       (--role-*)        what a thing IS, mapped to how it looks today
 *   components  (gc-components)   reference roles only
 *   sections    (markup + schema) reference components only
 *
 * Each test here guards one of those boundaries. They exist because this theme
 * already had a component layer that reached 0% adoption: .gc-card was defined
 * and used by none of 13 sections. Architecture that is not enforced erodes.
 *
 * See docs/superpowers/specs/2026-10-11-theme-architecture-design.md
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const THEME = 'shopify-theme';
const TOKENS = join(THEME, 'assets', 'gc-tokens.css');
const read = (p) => readFileSync(p, 'utf8');

const ROLES = [
  'page-bg', 'page-ink', 'ink-muted', 'ink-faint', 'line',
  'surface', 'surface-ink', 'cta-bg', 'cta-ink',
  'accent', 'accent-ink', 'band-tone', 'band-ink', 'eyebrow-ink', 'focus',
];

test('every semantic role is defined', () => {
  const css = read(TOKENS);
  for (const r of ROLES) {
    assert.match(css, new RegExp(`--role-${r}\\s*:`), `missing --role-${r}`);
  }
});

test('roles resolve to primitives, not to literals', () => {
  const css = read(TOKENS);
  for (const r of ROLES) {
    const m = css.match(new RegExp(`--role-${r}\\s*:\\s*([^;]+);`));
    assert.ok(m, `missing --role-${r}`);
    const value = m[1].trim();
    assert.ok(
      value.includes('var(--'),
      `--role-${r} is "${value}" — a role must point at a primitive so a re-skin ` +
      `is one edit here, not a hunt through the component layer`
    );
  }
});

test('no role points at another role (one hop only)', () => {
  const css = read(TOKENS);
  for (const r of ROLES) {
    const m = css.match(new RegExp(`--role-${r}\\s*:\\s*([^;]+);`));
    assert.ok(!/var\(--role-/.test(m[1]), `--role-${r} points at another role; keep it one hop`);
  }
});
