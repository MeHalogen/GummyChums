# Story / About / Contact pages — Shopify-lean

**Date:** 2026-08-02
**Goal:** Add Story, About, Contact pages built from the founder's Brand Discovery Questionnaire, in the index31 **Tapri** style, but **Shopify-lean** (plain CSS, no Tailwind runtime) so each pastes into a Liquid section with near-zero rework — **without losing any animation/experience**.

## Delivery
`tools/build_pages.py` — one shared plain-CSS design system (palette vars, tapri components, reveal/cursor/grain/marquee/fall-in) + shared nav + footer + JS, stamped into `story.html`, `about.html`, `contact.html`. All motion is pure CSS + vanilla JS (no framework, no build step).

## Shopify-friendliness
- No Tailwind CDN (verified). Plain CSS in one `<style>`; markup + one `<script>` — section-ready.
- Google Fonts (Anton + Baloo 2) via `<link>` (allowed; self-host later if desired).
- No cart on content pages ("Shop" / BAG → `index31.html#shop`), so nothing to rewire to Shopify's cart. (The commerce flow on index31 still needs Cart-AJAX rewiring for production — separate task.)

## Pages
- **story.html** — immersive scroll "unveiling": 7 full-bleed colour-block chapters (question → overwhelm → not-alone → **the spark (fall-in gummy takeover, `--z`)** → personal journey → the name → mission finale), bilingual Anton+Baloo type, reveals.
- **about.html** — what we solve / who it's for (3 cards) / how you'll feel (chips) / personality (chips) / never-be (animated strikethroughs) / 3 non-negotiables (colour-blocks). All from Q2–Q6, Q13.
- **contact.html** — "आओ बात करें · Say hi" + email/Instagram/WhatsApp colour-block tiles + collab callout. **Placeholder details** (`hello@gummychums.in`, `@gummychums`, `+91 00000 00000`) — swap for real.

## Shared motion (kept, plain CSS/JS)
Scroll-progress bar, IntersectionObserver reveals (blur→sharp + stagger, load/scroll failsafes), blob cursor (fine-pointer), film grain, fall-in `--z`. `prefers-reduced-motion` degrades gracefully (fall-in becomes static stacked sections).

## Wiring
Nav (Story/About/Contact/Shop/BAG) added to index31; content pages cross-link + Shop→index31#shop. Also fixed index31 game headline "GUMMY JUMPS" → "GUMMYCHUMS".

## Verified
All 3 render (screenshots: story hero, about hero, contact hero+tiles); no Tailwind runtime; no console errors; About 0 contrast issues; Story's only flags are the fall-in inside text (false positive — coral backdrop is the zoom-gummy sibling layer). Reveal animation confirmed (forced, since the backgrounded preview pane throttles the observer).

## Out of scope
Real contact details; porting index31's mock cart to Shopify Cart-AJAX; gallery listing.
