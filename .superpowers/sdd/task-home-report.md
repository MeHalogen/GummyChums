# Report — gc-home.liquid + gc-gummy.liquid rebuild

## Files changed
- `shopify-theme/sections/gc-home.liquid` — full token migration + flavour-card redesign
- `shopify-theme/snippets/gc-gummy.liquid` — gummy redesigned from glossy sphere to soft jelly

## What changed, and why

### 1. The gummy: sphere → jelly
`gc-gummy.liquid` previously took `c1/c2/c3` (three hardcoded hex shades per instance)
and drew a near-circular squircle with a crisp bright-white specular ellipse — the
"marble" the client was reacting to. Rewrote it:

- **Single `tone` param** (a token name, e.g. `--c-cherry`) — light/base/dark shades
  are now derived from that one token via `color-mix(in srgb, var(--c-cherry) 52%, white)`
  / `74%, black`. Every colour in the gummy traces back to one design token; no hex
  anywhere in this file (not even outside `<style>`, since SVG presentation attributes
  accept `var()`/`color-mix()` directly).
- **Squashed, irregular blob** — viewBox widened to 140×100 (was 120×120) and the path
  redrawn asymmetrically (different curvature per side) so it reads as hand-rolled
  candy, not a geometric primitive.
- **Diffuse specular instead of a sphere highlight** — the old solid white ellipse
  at 62% opacity (the single biggest "marble" cue) is replaced with a soft
  radial-gradient falloff (`hi-{id}`: 46% → 10% → 0% opacity), so there's no crisp
  glossy edge.
- **Inner translucency** — added a second radial-gradient layer (`inner-{id}`) low
  in the body to suggest light passing through jelly, plus a faint secondary glint
  near the underside for a "squished, not rigid" read.
- No `filter`/`drop-shadow` used anywhere (softness comes from gradient stops, not
  filters) — keeps it compliant with the no-blur-on-animated-elements rule.

Callers dropped from passing 3 hex literals each to passing one token name, e.g.
`{% render 'gc-gummy', tone: '--c-cherry', id: 'h1' %}` — this also deleted ~15
hardcoded hex literals from `gc-home.liquid`'s render calls.

### 2. Flavour cards — the client's active complaint
Per the brief's diagnosis, fixed all six points:
- **Cluster, not a giant ball**: each card's fallback media now renders three
  `gc-gummy` instances (`.gh-g1/2/3`) at different sizes (44%/29%/26% of the media
  box) and rotations (-9°/13°/-15°), independently bobbing (`ghBob` keyframe on the
  `translate` property, not `transform`, so it doesn't collide with the static
  rotate — same pattern already used for cursor-parallax elsewhere in this file).
- **Media ratio** changed from `1/1` to `5/4` (`.gh-shot{aspect-ratio:5/4}`), so the
  card is no longer a big empty square with squashed text underneath.
- **Richer background**: `background:var(--pc-soft)` (the actual `--c-*-soft`
  tokens, ~10-12% alpha) instead of the old `{{ col }}16` hex+alpha-suffix hack.
- **Fixed short benefit line** replaces the truncated description: "Wind down.
  Sleep tight." / "For screen-tired eyes." / "Big brain energy, tiny gummy." —
  exactly as specified in the brief.
- **Price**: `{{ product.price | money_without_trailing_zeros | replace: 'Rs.', '₹' }}`.
- **Add button colour = flavour identity**: `style="background:var({{ tone }})"`,
  i.e. `--c-cherry` / `--c-orange` / `--c-mango` per card — never `--c-accent`, so
  the "max one accent per region" rule isn't violated by three coloured buttons.

### 3. Token migration (whole file)
- Removed the local re-declared colour aliases (`--cherry/--mango/--orange/--ink/--cream`)
  and every raw hex in the `<style>` block (including the `#191316a0`-style
  8-digit alpha-hex shorthand, which is itself a raw-hex violation) — all mapped to
  the shared-contract roles (`var(--c-ink)`, `var(--c-ink-2)`, `var(--c-ink-3)`,
  `var(--c-surface)`, `var(--c-accent)`/`--c-accent-soft`, `--c-cherry/mango/orange`
  + `-soft`).
  - Decorative sticker backgrounds (`100% VEG` etc.) had no matching brand token, so
    they now use the flavour `-soft` tokens (mango/orange/cherry) instead of the old
    arbitrary yellow/green/peach hex — same visual family as the rest of the page.
  - Two raw `rgba()` glows tied to the old cherry hex (`.gh-tag mark`, `.gh-story::before`)
    now use `var(--c-accent-soft)`.
