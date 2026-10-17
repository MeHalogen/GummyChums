# Hero Threshold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the "What's inside?" contents of the hero's pink dome with a staggered kolam threshold, and move the displaced ingredient copy to the certifications strip.

**Architecture:** `.gh-reveal` keeps every structural property — it is the ground the Chums stand on — and only its children change. The kolam snippet is reused unmodified; its two hard-coded transition delays become CSS variables so three instances can be staggered from the markup. The reveal is fired once by the existing `.gc-rise` IntersectionObserver, never by scroll position.

**Tech Stack:** Shopify Liquid, plain CSS (custom properties, SVG `stroke-dashoffset`), `node:test`.

**Spec:** `docs/superpowers/specs/2026-10-17-hero-threshold-design.md`

## Global Constraints

- No `animation-timeline`, `position: sticky`, scroll listener, scaled gradient, or `will-change` anywhere in this work. (spec §6)
- Three kolam instances maximum. (spec §6)
- Sections carry no `<style>` block and no raw hex; all CSS lives in a linked stylesheet. Enforced by `tests/architecture.test.mjs`.
- Components reference `--role-*`, never `--c-*` primitives. Enforced by `tests/architecture.test.mjs`.
- Threshold copy, verbatim: line `Come in.`, sub `One a day, every day.` (spec §4.3)
- Stagger delays, verbatim (spec §4.2):
  | Instance | `--k-dot-delay` | `--k-delay` |
  |---|---|---|
  | 1 | `0s` | `.38s` |
  | 2 | `.54s` | `.92s` |
  | 3 | `1.08s` | `1.46s` |
- Shopify rejects `"default": ""` on a text setting — omit the key rather than setting it empty.
- A `theme push` reports per-file failures and still exits 0. Read the output, not the exit code.
- All three existing suites stay green: `architecture` (15), `design-system` (11), `locked-hero` (8).

## Review Focus

1. **Script absent or `gc-brand.js` fails to run** — `.in` is never added, so dots stay at `opacity: 0` and the line stays fully dashed. The hero's centrepiece renders as an empty pink band. A reasonable person expects the drawing to be visible, not animated, when scripting is off. Pinned in Task 1.
2. **Merchant blanks `reveal_title` or `reveal_sub` in the theme editor** — Liquid renders an empty `<h2>`/`<p>`, leaving its margins and a gap. Expect the element to be omitted entirely. Pinned in Task 2.
3. **`prefers-reduced-motion: reduce` combined with the new delay variables** — a delay must not resurrect motion the reduced-motion branch disabled. Expect dots and line at their final state with no transition. Pinned in Task 1.
4. **Viewport ≤ 380px** — three kolams plus gaps exceed the content width and introduce horizontal page scroll. Expect the row to drop to two rather than overflow or shrink below legibility. Pinned in Task 2.
5. **Merchant switches `gc-quality`'s `layout` to `full` on the homepage** — the no-sugar badge and the actives line live only in the `badges` branch and silently vanish. Expect both branches to carry the claim. Pinned in Task 3.

---

### Task 1: Kolam stagger variables

Makes the shared kolam animation parameterisable without changing what it does today, and closes two robustness gaps in it.

**Files:**
- Modify: `shopify-theme/assets/gc-brand.css:191-200`
- Create: `tests/hero-threshold.test.mjs`

**Interfaces:**
- Produces: two CSS custom properties read by `.gc2-kolam-dots` / `.gc2-kolam-line` —
  `--k-dot-delay` (default `0s`) and `--k-delay` (default `.38s`). Task 2 sets both per instance via inline `style`.

- [ ] **Step 1: Write the failing tests**

Create `tests/hero-threshold.test.mjs` following the idiom of `tests/architecture.test.mjs`: `node:test`, `assert/strict`, a `read(p)` helper over `readFileSync(p, 'utf8')`, and a file-level block comment saying why the file exists.

Four tests, against `shopify-theme/assets/gc-brand.css`:

```js
test('kolam delays are variables, not hard-coded', () => {
  // .gc2-kolam-line's transition must use var(--k-delay, …)
  // .gc2-kolam-dots's transition must use var(--k-dot-delay, …)
});

test('kolam delay fallbacks match what the story teaser relies on', () => {
  // --k-delay fallback is .38s, --k-dot-delay fallback is 0s
});

test('reduced motion still cancels the kolam transition', () => {
  // the prefers-reduced-motion block sets transition:none
  // and leaves dots at .55 opacity and the line at dashoffset 0
});

test('the kolam is drawn even when scripting is off', () => {
  // an @media (scripting: none) block sets the same final state,
  // so a failed or blocked gc-brand.js does not leave the band empty
});
```

- [ ] **Step 2: Run to verify they fail**

Run: `node --test tests/hero-threshold.test.mjs`
Expected: FAIL — 4 failing. The runner summarises with `ℹ fail 4`, not `# fail 4`; grep for `^ℹ fail` if filtering.

- [ ] **Step 3: Edit `gc-brand.css:191-193`**

