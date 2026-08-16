# GummyChums — Coming Soon Page · STATUS & HANDOFF

_Living doc. If the chat/context resets, read this first to continue exactly where we left off._
_Last updated: 2026-08-16._

## TL;DR — where we are
**🟢 LIVE.** The coming-soon page is deployed and serving on the real domains with valid SSL:
- **https://gummychums.com** (primary) · **https://gummychums.in** (also live)
- Emails flow to Klaviyo. Pushed to GitHub `main`.
- Remaining polish: set `gummychums.in` → redirect to `.com` (Vercel dashboard, optional); delete 2 Klaviyo test entries.

DNS = A-record method at Hostinger (records editable in hPanel; nameservers left at dns-parking): `A @ → 76.76.21.21`, `CNAME www → cname.vercel-dns.com` on BOTH domains. Verified resolving via Google + Cloudflare DNS.
- **Chosen design:** `coming-soon-b.html` (bold six-colour panels + marquees, real logo, gummy cursor).
- **Email capture:** wired to **Klaviyo**, tested live (HTTP `202`). Real emails flow into the "Coming Soon Waitlist".
- **HOSTING = Vercel (free).** NOT Hostinger hosting (that was never bought — Hostinger only holds the domain, parked). Project = **gummy-chums** (`mehalogens-projects`), CLI user `mehalogen`. Deployed the clean `deploy/` bundle as production → **LIVE at https://gummy-chums.vercel.app** (clean `/`, no experiments exposed).
  - How it was deployed: `cp -r .vercel deploy/.vercel && cd deploy && vercel --prod --yes` (then removed the nested copy). Re-deploy the same way after edits. (Repo-root `vercel --prod` would serve the OLD `index.html` at `/` because Vercel won't let a rewrite override an existing file — that's why we deploy the `deploy/` subfolder.)
- **NEXT ACTION:** connect **gummychums.com** (registered at Hostinger, nameservers currently `*.dns-parking.com`) → point it at Vercel (see Deploy section). Then SSL auto-issues and https://gummychums.com goes live.

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

## Deploy — Vercel (DONE) + connect domain (PENDING)
**Hosting is Vercel, free.** Live at https://gummy-chums.vercel.app. To connect gummychums.com:
1. **vercel.com → gummy-chums project → Settings → Domains → Add** `gummychums.com` (and `www.gummychums.com`).
2. Vercel shows DNS. Simplest = **nameserver method**: set the domain's nameservers to **`ns1.vercel-dns.com`** and **`ns2.vercel-dns.com`**.
3. **Hostinger → Domains → gummychums.com → DNS / Nameservers → Edit** → replace the two `*.dns-parking.com` nameservers with the two Vercel ones → Save.
4. Wait (mins–hours). Vercel auto-verifies + issues SSL. Then **https://gummychums.com** is live.
5. Test: submit an email on the live site → confirm it lands in Klaviyo.

_Re-deploy after edits:_ `cp coming-soon-b.html deploy/index.html && cp -r .vercel deploy/.vercel && (cd deploy && vercel --prod --yes) && rm -rf deploy/.vercel`
_(Also keep the zip fresh for reference:_ `cd deploy && zip -r -X ../gummychums-coming-soon.zip index.html fonts logo)`

## 2026-08 round 2 — founder feedback + 3-flavor mockups
Founder feedback on the live 6-colour version: too chaotic / not appealing, weak on mobile (most traffic = Instagram→phone). Wants: **3 colours = 3 real flavours** (not 6), a **tease**, **splashy** click interactions, mobile-first. Anti-gravity (another IDE tool) had edited the live bundle with Gemini photo-fruit + janky clicks — founder didn't like it.
- **Anti-gravity's version is PRESERVED on branch `antigravity-version`** (its `deploy/index.html`, 3 fruit PNGs in `deploy/images/`, and a tighter logo with the dotted underline removed). Don't delete that branch.
- **Flavour → colour:** 🍒 Cherry `#DE1D61` (sleep) · 🥭 Mango `#8DAA31` green/kaccha-aam (focus) · 🍊 Orange `#F9740D` (eye care). Black logo on light bg. Mango is swappable to gold if desired.
- **4 mockups built** (all: black logo, 3 flavours, smooth CSS/WAAPI splashes, gummy cursor, mobile-first, real Klaviyo capture, logo save-protection): `mock-splash.html` (tap gummy → colour splash), `mock-thirds.html` (3 colour bands, fills phone), `mock-liquid.html` (minimal, drifting flavour blobs, tap anywhere), `mock-cards.html` (3 flavour cards that tease each product).
- **Viewable publicly on phone** at `https://gummychums.com/mock-splash.html` / `-thirds` / `-liquid` / `-cards` (added into `deploy/`; **homepage `/` unchanged** = current live coming-soon). Remove these `/mock-*` files from `deploy/` once the founder picks a direction. (Vercel preview URLs are login-walled by Deployment Protection — that's why mockups are served from the prod domain instead.)

## The other drafts (kept as options/experiments)
- `coming-soon-a` Gummy Downpour · `-c` Squish jelly · `-d` Magnet Mochi · `-e` Scratch reveal · `-f` Fill-the-jar (all playful, **use NaN Jaune trial → not deploy-ready**).
- `coming-soon-g` (light) / `-h` (dark) = **minimalist** finalists, licence-clean (real logo PNG + Manrope). Mock email capture only — would need the same Klaviyo snippet as B to go live.

## Open items / next steps
- [x] Deploy B → **DONE** (Vercel, https://gummy-chums.vercel.app).
- [ ] **Connect gummychums.com** (Vercel Domains + Hostinger nameservers → Vercel). ← current step
- [ ] Delete the 2 Klaviyo test entries.
- [ ] (optional) Mirror the Klaviyo snippet into G/H if design changes; swap success id `done`→`thanks`.
- [ ] (optional) Real contact email once they have one.
- [ ] (later) Tidy A–F (swap trial font) or drop them; set up Hostinger Git auto-deploy once repo is tidied.
- [ ] (future) Full store likely on **Shopify** → repoint domain; Klaviyo connects natively, waitlist ready for a launch email.
