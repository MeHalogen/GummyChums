# Report: gc-footer.liquid rebuild

## What changed and why

Rebuilt `shopify-theme/sections/gc-footer.liquid` end-to-end on top of `gc-tokens.css`,
per `shared-contract.md` and `task-footer-brief.md`. Structure and functionality
(logo, tagline, three link columns, bottom bar, all four schema settings) were
preserved exactly; only the CSS and a couple of markup details changed.

Key decisions:

- **Grounding ink block:** `.gcf{background:var(--c-ink);color:var(--c-bg)}` —
  the footer is now a solid dark canvas with light text, as specified.
- **Single accent, restrained:** the old footer sprayed cherry/mango/orange
  everywhere (h4 headings in cherry, a dot that cycled through all three
  flavour colours via `@keyframes gcfDot`). I removed the flavour-colour
  cycling entirely and now use `var(--c-accent)` in exactly one place — the
  three column headings (`.gcf-col h4`) — which the brief explicitly allows
  ("column headings OR the gummy dot — not both"). The separator dot is now a
  plain neutral `var(--c-bg)` circle at reduced opacity, no colour, no
  animation — nothing else in the file touches `--c-accent`/`--c-cherry`/
  `--c-mango`/`--c-orange`.
- **Muted text on a dark surface:** the token set's `--c-ink-2`/`--c-ink-3` are
  translucent *dark* colours meant for dark-on-light text, so they'd be
  invisible on an ink background. Since the contract disallows `rgba()` of a
  token, muted steps here are built from `color:var(--c-bg)` + the CSS
  `opacity` property (0.4–0.78 depending on hierarchy) — this uses zero raw
  hex/rgba values while still producing the tagline/link/legal/hairline
  "muted steps" the brief calls for.
- **Decorative glow:** kept the closing-anchor glow but rebuilt it as
  `radial-gradient(60% 60% at 15% 0%, var(--c-bg), transparent 70%)` on
  `::before` with the whole pseudo-element faded via `opacity:.08`. Still a
  gradient (never `filter:blur()`), and neutral in colour so it doesn't count
  as a second accent element.
- **Contained:** `.gcf-in{max-width:var(--container);margin-inline:auto}`, and
  horizontal gutter is applied on the outer `.gcf` via
  `padding:var(--sp-8) var(--gutter) var(--sp-5)`.
- **Type:** headings `var(--fs-xs)` + `var(--ls-wide)` + uppercase; links
  `var(--fs-base)` (client's "text is small" complaint pushed me to the larger
  of the two allowed sizes); legal/bottom-bar text `var(--fs-xs)`. Every
  `font-size` in the file is a `var(--fs-*)` token — nothing off-scale.
- **Spacing:** all paddings/margins/gaps use the `--sp-*` scale (`--sp-1`
  through `--sp-8`); no arbitrary px/clamp values for spacing.
- **Motion:** link-hover uses a small `transform:translateX(var(--sp-1))` +
  opacity transition; added `@media (prefers-reduced-motion:reduce){.gcf-col
  a{transition:none}}` to respect reduced-motion preference. No other motion
  in the file (the old flavour-cycling dot animation was removed, which also
  incidentally removes a motion source that previously ignored
  reduced-motion... actually the old dot did have a `prefers-reduced-motion`
  guard already, but removing the animation entirely is simpler and calmer).
- **Accessibility:** the `<img>` logo keeps `alt="{{ shop.name }}"` and both
  `width="230" height="86"` (matches the 4146×1550 asset ratio, unchanged
  from the original — it was already correct). Decorative elements
  (`.gcf-hr`, `.gcf-dot`) got `aria-hidden="true"`.
- **Schema:** unchanged — `tagline`, `instagram` (still `text`, not `url`,
  per the hard rule), `email`, `legal`, all with their original
  labels/defaults.
- **No duplicate selectors:** every selector in the file's single `<style>`
  block is declared exactly once.

## Verification (exact commands + output)

```
$ cd /Users/mehalsrivastava/GitHub/GummyChums && npm test 2>&1 | grep "gc-footer.liquid"
(no output)
```

```
$ cd /Users/mehalsrivastava/GitHub/GummyChums/shopify-theme && shopify theme check 2>&1 | tail -4
╰──────────────────────────────────────────────────────────────────────────────╯

  Theme Check Summary.

  160 files inspected with 13 total offenses found across 10 files.
  13 warnings.
```

(0 errors; the 13 warnings are pre-existing in other files — confirmed with
`shopify theme check 2>&1 | grep -i "gc-footer\|error"`, which returned no
output at all, i.e. gc-footer.liquid contributes zero offenses of any kind.)

## Concerns

None. Only file touched was `shopify-theme/sections/gc-footer.liquid`. No git
commands or `shopify theme push` were run.
