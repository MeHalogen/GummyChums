# Sick-Motion Kit — index15–24

**Date:** 2026-08-02
**Goal:** Amplify motion across the Premium Motion Collection (`index15`–`index24`) — buttery flow, springy tactile, cinematic reveals, living ambient — via one shared, idempotent kit that *extends* the existing engine (mini-Lenis smooth scroll, `gc-reveal` IO, `data-scrub`, blob cursor, `pk-mag`, aurora/breathe glows). No second scroll loop; pinned/scrub heroes untouched.

## Delivery
`tools/add_motion.py` — idempotent injector (`<!-- MO:START --> … <!-- MO:END -->`), stamps one `<style id="mo-css">` + `<script id="mo-js">` before `</body>` in index15–24. Re-runnable; built HTML = source of truth. Pattern mirrors `upgrade_story.py` / `bundle_builder.py`.

## Four flavors (concrete, page-agnostic)
1. **Buttery flow** — read scrollY/velocity off the existing smooth scroll (read-only, no new loop): slim top **scroll-progress bar** (brand gradient); **parallax the existing `.pk-light` glows** by scroll; **cursor-trail stretch** by velocity. No content-layout skew (10 varied layouts stay safe).
2. **Springy tactile** — delegated: **squish-on-press** on every `button/.pk-btn/[data-hot]/a[href]`; **tilt-to-cursor** on known card classes (`.al-card,.sq-card,.ob-card,.sn-rim,.jb-card,.zv-card,.ve-card,.cf-slide,.ms-panel`); **3-blob lerping cursor trail** behind the gummy `#pkc`. Existing `pk-mag` magnetic kept.
3. **Cinematic reveals** — amplify `gc-reveal` additively: add **blur→sharp** to its transition (`filter`), keep existing opacity/translate. **Word-stagger** big `h1/h2` via JS wrap in `.mo-word` (skip `pk-chars` ones and anything inside `[data-scrub]`/pinned).
4. **Living ambient** — fixed **animated grain** overlay (mix-blend, ~5% — works on any bg); gentle **float** on `.pk-gummy` art; the `.pk-light` parallax from (1) adds depth.

## Guards
`prefers-reduced-motion` → no grain/trail/progress-anim/blobs, words shown instantly, tilt/squish off. Touch (no fine pointer) → no trail/tilt; squish + progress fine. Single rAF loop (trail + parallax) pauses on `document.hidden`. Transform/opacity only; `will-change` managed. Delegated listeners survive DOM changes.

## Verify
Run all 10 in browser: no console errors, scroll still smooth (no double-scroll), reveals fire, cards tilt, reduced-motion path clean, screenshots. Add MO to gallery note if needed.

## Out of scope
index.html, index2–14, 25–29, PDPs. Not rebuilding the existing engine — only adding on top.
