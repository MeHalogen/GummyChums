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
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const THEME = 'shopify-theme';
const TOKENS = join(THEME, 'assets', 'gc-tokens.css');
const read = (p) => readFileSync(p, 'utf8');

const ROLES = [
  'page-bg', 'page-ink', 'ink-muted', 'ink-faint', 'line',
  'surface', 'surface-ink', 'cta-bg', 'cta-ink',
  'accent', 'band-tone', 'band-ink', 'eyebrow-ink', 'focus',
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

const COMPONENTS = join(THEME, 'assets', 'gc-components.css');

test('component stylesheet exists', () => {
  assert.doesNotThrow(() => read(COMPONENTS), 'gc-components.css must exist');
});

test('components reference roles, never primitives', () => {
  const css = read(COMPONENTS).replace(/\/\*[\s\S]*?\*\//g, '');
  const offenders = [...css.matchAll(/var\(--c-[a-z0-9-]+/g)].map((m) => m[0]);
  assert.deepEqual(
    [...new Set(offenders)], [],
    'components must use var(--role-*). A component naming a brand colour is ' +
    'exactly what makes a re-skin expensive.'
  );
});

test('component stylesheet is loaded by the layout', () => {
  const layout = read(join(THEME, 'layout', 'theme.liquid'));
  assert.match(layout, /gc-components\.css/, 'theme.liquid must load gc-components.css');
});

test('page furniture components are defined', () => {
  const css = read(COMPONENTS);
  for (const sel of ['.gc-band', '.gc-eyebrow', '.gc-head']) {
    assert.ok(css.includes(sel), `missing ${sel}`);
  }
});

test('surface and layout components are defined', () => {
  const css = read(COMPONENTS);
  for (const sel of ['.gc-grid', '.gc-card', '.gc-media']) {
    assert.ok(css.includes(sel), `missing ${sel}`);
  }
});

test('no duplicate rule bodies inside the component layer', () => {
  const css = read(COMPONENTS).replace(/\/\*[\s\S]*?\*\//g, '');
  const seen = new Map();
  for (const m of css.matchAll(/([^{}]+)\{([^{}]+)\}/g)) {
    const body = m[2].replace(/\s+/g, '');
    if (body.length < 40) continue;
    const sel = m[1].trim().split('\n').pop().trim();
    if (seen.has(body)) {
      assert.fail(`"${sel}" duplicates "${seen.get(body)}" — make one a modifier of the other`);
    }
    seen.set(body, sel);
  }
});

const SNIPPETS = join(THEME, 'snippets');

test('control and price components are defined', () => {
  const css = read(COMPONENTS);
  for (const sel of ['.gc-chip', '.gc-price']) {
    assert.ok(css.includes(sel), `missing ${sel}`);
  }
});

test('every gc snippet documents its parameters', () => {
  const files = readdirSync(SNIPPETS).filter((f) => f.startsWith('gc-') && f.endsWith('.liquid'));
  for (const f of files) {
    const head = read(join(SNIPPETS, f)).slice(0, 900);
    assert.match(
      head, /\{%-?\s*comment\s*-?%\}/,
      `${f} must open with a comment block documenting its parameters — a snippet ` +
      `whose arguments you have to reverse-engineer is not a component`
    );
  }
});

/* Sections proven to live on the component layer. Adding a name here is a
   promise that the section carries no CSS of its own. Unmigrated sections are
   deliberately absent rather than failing — they predate the rule. */
const MIGRATED = ['gc-product.liquid', 'gc-home.liquid'];

test('migrated sections carry no CSS of their own', () => {
  for (const f of MIGRATED) {
    const src = read(join(THEME, 'sections', f));
    assert.ok(
      !/<style>/.test(src),
      `${f} still has a <style> block. Its styling belongs in gc-components.css, ` +
      `or it is specific enough to deserve a component of its own.`
    );
  }
});

test('migrated sections use no raw colour values', () => {
  for (const f of MIGRATED) {
    const src = read(join(THEME, 'sections', f))
      .replace(/\{%[\s\S]*?%\}/g, '')
      .replace(/\{\{[\s\S]*?\}\}/g, '');
    const hex = [...src.matchAll(/#[0-9a-fA-F]{3,8}\b/g)].map((m) => m[0]);
    assert.deepEqual([...new Set(hex)], [], `${f} hard-codes colours: ${hex.join(', ')}`);
  }
});

test('a brand colour change is one file', () => {
  /* The headline promise of this architecture. Every colour in the component
     layer resolves through a role, so gc-tokens.css is the only file that names
     a brand colour. If this fails, the Figma pivot has stopped being cheap and
     whoever broke it should find out now rather than in six months. */
  const css = read(COMPONENTS).replace(/\/\*[\s\S]*?\*\//g, '');
  const prims = [...css.matchAll(/var\(--c-[a-z0-9-]+/g)].map((m) => m[0]);
  assert.deepEqual(
    [...new Set(prims)], [],
    `gc-components.css names a brand colour directly. Route it through a ` +
    `--role-* token so a re-skin stays a single-file edit.`
  );
});

test('migrated sections keep their CSS in a stylesheet, not in Liquid', () => {
  for (const f of MIGRATED) {
    const src = read(join(THEME, 'sections', f));
    assert.match(
      src, /asset_url\s*\|\s*stylesheet_tag/,
      `${f} should link a stylesheet — that is where its CSS now lives`
    );
  }
});

/* A role that nothing consumes is not architecture, it is a promise. --role-focus
   sat declared and unreferenced from the day the role tier landed, which is why
   no GummyChums component had a focus ring and no keyboard user could see where
   they were. The general form of that bug is worth catching. */
test('every declared role is actually consumed by something', () => {
  const dir = join(THEME, 'assets');
  const consumers = readdirSync(dir)
    .filter((f) => f.endsWith('.css') && f !== 'gc-tokens.css')
    .map((f) => read(join(dir, f)))
    .join('\n');
  const unused = ROLES.filter((r) => !consumers.includes(`var(--role-${r})`));
  assert.deepEqual(
    unused, [],
    `these roles are declared in gc-tokens.css and used by no stylesheet: ${unused.join(', ')}. ` +
    'Either something should be using them, or they should not exist.',
  );
});

/* Dawn sets html{font-size:62.5%}, so 1rem is 10px in this theme, not 16px.
   gc-brand.css was written against the usual 16px assumption and its .gc-btn
   carried font-size:1rem — the primary CTA rendered at 10px, smaller than the
   secondary link beside it, store-wide. The --fs- and --sp- tokens are px-based
   and cannot drift this way, so the brand layer uses those instead. */
test('the brand layer does not size anything in rem', () => {
  const dir = join(THEME, 'assets');
  const offenders = [];
  for (const f of readdirSync(dir).filter((x) => /^(gc-|section-gc-).*\.css$/.test(x))) {
    /* Strip comments first: the note in gc-brand.css explaining this very bug
       quotes "font-size:1rem", and a linter that flags its own documentation is
       a linter people switch off. */
    const css = read(join(dir, f)).replace(/\/\*[\s\S]*?\*\//g, '');
    for (const m of css.matchAll(/([\w-]+)\s*:\s*[^;{}]*?[\d.]+rem/g)) {
      offenders.push(`${f}: ${m[0].trim()}`);
    }
  }
  assert.deepEqual(
    offenders, [],
    'rem in the brand layer resolves against a 10px root in Dawn, so these are ' +
    `37.5% smaller than they read as:\n  ${offenders.join('\n  ')}`,
  );
});
