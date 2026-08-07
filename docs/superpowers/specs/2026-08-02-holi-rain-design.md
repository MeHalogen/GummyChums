# Holi Colour-Rain page — index30.html

**Date:** 2026-08-02
**Goal:** A new page on index21's "raining clickable gummies" concept, made an Indian **Holi colour-rain** on the finalized palette, with **pop-for-fun** clicks and the **3 real products**.

## Build
`index30.html`, copied from index21 (reuses shared bill/checkout, nav, sick-motion kit), with a fresh Holi hero grafted on. Direct HTML edit (not a generator) — one-off page.

## Hero — रंगों की बारिश
- Gulaab-pink stage, big central hero gummy, "BOING. BOING." + eyebrow "रंगों की बारिश · CATCH THE COLOURS".
- **Colour-rain**: `#holi-rain` spawns capped gummy `<button>`s (36 desktop / 20 mobile / 8 reduced-motion) in all brand hues (coral, saffron, gulaab, mango, teal, jamun, maroon, sindoor); each falls via CSS `holi-fall` (translateY + sway + rotate), recycles on `animationend`. Pure CSS animation — no rAF loop.
- **Pop-for-fun**: tap a gummy → 12-particle **gulaal puff** (`.holi-puff`, fixed-position, in the gummy's colour) + increments the **पकड़े / Caught** counter, then that gummy resets to the top. No cart.
- Rain sits z-5 behind hero content (z-10, `pointer-events:none` so taps pass through); CTA + counter are `pointer-events:auto`.

## Shop — the 3 REAL products (see [[real-products]])
Brain Booster (Bacopa/Brahmi 60mg · Mango), Melatonin (Melatonin 5mg + Ashwagandha + Chamomile + Valerian + Passion Flower + Magnesium · Cherry), Eye Care (Lutein + Zeaxanthin + Bilberry + A·C·E·B · Orange) — real specs, add-to-cart into the shared bill. Chum Box trimmed to these 3 (fake minty/burnt/coral removed).

## Guards
`prefers-reduced-motion` → slow 22s drift, no puffs. Mobile caps count. Touch = tap to pop. CSS animations auto-pause when tab hidden.

## Verified
20 drops spawn + animate; click → counter++ & 12 puffs; no console errors; rain renders in all brand hues (forced-position screenshot, since the preview pane was backgrounded and froze the live CSS timeline); Chum Box = 3 rows, 0 fake product refs.

## Out of scope
Other pages. Gallery listing optional (ask user).
