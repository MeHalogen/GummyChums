# Theme architecture — built to be re-skinned

**Date:** 2026-10-11
**Owner:** Mehal (client: Priyal Ojha / Nirmay)
**Goal:** Make `gc-home` and `gc-product` pivot to a new Figma design by editing
tokens, components and composition — never by hunting CSS across thirteen files.

**Scope decision:** home + product only. The other eleven sections keep working
untouched and migrate opportunistically.
**Pivot model:** a developer does the pivot in code. Not merchant re-theming,
so rich theme-editor schema is explicitly NOT a goal.

---

## 1. The problem, measured

| Measure | Value |
|---|---|
| CSS inside section `<style>` blocks | **1,062 lines across 13 sections** |
| CSS in shared stylesheets | 307 lines |
| Share of styling that cannot be reused without editing a section | **77%** |
| Byte-identical CSS rule bodies duplicated across sections | **21** |

`gc-home` carries 279 lines of CSS; `gc-product` carries 161.

The duplicates are not coincidence — they are components that were
re-implemented per section under a private prefix:

- the eyebrow/kicker: `.gcc-kick` `.gcq-kick` `.gcr-kick` and three more — **6 sections**
- the inner wrapper: `.gcn-in` `.gck-in` `.gcc-in` and two more — **5 sections**
- the product grid: `.gcc-grid` `.gcq-grid` `.gcs-grid`
- the price cluster: `.gcc-price`/`.gh-price`, `.gcc-perday`/`.gh-perday`

## 2. What already exists — do not rebuild it

This is the important finding. The foundation is already here and is good:

- **Tokens are solid.** 64 tokens in `gc-tokens.css` covering colour, type scale,
  weight, line-height, letter-spacing, spacing, radius, shadow, motion and layout.
- **A component layer already exists** in `gc-brand.css`: `.gc-btn`, `.gc-card`,
  `.gc-kick`, `.gc-h1`, `.gc-h2`, `.gc-lede`, `.gc-wrap`.

And it is almost entirely unused:

| Component | Sections using it |
|---|---|
| `.gc-card` | **0 of 13** |
| `.gc-wrap` | 1 of 13 |
| `.gc-kick` | 1 of 13 |
| `.gc-btn` | 5 of 13 |

**So this project is not "introduce a design system". It is "finish the one that
exists, and make it impossible to ignore."** That materially reduces the work and
the risk.

## 3. Architecture

Four layers, each with one job.

### Layer 1 — Primitive tokens (`gc-tokens.css`)
The palette and scales. `--c-cherry`, `--sp-5`, `--fs-3xl`. Unchanged in
structure; these already work.

### Layer 2 — Semantic roles (new, in `gc-tokens.css`)
**This is the layer that makes the pivot cheap, and it is the main thing missing.**

Components must never reference the palette directly. They reference a role:

```css
--role-cta-bg:       var(--c-cherry);
--role-cta-ink:      var(--c-surface);
--role-card-bg:      var(--c-surface);
--role-band-ink:     var(--c-ink);
--role-eyebrow-ink:  var(--c-ink-3);
```

A re-skin then becomes: remap roles to new primitives. One file, one place per
concept. Without this tier, every component hard-codes brand colours and a
re-skin is a find-and-replace across the component layer.

Rule: **primitives are only ever referenced by role definitions.** Components and
sections use roles.

### Layer 3 — Components (`gc-brand.css` extended, or a new `gc-components.css`)
Real, named, documented components with token-only values and no section
prefixes. Inventory derived from the duplication evidence above, not invented:

| Component | Replaces | Notes |
|---|---|---|
| `.gc-band` | per-section section shells | vertical rhythm + optional tone |
| `.gc-wrap` | `.gcn-in` `.gck-in` `.gcc-in` +2 | exists; adopt it |
| `.gc-eyebrow` | `.gcc-kick` `.gcq-kick` +4 | exists as `.gc-kick`; rename or alias |
| `.gc-head` | `.gcc-title`/`.gcv-head h2` + subs | heading + sub cluster |
| `.gc-card` | `.gh-hs-card`, `.gcc-card` | exists; adopt and extend with tone variants |
| `.gc-btn` | partially adopted | exists; add tone + size variants |
| `.gc-price` | `.gcc-price`/`.gh-price` + perday | price cluster |
| `.gc-grid` | `.gcc-grid` `.gcq-grid` `.gcs-grid` | responsive product grid |
| `.gc-media` | `.gcc-shot`, `.gcr-stage` | aspect-boxed media frame |
| `.gc-chip` | `.gck-chips`, `.gp-pay-row` | small pill |
| `.gc-sticker` | new | desi die-cut badge, per the Tapri spec |

### Layer 4 — Sections = composition + schema
A migrated section contains markup and `{% schema %}`. **No `<style>` block.**
It assembles snippets and component classes.

### Snippets as components
CSS alone does not capture markup structure. Where a component has internal
structure that a redesign would change, it gets a snippet:

- `snippets/gc-card.liquid`
- `snippets/gc-section-head.liquid`
- `snippets/gc-price.liquid`
- `snippets/gc-sticker.liquid`
- `snippets/gc-button.liquid`

Conventions:
- Always `{% render %}`, never `{% include %}` — render isolates scope, so a
  snippet cannot accidentally read a section's variables.
- Every snippet opens with a comment block documenting each parameter, whether
  it is required, and what it defaults to.
- A snippet takes data, not markup. No passing HTML strings.

## 4. Enforcement

Architecture that is not enforced erodes — this theme is itself the proof, with a
component layer sitting unused at 0 of 13 adoption. Extend
`tests/design-system.test.mjs`:

