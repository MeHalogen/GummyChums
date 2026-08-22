# TASK: Refactor `shopify-theme/sections/gc-product.liquid`

Read `.superpowers/sdd/shared-contract.md` first — it is binding.

## Context
This is the product detail page (template `templates/product.json` renders it).
It works functionally but is built entirely from hard-coded values and invented
font sizes, and it never constrains itself with `--container`.

## Required design
1. **Move fully onto tokens.** No raw hex, no off-scale `font-size`, spacing on
   the `--sp-*` scale, radii/shadows from tokens.
2. **Colour discipline — important nuance:**
   - The **flavour colour** (`--c-cherry` / `--c-mango` / `--c-orange`) is
     legitimate *product identity* here: use it for the media backdrop tint,
     the role badge, and the price.
   - The **Add to bag button** is the primary action → `var(--c-accent)`.
   - Do not additionally tint every surface. One identity colour + one action colour.
   - The existing Liquid maps title→flavour (melatonin/sleep→cherry, eye→orange,
     else→mango). Keep that mapping; drive it through the flavour tokens.
3. **Contained:** page wrapper on `var(--container)` + `var(--gutter)`.
4. **Layout:** two columns on desktop (media left, buy box right), single column
   under ~900px. Media is a square, radius `var(--r-lg)`.
5. **Preserve ALL existing functionality — do not regress:**
   - Breadcrumb; role/flavour badge; title; tagline line; price (+ compare-at
     strikethrough when higher); tax/shipping note; quick-fact pills
   - Variant picker buttons (`aria-pressed`, writes the chosen id into the
     hidden `id` input), quantity stepper (clamped 1–20, writes hidden
     `quantity` input), POST form to `routes.cart_add_url`, sold-out state
   - Accordions (What's inside / How to take it / Shipping & returns)
   - "Meet the other chums" cross-sell grid
   - `image_tag` calls must keep `width:` and `height:` params
6. Keep the floating-gummy animation but transform-only (no `filter:` on animated
   elements — that caused scroll jank). Respect `prefers-reduced-motion`.
7. The section renders a `{% schema %}` with name "GummyChums Product" and no settings.

## Definition of done
- `npm test 2>&1 | grep "gc-product.liquid"` outputs nothing.
- `shopify theme check` shows 0 errors.
- Add-to-cart, variant selection and quantity still work (verify the markup/JS
  wiring by reading it — you cannot load the store).
