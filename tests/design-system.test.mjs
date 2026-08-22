import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const THEME = 'shopify-theme';
const TOKENS = join(THEME, 'assets', 'gc-tokens.css');
const SECTIONS = join(THEME, 'sections');

const read = (p) => readFileSync(p, 'utf8');
const gcSections = () =>
  readdirSync(SECTIONS).filter((f) => f.startsWith('gc-') && f.endsWith('.liquid'));

/** Strip liquid tags + comments so we only lint real CSS. */
function styleCss(file) {
  const src = read(join(SECTIONS, file));
  const blocks = [...src.matchAll(/<style>([\s\S]*?)<\/style>/g)].map((m) => m[1]);
  return blocks.join('\n')
    .replace(/\{%[\s\S]*?%\}/g, '')
    .replace(/\{\{[\s\S]*?\}\}/g, '')
    .replace(/\/\*[\s\S]*?\*\//g, '');
}

// ---------------------------------------------------------------- tokens

test('tokens file exists', () => {
  assert.ok(existsSync(TOKENS), `${TOKENS} must exist — single source of truth`);
});

test('tokens define the full spacing scale (--sp-1..--sp-10)', () => {
  const css = read(TOKENS);
  for (let i = 1; i <= 10; i++) {
    assert.match(css, new RegExp(`--sp-${i}\\s*:`), `missing --sp-${i}`);
  }
});

test('type scale defines exactly the 8 approved sizes', () => {
  const css = read(TOKENS);
  const expected = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl'];
  for (const n of expected) {
    assert.match(css, new RegExp(`--fs-${n}\\s*:`), `missing --fs-${n}`);
  }
  const found = [...css.matchAll(/--fs-([a-z0-9]+)\s*:/g)].map((m) => m[1]);
  assert.equal(new Set(found).size, 8, `type scale must be exactly 8 sizes, found ${new Set(found).size}`);
});

test('tokens define colour roles including a single reserved accent', () => {
  const css = read(TOKENS);
  for (const t of ['--c-bg', '--c-surface', '--c-ink', '--c-accent']) {
    assert.match(css, new RegExp(`${t}\\s*:`), `missing ${t}`);
  }
});

test('tokens define layout container and gutter', () => {
  const css = read(TOKENS);
  assert.match(css, /--container\s*:/, 'missing --container');
  assert.match(css, /--gutter\s*:/, 'missing --gutter');
});

// ------------------------------------------------------- component contracts

test('sections declare each selector only once (no duplicate rules)', () => {
  // Duplicates are scoped: top-level and each @media block are separate scopes,
  // so legitimately re-declaring a selector inside a media query is NOT a duplicate.
  const scopesOf = (css) => {
    const scopes = [];
    let top = '';
    for (let i = 0; i < css.length; i++) {
      if (css.startsWith('@media', i) || css.startsWith('@supports', i)) {
        const open = css.indexOf('{', i);
        if (open === -1) break;
        let depth = 1, j = open + 1;
        while (j < css.length && depth > 0) {
          if (css[j] === '{') depth++;
          else if (css[j] === '}') depth--;
          j++;
        }
        scopes.push(css.slice(open + 1, j - 1));
        i = j - 1;
      } else {
        top += css[i];
      }
    }
    scopes.push(top);
    return scopes;
  };

  const problems = [];
  for (const file of gcSections()) {
    for (const scope of scopesOf(styleCss(file))) {
      const seen = new Map();
      for (const m of scope.matchAll(/(^|\})\s*([^{}@]+?)\s*\{/g)) {
        const sel = m[2].trim().replace(/\s+/g, ' ');
        if (!sel || sel.startsWith('@') || sel.includes('%')) continue;
        seen.set(sel, (seen.get(sel) || 0) + 1);
      }
      for (const [sel, n] of seen) if (n > 1) problems.push(`${file}: "${sel}" declared ${n}x in one scope`);
    }
  }
  assert.deepEqual(problems, [], `duplicate selectors:\n${problems.join('\n')}`);
});

test('sections use no raw hex colours (tokens only)', () => {
  const problems = [];
  for (const file of gcSections()) {
    const hexes = [...styleCss(file).matchAll(/#[0-9a-fA-F]{3,8}\b/g)].map((m) => m[0]);
    if (hexes.length) problems.push(`${file}: ${[...new Set(hexes)].join(', ')}`);
  }
  assert.deepEqual(problems, [], `raw hex outside tokens:\n${problems.join('\n')}`);
});

test('sections use no off-scale font sizes', () => {
  const problems = [];
  for (const file of gcSections()) {
    for (const m of styleCss(file).matchAll(/font-size\s*:\s*([^;}]+)/g)) {
      const v = m[1].trim();
      if (!v.includes('var(--fs-')) problems.push(`${file}: font-size:${v}`);
    }
  }
  assert.deepEqual(problems, [], `off-scale font sizes:\n${problems.join('\n')}`);
});

test('every section constrains content with --container', () => {
  const missing = gcSections().filter((f) => !styleCss(f).includes('var(--container)'));
  assert.deepEqual(missing, [], `sections not using --container: ${missing.join(', ')}`);
});

test('images declare width and height (no layout shift)', () => {
  const problems = [];
  for (const file of gcSections()) {
    const src = readFileSync(join(SECTIONS, file), 'utf8');
    for (const m of src.matchAll(/image_tag[^}]*/g)) {
      const call = m[0];
      if (!/\bwidth:/.test(call) || !/\bheight:/.test(call)) {
        problems.push(`${file}: ${call.trim().slice(0, 60)}`);
      }
    }
  }
  assert.deepEqual(problems, [], `image_tag missing width/height:\n${problems.join('\n')}`);
});

test('raw <img> tags declare both width and height', () => {
  const problems = [];
  for (const file of gcSections()) {
    const src = readFileSync(join(SECTIONS, file), 'utf8');
    for (const m of src.matchAll(/<img\b[^>]*>/g)) {
      const tag = m[0];
      if (!/\bwidth=/.test(tag) || !/\bheight=/.test(tag)) {
        problems.push(`${file}: ${tag.slice(0, 70)}`);
      }
    }
  }
  assert.deepEqual(problems, [], `<img> missing width/height:\n${problems.join('\n')}`);
});
