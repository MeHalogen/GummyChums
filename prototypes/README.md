# Prototypes

Static design explorations. **None of this is the live site.**

The live store is the Shopify theme in [`../shopify-theme/`](../shopify-theme/),
served at gummychums.com. Everything here is reference: earlier directions,
rejected layouts, and the coming-soon pages that ran before launch. Nothing in
this folder is deployed by the Shopify build, and changing a file here changes
nothing a customer sees.

## What's in here

| | |
|---|---|
| `index*.html` | numbered design iterations, oldest to newest |
| `index-gallery.html` | an index of the iterations — open this first |
| `coming-soon-a…h.html` | the pre-launch holding pages |
| `about` · `contact` · `brain-booster` · `deep-sleep` · `eye-care` · `bundle-builder` | page-level explorations |
| `deploy/` | the self-contained bundle that was deployed as the coming-soon site |
| `logo/` `fonts/` `logo.png` `mascot.png` `bears.png` | assets these pages reference |

## Opening them

They are plain static files with relative links, so open any one directly:

```bash
open prototypes/index-gallery.html
```

Every page links to its siblings, and every asset path is relative to this
folder — which is why the assets moved in here with the HTML rather than
staying at the repo root.

## Vercel

`vercel.json` at the repo root rewrites `/` to `prototypes/coming-soon-b.html`.
That deployment is legacy: gummychums.com now points at Shopify. If you move
or rename files in here, update that rewrite or the deployment's front page
404s.

## The trial font

`fonts/NaNJaune-MaxiMedium-TRIAL.ttf` is gitignored and must stay that way —
the trial licence does not permit redistribution or web embedding. The licensed
build used by the real site lives in `../shopify-theme/assets/`.
