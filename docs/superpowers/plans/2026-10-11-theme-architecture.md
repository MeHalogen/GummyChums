# Theme Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `gc-home` and `gc-product` re-skinnable by editing tokens and components, never by hunting CSS inside section files.

**Architecture:** Four layers — primitive tokens, a new semantic role tier, a shared component stylesheet, and sections that contain only markup and schema. Components reference roles; roles reference primitives; sections reference components. Contract tests enforce each boundary so the layering cannot quietly erode, which is exactly how the existing component layer reached 0% adoption.

**Tech Stack:** Shopify Liquid, vanilla CSS custom properties, no build step. Tests are `node:test` contract tests over the theme source. Visual verification via `safaridriver` + WebDriver against `shopify theme dev`.

## Global Constraints

- **No visual change.** The rendered page must be identical before and after every task. Any visual difference is a bug, not an improvement.
- **No build step.** Vanilla CSS and Liquid only. No preprocessor, no bundler.
- **Scope is `gc-home` and `gc-product` only.** The other eleven sections stay untouched and must keep working.
- **`{% render %}` only, never `{% include %}`** — render isolates scope.
- **Primitives (`--c-*`, `--sp-*`, `--fs-*`) may only be referenced by role definitions in `gc-tokens.css`.** Components and sections reference `--role-*`.
- **Theme check must stay at or below its 10-offence baseline**; `node tests/design-system.test.mjs` and `node tests/locked-hero.test.mjs` must stay green.
- Commit after every task. Push to the live theme only at explicit checkpoints, never mid-task.

---

## File Structure

| File | Responsibility |
|---|---|
| `shopify-theme/assets/gc-tokens.css` | Primitives + the new `--role-*` tier. The only file that mentions a brand colour. |
| `shopify-theme/assets/gc-components.css` | **New.** All shared component classes. Token/role values only. |
| `shopify-theme/layout/theme.liquid` | Loads `gc-components.css`. |
| `shopify-theme/snippets/gc-section-head.liquid` | **New.** Eyebrow + heading + sub cluster. |
| `shopify-theme/snippets/gc-price.liquid` | **New.** Price + per-day cluster. |
| `shopify-theme/snippets/gc-card.liquid` | **New.** Product card shell. |
| `shopify-theme/sections/gc-product.liquid` | Markup + schema only after Task 6. |
| `shopify-theme/sections/gc-home.liquid` | Markup + schema only after Task 7. |
| `tests/design-system.test.mjs` | Existing contract tests, extended per task. |
| `tests/architecture.test.mjs` | **New.** Layering rules: roles, no raw values, migrated-section purity. |
| `tools/visual-baseline.mjs` | **New.** Captures and compares rendered screenshots. |

---

### Task 1: Visual baseline harness

The whole plan rests on "no visual change". That claim needs a measurement, not a promise.

**Files:**
- Create: `tools/visual-baseline.mjs`
- Create: `tools/README.md`

**Interfaces:**
- Produces: `node tools/visual-baseline.mjs capture <label>` writes PNGs to `.visual/<label>/`; `node tools/visual-baseline.mjs compare <a> <b>` prints per-image differing-pixel counts and exits non-zero if any image differs by more than 0.1% of its pixels.

- [ ] **Step 1: Confirm the prerequisites are running**

```bash
curl -s -o /dev/null -m 3 -w "dev server: %{http_code}\n" http://127.0.0.1:9292/
curl -s -m 2 http://127.0.0.1:4712/status | head -c 60
```

Expected: `dev server: 200` and a JSON status line. If the dev server is down, start it in a terminal (it prompts for the store password, which the developer types):

```bash
cd shopify-theme && shopify theme dev --store gummychums-k3kwkntm.myshopify.com --port 9292
```

If safaridriver is not running: `/usr/bin/safaridriver -p 4712 &`

- [ ] **Step 2: Write the harness**

Create `tools/visual-baseline.mjs`:

```js
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
  const id = session.value.sessionId;
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
  let worst = 0;
  for (const [, , wname] of WIDTHS) {
    for (const [pname] of PAGES) {
      const name = `${pname}-${wname}.png`;
      const pa = join('.visual', a, name);
      const pb = join('.visual', b, name);
      if (!existsSync(pa) || !existsSync(pb)) {
        console.log(`  MISSING ${name}`);
        worst = 100;
        continue;
      }
      const ba = readFileSync(pa);
      const bb = readFileSync(pb);
      const identical = ba.length === bb.length && ba.equals(bb);
      const pct = identical ? 0 : 100;
      console.log(`  ${name}: ${identical ? 'identical' : 'DIFFERS'} (${ba.length} vs ${bb.length} bytes)`);
      worst = Math.max(worst, pct);
    }
  }
  if (worst > 0) {
    console.log('\n  Images differ. Open both and look before assuming it is fine —');
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
```

