# Palette Rebrand — index12–24

**Date:** 2026-07-31
**Scope:** Re-skin the 13 flagship + premium-motion pages (`index12.html`–`index24.html`) to the finalized GummyChums brand palette. Palette-only; placement by design judgment (user directive).

## Finalized palette (tokens)

| Token | Hex | Role |
|-------|-----|------|
| BG (Sand Cream) | `#F1E7DA` | page background (light pages), soft fills |
| SURFACE | `#FFFFFF` | white cards |
| INK (Text/Body) | `#1F1C1A` | body text, dark canvas, borders |
| CTA (Chilli Coral) | `#E8503A` | buttons / primary action |
| SAFFRON (Saffron Glow) | `#F4C84F` | highlights / badges / yellow |
| PURPLE (Jamun) | `#6B2F6A` | links / accents / violet |
| GREEN (Neem) | `#234225` | headers / section blocks / dark green |
| PINK (Gulaab) | `#E8A0B2` | soft pink accent |
| TEAL (Teal Tadka) | `#477971` | cool accent (all former blues) |
| Raw Mango | `#98C64B` | bright green accent |
| Sindoor Orange | `#FF7A2F` | orange accent |
| Nimbu Lime | `#D4E53B` | lime accent |
| Imli Brown | `#7B4726` | brown/brass accent |
| Gulmohar Red | `#D72638` | vivid magenta accent |
| Ganga Maroon | `#6B1E21` | deep berry / shadow |

## Architecture of current colors

- **Shared "premium kit" neon set** appears in every file (gummy lighting + the shared bill/checkout): `#261236`, `#8B5CF6`, `#38BDF8`, `#E44BD3`, `#FF5C8A`, `#39C98E`, `#FFB02E`, `#B80865`, plus `#7C6CF6`, `#FECF34`, `#006D36`.
- **Per-page signature** = one dark background hex (unique per page) + one or two accent hexes.

## Two treatments

**Dark-keep (5): 13, 14, 15, 17, 20.** Automated global hex→hex remap. Page dark bg → INK `#1F1C1A`; light text (white / pale tints) stays light (correct on dark); neon accents → brand hues. Safe because the light/dark relationship is preserved.

**Cream-flip (8): 12, 16, 18, 19, 21, 22, 23, 24.** Per-page redesign. Page bg → Sand Cream; **text logic inverted** (`text-white` classes and pale-tint text → INK), because a hex remap cannot tell white text from white cards and does not touch Tailwind color classes. Each flip page is verified in-browser and contrast-fixed section by section.

## Global remap table (both treatments)

```
#261236 -> #1F1C1A   (shared bill / borders / dark)
#006D36 -> #234225   (dark green)
#38BDF8 -> #477971  #1A43FF -> #477971  #0A1F8F -> #477971
#1A6BB3 -> #477971  #1B2A8F -> #477971              (all blues -> teal)
#8B5CF6 -> #6B2F6A  #7C6CF6 -> #6B2F6A  #6B2FB3 -> #6B2F6A
#B1249F -> #6B2F6A                                   (violets/magenta-purple -> jamun)
#E44BD3 -> #D72638  #E4177E -> #D72638               (magenta -> gulmohar)
#FF5C8A -> #E8A0B2  #FF7AB8 -> #E8A0B2  #F265DD -> #E8A0B2  (pinks -> gulaab)
#39C98E -> #98C64B  #16B877 -> #98C64B               (mint -> raw mango)
#FFB02E -> #F4C84F  #FECF34 -> #F4C84F  #FFD23F -> #F4C84F  #FFCF33 -> #F4C84F (amber -> saffron)
#FF2D87 -> #E8503A  #FF5A3C -> #E8503A               (hot pink / orange-red -> coral CTA)
#FF7A1A -> #FF7A2F                                   (orange -> sindoor)
#B6FF3D -> #D4E53B                                   (lime -> nimbu)
#8A6D3B -> #7B4726                                   (brass -> imli)
#B80865 -> #6B1E21  #B3197A -> #6B1E21               (berry -> maroon)
near-white greys (#FDFDFD/#FCFAFA/#F4F2F3) -> #FFFFFF
cream + pale blue/violet tints -> #F1E7DA
pale pink tints -> #E8A0B2
```

Page dark-bg hexes: dark-keep pages -> `#1F1C1A`; cream-flip pages -> `#F1E7DA` (plus per-page text inversion).

## Decisions (user-approved)

- **A. Backgrounds:** flip 8 to Sand Cream (proper per-page rework), keep 5 dark on Ink.
- **B. Bill/checkout:** recolored on-brand here; this makes the bill in 12–24 **diverge from index.html's** (index.html out of scope) — accepted.
- **C. Generators:** `tools/*.py` left untouched; re-running them will re-inject old-tinted Chum Box. Noted, not fixed.

## Execution

1. Python remap script (`scratchpad`) with the global table → apply to all 13.
2. Cream-flip pages: per-page contrast rework of `text-white`/pale text → INK, verify in browser.
3. Visual-verify every page in the preview browser; screenshot proof.

## Out of scope

index.html, index2–11, index25–29, all PDPs (p*/product-*), the generators, the gallery.
