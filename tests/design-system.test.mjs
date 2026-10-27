import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const THEME = 'shopify-theme';
const TOKENS = join(THEME, 'assets', 'gc-tokens.css');
const SECTIONS = join(THEME, 'sections');

const read = (p) => readFileSync(p, 'utf8');
const ASSETS = join(THEME, 'assets');
/* Was `startsWith('gc-')`, which quietly excluded gc2-story-teaser.liquid — the
   one section carrying a dead `border-radius:2px solid …` declaration. Every
   first-party section is linted now, whatever the generation prefix. */
const gcSections = () =>
  readdirSync(SECTIONS).filter((f) => /^gc\d*-/.test(f) && f.endsWith('.liquid'));

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

// 9, not 8, since 11 Sep 2026: --fs-display added deliberately for the
// display headline (now the "Meet our Chums" title). A tenth needs the same
// conversation, not a quiet edit.
test('type scale defines exactly the 9 approved sizes', () => {
  const css = read(TOKENS);
  const expected = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', 'display'];
  for (const n of expected) {
    assert.match(css, new RegExp(`--fs-${n}\\s*:`), `missing --fs-${n}`);
  }
  const found = [...css.matchAll(/--fs-([a-z0-9]+)\s*:/g)].map((m) => m[1]);
  assert.equal(new Set(found).size, 9, `type scale must be exactly 9 sizes, found ${new Set(found).size}`);
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

/* A section's CSS may live in its own <style> block or, once migrated, in a
   stylesheet it links. This follows the link rather than assuming the former —
   the assumption the architecture refactor set out to remove. */
function sectionCss(file) {
  const src = read(join(SECTIONS, file));
  let css = styleCss(file);
  for (const m of src.matchAll(/'([a-z0-9-]+\.css)'\s*\|\s*asset_url/g)) {
    const asset = join(THEME, 'assets', m[1]);
    if (existsSync(asset)) css += '\n' + read(asset);
  }
  return css;
}

test('every section constrains content with --container', () => {
  const missing = gcSections().filter((f) => !sectionCss(f).includes('var(--container)'));
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

/* A malformed CSS declaration is dropped silently by the browser — nothing
   logs, nothing fails, the rule just does not apply. `border-radius:2px solid
   <colour>` shipped in the story teaser for exactly that reason: the author
   meant `border`, the declaration was void, and the CTA rendered as a hard
   rectangle on a site where every other control is a pill. */

const allCss = () => {
  const out = gcSections().map((f) => [f, styleCss(f)]);
  for (const f of readdirSync(ASSETS).filter((n) => n.endsWith('.css'))) {
    out.push([f, read(join(ASSETS, f)).replace(/\/\*[\s\S]*?\*\//g, '')]);
  }
  return out;
};

test('length-only properties never carry a border shorthand', () => {
  // these take lengths only; a `solid`/`dashed`/`dotted` in the value means the
  // author typed the wrong property name and the whole declaration is dead
  const lengthOnly =
    /(?<![-\w])(border-radius|margin|padding|gap|inset|top|right|bottom|left)\s*:\s*([^;{}]*)/g;
  const problems = [];
  for (const [file, css] of allCss()) {
    for (const m of css.matchAll(lengthOnly)) {
      if (/\b(solid|dashed|dotted|double|groove|ridge)\b/.test(m[2])) {
        problems.push(`${file}: ${m[0].trim().slice(0, 70)}`);
      }
    }
  }
  assert.deepEqual(problems, [], `border shorthand on a length-only property:\n${problems.join('\n')}`);
});

test('no declaration is left with an empty value', () => {
  const problems = [];
  for (const [file, css] of allCss()) {
    for (const m of css.matchAll(/(?<![-\w])([a-z][a-z-]+)\s*:\s*(?=[;}])/g)) problems.push(`${file}: ${m[1]}`);
  }
  assert.deepEqual(problems, [], `empty CSS values:\n${problems.join('\n')}`);
});

/* The trust badges lost their pill styling once — a block deletion that was
   meant to remove a card took .gcq-badge and .gcq-actives out with it, and the
   checks in flight only counted badges rather than looking at them, so plain
   text passed. Cheap assertion that the rules still exist. */
test('the trust badges are still styled as pills', () => {
  const css = styleCss('gc-quality.liquid');
  for (const need of ['.gcq-badge{', 'border-radius:var(--r-full)', '.gcq-actives{']) {
    assert.ok(css.includes(need), `gc-quality.liquid lost "${need}"`);
  }
});

/* NaN Jaune ships as a TRIAL build and a licensed build with near-identical
   filenames, and a trial file sitting next to the licensed one in Downloads is
   exactly how the wrong one gets copied. The trial licence forbids web
   embedding, so shipping it is a licensing problem, not a visual one. */
test('no TRIAL font build is in the theme', () => {
  const offenders = readdirSync(ASSETS).filter((f) => /trial/i.test(f));
  assert.deepEqual(offenders, [], `TRIAL font in assets: ${offenders.join(', ')}`);
});

test('the display font is declared and actually used by headings', () => {
  const css = read(join(ASSETS, 'gc-brand.css'));
  assert.ok(/@font-face\{font-family:'NaN Jaune Maxi'/.test(css.replace(/\s+/g, '')) ||
            css.includes("font-family:'NaN Jaune Maxi'"), 'NaN Jaune @font-face missing');
  const heading = css.split('\n').find((l) => l.startsWith('h1,h2,h3,h4'));
  assert.ok(heading && heading.includes("'NaN Jaune Maxi'"),
    'headings are not set in the brand display face');
});

test('every @font-face file referenced by the CSS exists in assets', () => {
  const css = read(join(ASSETS, 'gc-brand.css'));
  const missing = [];
  for (const m of css.matchAll(/url\('([^']+\.(?:woff2|ttf))'\)/g)) {
    if (!existsSync(join(ASSETS, m[1]))) missing.push(m[1]);
  }
  assert.deepEqual(missing, [], `@font-face points at files that are not there: ${missing.join(', ')}`);
});

/* Declared width/height must match the FILE, not just exist. All three shop
   rows carried width="406" (Dhi's width) while Nain is 316 and Tara 330, so
   two of three reserved a box a quarter wider than the image that arrived and
   shifted on load. The existing guard only checked the attributes were
   present, which they were — wrongly. This reads the real pixels out of the
   WebP header, with no dependency and no shelling out. */
function webpSize(buf) {
  if (buf.length < 30) return null;
  if (buf.toString('ascii', 0, 4) !== 'RIFF' || buf.toString('ascii', 8, 12) !== 'WEBP') return null;
  const tag = buf.toString('ascii', 12, 16);
  if (tag === 'VP8X') return { w: buf.readUIntLE(24, 3) + 1, h: buf.readUIntLE(27, 3) + 1 };
  if (tag === 'VP8 ') return { w: buf.readUInt16LE(26) & 0x3fff, h: buf.readUInt16LE(28) & 0x3fff };
  if (tag === 'VP8L') {
    const b = buf.readUInt32LE(21);
    return { w: (b & 0x3fff) + 1, h: ((b >> 14) & 0x3fff) + 1 };
  }
  return null;
}

test('declared image dimensions match the actual asset files', () => {
  const problems = [];
  const files = [...gcSections().map((f) => [f, join(SECTIONS, f)]),
                 ...readdirSync(join(THEME, 'snippets')).filter((f) => /^gc/.test(f))
                   .map((f) => [f, join(THEME, 'snippets', f)])];
  for (const [label, path] of files) {
    const src = read(path);
    for (const m of src.matchAll(/<img\b[^>]*?>/gs)) {
      const tag = m[0];
      const file = (tag.match(/'([\w.-]+\.webp)'/) || [])[1];
      const w = (tag.match(/width="(\d+)"/) || [])[1];
      const h = (tag.match(/height="(\d+)"/) || [])[1];
      if (!file || !w || !h) continue;
      const asset = join(ASSETS, file);
      if (!existsSync(asset)) continue;
      const real = webpSize(readFileSync(asset));
      if (!real) continue;
      if (Number(w) !== real.w || Number(h) !== real.h) {
        problems.push(`${label}: ${file} declared ${w}x${h}, file is ${real.w}x${real.h}`);
      }
    }
  }
  assert.deepEqual(problems, [], `wrong intrinsic size (causes layout shift):\n${problems.join('\n')}`);
});

/* A section's {% schema %} must be valid JSON. Shopify silently falls back —
   settings stop resolving and every `default` in the file stops applying — and
   `theme check` did not flag it. This was found the hard way: deleting one
   setting with a regex left a trailing comma before the closing bracket, which
   would have taken out every footer setting at once. */
test('every section schema is valid JSON', () => {
  const problems = [];
  for (const f of gcSections()) {
    const src = read(join(SECTIONS, f));
    const m = src.match(/\{%-?\s*schema\s*-?%\}([\s\S]*?)\{%-?\s*endschema\s*-?%\}/);
    if (!m) continue;
    try { JSON.parse(m[1]); }
    catch (e) { problems.push(`${f}: ${e.message}`); }
  }
  assert.deepEqual(problems, [], `invalid section schema:\n${problems.join('\n')}`);
});