- Every `font-size` mapped to the nearest of the 8 approved `--fs-*` sizes (hero
  headline → `--fs-4xl`, card titles → `--fs-xl` as the token comment intends,
  body/meta → `--fs-sm`/`--fs-base`, etc).
- `font-weight` mapped to the three tokens actually used in the original design
  (600→`--fw-body`, 700→`--fw-bold`, 800→`--fw-black` — verified against every
  original declaration so nothing shifted visual weight).
- Radii → `--r-sm/md/lg/full`; shadows → `--sh-1/2/3` (dropped a couple of
  one-off custom box-shadows — e.g. the pink-tinted card hover glow — in favour of
  the shared `--sh-3`, which also nudges the client's "too flashy" complaint in the
  right direction).
- Spacing (margin/padding/gap) mapped to the nearest `--sp-*` step throughout;
  element/illustration *sizing* (icon widths, decorative offsets) was left as
  authored, matching the precedent in `gc-product.liquid` (e.g. `.gp-mini .sh{width:78px}`)
  — the spacing scale applies to layout spacing, not arbitrary asset dimensions.
- **Duplicate `.gh-cta` removed** — merged into one declaration.
- **`var(--container)`**: `.gc-wrap` now reads `max-width:var(--container);
  margin-inline:auto;padding-inline:var(--gutter)` (same recipe as `.gc-container`
  in tokens.css / as `.gp` in `gc-product.liquid`); also wrapped the closing-CTA
  section's content in `.gc-wrap` for consistency (it had no width constraint before).
- Removed the now-dead `GPATH` liquid assign and the old single-SVG card fallback
  it fed (superseded by the gummy cluster).

### Preserved (unchanged behaviour)
- 200vh `.gh-stage` / sticky `.gh-pin` scroll fall-in, the `--z` scroll-progress
  script, the zooming gummy with its 20x cap, "WHAT'S INSIDE?" reveal, eyebrow
  chip, `[ ]` → `<mark>` headline highlight, dual CTA, sticker badges, cursor-parallax
  characters, story section, FAQ accordion, closing CTA, real product loop with
  working add-to-cart POST forms, and all `{% schema %}` settings/ids (untouched).
- `prefers-reduced-motion` block extended to also stop the new card-gummy bob
  animation (`.gh-g{animation:none}`).
- No `filter:blur()`/`drop-shadow` introduced; all new animation is on
  `translate`/`transform`/`opacity`.

## Verification

```
$ cd /Users/mehalsrivastava/GitHub/GummyChums && npm test 2>&1 | grep -E "gc-home.liquid|gc-gummy"
(no output)

$ npm test 2>&1 | tail -15
✔ tokens file exists
✔ tokens define the full spacing scale (--sp-1..--sp-10)
✔ type scale defines exactly the 8 approved sizes
✔ tokens define colour roles including a single reserved accent
✔ tokens define layout container and gutter
✔ sections declare each selector only once (no duplicate rules)
✔ sections use no raw hex colours (tokens only)
✔ sections use no off-scale font sizes
✔ every section constrains content with --container
✔ images declare width and height (no layout shift)
✔ raw <img> tags declare both width and height
tests 11, pass 11, fail 0

$ cd shopify-theme && shopify theme check 2>&1 | tail -4
160 files inspected with 12 total offenses found across 9 files.
12 warnings.
(0 errors; confirmed via grep that none of the 12 warnings touch gc-home.liquid or gc-gummy.liquid)
```

One fix needed mid-way: the new `@keyframes ghBob{from{...}to{...}}` collided with
the existing `ghDrift` keyframe's `from`/`to` selectors in the duplicate-selector
scope check (the test doesn't treat `@keyframes` as its own scope the way it does
`@media`). Rewrote `ghBob` to use `0%{...}100%{...}` instead — cosmetically
identical, test-clean.

## Concerns
- `color-mix()` (used in `gc-gummy.liquid` to derive the highlight/shadow tones
  from a single token) needs a reasonably modern browser (Chrome 111+, Safari
  16.2+, Firefox 113+, all 2023-era). Given the store's Sept-2026 launch this
  should be a non-issue, but flagging it since it's the one new CSS feature this
  work introduces.
- Some spacing/radius/shadow values shifted by a few px versus the original
  hand-tuned numbers now that they're snapped to the `--sp-*`/`--r-*`/`--sh-*`
  scale (e.g. story panel radius 34px→28px, several 2-6px spacing rounds). Visual
  differences are minor and in the direction of "more consistent," not "worse,"
  but flagging since it wasn't literally pixel-identical to before.
- I did not attempt to visually render the theme (no `shopify theme dev`/browser
  preview was run) — verification is via the automated test suite and theme
  check only, per the task's stated verification commands.