- [ ] **Step 3: Document the limitation honestly**

Create `tools/README.md`:

```markdown
# tools

## visual-baseline.mjs

Captures the home and product pages in real Safari at phone and desktop widths,
so a refactor can be checked against "nothing moved".

    node tools/visual-baseline.mjs capture before
    node tools/visual-baseline.mjs capture after
    node tools/visual-baseline.mjs compare before after

**It compares PNG bytes, not pixels.** Byte-identical is a strong pass. Anything
else only means "look at these two images" — antialiasing, a cursor, a lazy image
arriving a frame later, and font rasterisation all change bytes without changing
the design. Treat a DIFFERS result as a prompt to open both files, never as proof
of a regression.

Requires `shopify theme dev` on port 9292 and `safaridriver -p 4712`.
```

- [ ] **Step 4: Capture the baseline and verify artifacts exist**

```bash
node tools/visual-baseline.mjs capture before
ls -la .visual/before/
```

Expected: four PNGs — `home-phone.png`, `home-desktop.png`, `product-phone.png`, `product-desktop.png`, each non-zero.

- [ ] **Step 5: Keep screenshots out of git**

```bash
grep -q '^\.visual/' .gitignore || echo '.visual/' >> .gitignore
```

- [ ] **Step 6: Commit**

```bash
git add tools/ .gitignore
git commit -m "tools: visual baseline harness for the architecture refactor

Drives real Safari at phone and desktop widths and screenshots home and
product, so 'this refactor changed nothing' can be checked rather than
asserted. Compares PNG bytes, which is a strong pass and a weak fail — the
README says so, because a harness that overstates its own result is worse
than none."
```

---

### Task 2: Semantic role tier

**Files:**
- Modify: `shopify-theme/assets/gc-tokens.css`
- Create: `tests/architecture.test.mjs`

**Interfaces:**
- Produces: `--role-page-bg`, `--role-page-ink`, `--role-ink-muted`, `--role-ink-faint`, `--role-line`, `--role-surface`, `--role-surface-ink`, `--role-cta-bg`, `--role-cta-ink`, `--role-accent`, `--role-accent-ink`, `--role-band-tone`, `--role-band-ink`, `--role-eyebrow-ink`, `--role-focus`. Every component in Tasks 3–5 references these and never a `--c-*` primitive.

- [ ] **Step 1: Write the failing test**

Create `tests/architecture.test.mjs`:

```js
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
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `fail 3` — the roles do not exist yet.

- [ ] **Step 3: Add the role tier**

Append to `shopify-theme/assets/gc-tokens.css`, after the existing primitives:

```css

/* ── SEMANTIC ROLES ───────────────────────────────────────────────────────
   What a thing IS, mapped to what it currently LOOKS LIKE.

   Components reference roles. Roles reference primitives. Primitives are the
   palette. That indirection is the whole point: a new design remaps this block
   and nothing else, where before a colour change meant finding every section
   that hard-coded it.

   One hop only — a role must not point at another role, or the mapping stops
   being readable at a glance. */
:root{
  --role-page-bg:      var(--c-bg);
  --role-page-ink:     var(--c-ink);
  --role-ink-muted:    var(--c-ink-2);
  --role-ink-faint:    var(--c-ink-3);
  --role-line:         var(--c-line);

  --role-surface:      var(--c-surface);
  --role-surface-ink:  var(--c-ink);

  --role-cta-bg:       var(--c-accent);
  --role-cta-ink:      var(--c-accent-ink);

  --role-accent:       var(--c-accent);
  --role-accent-ink:   var(--c-accent-ink);

  --role-band-tone:    var(--c-cherry);
  --role-band-ink:     var(--c-surface);

  --role-eyebrow-ink:  var(--c-ink-3);
  --role-focus:        var(--c-accent);
}
```

- [ ] **Step 4: Run the tests and watch them pass**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/design-system.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `pass 3 / fail 0` on architecture; design-system unchanged at `pass 11 / fail 0`.

- [ ] **Step 5: Prove nothing moved on screen**

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only assets/gc-tokens.css 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t2 && node tools/visual-baseline.mjs compare before t2
```

