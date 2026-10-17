# Hero Threshold — Design

**Date:** 2026-10-17
**Branch:** `rebrand/v2`
**Status:** approved in conversation, pending implementation plan

---

## 1. Problem

The homepage hero once ended in two scroll-coupled set pieces — a pink gummy that
zoomed as you scrolled, and a horizontal "ride" through the three Chums. Both were
removed because they jittered badly on the founder's phone. The traced cause was a
three-stop `color-mix` radial gradient scaled uncapped to 27× (~26 megapixels) with
`will-change` pinning a backing store, re-rasterised on every frame of a scroll.

Removing them fixed the jitter and left the page flat. The hero now ends in a pink
dome carrying the line "WHAT'S INSIDE? / Bacopa · Melatonin · Lutein. No added
sugar." and nothing happens anywhere on the page.

Two things are wrong with that band:

1. It is the least interesting thing in the hero, in the most prominent position.
2. It is **structurally load-bearing** and that is not obvious from its markup.
   `.gh-reveal` is the ground the two Chums stand on — it is pulled up under their
   feet by `calc(var(--gh-chum-h) * -0.14)`, and `.gh-edge`'s stepped teeth exist
   to step its pink down into the cream below. It cannot simply be deleted.

## 2. Goal

Replace the contents of the pink dome with a moment worth having, without
reintroducing anything coupled to scroll position, and without the Chums losing
the floor they stand on.

## 3. The asset we already own

`snippets/gc2-kolam.liquid` draws a kolam — the threshold drawing set out at Indian
doorways each morning. Nine pulli (dots) placed first, then one unbroken line looped
around them, four petals, closed back to its start.

It already animates in the order the drawing is actually made: dots fade in
(`opacity .45s`), then the line draws itself (`stroke-dashoffset 900 → 0` over
`2.1s` with a `.38s` delay). It already has a `prefers-reduced-motion` branch that
jumps to the final state. It takes `tone` and `size` parameters.

It is rendered **once** on the entire site, at 108px, inside `gc2-story-teaser`.

Three properties make it the right answer here rather than a decoration:

- **It is the same motif as everything else.** A kolam is built on a dot grid. So is
  the halftone texture now on the pink and closing bands. So are the pixel-stepped
  teeth. Showing it large is the identity going deeper, not a new ornament.
- **Its meaning is the product's meaning.** A kolam is a daily ritual of welcome,
  redrawn every morning. "One a day, every day" is the same sentence.
- **It is the safe class of motion.** See §6.

## 4. Design

### 4.1 The band

`.gh-reveal` keeps every structural property it has today — grid placement, the
negative top margin that tucks it under the Chums' feet, the dome's
`border-radius`, `z-index: 3`, the bottom padding sized to clear `.gh-edge`'s
`-128px` pull, the halftone. Only its contents change.

```
        [Chum L]              [Chum R]
   ╭──────── pink dome ──────────────╮
   │          Come in.               │   threshold line
   │    One a day, every day.        │   sub
   │                                 │
   │    ✿        ✿        ✿         │   three kolams
   │   1st      2nd      3rd         │   drawn left → right
   ╰─▲─▲─▲─▲─▲─▲─▲─▲─▲─▲─▲─▲─▲─▲────╯   teeth step into cream
```

### 4.2 The stagger — the detail that carries it

The three kolams must **not** draw simultaneously. Each starts roughly `0.54s` after
the one to its left, so the sequence reads as one hand drawing across the doorway
rather than three ornaments appearing together. Each kolam's own internal order is
preserved: its dots settle, then its line travels.

Delays, as authored:

| Instance | `--k-dot-delay` | `--k-delay` |
|---|---|---|
| 1 (left)   | `0s`    | `.38s`  |
| 2 (centre) | `.54s`  | `.92s`  |
| 3 (right)  | `1.08s` | `1.46s` |

The third line finishes at `1.46s + 2.1s = 3.56s` after the row enters view.

### 4.3 Copy

The band carries a threshold welcome, matching what a kolam means, in the voice the
brand already uses ("Your daily Chums are waiting", "Sleep tight, Chum"):

- Line: **Come in.**
- Sub: **One a day, every day.**

Both stay theme-editor settings so Priyal can change them without code. They reuse
the existing setting ids `reveal_title` and `reveal_sub` with new labels and
defaults.

### 4.4 Where the ingredients go

`templates/index.json` saves only `eyebrow`, `headline` and `sub` for `gc_home`.
`reveal_title` and `reveal_sub` render from schema defaults, so changing the
defaults does reach the live site with no template edit. Verified against a fresh
`theme pull` of the live theme.

The displaced copy moves to `gc-quality`, the page's factual block. Note that its
schema default for `layout` is `full`, but the homepage instance **saves**
`layout: "badges"` in `templates/index.json` — so the change belongs in the
`badges` branch of the markup, and a change made in the `full` branch would not
appear on the homepage at all. The badges there are hard-coded rather than
settings, so the additions follow that same pattern:

- A fifth badge, `🍬 No added sugar`, joins FSSAI / lab-tested / vegetarian /
  made in India.
