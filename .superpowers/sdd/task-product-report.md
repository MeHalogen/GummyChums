# Report: gc-product.liquid refactor

## What changed and why

Refactored `shopify-theme/sections/gc-product.liquid` end-to-end onto
`gc-tokens.css`, per `shared-contract.md` and `task-product-brief.md`. All
structure, ids, form wiring, and JS were preserved exactly; only the `<style>`
block and a handful of colour-related markup details changed.

Key decisions:

- **Flavour identity via CSS vars, not hex:** the old code did
  `{%- assign col = '#DE1D61' -%}` etc. and threaded raw hex through
  `{{ col }}` into the stylesheet and inline SVG. Replaced with
  `{%- assign pc_var = '--c-cherry' -%}` / `pc_soft_var` (and `--c-orange`,
  `--c-mango` for the other two branches), then `.gp{--pc:var({{ pc_var }})
  ;--pc-soft:var({{ pc_soft_var }})}`. Every place that used to reference a
  literal hex now references `var(--pc)` / `var(--pc-soft)`. Same pattern for
  the cross-sell loop (`mpc_var`/`mpc_soft_var` per other product). Zero raw
  hex anywhere in the file (verified beyond the test's `<style>`-only scan —
  the SVG fallback icons also use `style="fill:var(--pc)"` instead of a hex
  attribute, and the highlight ellipse uses `style="fill:var(--c-surface)"`
  instead of `fill="#fff"`).
- **Colour discipline per the brief's nuance:** flavour colour (`--pc`,
  resolving to `--c-cherry`/`--c-mango`/`--c-orange`) is used in exactly
  three places as instructed — the media backdrop tint (`background:
  var(--pc-soft)`), the role/flavour badge text, and the price. Everything
  else that used to be flavour-tinted (variant-picker pressed state, qty
  stepper, accordion chevron) is now neutral ink (`var(--c-ink)` /
  `var(--c-ink-2)`), so there's exactly one identity colour and it doesn't
  bleed into every surface. `var(--c-accent)` is used in exactly one place:
  the Add to bag button (bg `--c-accent`, hover `--c-accent-hover`, text
  `--c-accent-ink`) — the single primary action / accent element on the page.
  The old "sold out" disabled state (`background:#bbb`) is now
  `background:var(--c-ink-3);color:var(--c-surface)`.
- **Contained:** `.gp{max-width:var(--container);margin-inline:auto;
  padding-inline:var(--gutter)}` — the wrapper is self-sufficient (doesn't
  rely on an external `.gc-container` class living in another file), so the
  design-system test's per-file `--container` check passes on this file
  alone.