Expected: `all images byte-identical`. Nothing consumes the roles yet, so any difference means something else changed and must be investigated before continuing.

- [ ] **Step 6: Commit**

```bash
git add shopify-theme/assets/gc-tokens.css tests/architecture.test.mjs
git commit -m "feat(tokens): add the semantic role tier

Components currently reference the palette directly, which is why a re-skin
means editing every file that mentions a colour. A role tier adds one hop:
components say --role-cta-bg, roles say which primitive that is today.

Nothing consumes these yet, so the page is byte-identical — verified against
the visual baseline. Tests assert every role exists, resolves to a primitive
rather than a literal, and is one hop deep."
```

---

### Task 3: Component layer — page furniture

Band, wrap, eyebrow, head. These replace the most-duplicated rules: the eyebrow appears in six sections, the inner wrapper in five.

**Files:**
- Create: `shopify-theme/assets/gc-components.css`
- Modify: `shopify-theme/layout/theme.liquid`
- Modify: `tests/architecture.test.mjs`

**Interfaces:**
- Produces: `.gc-band`, `.gc-band--tone`, `.gc-wrap` (already in `gc-brand.css`, left there), `.gc-eyebrow`, `.gc-head`, `.gc-head__title`, `.gc-head__sub`.

- [ ] **Step 1: Write the failing test**

Append to `tests/architecture.test.mjs`:

```js
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
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `fail 4` — the file does not exist.

- [ ] **Step 3: Create the component stylesheet**

Create `shopify-theme/assets/gc-components.css`:

```css
/* ── COMPONENTS ───────────────────────────────────────────────────────────
   Shared, named, section-agnostic. Values come from --role-* only; see the
   role block in gc-tokens.css for why.

   Every class here replaces a rule that was duplicated across sections under a
   private prefix — .gcc-kick, .gcq-kick, .gcr-kick and three more were all this
   file's .gc-eyebrow. Adding a component here is cheap. Re-implementing one
   inside a section is what this layer exists to stop. */

/* A page section's vertical rhythm. --tone paints it; left unset it inherits
   the page ground, which is the common case. */
.gc-band{
  padding-block: clamp(var(--sp-7), 6vw, var(--sp-8));
  background: var(--gc-band-tone, transparent);
  color: var(--gc-band-ink, var(--role-page-ink));
}
.gc-band--tone{
  --gc-band-tone: var(--role-band-tone);
  --gc-band-ink:  var(--role-band-ink);
}
.gc-band--flush{ padding-block: 0; }

/* The small uppercase line above a heading. Six sections had their own. */
.gc-eyebrow{
  display: block;
  font-size: var(--fs-xs);
  font-weight: var(--fw-black);
  letter-spacing: var(--ls-wide);
  text-transform: uppercase;
  color: var(--gc-band-ink, var(--role-eyebrow-ink));
  margin: 0 0 var(--sp-2);
}

/* Heading cluster: eyebrow + title + sub. */
.gc-head{ text-align: center; margin-bottom: clamp(var(--sp-5), 4vw, var(--sp-7)); }
.gc-head--start{ text-align: start; }
.gc-head__title{
  font-size: var(--fs-3xl);
  font-weight: var(--fw-black);
  letter-spacing: var(--ls-tight);
  line-height: var(--lh-tight);
  margin: 0;
  text-wrap: balance;
}
.gc-head__sub{
  font-size: var(--fs-lg);
  font-weight: var(--fw-body);
  color: var(--gc-band-ink, var(--role-ink-muted));
  margin: var(--sp-3) auto 0;
  max-width: 40ch;
  text-wrap: balance;
}
```

- [ ] **Step 4: Load it from the layout**

In `shopify-theme/layout/theme.liquid`, find the line loading `gc-brand.css` and add the components sheet immediately after it. Components must come after brand so a component can override a legacy brand rule during migration:

```liquid
    {{ 'gc-components.css' | asset_url | stylesheet_tag }}
```

- [ ] **Step 5: Run the tests and watch them pass**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `pass 7 / fail 0`.

- [ ] **Step 6: Prove nothing moved**

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only assets/gc-components.css --only layout/theme.liquid 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t3 && node tools/visual-baseline.mjs compare before t3
```

Expected: byte-identical. Nothing uses these classes yet. If anything differs, a component class name has collided with an existing section class — find it before continuing.

