# Plan — Mirror index31.html into Shopify at ~97% fidelity

## Goal
Reproduce `index31.html` on the Shopify store so it is eye-to-eye identical in
**look, scroll and behaviour**. Colours get re-themed afterwards (client's stated plan).

## Fidelity ceiling — what stops 100%
| # | Blocker | Status |
|---|---|---|
| 1 | **Shopify hosted checkout.** index31's "bill" is a mock. The bill UI can be copied exactly up to the Pay button; pressing it hands off to Shopify's checkout, restylable only via Shopify's checkout editor. | **IRREDUCIBLE** — the final screen differs |
| 2 | **Products are dynamic.** index31 hardcodes 3 products at ₹699/749/899; Shopify renders from the DB. | Visually identical; numbers come from real data (desired) |
| 3 | **Dawn CSS/JS interference** (14 scripts, global resets, colour schemes) — causes both pixel drift and the scroll lag. | **SOLVED** by a bare custom layout (Task 1) |
| 4 | Tailwind CDN is dev-only and slow. | **SOLVED** — compiled to a 16KB static asset; verified all 29 arbitrary-value classes + responsive utilities survive |

**Realistic ceiling: ~97%.** Everything except the checkout screen and live product data.

## Architecture decision
Do **not** fight Dawn. Bypass it: a dedicated layout that loads *none* of Dawn's
assets — only Google Fonts, the compiled Tailwind CSS, and index31's own CSS/JS.
The mirrored page then has exactly index31's CSS cascade and no framework JS,
which is what restores index31's scroll smoothness.

## Tasks
### Task 1 — Bare mirror layout + compiled Tailwind
- `assets/gc-tw.css` — Tailwind compiled against index31 (`npx tailwindcss@3 -i in.css -o gc-tw.css --content index31.html --minify`). No CDN.
- `layout/gc-mirror.liquid` — minimal layout: `{{ content_for_header }}`, Google Fonts (Anton, Baloo 2, Material Symbols), `gc-tw.css`, index31's `<style>` blocks, `{{ content_for_layout }}`. **No Dawn CSS, no Dawn JS.**
- Verify: page loads, zero Dawn assets in the network panel.

### Task 2 — Port the page body verbatim
- `sections/gc-mirror-home.liquid` — index31's body copied **verbatim**: nav, `.tp-stage` (270vh scroll fall-in), `#game`, `#shop`, "serious science", `.kc` manifesto, footer.
- The ONLY change: the 3 product cards loop over `collections.all.products` and use
  `product.title`, `product.price | money`, `product.url`, and the real variant id.
- Keep every class name, size, animation, easing and the `--z` scroll script unchanged.
- `templates/index.json` → renders this section with `layout: gc-mirror`.

### Task 3 — Real cart behind the mock bill
- Keep the receipt/bill modal markup and styling **exactly** as index31.
- Rewire: `.add-to-cart-btn` → `POST /cart/add.js`; bill contents from `/cart.js`;
  `.cart-trigger` opens the modal; the checkout button → `/checkout`.
- Line items render in the existing receipt rows — visually identical, real data.

### Task 4 — Chum Box builder on the real cart
- Port `#bb-builder` verbatim (canvas physics sim, jar, steppers).
- Rewire "Pack my box" to push each jar as its own line item via `/cart/add.js`
  with real variant ids (preserve the existing per-flavour/size line-item rule).

### Task 5 — Parity QA
- Side-by-side: local `index31.html` vs the Shopify mirror at 1440px and 390px.
- Check: hero zoom timing, sticky behaviour, game, card hover, manifesto reveal,
  marquee speed, builder physics. Log any drift and fix.

## Test-suite interaction
A verbatim copy intentionally violates the design-system contract (raw hex,
off-scale type). **Exempt the mirror files** from `tests/design-system.test.mjs`
while mirroring; re-apply tokens in the later re-theming pass (which is exactly
what the token layer is for).

## Risks
- **Chum Box rewiring** is the largest/riskiest task — it has its own cart model.
- Dawn's `content_for_header` still injects some Shopify CSS; if it interferes, scope index31's CSS under a wrapper class.
- Re-theming later must not undo the mirror; do it via tokens, not edits.