Replace the two hard-coded delays with `var(--k-dot-delay, 0s)` and `var(--k-delay, .38s)`. Change nothing else about the transitions — durations and easing stay as they are, because the story teaser's kolam must be byte-equivalent in behaviour.

- [ ] **Step 4: Add the `scripting: none` branch after the reduced-motion block**

Mirror the three declarations the reduced-motion block already uses for the final state.

- [ ] **Step 5: Run to verify they pass**

Run: `node --test tests/hero-threshold.test.mjs`
Expected: `ℹ pass 4`, `ℹ fail 0`.

- [ ] **Step 6: Confirm nothing else regressed**

Run: `node --test tests/architecture.test.mjs tests/design-system.test.mjs tests/locked-hero.test.mjs`
Expected: `ℹ pass 34`, `ℹ fail 0`.

- [ ] **Step 7: Commit**

```bash
git add tests/hero-threshold.test.mjs shopify-theme/assets/gc-brand.css
git commit -m "refactor(kolam): make the draw delays settable, and survive no-JS"
```

---

### Task 2: The threshold band

Replaces the dome's contents and proves the dome itself survives intact.

**Files:**
- Modify: `shopify-theme/sections/gc-home.liquid:1-14` (the stale lock banner), `:47-52` (the band's children), `:205-206` (schema)
- Modify: `shopify-theme/assets/section-gc-home.css` (add threshold layout near the existing `.gh-reveal` rules at `:128-139`)
- Modify: `tests/hero-threshold.test.mjs`

**Interfaces:**
- Consumes: `--k-delay` / `--k-dot-delay` from Task 1.
- Consumes: `{% render 'gc2-kolam', id: <unique>, tone: '--c-surface', size: 96 %}` — `id` MUST be pre-assigned with `{%- assign -%}`; `{% render %}` does not evaluate filters.
- Produces: `.gh-thresh`, `.gh-thresh__line`, `.gh-thresh__sub`, `.gh-thresh__kolams`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/hero-threshold.test.mjs`. Read the section plus its linked stylesheets, the way `tests/locked-hero.test.mjs` does — reading only the `.liquid` would miss CSS regressions.

```js
test('the dome keeps the floor the Chums stand on', () => {
  // .gh-reveal still declares: the negative top margin
  // calc(var(--gh-chum-h) * -0.14), the dome radius 50% 50% 0 0,
  // and bottom padding including 128px to clear .gh-edge's -128px pull
});

test('the threshold renders exactly three kolams', () => {
  // three gc2-kolam renders, no more — spec §6 caps it
});

test('each kolam carries its own stagger delays', () => {
  // the three --k-delay values are .38s, .92s, 1.46s
  // and the three --k-dot-delay values are 0s, .54s, 1.08s
});

test('threshold copy is omitted when blank, not rendered empty', () => {
  // both reveal_title and reveal_sub are guarded by `!= blank`
});

test('the kolam row narrows before it overflows', () => {
  // section-gc-home.css hides the third kolam at max-width:380px
});
```

- [ ] **Step 2: Run to verify they fail**

Run: `node --test tests/hero-threshold.test.mjs`
Expected: 5 new failures; Task 1's 4 still pass.

- [ ] **Step 3: Replace the band's children in `gc-home.liquid:48-51`**

`.gh-reveal`'s own opening and closing tags and its class list stay exactly as they are. Inside it: a `.gh-thresh` wrapper holding the guarded `<h2 class="gh-thresh__line">` and `<p class="gh-thresh__sub">`, then a `.gh-thresh__kolams gc-rise` row marked `aria-hidden="true"` holding three spans. Each span sets both delay variables inline from the Global Constraints table and renders the kolam with `tone: '--c-surface'`.

`.gc-rise` goes on the kolam row only — putting it on `.gh-reveal` would apply its transform to the dome geometry itself.

- [ ] **Step 4: Update the schema at `:205-206`**

Keep the ids `reveal_title` and `reveal_sub` so no template edit is needed. Relabel to "Threshold line" / "Threshold sub" and set the defaults to the verbatim copy in Global Constraints.

- [ ] **Step 5: Rewrite the stale lock banner at `:1-14`**

It currently claims to lock the pink gummy scroll sequence, naming `--zoom-k`, `--rise-end`, `.gh-pin .gh-gummy` and `.gh-reveal`'s transform and fade — none of which exist since the sequence was removed on 11 Oct 2026. Replace it with what is actually load-bearing now: `.gh-reveal` is the Chums' floor, its negative margin / dome radius / bottom padding are structural rather than cosmetic, and `tests/hero-threshold.test.mjs` fails if they move.

- [ ] **Step 6: Add the threshold layout to `section-gc-home.css`**

Place it beside the existing `.gh-reveal` rules. Decisions the implementer should not re-derive:
- kolam width override `clamp(64px, 20vw, 112px)` with `height: auto`, which beats the snippet's px attributes because the SVG has a `viewBox`
- the row is a centred flex row with `var(--sp-6)` gaps
- at `max-width: 380px` the third kolam is `display: none` (spec §5.2 — drop one rather than shrink below legibility)
- `.gh-thresh__line` inherits the existing `.gh-reveal h2` treatment; restate `color` only if the cascade requires it, since Dawn sets an explicit heading colour

- [ ] **Step 7: Run every suite**

Run: `node --test tests/hero-threshold.test.mjs tests/architecture.test.mjs tests/design-system.test.mjs tests/locked-hero.test.mjs`
Expected: `ℹ pass 43`, `ℹ fail 0`.

- [ ] **Step 8: Run theme check**

Run: `cd shopify-theme && shopify theme check`
Expected: 10 offences — the pre-existing count. A higher number is a regression introduced here.

- [ ] **Step 9: Commit**

```bash
git add shopify-theme/sections/gc-home.liquid shopify-theme/assets/section-gc-home.css tests/hero-threshold.test.mjs
git commit -m "feat(home): the dome becomes a drawn threshold"
```

---

### Task 3: The ingredients find a new home

**Files:**
- Modify: `shopify-theme/sections/gc-quality.liquid:55-61` (badges branch) and the `full` branch below it
- Modify: `tests/hero-threshold.test.mjs`

**Interfaces:**
- Consumes: nothing from Tasks 1–2.

- [ ] **Step 1: Write the failing tests**

```js
test('the no-sugar claim survives either quality layout', () => {
  // "No added sugar" appears in BOTH the badges and full branches,
  // so switching layout in the theme editor cannot drop it
});

test('the actives are listed on the certifications strip', () => {
  // Bacopa, Melatonin and Lutein all appear in gc-quality.liquid
});
```

- [ ] **Step 2: Run to verify they fail**

Run: `node --test tests/hero-threshold.test.mjs`
Expected: 2 new failures.

- [ ] **Step 3: Add to the `badges` branch**

A fifth `.gcq-badge` reading `🍬 No added sugar`, and below the badge row a `.gcq-actives` paragraph reading `Bacopa · Melatonin · Lutein`. Hard-coded like the badges beside them, not settings.

The homepage saves `layout: "badges"` in `templates/index.json` even though the schema default is `"full"`. A change made only in the `full` branch would not appear on the homepage at all.

- [ ] **Step 4: Add the same claim to the `full` branch**

A seventh `.gcq-card` for no added sugar, so the claim does not depend on which layout is selected.

- [ ] **Step 5: Style `.gcq-actives`**

In `gc-quality.liquid`'s own `<style>` block at `:14`. This section is deliberately
NOT in `tests/architecture.test.mjs`'s `MIGRATED` list — only `gc-product.liquid`
and `gc-home.liquid` are — so an inline block is the section's existing pattern
here and does not fail the no-`<style>` assertion. Do not migrate this section as
part of this work; that is a separate change with its own verification.

Centred, `--fs-sm`, `--role-ink-muted`, top margin `--sp-4`.

- [ ] **Step 6: Run every suite and theme check**

Run: `node --test tests/*.test.mjs` then `cd shopify-theme && shopify theme check`
Expected: `ℹ pass 45`, `ℹ fail 0`; 10 offences. (34 exist today across three files;
Task 1 adds 4, Task 2 adds 5, Task 3 adds 2.)

- [ ] **Step 7: Commit**

```bash
git add shopify-theme/sections/gc-quality.liquid tests/hero-threshold.test.mjs
git commit -m "feat(quality): the actives and the no-sugar claim move to the facts strip"
```

---

### Task 4: Verify it on a phone before believing it

Tests prove the contract held. They do not prove it looks right, and this project has a history of changes that passed and still shipped wrong.

**Files:** none — verification only, plus any fix it surfaces.

- [ ] **Step 1: Serve the theme**

The dev server must be started by Mehal — `shopify theme dev` needs the storefront password and the password is never typed by the agent. Confirm it is up: `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9292/` returns `200`.

- [ ] **Step 2: Check the drawing actually draws, staggered**

At 375×812, scroll the threshold into view and confirm by computed style that the three `.gc2-kolam-line` elements carry three different `transition-delay` values and that `stroke-dashoffset` reaches 0. A screenshot taken mid-animation proves nothing; read the computed values.

Note: the page uses smooth scrolling, so a screenshot taken immediately after a scroll call captures the page mid-flight. Settle before capturing.

- [ ] **Step 3: Check the two open items from spec §9**

Dots-on-dots: if kolam pulli and the 14px halftone read muddy together, lower `--gc-halftone-strength` on this band only.
Three across at 375px: confirm no horizontal page scroll — `document.documentElement.scrollWidth` must not exceed `clientWidth`.

- [ ] **Step 4: Check the Chums still stand on something**

Confirm visually that the dome still sits under their feet and the stepped teeth still bite down into cream. This is the §1.2 trap; the test asserts the declarations exist, only the eye confirms the result.

- [ ] **Step 5: Push and verify what is live**

```bash
cd shopify-theme && shopify theme push --live --allow-live
```
Read the per-file results in the output. Then confirm live matches the repo by pulling to a scratch directory and diffing — `header-group.json` and `footer-group.json` differ by a Shopify-prepended banner comment and that difference is expected.

- [ ] **Step 6: Report with evidence**

A screenshot of the settled threshold, the computed delay values, and the suite counts. No success claim without the output that backs it.