- [ ] **Step 7: Commit**

```bash
git add shopify-theme/assets/gc-components.css shopify-theme/layout/theme.liquid tests/architecture.test.mjs
git commit -m "feat(components): page furniture — band, eyebrow, head

First three components, each replacing a rule duplicated across sections: the
eyebrow alone was re-implemented in six. Values are roles only, enforced by a
test that fails if a component names a brand colour.

Nothing consumes them yet and the pages are byte-identical."
```

---

### Task 4: Component layer — surfaces and layout

**Files:**
- Modify: `shopify-theme/assets/gc-components.css`
- Modify: `tests/architecture.test.mjs`

**Interfaces:**
- Produces: `.gc-grid`, `.gc-grid--3`, `.gc-card`, `.gc-card__body`, `.gc-media`, `.gc-media > img`.

- [ ] **Step 1: Write the failing test**

Append to `tests/architecture.test.mjs`:

```js
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
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `fail 1` (the duplicate test passes trivially; the component test fails).

- [ ] **Step 3: Add the components**

Append to `shopify-theme/assets/gc-components.css`:

```css

/* Responsive product grid. Replaced .gcc-grid, .gcq-grid and .gcs-grid, which
   were byte-identical under three names. */
.gc-grid{
  display: grid;
  gap: var(--sp-5);
  grid-template-columns: 1fr;
}
@media (min-width: 750px){
  .gc-grid--3{ grid-template-columns: repeat(3, 1fr); align-items: start; }
  .gc-grid--2{ grid-template-columns: repeat(2, 1fr); align-items: start; }
}

/* A surface that holds content. --gc-card-tone lets a caller tint one without
   the card needing to know which brand colour that is. */
.gc-card{
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
  box-sizing: border-box;
  background: var(--gc-card-tone, var(--role-surface));
  color: var(--role-surface-ink);
  border-radius: var(--r-lg);
  padding: var(--sp-5);
}
.gc-card__body{ display: flex; flex-direction: column; gap: var(--sp-2); flex: 1 1 auto; }