- **Layout:** unchanged 2-col → 1-col breakpoint at 899px (brief's "~900px"),
  media stays a square with `border-radius:var(--r-lg)`. Removed the old
  `::before` radial-gradient hack on `.gp-media` (relied on a non-existent
  "hex+alpha suffix" trick, `var(--pc)18`, which isn't valid CSS) in favour of
  a plain `background:var(--pc-soft)` tint — simpler, restrained, and
  actually renders correctly.
- **Type:** every `font-size` is now `var(--fs-*)` (mapped each old ad-hoc
  size to its nearest token: crumb/tax/note/fact/variant/accordion-body →
  `--fs-sm`; body/CTA/accordion-summary/mini-title → `--fs-base`; tagline/qty
  glyphs → `--fs-lg`; price → `--fs-2xl`; title → `--fs-3xl`; badge/kicker →
  `--fs-xs`; section heading → `--fs-2xl`). Also moved font-weight,
  letter-spacing, and line-height onto the matching `--fw-*`/`--ls-*`/`--lh-*`
  tokens where the file used to hard-code raw numbers (`800` → `var(--fw-black)`,
  `-.03em` → `var(--ls-tight)`, `1.04`/`1.55` → `var(--lh-tight)`/`var(--lh-body)`,
  etc.) — not machine-tested but keeps the file fully on-system.
- **Spacing:** every margin/padding/gap now uses the `--sp-*` scale (mapped
  each pixel value to its nearest token, e.g. `16px 20px` accordion-summary
  padding → `var(--sp-4) var(--sp-5)` which is an exact match).
- **Radii/shadows:** all hard-coded `border-radius`/`box-shadow` replaced with
  `var(--r-sm/md/lg/full)` and `var(--sh-1/2/3)`.
- **Removed dead code:** `.gp-desc`/`.gp-desc p` CSS rules existed in the old
  file but were never referenced by any element in the markup (the actual
  description renders inside the "What's inside" accordion `.body`). Since
  they still contained raw hex/off-scale sizes that the test scans regardless
  of use, I deleted the unused rules rather than token-ifying dead CSS.
- **Motion:** floating-gummy `@keyframes gpFloat` kept as transform-only
  (`translateY` + `rotate`, no `filter`), now wrapped with
  `@media(prefers-reduced-motion:reduce){.gp-media svg{animation:none}}`.
  Also replaced the `.gp-buy:hover{filter:brightness(1.08)}` micro-interaction
  with a colour swap (`background:var(--c-accent-hover)`) to avoid `filter`
  entirely in the file, and fixed two dangling variable references
  (`var(--gc-spring)`, `var(--gc-ease)` — these token names don't exist; the
  real tokens are `--spring`/`--ease`) to the correct token names, adding
  `--dur-1/2/3` for transition durations.
- **No duplicate selectors:** every selector in the file's single `<style>`
  block is declared exactly once.
- **Schema unchanged:** `{ "name": "GummyChums Product", "settings": [] }`.

## Cart/variant/quantity wiring — confirmed intact

Read the markup and `<script>` block after editing; none of it was touched
except CSS classes/values:
- Form: `<form method="post" action="{{ routes.cart_add_url }}" ... id="gp-form">`
  unchanged.
- Variant buttons: still `data-vid="{{ v.id }}"`, `aria-pressed` toggling,
  still write into `#gp-vid` (`<input type="hidden" name="id" id="gp-vid">`)
  via the same click handler.
- Quantity: `#gp-minus`/`#gp-plus` still call `set()`, clamped `1–20`, still
  write into `#gp-qtyv` (display) and `#gp-qty` (`<input type="hidden"
  name="quantity">`).
- Sold-out state: `product.available` branch unchanged, still renders a
  disabled button in place of the submit button.
- `image_tag` calls for both the main image and the cross-sell thumbnails
  still pass both `width:` and `height:`.
- `<script>` block is byte-for-byte identical to the original.

## Verification (exact commands + output)

```
$ cd /Users/mehalsrivastava/GitHub/GummyChums && npm test 2>&1 | grep "gc-product.liquid"
(no output)
```

```
$ cd /Users/mehalsrivastava/GitHub/GummyChums/shopify-theme && shopify theme check 2>&1 | tail -4
╰──────────────────────────────────────────────────────────────────────────────╯

  Theme Check Summary.

  160 files inspected with 13 total offenses found across 10 files.
  13 warnings.
```

0 errors overall. Confirmed `gc-product.liquid` contributes only a single
pre-existing warning (unrelated to this refactor, present before my changes
too):

```
$ shopify theme check 2>&1 | grep -A3 "sections/gc-product.liquid"
sections/gc-product.liquid
[warning]: VariableName
The variable 'GPATH' uses wrong naming format
```

`grep -i "error"` over the full theme-check output returned nothing — 0
errors theme-wide.

## Concerns

None blocking. Two notes for the controller:
- The only theme-check item attributed to this file is the pre-existing
  `VariableName` warning on `GPATH` (SVG path constant) — it was already
  there before my change, is a warning not an error, and renaming it wasn't
  in scope for this refactor.
- `npm test` still reports one project-wide failure for
  `gc-home.liquid` missing `--container` — that's another agent's file, not
  touched here, and outside this task's scope per the shared contract.

Only file touched: `shopify-theme/sections/gc-product.liquid`. No git
commands or `shopify theme push` were run.
