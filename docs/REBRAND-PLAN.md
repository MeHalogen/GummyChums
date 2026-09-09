# GummyChums v2 — rebrand plan

_Read alongside [`NOTES-TO-PRIYAL.md`](NOTES-TO-PRIYAL.md), which stays the single parked to-do list. This file is a **spec**, not a task list — it describes what the new brand book changes and how to build it._

**Source:** `GC_brand book.pdf` (17 pages, received 9 Sep 2026)
**Written:** 9 Sep 2026

---

## The headline

**The strategy hasn't changed. The visual execution has.**

Every word of positioning, voice and narrative in the new book matches what the site already says — same origin story, same "wellness shouldn't feel like work", same voice rules ("Your daily Chums are waiting", "Sleep tight, Chum"). The site's copy needs no rewriting.

What's new is a **visual identity**: two illustrated characters, a purple that didn't exist before, a pixel-stepped border motif, grain texture, and a display typeface.

---

## What actually changed

| | Current site | Brand book v2 |
|---|---|---|
| **Pink** | `#DE1D61` | `#DE1D62` — near-identical |
| **Olive** | `#8DAA31` | `#8DAA3D` — near-identical |
| **Orange** | `#F9740D` | `#F47421` — close |
| **Purple** | *(none)* | **`#592354` — new, and used heavily** |
| **Cream** | `#FDF7F4` | `#F8EBDF` — warmer, more peach |
| **Ink** | `#191316` near-black | `#000000` true black |
| **Hero motif** | Abstract gummy blobs (SVG) | **Two illustrated human characters** |
| **Decoration** | Soft blurred gradient blobs | **Pixel-stepped zigzag borders** |
| **Texture** | Smooth gradients | **Grainy, tactile** |
| **Display type** | Manrope (bold) | **NaN Jaune** |
| **Body type** | Manrope | Manrope — unchanged |
| **Product imagery** | Illustrated SVG gummies | **Real gummy photography** |
| **Pattern** | *(none)* | **`gC` monogram repeat, grainy** |

### The reassuring part

**Three of the four primary colours are already correct to within a hex digit.** The current site is not off-brand — it's the same colour family, missing purple. That matters for the timing decision below.

---

## The four signature devices to build

### 1. The pixel-stepped border ⭐ highest impact

The strongest new device, on nearly every page: a zigzag/stepped edge in purple or orange, running along the top, side or as a full frame. It reads as a traditional Indian textile or temple motif rendered in pixel steps — exactly the "proudly modern India" the book asks for.

**Buildable in pure CSS/SVG.** No assets needed. A repeating SVG or `conic-gradient` step pattern as a border element, sized by a token so it scales. This alone would move the site a long way toward the new identity.

### 2. The characters

Two illustrated chums — a boy (paper-boat print shirt, phone in hand) and a girl (purple auto-rickshaw print dress, reading a *Brain Booster* book). Flat cartoon style, Indian, warm.

**We need source files.** The PDF has them flattened into full-page composites, so they cannot be extracted cleanly. Ask the designer for transparent PNGs at 2x, or SVG if it was vector-drawn.

They'd replace the floating gummy blobs in the hero and could appear on product pages, empty cart, and 404.

### 3. Grain and tactile texture

*"Bold colour, grainy gradients and tactile textures… expressive rather than polished."*

Currently every surface is a smooth gradient. A subtle grain overlay (SVG `feTurbulence`, one tiny tiled PNG, or a CSS noise layer) over colour blocks would land most of this. Cheap, and it changes the feel disproportionately.

### 4. NaN Jaune display type

Primary typeface. Manrope stays as the body face, so **only headings change**. Priyal confirmed she's buying the web licence — we need the woff2 files.

Until then the site keeps Manrope for headings, which is what the book lists as the secondary face, so nothing is *wrong* meanwhile.

---

## Approach: build in parallel, don't touch what works

Per your instruction — new build, current site untouched.

**Mechanically:**

1. **Duplicate the theme** in Shopify (Themes → ⋯ → Duplicate) → rename `GummyChums v2`. It sits unpublished in the library; the live theme is unaffected.
2. **New git branch** `rebrand/v2`, so `main` continues to hold what's live.
3. New sections get a `gc2-` prefix so both generations can coexist in one repo if we later want an A/B.
4. The design-system contract tests carry over — the token file changes values, not structure.

**Nothing about this can break the live store.** Worst case we abandon the branch.

---

## Phased build

**Phase 1 — Foundations** *(no external assets needed)*
Token file to the new palette, purple added as a first-class role, warmer cream, true black. The pixel-border device as a reusable snippet. Grain overlay. This is the biggest visual shift available without waiting on anybody.

**Phase 2 — Characters** *(needs asset files)*
Replace hero gummy blobs with the two chums. Rework the hero composition around them — they're figures with a ground line, which is a different layout problem from floating blobs. Extend to empty cart and 404.

**Phase 3 — Type and texture** *(needs NaN Jaune files)*
Swap headings to NaN Jaune, keep Manrope for body. Retune the type scale — NaN Jaune's proportions differ from Manrope, so sizes will need adjusting, not just substituting.

**Phase 4 — Product imagery** *(needs the photo shoot)*
Real gummy photography replaces the SVG illustrations. The `gC` monogram pattern as a section background.

---

## What we need, and from whom

| Asset | From | Blocks |
|---|---|---|
| Character files (transparent PNG 2x, or SVG) | Designer | Phase 2 |
| NaN Jaune woff2 | Priyal (licence being bought) | Phase 3 |
| Gummy photography | Priyal (shoot being arranged) | Phase 4 |
| Pixel-border source, if it was drawn rather than generated | Designer | Nothing — can be rebuilt in CSS |

---

## ⚠️ The timing problem — read this before deciding

**Launch is 19 Sep. That's 10 days.**

A full visual rebrand is realistically **5–7 focused days** *if every asset were in hand today* — and none of them are. Characters, fonts and photos are all still with other people.

Meanwhile the live store still has a hard blocker: **no payment gateway**, waiting on KYC that neither of us controls.

**Recommendation: do not rebrand before launch.**

Launch on the current design. It is built, tested, fast, and — importantly — **already carries three of the four brand colours almost exactly**. It is not off-brand; it is an earlier expression of the same brand.

Then land the rebrand properly, with time to test on real devices, and switch themes when it's ready. Swapping a Shopify theme is one click and instantly reversible.

### A middle path worth considering

If you want the site visibly closer to the new book *before* launch, **Phase 1 alone is about a day and needs nothing from anyone:**

- Exact new hex values
- Purple `#592354` introduced as a real colour
- The pixel-stepped border motif
- Grain overlay

That would make the current site feel materially like the new brand book, without touching the parts that are tested and working, and without waiting on a single asset. The characters and NaN Jaune then follow after launch as Phase 2–3.

**My recommendation: Phase 1 now on a branch, everything else after launch.**