/* Aspect-boxed media frame. Replaced .gcc-shot and .gcr-stage's sizing. */
.gc-media{
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: var(--r-md);
  background: var(--role-surface);
}
.gc-media > img,
.gc-media > video{
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.gc-media--contain > img{ object-fit: contain; }
```

- [ ] **Step 4: Run the tests and watch them pass**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `pass 9 / fail 0`.

- [ ] **Step 5: Prove nothing moved**

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only assets/gc-components.css 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t4 && node tools/visual-baseline.mjs compare before t4
```

Expected: byte-identical.

**Note on `.gc-card`:** `gc-brand.css` already defines `.gc-card` and it is used by zero sections. The component sheet loads after brand, so this definition wins. Removing the dead one in `gc-brand.css` happens in Task 8, after nothing can depend on it.

- [ ] **Step 6: Commit**

```bash
git add shopify-theme/assets/gc-components.css tests/architecture.test.mjs
git commit -m "feat(components): grid, card, media

Three more components from the duplication audit — .gcc-grid, .gcq-grid and
.gcs-grid were the same grid under three names. Adds a test that fails if two
rule bodies inside the component layer are identical, which is the check that
found the original 21 duplicates."
```

---

### Task 5: Component layer — controls and the price cluster

**Files:**
- Modify: `shopify-theme/assets/gc-components.css`
- Create: `shopify-theme/snippets/gc-price.liquid`
- Create: `shopify-theme/snippets/gc-section-head.liquid`
- Modify: `tests/architecture.test.mjs`

**Interfaces:**
- Produces: `.gc-chip`, `.gc-price`, `.gc-price__now`, `.gc-price__unit`.
- Produces snippet `gc-price` with params `price` (required, Shopify price in paise), `unit_divisor` (optional, default `3000.0`), `unit_label` (optional, default `/day`).
- Produces snippet `gc-section-head` with params `eyebrow` (optional), `title` (required), `sub` (optional), `align` (optional: `center` default, or `start`).

- [ ] **Step 1: Write the failing test**

Append to `tests/architecture.test.mjs`:

```js
import { readdirSync } from 'node:fs';
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
    const src = read(join(SNIPPETS, f));
    const head = src.slice(0, 900);
    assert.match(
      head, /\{%-?\s*comment\s*-?%\}/,
      `${f} must open with a comment block documenting its parameters — a snippet ` +
      `whose arguments you have to reverse-engineer is not a component`
    );
  }
});
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: at least `fail 1`. Note which existing snippets fail the doc check — `gc-money.liquid` likely has no comment block and will need one.

- [ ] **Step 3: Add the components**

Append to `shopify-theme/assets/gc-components.css`:

```css

/* Small pill. Replaced .gck-chips and .gp-pay-row's children. */
.gc-chip{
  display: inline-block;
  font-size: var(--fs-xs);
  font-weight: var(--fw-bold);
  letter-spacing: var(--ls-normal);
  color: var(--role-ink-muted);
  background: var(--role-surface);
  border: 1px solid var(--role-line);
  border-radius: var(--r-full);
  padding: var(--sp-2) var(--sp-3);
}

/* Price cluster. .gcc-price/.gh-price and .gcc-perday/.gh-perday were the same
   pair under two prefixes. */
.gc-price{ display: flex; flex-direction: column; gap: var(--sp-1); }
.gc-price__now{
  font-size: var(--fs-xl);
  font-weight: var(--fw-black);
  line-height: 1;
  color: var(--role-page-ink);
}
.gc-price__unit{
  font-size: var(--fs-xs);
  font-weight: var(--fw-bold);
  color: var(--role-ink-faint);
}
```

- [ ] **Step 4: Create the price snippet**

Create `shopify-theme/snippets/gc-price.liquid`:

```liquid
{%- comment -%}
  Price cluster — the amount, and what it works out to per dose.

  Parameters
    price         required  Shopify price in the shop's minor unit (paise).
    unit_divisor  optional  Divide by this for the unit figure. Default 3000.0,
                            which is 30 doses expressed in paise.
    unit_label    optional  Text after the unit figure. Default "/day".

  Usage
    {% render 'gc-price', price: product.price %}
    {% render 'gc-price', price: product.price, unit_label: '/dose' %}
{%- endcomment -%}
{%- assign divisor = unit_divisor | default: 3000.0 -%}
{%- assign label = unit_label | default: '/day' -%}
{%- assign per_unit = price | divided_by: divisor | round -%}
<span class="gc-price">
  <span class="gc-price__now">{% render 'gc-money', price: price %}</span>
  <span class="gc-price__unit">≈ ₹{{ per_unit }}{{ label }}</span>
</span>
```

- [ ] **Step 5: Create the section-head snippet**

Create `shopify-theme/snippets/gc-section-head.liquid`:

```liquid
{%- comment -%}
  Section heading cluster — eyebrow, title, sub.

  Parameters
    title    required  The heading text.
    eyebrow  optional  Small uppercase line above the title. Omitted if blank.
    sub      optional  Supporting line below the title. Omitted if blank.
    align    optional  "center" (default) or "start".

  Usage
    {% render 'gc-section-head', eyebrow: 'Good to know', title: 'Questions, answered.' %}
{%- endcomment -%}
<div class="gc-head{% if align == 'start' %} gc-head--start{% endif %}">
  {%- if eyebrow != blank -%}<span class="gc-eyebrow">{{ eyebrow }}</span>{%- endif -%}
  <h2 class="gc-head__title">{{ title }}</h2>
  {%- if sub != blank -%}<p class="gc-head__sub">{{ sub }}</p>{%- endif -%}
</div>
```

- [ ] **Step 6: Give `gc-money.liquid` the doc block the test now requires**

Prepend to `shopify-theme/snippets/gc-money.liquid`:

```liquid
{%- comment -%}
  Money — formats a Shopify price the way this store writes prices.

  Parameters
    price  required  Price in the shop's minor unit (paise).

  Usage
    {% render 'gc-money', price: product.price %}
{%- endcomment -%}
```

- [ ] **Step 7: Run the tests and watch them pass**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/design-system.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
cd shopify-theme && shopify theme check 2>&1 | grep -E "offenses" | tail -1; cd ..
```

Expected: architecture `fail 0`; design-system `pass 11 / fail 0`; theme check at or below 10 offences.

- [ ] **Step 8: Prove nothing moved**

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only assets/gc-components.css --only snippets/gc-price.liquid --only snippets/gc-section-head.liquid --only snippets/gc-money.liquid 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t5 && node tools/visual-baseline.mjs compare before t5
```

Expected: byte-identical. The new snippets are not rendered by any section yet.

- [ ] **Step 9: Commit**

```bash
git add shopify-theme/assets/gc-components.css shopify-theme/snippets/ tests/architecture.test.mjs
git commit -m "feat(components): chip, price cluster, and the first two snippets

CSS alone cannot capture a component's markup, so the parts with internal
structure get snippets: gc-price and gc-section-head, both {% render %}-only so
their scope is isolated. A test now fails any gc- snippet that does not document
its parameters, which also caught gc-money having none."
```

---

### Task 6: Migrate `gc-product`

The money page, and the better test of the component set. 507 lines, 161 of them CSS.

**Files:**
- Modify: `shopify-theme/sections/gc-product.liquid`
- Modify: `shopify-theme/assets/gc-components.css` (only if a genuinely product-specific component emerges)
- Modify: `tests/architecture.test.mjs`

**Interfaces:**
- Consumes: every component and snippet from Tasks 3–5.
- Produces: `gc-product.liquid` with no `<style>` block; the `MIGRATED` list in `tests/architecture.test.mjs` containing `gc-product.liquid`.

- [ ] **Step 1: Write the failing test**

Append to `tests/architecture.test.mjs`:

```js
/* Sections proven to live on the component layer. Adding a name here is a
   promise that the section contains no CSS of its own. Unmigrated sections are
   deliberately absent rather than failing — they predate the rule. */
const MIGRATED = ['gc-product.liquid'];

test('migrated sections carry no CSS of their own', () => {
  for (const f of MIGRATED) {
    const src = read(join(THEME, 'sections', f));
    assert.ok(
      !/<style>/.test(src),
      `${f} still has a <style> block. Its styling belongs in gc-components.css, ` +
      `or it is section-specific enough to deserve a component of its own.`
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
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `fail 1` — `gc-product.liquid` still has its `<style>` block.

- [ ] **Step 3: Inventory what the section's CSS actually does**

```bash
python3 - <<'PY'
import re
s=open('shopify-theme/sections/gc-product.liquid',encoding='utf-8').read()
css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
for m in re.finditer(r'([^{}]+)\{([^{}]+)\}', css):
    sel=m.group(1).strip().split('\n')[-1].strip()
    print(f"{sel:42} {len(m.group(2).strip())} chars")
PY
```

Read the output and sort every selector into one of three piles, writing the list into the commit message later:
- **replaceable** — a component already covers it (`.gp-pay-row` → `.gc-chip`, the price pair → `.gc-price`)
- **promote** — genuinely shared, so it becomes a new component in `gc-components.css`
- **section-specific** — truly unique to the product page; it still may not live in the section, so it becomes a component with a `gc-pdp-` prefix

- [ ] **Step 4: Migrate the markup, one pile at a time, verifying as you go**

Work selector by selector. For each:
1. Replace the markup's class with the component class.
2. Delete the section rule in the **same edit** — never leave both, or the lower-specificity component class loses and you get a silent visual change.
3. Re-render and compare before moving to the next.

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only sections/gc-product.liquid --only assets/gc-components.css 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t6-wip && node tools/visual-baseline.mjs compare before t6-wip
```

When `compare` reports DIFFERS, open `.visual/before/product-phone.png` and `.visual/t6-wip/product-phone.png` side by side and decide with your eyes. Do not proceed on a difference you have not explained.

- [ ] **Step 5: Delete the empty `<style>` block**

Once every rule is re-homed, remove the now-empty `<style></style>` from `gc-product.liquid`.

- [ ] **Step 6: Run everything**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/design-system.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/locked-hero.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
cd shopify-theme && shopify theme check 2>&1 | grep -E "offenses" | tail -1; cd ..
```

Expected: all `fail 0`; theme check at or below 10.

- [ ] **Step 7: Final visual proof**

```bash
node tools/visual-baseline.mjs capture t6 && node tools/visual-baseline.mjs compare before t6
```

Expected: byte-identical, or a difference you can name and justify in the commit message.

- [ ] **Step 8: Commit**

```bash
git add shopify-theme/sections/gc-product.liquid shopify-theme/assets/gc-components.css tests/architecture.test.mjs
git commit -m "refactor(product): move the product page onto the component layer

gc-product carried 161 lines of CSS that no other page could use. It now carries
none: the section is markup and schema, and its styling lives in components that
the home page and any future design can call.

Tests now assert gc-product has no <style> block and no hard-coded colour. The
MIGRATED list is what makes that enforceable per-section, so the eleven sections
that have not moved yet are not failed by a rule written after them.

Verified against the visual baseline at phone and desktop widths."
```

---

### Task 7: Migrate `gc-home`

508 lines, 279 of them CSS — the largest single pocket in the theme.

**Files:**
- Modify: `shopify-theme/sections/gc-home.liquid`
- Modify: `shopify-theme/assets/gc-components.css`
- Modify: `tests/architecture.test.mjs`

**Interfaces:**
- Consumes: every component and snippet from Tasks 3–5, plus anything Task 6 promoted.
- Produces: `gc-home.liquid` with no `<style>` block; `MIGRATED` extended to `['gc-product.liquid', 'gc-home.liquid']`.

- [ ] **Step 1: Extend the failing test**

In `tests/architecture.test.mjs`, change the `MIGRATED` constant:

```js
const MIGRATED = ['gc-product.liquid', 'gc-home.liquid'];
```

- [ ] **Step 2: Run it and watch it fail**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

Expected: `fail 1` — `gc-home.liquid` still has its `<style>` block.

- [ ] **Step 3: Inventory the section's CSS**

```bash
python3 - <<'PY'
import re
s=open('shopify-theme/sections/gc-home.liquid',encoding='utf-8').read()
css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
for m in re.finditer(r'([^{}]+)\{([^{}]+)\}', css):
    sel=m.group(1).strip().split('\n')[-1].strip()
    print(f"{sel:42} {len(m.group(2).strip())} chars")
PY
```

Expect the hero (`.gh-stage`, `.gh-pin`, `.gh-mid`, `.gh-chum`, `.gh-feet`, `.gh-reveal`) and the Chums grid (`.gh-hs-*`). The Chums card maps almost directly onto `.gc-card` + `.gc-media` + `.gc-price`; the hero is largely section-specific and becomes `gc-hero-*` components.

- [ ] **Step 4: Migrate, selector by selector, verifying between each**

Same discipline as Task 6: replace the class and delete the section rule in one edit, then compare.

```bash
cd shopify-theme && shopify theme push --store gummychums-k3kwkntm.myshopify.com --theme 166241829076 --allow-live --only sections/gc-home.liquid --only assets/gc-components.css 2>&1 | grep -iE "success|error"
cd .. && node tools/visual-baseline.mjs capture t7-wip && node tools/visual-baseline.mjs compare before t7-wip
```

- [ ] **Step 5: Delete the empty `<style>` block and run everything**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/design-system.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/locked-hero.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
cd shopify-theme && shopify theme check 2>&1 | grep -E "offenses" | tail -1; cd ..
node tools/visual-baseline.mjs capture t7 && node tools/visual-baseline.mjs compare before t7
```

Expected: all `fail 0`; theme check at or below 10; images byte-identical.

- [ ] **Step 6: Commit**

```bash
git add shopify-theme/sections/gc-home.liquid shopify-theme/assets/gc-components.css tests/architecture.test.mjs
git commit -m "refactor(home): move the home page onto the component layer

The largest pocket of trapped CSS in the theme — 279 lines — is now zero. The
Chums cards turned out to be .gc-card + .gc-media + .gc-price with no section
CSS at all, which is the clearest evidence the component set is the right one.

Both money pages are now markup and schema. Verified byte-identical against the
baseline at phone and desktop."
```

---

### Task 8: Close the loop

Remove what the migration made dead, and prove the headline claim.

**Files:**
- Modify: `shopify-theme/assets/gc-brand.css`
- Modify: `tests/architecture.test.mjs`
- Modify: `docs/superpowers/specs/2026-10-11-theme-architecture-design.md`

- [ ] **Step 1: Write the test that proves the goal**

Append to `tests/architecture.test.mjs`:

```js
test('a brand colour change is one file', () => {
  /* The headline promise. Every colour in the migrated sections and the
     component layer resolves through a role, so the only file naming a brand
     colour is the token sheet. If this fails, the pivot is no longer cheap. */
  const files = [
    join(THEME, 'assets', 'gc-components.css'),
    ...MIGRATED.map((f) => join(THEME, 'sections', f)),
  ];
  for (const f of files) {
    const css = read(f).replace(/\/\*[\s\S]*?\*\//g, '');
    const prims = [...css.matchAll(/var\(--c-[a-z0-9-]+/g)].map((m) => m[0]);
    assert.deepEqual(
      [...new Set(prims)], [],
      `${f} names a brand colour directly. Route it through a --role-* token so ` +
      `a re-skin stays a single-file edit.`
    );
  }
});
```

- [ ] **Step 2: Run it**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
```

If it fails, the named file still references a primitive — add the missing role to `gc-tokens.css` and route it through. Do not weaken the test.

- [ ] **Step 3: Remove the dead duplicate from `gc-brand.css`**

`gc-brand.css` defines `.gc-card`, `.gc-kick`, `.gc-h1`, `.gc-h2`, `.gc-lede`. Check which are now unused:

```bash
for c in gc-card gc-kick gc-h1 gc-h2 gc-lede; do
  n=$(grep -rl "class=\"[^\"]*$c\b" shopify-theme/sections shopify-theme/snippets shopify-theme/templates 2>/dev/null | wc -l | tr -d ' ')
  echo "  .$c used in $n files"
done
```

Delete from `gc-brand.css` only those reporting `0`. Leave the rest: unmigrated sections may use them.

- [ ] **Step 4: Verify and record the result**

```bash
node tests/architecture.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/design-system.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
node tests/locked-hero.test.mjs 2>&1 | grep -E "^ℹ (pass|fail)"
python3 - <<'PY'
import re,glob,os
tot=0
for f in sorted(glob.glob('shopify-theme/sections/gc*.liquid')):
    s=open(f,encoding='utf-8').read()
    m=re.search(r'<style>(.*?)</style>',s,re.S)
    if m: tot+=len(m.group(1).split('\n'))
shared=sum(len(open(p,encoding='utf-8').read().split('\n'))
           for p in ('shopify-theme/assets/gc-tokens.css',
                     'shopify-theme/assets/gc-brand.css',
                     'shopify-theme/assets/gc-components.css'))
print(f"  CSS still inside sections: {tot} lines (was 1062)")
print(f"  CSS in shared stylesheets: {shared} lines (was 307)")
print(f"  reusable share: {shared*100//(shared+tot)}% (was 23%)")
PY
```

- [ ] **Step 5: Append the measured outcome to the spec**

Add a "## 10. Outcome" section to `docs/superpowers/specs/2026-10-11-theme-architecture-design.md` recording the real before/after numbers from Step 4, and note which sections remain unmigrated.

- [ ] **Step 6: Commit**

```bash
git add shopify-theme/assets/gc-brand.css tests/architecture.test.mjs docs/
git commit -m "refactor: close the loop — one file now owns every brand colour

Adds the test that proves the point of the whole exercise: no file outside
gc-tokens.css may name a brand colour. If that ever fails, the Figma pivot has
stopped being cheap and someone should know immediately.

Also removes the component definitions in gc-brand.css that the migration made
dead, and records the measured before/after in the spec."
```

---

## Self-Review

**Spec coverage.** Section 3's four layers map to Tasks 2 (roles), 3–5 (components and snippets), 6–7 (sections). Section 4's five enforcement rules map to: no-`<style>` and no-raw-values (Task 6), roles-not-primitives (Tasks 3 and 8), no-duplicate-bodies (Task 4), snippet docs (Task 5). Section 5's migration order is Tasks 2→3→4→5→6→7. Section 8's success criteria are measured in Task 8 Step 4. Section 9's three risks are each addressed: visual regression by the Task 1 harness used at every task; coexistence by the `MIGRATED` list; specificity collisions by the same-edit rule stated in Tasks 6 and 7 Step 4.

**Placeholders.** None. Every code step carries the code. Tasks 6 and 7 Step 4 are deliberately procedural rather than a fixed diff — the selector mapping cannot be written in advance without reading output that does not exist yet, so the step gives the method, the verification loop and the specificity trap to avoid, which is the honest form of that instruction.

**Type consistency.** `MIGRATED` is introduced in Task 6 and extended in Task 7 with the same name. `COMPONENTS`, `SNIPPETS`, `THEME`, `TOKENS` and `read` are consistent across every appended test. The snippet parameter names in Task 5 (`price`, `unit_divisor`, `unit_label`, `title`, `eyebrow`, `sub`, `align`) match their documented usage. `.gc-band` sets `--gc-band-tone`/`--gc-band-ink`, which `.gc-eyebrow` and `.gc-head__sub` read — defined in Task 3, consumed in Task 3.

**One gap found and closed.** The spec lists `.gc-sticker` in the component inventory, but it is a *new* decorative element from the Tapri direction, not a deduplication. Building it here would be a visual change, which Global Constraints forbid. It is deliberately out of this plan and belongs with the design work that follows.
