# GummyChums — SHARED CONTRACT (all Batch 2 components)

## Brand & direction
GummyChums: Indian wellness gummy brand. 3 products (Melatonin/Cherry=sleep,
Eye Care/Orange=eye care, Brain Booster/Mango=focus).
**Design direction: RESTRAINED PREMIUM.** Calm canvas, ONE accent used sparingly,
disciplined spacing, confident type. The client's complaints were literally:
"too flashy", "scattered", "text is small", "lazy". Fix those.

## Token contract — assets/gc-tokens.css is the ONLY source of values
Read `shopify-theme/assets/gc-tokens.css` first. It defines:
- Spacing `--sp-1`(4px) … `--sp-10`(128px)
- Type — EXACTLY 8: `--fs-xs --fs-sm --fs-base --fs-lg --fs-xl --fs-2xl --fs-3xl --fs-4xl`
- Colour BY ROLE:
  - `--c-bg` canvas, `--c-bg-warm`, `--c-surface`, `--c-ink`, `--c-ink-2`, `--c-ink-3`, `--c-line`
  - `--c-accent` / `--c-accent-hover` / `--c-accent-ink` / `--c-accent-soft`
    → **RESERVED for interactive & primary actions ONLY. Max ONE accent element per viewport region.**
  - `--c-cherry --c-mango --c-orange` (+ `-soft`) → **product identity ONLY, never chrome**
- Radii `--r-sm --r-md --r-lg --r-full`; shadows `--sh-1 --sh-2 --sh-3`
- Layout `--container` (1200px), `--gutter`, `--header-h` (68px)
- Motion `--ease --spring --dur-1 --dur-2 --dur-3`
- Layout primitive class `.gc-container` (max-width + auto margin + gutter padding)

## HARD RULES (these are machine-tested — you WILL be checked)
1. **No raw hex** anywhere in your file's CSS. Use `var(--token)`. (rgba() of a
   token is not available — if you need transparency use the provided `-soft`/
   `--c-ink-2/3` tokens, or add nothing.)
2. **No off-scale `font-size`** — every `font-size` must be `var(--fs-*)`.
3. **No duplicate selectors** — declare each selector exactly once. (The old code
   had 6 selectors declared twice, silently overriding each other.)
4. **Must use `var(--container)`** to constrain content width.
5. Keep spacing on the `--sp-*` scale.

## Verify your work (MANDATORY before you report DONE)
From the repo root `/Users/mehalsrivastava/GitHub/GummyChums`:
```
npm test 2>&1 | grep "YOUR_FILE.liquid"
```
**This must output NOTHING.** Any line naming your file = a violation you must fix.
(Other files will still show violations — those belong to other agents. Ignore them.)

Also run: `cd shopify-theme && shopify theme check 2>&1 | tail -4` — must show 0 errors.

## Constraints
- Edit ONLY your assigned file. Do not touch any other file.
- **Do NOT run any git command.** Do not commit, stage, or push. The controller commits.
- Do NOT run `shopify theme push`. The controller deploys.
- Preserve all existing functionality (links, cart, forms, schema settings).
- Keep the `{% schema %}` block valid (note: a `url` setting type may NOT have a default).
- Accessibility: keep alt text; `<img>` needs BOTH width and height attributes.
- Respect `prefers-reduced-motion`.