1. **No `<style>` in migrated sections.** Driven by an explicit `MIGRATED` list,
   so unmigrated sections keep working and are not failed by a rule they predate.
2. **No raw values in migrated sections.** No hex colours, no `px` spacing except
   where a token genuinely cannot express it (hairlines, 1px borders).
3. **Components reference roles, not primitives.** A component file matching
   `var(--c-[a-z]` outside a role definition fails.
4. **No duplicate rule bodies** within the component layer — the exact check that
   found the original 21.
5. **Every snippet documents its parameters.**

The existing design-system suite (11 tests) and the inverted hero lock (8 tests)
continue to run alongside.

## 5. Migration

One section at a time, each independently shippable and verifiable:

1. **Semantic role tier** added to `gc-tokens.css`. No visual change. Verify by
   rendering before/after and diffing computed styles.
2. **Component layer completed** in the shared stylesheet. Still no visual change
   — nothing consumes it yet.
3. **`gc-product` migrated.** It is the page that earns money and the better test
   of the component set.
4. **`gc-home` migrated.**
5. Tests tightened to lock each migrated section as it lands.

Each step keeps the site shippable. Nothing is big-bang.

## 6. How a Figma pivot then works

1. Remap semantic roles to the new palette and scales — `gc-tokens.css`.
2. Adjust component CSS where a component's own shape changed — one file.
3. Recompose sections: reorder, add, remove, swap snippets — markup only.

No step requires finding where a colour was hard-coded.

## 7. Non-goals

- Not migrating the other eleven sections now.
- Not building merchant-facing theme-editor controls for layout.
- Not changing the palette, typefaces or visual design. This is structural work;
  the site should look **identical** when it lands. Any visual change is a bug.
- No build step. The theme stays vanilla CSS and Liquid.

## 8. Success criteria

- `gc-home` and `gc-product` contain zero `<style>` and zero raw colour values.
- The 21 duplicated rule bodies collapse to single definitions.
- Component adoption across the two migrated sections is 100%.
- Rendered output is visually identical before and after — verified by
  screenshot comparison in Safari at phone and desktop widths.
- All suites green; theme check no worse than its 10-offence baseline.
- A colour change anywhere in the brand requires editing exactly one file.

## 9. Risks

- **Visual regression during migration.** Mitigated by screenshotting each page
  before and after each step and comparing, not by trusting the diff.
- **Two systems coexisting** while eleven sections stay unmigrated. Accepted
  deliberately; the `MIGRATED` list makes the boundary explicit rather than
  ambiguous.
- **Specificity collisions** when section-prefixed rules are replaced by shared
  component classes — the lower-specificity shared class can lose to a leftover
  section rule. Mitigated by removing the section rule in the same commit as the
  adoption, never leaving both.

---

## 10. Outcome — measured 11 Oct 2026

| | before | after |
|---|---|---|
| CSS inside section `<style>` blocks | 1,062 lines | **611** |
| CSS in stylesheets | 307 lines | **912** |
| Reusable / re-themable share | 23% | **59%** |
| `gc-home` | 508 lines, 279 CSS | **218 lines, 0 CSS** |
| `gc-product` | 507 lines, 161 CSS | **347 lines, 0 CSS** |

Both target sections carry zero CSS. The remaining 611 lines are the eleven
unmigrated sections, which were always out of scope.

Every step verified byte-identical against a Safari baseline at phone and
desktop widths. Theme check finished at its 10-offence baseline; all three
suites green (architecture 15, design-system 11, hero lock 8).

### What did not go to plan, and what it taught

**The plan over-estimated how much was duplicated.** The spec predicted the
product page's rules would collapse into components. They did not: `.gp-kick`,
`.gp-grid` and `.gp-perday` only *look* like `.gc-eyebrow`, `.gc-grid` and
`.gc-price__unit` — different font size, a fixed two-column 760px grid, `--fs-sm`
against `--fs-xs`. Adopting them would have changed the design, which the
constraints forbid. The 21 measured duplicates are across collection, quality,
search and reviews; the product page's controls are genuinely bespoke.

Forcing them would have improved the adoption metric by editing pixels. The real
convergence belongs with the Figma, when the designs are meant to agree.

**One component was deleted rather than used.** `gc-section-head` was built from
the duplication audit, but its duplicates are all in unmigrated sections, and the
home page's own heading legitimately differs. It was removed. Build the component
when the second caller exists, not before.

**The verification harness was wrong three times.** It reported false differences
from animation frames until captures were frozen; it screenshotted a blank window
and called it a regression until it asserted the page had rendered; and it
captured blank again whenever Safari was not frontmost, until it brought Safari
forward itself. Each was caught by a control — capturing an unchanged site twice
and expecting identity. A verification tool is not trustworthy because it was
written carefully; it is trustworthy once it has been shown to fail when it
should and pass when it should.

**Two existing guards assumed CSS lived in sections.** `design-system`'s
`--container` check and the hero lock both read section `<style>` blocks, so
moving CSS to stylesheets would have silently hollowed them out — the hero lock
in particular would have stopped seeing scroll-coupling entirely. Both now follow
a section's linked stylesheets. The lock was re-proved by reintroducing a banned
pattern and watching it fail.

### Where this leaves the Figma pivot

1. Remap `--role-*` in `gc-tokens.css` — one file, 15 roles.
2. Adjust `gc-components.css` where a component's own shape changed.
3. Recompose sections, and move page-specific rules in
   `section-gc-home.css` / `section-gc-product.css`.

No step requires finding where a colour was hard-coded in Liquid, which is what
it required before.