- The actives become a line under the badge row: **Bacopa · Melatonin · Lutein** —
  one active per SKU (Brain Booster, Melatonin, Eye Care). It is a list, not a
  claim, so it is not a badge.

## 5. Implementation surface

Four files. No new files.

| File | Change |
|---|---|
| `sections/gc-home.liquid` | Replace the two children of `.gh-reveal` with the threshold block and the kolam row. Update the `reveal_title` / `reveal_sub` schema labels and defaults. |
| `assets/gc-brand.css` | Make the two kolam transition delays variable: `var(--k-delay, .38s)` and `var(--k-dot-delay, 0s)`. |
| `assets/section-gc-home.css` | Layout for the threshold block and the kolam row, plus the responsive width override. |
| `sections/gc-quality.liquid` | Fifth badge and the actives line in the `badges` branch. |

`snippets/gc2-kolam.liquid` is **not** modified. It already takes everything needed.

### 5.1 Backward compatibility

The delay variables default to the values currently hard-coded (`.38s` and `0s`),
so `gc2-story-teaser`'s kolam renders and animates exactly as it does today. This
must be asserted, not assumed.

### 5.2 Sizing

The snippet writes `width`/`height` attributes in px. The SVG carries a `viewBox`,
so a CSS rule overrides those attributes and lets the kolams scale with the
viewport. Target `clamp(64px, 20vw, 112px)`.

At 375px with a 20px gutter, three kolams at the 20vw mid-value (75px) plus two
gaps fit in the 335px available. If measurement shows crowding, the row drops to
**two** kolams below 380px rather than shrinking them below legibility — the
stagger still reads with two.

### 5.3 Reveal trigger

`.gc-rise` goes on the kolam row, not on `.gh-reveal`. `gc-brand.js` adds `.in`
when the element enters view, and the existing CSS keys off `.in` as a descendant
selector. Putting it on `.gh-reveal` would apply `.gc-rise`'s own transform to the
entire band, including the dome geometry the Chums stand on.

## 6. Why this does not reintroduce the jitter

This needs stating precisely, because the honest answer is not "it's GPU
accelerated".

`stroke-dashoffset` is **not** a compositor-only property. It repaints on the main
thread, unlike `transform` and `opacity`. This design does not claim it is free.

What makes it safe is the trigger, not the property. It is a **one-shot transition
fired once when the row enters view**. It performs zero work while the user scrolls.
The removed set pieces were bound to scroll *position*, so every frame of every
scroll gesture paid their cost — that is what produced the jitter, and it is a
different mechanism entirely.

Supporting evidence rather than argument: this exact animation has been live in
`gc2-story-teaser` throughout every jitter report in this project, and was never
among them.

Constraints that keep it that way, to be enforced by test:

- No `animation-timeline`, no `position: sticky`, no scroll listener in this band.
- No scaled gradients. The kolam is a stroked path on a flat fill.
- No `will-change`.
- Three instances maximum.

## 7. Accessibility

- The kolam row is ornamental: `aria-hidden="true"`, and the snippet already sets
  `role="presentation"` and `focusable="false"` on the SVG.
- `prefers-reduced-motion: reduce` is already handled by the existing rules — dots
  at their final opacity, line at `stroke-dashoffset: 0`, no transition. The new
  delay variables must not defeat this; the reduced-motion branch sets
  `transition: none`, which ignores delay entirely.
- The threshold line stays a real heading in the document, not an image.
- Contrast: cream (`--c-surface`, `#FFFFFF`) on cherry (`--c-cherry`) is the pairing
  the band already uses for its current text, so it is unchanged and already passes.

## 8. Testing

Existing suites must stay green: `architecture` (15), `design-system` (11),
`locked-hero` (8).

`locked-hero` already asserts scroll-coupling stays gone and reads the section plus
its linked stylesheets, so it covers the constraint in §6 for free.

New assertions to add:

1. The kolam delay values are authored as the CSS variables, not hard-coded, so a
   future change cannot silently desync the stagger.
2. `gc-brand.css`'s delay fallbacks equal the values the story teaser relies on
   (`.38s`, `0s`) — the backward-compatibility guarantee in §5.1.
3. `.gh-reveal` retains the structural properties the Chums stand on: the negative
   top margin, the dome `border-radius`, and bottom padding sufficient to clear
   `.gh-edge`'s `-128px`. This is the §1.2 trap, caught by test rather than by eye.

## 9. Open items to judge on screen, not now

- **Dots on dots.** The band already carries the halftone. Kolam pulli at ~96px
  against a 14px halftone grid should separate by scale. If it reads muddy, lower
  `--gc-halftone-strength` on this band only — the variable exists for this.
- **Three across at 375px.** Per §5.2, measure before assuming it fits.

## 10. Out of scope

- The product page.
- The removed scroll sequences. They stay removed.
- Product photography, the cookie banner, GA4, the invented reviews, and the
  dev-store payment question — all tracked in `docs/LAUNCH-BLOCKERS.md`.
