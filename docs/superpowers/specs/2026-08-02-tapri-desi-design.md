# Tapri desi-Gen-Z page — index31.html

**Date:** 2026-08-02
**Goal:** A *new* page (index30 kept) fixing the Holi/pink miss — **Tapri street-pop, desi Gen-Z**, full palette balanced (no pink field), combining the two mechanics the user loved: the **scroll "fall-into-the-gummy" takeover** (index22 Zoom Voyage) + the **gummy-catching game** (index30). Hero wordmark = **GUMMYCHUMS**; no "BOING".

## Build
`index31.html` copied from index30 (reuses shared bill/checkout, sick-motion kit, game engine, 3 real products, manifesto), re-themed + restructured via direct edits.

## Aesthetic
Sand-Cream base + halftone dots; bold **colour-blocks** in Coral / Saffron / Neem-Green / Teal; Maroon depth; **Gulaab pink only as a minor accent**. Tapri sticker die-cuts ("100% देसी", "No Added Sugar", "Made in India") with hard black borders + offset shadows. **Anton** (Latin display) + **Baloo 2** (Devanagari). Bilingual Hindi-Latin copy, meme swagger.

## Four acts
1. **Fall-in hero** — `.tp-stage` (270vh) with a sticky `.tp-pin`; giant **GUMMYCHUMS** Anton wordmark (ink + coral) + stickers + Hindi copy; a coral gummy at bottom-centre. A custom **`--z`** (0 at top → 1 at stage end; NOT the shared `--p`, which reads 0.27 at rest) scales the gummy up to 27× so it **swallows the screen**, fades the title out, fades **Act 2** in.
2. **Inside** — "अंदर क्या है? · Bacopa · Melatonin · Lutein — sirf असली देसी सेहत" (cream on the coral gummy).
3. **Catch the Chums (game)** — neem-green `.tp-game`; the index30 `#holi-rain` engine (gummies in all brand hues fall, tap → pop, पकड़े/Caught counter). Re-skinned street-pop ("GUMMY JUMPS!"), no Holi/gulaal wording.
4. **Shop** — the 3 real products as `.tp-card` (hard-border + offset-shadow tapri cards, coral `.tp-add` buttons), real specs, shared bag.
+ marquee (देसी सेहत ✦ मस्त स्वैग…), founder manifesto, shared bill.

## Verified
Hero renders (screenshot); fall-in zoom works (screenshot at --z=.8 — gummy fills screen, Act-2 reveals); game section neem-green + 20 drops + counter (DOM); 3 tp-cards (DOM); no console errors. Contrast resolver's only hits are the Act-2 inside text — false positives (its coral backdrop is the zoom-gummy sibling layer, not a CSS ancestor). Live rain fall + scrolled screenshots blocked by the backgrounded preview pane (froze CSS timeline), not the code.

## Out of scope
index30 and other pages. Gallery listing optional.
