# Maachis Collection — 4 hyper-Indian animated pages

**Date:** 2026-08-01
**Goal:** 4 new pages riffing on index26 (Maachis / matchbox), each a distinct "old Indian" aesthetic, on the finalized palette, sharing a **strike-to-ignite** hero animation. index26 stays untouched.

## Files (built by `tools/build_maachis.py`, committed; built HTML = source of truth)
- `maachis-label.html` — Vintage matchbox-brand label
- `maachis-bollywood.html` — Retro hand-painted film poster
- `maachis-bazaar.html` — Bazaar / dukaan enamel signboard
- `maachis-dd.html` — Doordarshan / 80s CRT TV (the dark one)

## Shared kit (identical across all 4)
- **Strike-to-ignite hero engine**: on load a matchstick strikes a striking-strip → bursts into a coral→saffron flickering flame → the flame's glow "ignites" the logo/headline; embers drift up. Each vibe re-skins *what* lights. `prefers-reduced-motion` → lit end-state shown instantly. rAF paused when tab hidden; JS-hiccup failsafe reveals content.
- Matchbox product mechanic (boxes slide open on hover), custom blob cursor, kinetic manifesto, Chum Box builder, shared bill/checkout — all recolored to the finalized palette (see [[finalized-palette]]). Vanilla JS only (Shopify-safe).

## Palette usage (finalized)
Sand Cream `#F1E7DA` paper/base · Ink `#1F1C1A` text/dark canvas · Chilli Coral `#E8503A` matchbox red / CTAs · Gulmohar Red `#D72638` deep drama · Saffron `#F4C84F` flame/gold/sunburst · Jamun Purple `#6B2F6A` · Neem Green `#234225` · Teal Tadka `#477971` · Gulaab Pink `#E8A0B2` · Imli Brown `#7B4726` / Ganga Maroon `#6B1E21` frames+type. Flame = coral→saffron. 6 flavours keep their accent hues (jamun/teal/coral/mango/saffron/gulaab).

## Per-vibe skins
1. **Label**: double coral/maroon frame; bear mascot in an oval medallion over a saffron sunburst; "SAFETY GUMMIES · सुरक्षित" banner; "REGD. No. 2026 · MADE IN INDIA" stamp; "SUPERIOR QUALITY" seal; Bevan type on grainy Sand-Cream paper. Strike runs the side rail → lights medallion. Products = mini matchbox labels.
2. **Bollywood**: maroon/coral spotlight vignette; giant saffron-glow film title; "NOW SHOWING" starburst; "A WELLNESS BLOCKBUSTER"; "STARRING: …" cast strip; aged paper. Strike = projector flickers on, spotlight sweeps → ignites title. Products = lobby cards.
3. **Bazaar**: hanging enamel board; stacked hand-painted palette lettering; price tags; "★ BEST QUALITY ★" seals; bulb-marquee border. Strike lights border bulbs in sequence. Products = shelf price-tag cards.
4. **Doordarshan**: ink CRT canvas; palette color-bars; spinning "GC" ident; "GUMMYCHUMS · रंग-बिरंगी सेहत"; VHS scanline+grain; "TRANSMISSION BEGINS" ticker. Strike = TV powers on (flash → bars → logo). Products = channel/program cards.

## Wiring
- Add all 4 to `index-gallery.html` as a "Maachis Collection" group.
- Same shared-cart contract as every page (`.add-to-cart-btn[data-product-id]`, `.cart-trigger`, `.cart-count`; product ids dreamy-sleep/electric-blue/neon-violet + minty-fresh/burnt-orange/coral-sunrise + Chum Box jars).
- Bill diverges from index.html's (accepted, as with index12–24).

## Build order
Shared base + `maachis-label` first (establishes the kit + strike engine), verify in browser; then bollywood, bazaar, dd; then gallery. Verify each with the luminance contrast resolver + screenshots.

## Out of scope
index26 and all other existing pages; the generators for other collections.
