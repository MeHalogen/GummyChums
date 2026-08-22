# TASK: Rebuild `shopify-theme/sections/gc-home.liquid` (+ `snippets/gc-gummy.liquid`)

Read `.superpowers/sdd/shared-contract.md` first — it is binding.
This file currently has **76 contract violations** (raw hex, off-scale font-sizes,
a duplicate `.gh-cta`, no `var(--container)`). All must go.

## PRIORITY 1 — the flavour cards are the client's active complaint
Client on the current cards: *"i dont like this UI and colors."* Diagnosis:

1. **The gummy renders as a glossy SPHERE — it reads as a marble/bouncy ball,
   not a candy gummy.** This is the single biggest failure: it's a gummy brand.
   Fix in `snippets/gc-gummy.liquid`: make it read as a soft, squishy, slightly
   translucent JELLY — flatter and more organic than a perfect circle, softer
   specular highlight (a sphere highlight is what makes it look like a marble),
   a hint of translucency/inner light, subtle irregular edge. Squash it slightly
   (wider than tall) so it looks soft, not rigid.
2. **Show a CLUSTER of 2–3 gummies** per card at different sizes/rotations
   instead of one giant centred ball. That reads as *product*; one ball reads as
   an icon.
3. **Media area is a huge empty 1:1 square** — the gummy floats in a void and the
   text is squashed at the bottom. Use a shorter ratio (4/3 or 5/4) so the card
   is balanced.
4. **Washed-out pastel tints** — the `16`-alpha tints are nearly white. Use the
   `--c-*-soft` tokens for a richer, more confident flavour ground.
5. **Truncated description** (`Big brain energy, tiny gummy. Bacopa (Brahmi) 60mg
   to help you focus, remember, and stay…`) looks broken. Use a SHORT fixed
   benefit line per flavour instead of truncating the product description:
   - Melatonin/sleep → "Wind down. Sleep tight."
   - Eye care       → "For screen-tired eyes."
   - Brain booster  → "Big brain energy, tiny gummy."
6. **Price shows `Rs. 399.00`.** Use `money_without_trailing_zeros` and map the
   `Rs.` prefix to `₹` (e.g. `| money_without_trailing_zeros | replace: 'Rs.', '₹'`).
7. **Colour rule for the Add buttons:** each card's Add button uses ITS FLAVOUR
   colour (product identity). Do NOT make all three `--c-accent` — three accent
   buttons in one region would violate "max one accent per viewport region".

## PRIORITY 2 — token migration for the whole file
Every section in this file (hero, flavour cards, story, FAQ, closing CTA):
- no raw hex → tokens only
- every `font-size` → `var(--fs-*)`
- spacing → `--sp-*`; radii → `--r-*`; shadows → `--sh-*`
- wrap content in `var(--container)` (a `.gc-container` class exists in tokens)
- remove the duplicate `.gh-cta` declaration (declare each selector ONCE per scope)

## Preserve (do not regress)
- The scroll fall-in hero: 200vh `.gh-stage` + sticky `.gh-pin`, the `--z` scroll
  progress script, the zooming gummy (keep the 20x cap — higher caused jank),
  the "WHAT'S INSIDE?" reveal, the eyebrow chip, marker-highlighted headline
  (`[ ]` → `<mark>`), dual CTA, sticker badges, cursor-parallax gummy characters.
- Story section (`#gc-story`), FAQ accordion (`#gc-faq`), closing CTA.
- Real product loop with working add-to-cart POST forms.
- All `{% schema %}` settings and their ids.

## Performance (a live client complaint — the page lagged)
- No `filter:blur()` or `drop-shadow` on animated elements (forces re-raster).
- Animate transform/opacity only.
- Respect `prefers-reduced-motion`.

## Definition of done
- `npm test 2>&1 | grep -E "gc-home.liquid|gc-gummy"` outputs NOTHING.
- `cd shopify-theme && shopify theme check` → 0 errors.
