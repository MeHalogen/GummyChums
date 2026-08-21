# GummyChums Design System — Design Doc

## Problem
The Shopify theme was built component-by-component with hand-typed values. Symptoms the client reported:
- **"Too flashy"** — pink used simultaneously for the header bar, buttons, badges, prices and background. No focal point.
- **"Scattered / lazy"** — header uses `margin-left:auto`, leaving ~900px dead space between logo and nav.
- **"Text is small"** — type sized ad-hoc per component, dwarfed by its containers.
- Recurring bugs (duplicate `.gh-cta` selectors, a cart label overridden to the wrong colour, an invalid `url` schema default) survived multiple rounds because **nothing tests the theme**.

Root cause: **no design tokens, no component contracts, no tests.**

## Direction (approved)
**Restrained premium.** Calm cream canvas, ONE accent used sparingly for actions only, disciplined spacing, confident large type.

## Architecture

### 1. Tokens — `assets/gc-tokens.css` (single source of truth)
No component may hard-code a raw value.

- **Spacing:** 4px base, `--sp-1`(4) … `--sp-10`(128).
- **Type:** exactly 8 sizes — `--fs-xs, -sm, -base, -lg, -xl, -2xl, -3xl, -4xl`. Nothing else permitted.
- **Colour by role:**
  - `--c-bg` canvas, `--c-surface`, `--c-ink` + 2 muted steps
  - `--c-accent` (cherry) — **reserved for interactive / primary actions ONLY**
  - `--c-cherry / --c-mango / --c-orange` — **product identity only**, never chrome
  - Rule: at most ONE accent element per viewport region
- **Radii:** 4 steps. **Shadows:** 3 steps. **Layout:** `--container` 1200px, `--gutter` clamp(20px,4vw,40px).

### 2. Component contracts
Each `sections/gc-*.liquid` must: consume tokens only, wrap content in `--container` + `--gutter`, declare each selector once.

### 3. Header rebuild (Batch 2)
3-zone CSS grid `1fr auto 1fr` — logo left, nav centred, cart right. Structural fix for dead space (no `margin-left:auto`). Canvas-coloured bar with hairline border; the cart pill is the only accent. Nav at `--fs-base`/600.

## Testing (TDD — tests written first, must fail on current code)
1. `shopify theme check` — official Liquid/schema linter.
2. `tests/design-system.test.mjs` — fails on: raw hex outside tokens file, font-size off-scale, spacing off-scale, duplicate selector declarations, section missing `--container`.
3. Per-component contract assertions (e.g. header exposes 3 grid zones; cart label resolves to `#fff`).

Runner: Node's built-in `node:test` (no new dependencies).

## Batches
1. **Tokens + test harness** ← this batch
2. Header + footer (parallel subagents)
3. Homepage sections
4. Product page

Review gate after each batch.

## Non-goals
No redesign of cart/checkout (Shopify-owned). No new dependencies. No JS framework.
