# GummyChums — Coming Soon Page · STATUS & HANDOFF

_Living doc. If the chat/context resets, read this first to continue exactly where we left off._
_Last updated: 2026-08-16._

## TL;DR — where we are
The **coming-soon page is built, working, and packaged for deploy** — but **not yet uploaded** to the live domain.
- **Chosen design:** `coming-soon-b.html` (bold six-colour panels + marquees, real logo, gummy cursor).
- **Email capture:** wired to **Klaviyo**, tested live (got HTTP `202`). Real emails flow into the "Coming Soon Waitlist".
- **Deploy bundle ready:** `deploy/` folder + `gummychums-coming-soon.zip` (self-contained: index.html + fonts/ + logo/).
- **Next action:** upload the zip to **Hostinger `public_html`**, extract, enable SSL, open **https://gummychums.com**.

## The brand (source of truth)
- **Domain:** gummychums.com (bought; hosting is on **Hostinger**). This repo is the **home/source repo**.
- **Instagram:** https://www.instagram.com/gummy.chums/  (note the dot)
- **Contact email:** none yet (removed from the page for now).
- **Palette (final, 2026-08-12):** Black `#000` · White `#fff` · Brown `#6E2F15` · Purple `#592354` · Green `#8DAA31` · Pink `#DE1D61` · Orange `#F9740D`.
- **Fonts:** display/logo = the real **logo PNGs** in `logo/` (custom face, NOT a font we have). Body = **Manrope** (free, in `fonts/Manrope-Variable.ttf`). ⚠️ **NaN Jaune** (`fonts/NaNJaune-...TRIAL.ttf`) is **trial-licensed — do NOT ship it**. Draft B does not use it; drafts A–F still do.
- **Logo files** (`logo/`): `gc-monogram.png`, `gc-wordmark-stack.png` (used as hero), `gc-wordmark-row.png`. Pure black on transparent → use `filter:invert(1)` for white on dark.
- **Voice:** playful, proudly Indian, "wellness as a treat not a task." Hero line: **"Not another supplement brand." / "We're making healthy habits feel good."**

## The chosen page — `coming-soon-b.html`
Self-contained single HTML file, vanilla JS, Shopify/Hostinger-portable. Features:
- Six reactive colour panels (flex toward cursor) + top/bottom marquees ("GUMMY CHUMS ✦ COMING SOON ✦ WELLNESS, BUT MAKE IT FUN ✦ MADE IN INDIA").
- Real logo (white via invert) centre; `gc` favicon; OG/theme-color meta.
- **Gummy cursor** (glossy blob SVG following the pointer; hidden on touch).
- Email form → **Klaviyo**; honeypot + consent line + success/error states.
- Mobile: stacks, fits, scrolls instead of truncating. Verified desktop + mobile.

## Email capture — Klaviyo (client-side, no backend, no database)
- **Public Site ID:** `RVzvWv` (safe to expose in front-end)
- **List ID:** `UaVrj2` ("Coming Soon Waitlist")
- Endpoint: `POST https://a.klaviyo.com/client/subscriptions/?company_id=<pubkey>` with header `revision:2024-10-15`. Tested → `202`.
- ⚠️ **TODO: delete 2 test signups** in Klaviyo: `waitlist.test@gummychums.in`, `waitlist.test2@gummychums.in`.

## Deploy — Hostinger (NOT yet done)
1. hPanel → confirm `gummychums.com` points to this hosting (nameservers if bought elsewhere).
2. hPanel → **Files → File Manager → `public_html`**. Remove only the default placeholder file.
3. Upload **`gummychums-coming-soon.zip`** → right-click **Extract** → delete the zip. Result: `public_html/index.html`, `/fonts/`, `/logo/`.
4. hPanel → **Security → SSL** on.
5. Open **https://gummychums.com**, submit a test email, confirm it appears in Klaviyo.
_To rebuild the bundle after edits:_ `cp coming-soon-b.html deploy/index.html && (cd deploy && zip -r -X ../gummychums-coming-soon.zip index.html fonts logo)`

## The other drafts (kept as options/experiments)
- `coming-soon-a` Gummy Downpour · `-c` Squish jelly · `-d` Magnet Mochi · `-e` Scratch reveal · `-f` Fill-the-jar (all playful, **use NaN Jaune trial → not deploy-ready**).
- `coming-soon-g` (light) / `-h` (dark) = **minimalist** finalists, licence-clean (real logo PNG + Manrope). Mock email capture only — would need the same Klaviyo snippet as B to go live.

## Open items / next steps
- [ ] Deploy B to Hostinger (steps above).
- [ ] Delete the 2 Klaviyo test entries.
- [ ] (optional) Mirror the Klaviyo snippet into G/H if design changes; swap success id `done`→`thanks`.
- [ ] (optional) Real contact email once they have one.
- [ ] (later) Tidy A–F (swap trial font) or drop them; set up Hostinger Git auto-deploy once repo is tidied.
- [ ] (future) Full store likely on **Shopify** → repoint domain; Klaviyo connects natively, waitlist ready for a launch email.
