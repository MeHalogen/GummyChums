# TASK: Rebuild `shopify-theme/sections/gc-header.liquid`

Read `.superpowers/sdd/shared-contract.md` first — it is binding.

## The problem you are fixing (client's own words)
Screenshot review of the current header: *"TOO FLASHY... THE TEXT IS SMALL...
THE BAR HAS SO MANY OPEN SPACES ON LEFT RIGHT... WE DONT WANT A LAZY AND
SCATTERED THING."*

Diagnosis:
- Logo pinned hard-left, nav pinned hard-right via `margin-left:auto` →
  ~900px of dead space in the middle on wide screens. **Structural laziness.**
- Three loud bands stacked (dark marquee → bright pink bar → hot-pink pill).
  No hierarchy — everything shouts.
- Nav type at `.98rem` inside a tall bar → dwarfed by its container.
- Bar background is full-bleed but content is `max-width:1180px` hard-coded.

## Required design
1. **Three-zone CSS grid — this is the core fix.**
   `grid-template-columns: 1fr auto 1fr;` → **logo left · nav CENTRED · cart right.**
   The centred nav occupies the middle, so the dead space disappears structurally.
   Do NOT use `margin-left:auto`.
2. **Calm bar:** background `var(--c-bg)` (canvas — NOT pink), bottom hairline
   `1px solid var(--c-line)`. Sticky, height `var(--header-h)`.
   Do NOT use `backdrop-filter` (it repaints every scroll frame and caused jank).
3. **The cart pill is the ONLY accent element in the header.**
   `background:var(--c-accent)`, text `var(--c-accent-ink)`.
   **Known bug to fix:** the label text renders dark because Dawn's `.header a`
   colour rule wins over a bare text node. Wrap the label in its own element and
   set its colour explicitly; lock `:link/:visited/:hover/:active` too.
   The item-count badge must not be clipped or overflow the pill.
4. **Nav type sized to its container:** `var(--fs-base)`, weight 600,
   `color:var(--c-ink)`; hover → `var(--c-accent)`. Keep the existing links
   (Shop, Story `#gc-story`, FAQ `#gc-faq`) and the cart link.
5. **Announcement marquee:** keep it, but muted and subordinate — `var(--c-ink)`
   background, `var(--fs-xs)`, wide letter-spacing, slow (≥60s), pausable under
   reduced-motion. It must read as a quiet detail, not a third shouting band.
   Keep the existing `show_bar` + `bar_text` schema settings.
6. **Contained:** inner wrapper uses `var(--container)` + `var(--gutter)` so the
   content is anchored, not floating at the viewport edges.
7. **Mobile (<749px):** logo + cart stay; secondary nav links may hide. Must not
   overflow horizontally. Logo `<img>` keeps BOTH width and height attrs
   (logo asset ratio is 4146x1550).

## Definition of done
- `npm test 2>&1 | grep "gc-header.liquid"` outputs nothing.
- `shopify theme check` shows 0 errors.
- Header renders: logo left, nav centred, cart right, no dead middle gap.
