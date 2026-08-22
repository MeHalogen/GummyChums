# TASK: Rebuild `shopify-theme/sections/gc-footer.liquid`

Read `.superpowers/sdd/shared-contract.md` first — it is binding.

## Context
This footer already replaced Dawn's default "Subscribe to our emails" block —
keep it that way, do NOT reintroduce a newsletter form. It is currently built
from hard-coded hex values and off-scale font sizes; it must move onto tokens.

## Required design
1. **Grounding ink block:** `background:var(--c-ink)`, text `var(--c-bg)` /
   muted steps. This is the page's closing anchor.
2. **Restraint:** accent may appear at most **once** as a role colour (e.g. the
   column headings OR the gummy dot — not both, not everywhere). The current
   version sprays cherry/mango/orange around; that reads flashy.
3. **Contained:** inner wrapper on `var(--container)` + `var(--gutter)`.
4. **Structure to preserve:**
   - Brand block: logo image (inverted so it reads on ink; keep BOTH width and
     height attrs — asset ratio 4146x1550) + tagline
   - Three link columns: Shop (loops `collections.all.products limit: 3` + an
     "All gummies" link), Company (Our story `#gc-story`, FAQ `#gc-faq`,
     Instagram if set), Help (loops `linklists.footer.links` + mailto if email set)
   - Bottom bar: `© <year> <shop.name>`, "Made in India", and the legal line
5. **Type:** headings `var(--fs-xs)` uppercase w/ wide tracking; links
   `var(--fs-sm)` or `var(--fs-base)`; legal `var(--fs-xs)`. All from the scale.
6. **Keep all existing schema settings** (`tagline`, `instagram` [type `text`,
   NOT `url` — a `url` setting cannot have a default], `email`, `legal`).
7. Any decorative glow must be a gradient, not `filter:blur()` (blur on large
   surfaces caused scroll jank). Respect `prefers-reduced-motion`.

## Definition of done
- `npm test 2>&1 | grep "gc-footer.liquid"` outputs nothing.
- `shopify theme check` shows 0 errors.
