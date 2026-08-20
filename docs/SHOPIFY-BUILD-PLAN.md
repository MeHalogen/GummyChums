# GummyChums — Shopify Store Build Plan

_Your calm, step-by-step plan. Today = 20 Aug 2026. Client launch target = **14 Sep 2026**. First paid client project — read this whenever you feel anxious._

## 0. The single most important truth (read this first)
**Shopify handles everything scary. You build only the UI.**
- **Payments, credit cards, checkout** → 100% Shopify. Card data NEVER touches your code or theme. Checkout runs on Shopify's own **PCI-DSS Level 1** servers. You literally *cannot* leak card data because you never see it.
- **Security, SSL/HTTPS, hosting, scaling, DDoS, backups, patching** → Shopify.
- **Customer passwords/accounts, fraud analysis, order storage** → Shopify.
- **You are responsible for:** the storefront look (theme), correct product data/prices, working links, mobile layout, and store settings (shipping, tax, legal pages). **All of these are visible and fixable before launch. None are catastrophic security risks.**

So the disaster scenarios you're imagining (a breach, leaked cards, a payment bug that loses money) are Shopify's surface, not yours. Your job is the part you're already good at: UI.

## 1. How we'll build it (the safe path for a first project + deadline)
**Customize a solid existing Shopify theme — do NOT build a custom theme from scratch, and do NOT go headless/React.**
- Start from **Dawn** (Shopify's free, official, fast, accessible reference theme) OR a good premium theme (~$100–350, e.g. from the Shopify Theme Store), then restyle it to the finalized design and add a few custom sections for the unique bits.
- Why: you inherit working, tested cart/product/collection/checkout templates + the theme editor (so the client can edit content later). This is how most real stores are built. Fastest, safest.
- Your vanilla HTML/CSS/JS prototypes (coming-soon, index pages) **port into Liquid "sections"** — reuse them as custom sections.

## 2. You can build for FREE right now — no client payment needed yet
- Create a **Shopify Partner account** (free) → make a **development store** (free, unlimited time). You can build and test the *entire* theme + fake/test orders on it without anyone paying.
- The client's **paid Shopify plan** is only needed to: (a) accept REAL money, (b) connect the real domain, (c) go live.
- When ready, you **transfer/publish the theme** to the client's paid store.

## 3. The timeline (dated, with buffer before 14 Sep)

### Phase 0 — Foundation · **Aug 20–24** (your aggressive 4 days)
- [ ] Create Shopify **Partner account** + a free **development store**.
- [ ] Install **Shopify CLI**; connect the theme to your GitHub repo (version control the theme like normal code).
- [ ] Pick the base theme (Dawn to start — free, safe).
- [ ] Spend ~half a day learning **Liquid + sections/blocks** structure (it's just templating over HTML — easy for you).
- [ ] Load the **3 real products** (Brain Booster/Mango, Melatonin/Cherry, Eye Care/Orange) with prices, images, descriptions, nutrition. Create a "Shop All" collection.
- [ ] Build the page **skeleton** using the design you already have in mind (home, PDP, collection, cart, story/about/contact, header/footer). Structure now → restyle later.

### Phase 1 — Core build · **Aug 25–31**
- [ ] Build out all storefront pages/sections on the dev store; reuse your prototype components as Liquid sections.
- [ ] Chase the designer for the **final design**. The moment it lands, it's a *restyle*, not a rebuild (because structure is done).
- [ ] Gather real assets: product photos, copy, policies content.
- [ ] Keep the store behind Shopify's built-in **password page** the whole time.

### Phase 2 — Main build week · **Sep 1–7**
- [ ] Apply the finalized design across all pages; polish; full **mobile QA** (most traffic = phone).
- [ ] Announcement bar, nav, search, 404, cart drawer, empty states.
- [ ] **⚠️ Sep 1–3: Client action needed (see §4).**

### Phase 3 — Commerce wiring + test · **Sep 8–11**
- [ ] Publish/transfer the theme to the client's **paid store**.
- [ ] Configure: **payment gateway** (Razorpay or Shopify Payments India — needs KYC, see §4), **shipping** zones/rates, **taxes/GST**, order/shipping **email notifications**, **legal pages** (Privacy, Refund/Return, Shipping, Terms — Shopify has free generators).
- [ ] **Test orders** end-to-end in test mode (see §5).

### Phase 4 — Pre-launch QA · **Sep 12–13**
- [ ] Run the full launch checklist (§6). Place a **real test order** with a real card, then refund it.
- [ ] Analytics (GA4 + Meta Pixel), favicon, SEO titles/meta, social share image.

### Phase 5 — Launch · **Sep 14**
- [ ] Remove the password page. Point **gummychums.com / .in** DNS from Vercel (coming-soon) → **Shopify**.
- [ ] Place one real order yourself. Monitor. Buffer day for fixes.

> **Reality check:** 14 Sep is very achievable *if the design is finalized by ~end of Aug / first days of Sep*. The main risk to the date is **design delay** and **payment KYC delay** (§4) — both are about other people, so chase them early and tell the client the date depends on them.

## 4. When the client must act (THE thing people miss) ⚠️
The long pole is **payment gateway KYC/verification** — in India, activating Razorpay or Shopify Payments needs business documents (PAN, GST, bank account, address proof) and can take **2–5 business days** (sometimes longer) to approve.

**Ask the client to, by ~Sep 1 at the latest (earlier is safer):**
1. Start the **Shopify subscription** (Basic plan is fine; there's often a $1/month promo).
2. **Begin payment gateway onboarding** and submit KYC docs (PAN, GST, bank details).
3. Confirm the **business/legal details** for policies (business name, address, support email/phone, return policy).

If they do this early, everything else fits. If they wait until launch week, the gateway won't be approved in time → launch slips. **Message the client about the payment KYC now.**

## 5. How to test it "live" (proving it actually works)
**On the dev store (free, anytime):**
- Enable a **test payment provider** — either Shopify Payments **test mode** or the **"(for testing) Bogus Gateway"**. Place orders using Shopify's **test card numbers** — no real money moves.
- Walk the full flow: add to cart → checkout → pay (test) → order confirmation.

**On the real paid store (before launch, still password-protected):**
- Do ONE **real order with a real card**, then **refund it**. This is the definitive proof the live gateway + emails + inventory all work.

**"How do I know it worked?" — the test-order checklist:**
- [ ] Order appears in **Shopify Admin → Orders**.
- [ ] **Order confirmation email** arrives to the customer.
- [ ] **Inventory decremented** by 1.
- [ ] Money shows in the (test or real) **gateway dashboard**.
- [ ] **Refund** works and sends a refund email.
- [ ] Repeat on **mobile**.

## 6. Pre-launch checklist (don't-miss-anything)
**Store:** 3 products w/ variants, images, SEO, prices, inventory · collection(s) · shipping zones + rates · taxes/GST · payment gateway live · order/shipping emails · **legal pages** (Privacy, Refund, Shipping, T&C) · checkout settings (guest checkout, required fields).
**Theme:** home · product page · collection · cart/drawer · search · 404 · header/nav · footer · announcement bar · policies linked in footer · mobile everything.
**Launch:** remove password page · domain connected + SSL · GA4 + Meta Pixel · favicon · social share meta · one real test order placed & refunded · client has admin access.

## 7. Your responsibilities vs Shopify's (so you stop worrying)
| You (fixable, visible, UI-level) | Shopify (don't worry) |
|---|---|
| Theme look & layout, mobile | Payments, checkout, PCI compliance |
| Correct product data & prices | Card data, fraud, chargebacks |
| Working links, no broken pages | SSL, hosting, uptime, scaling, backups |
| Store settings (shipping/tax) | Customer passwords/accounts |
| Legal pages present | Security patching, DDoS |
| Least-privilege on any 3rd-party apps | The database & infra |

## 8. Golden rules to stay safe
- Build on the **dev store** first; transfer when ready. Never experiment on the live store.
- Keep the store **password-protected** until the final go-live.
- **Never** paste API keys/secrets into theme code. Only install **reputable** apps, and as few as possible.
- **Version-control the theme** (Shopify CLI + git) so you can always roll back.
- Keep the **coming-soon page live** on the domain until the very moment you repoint DNS to Shopify at launch.
- Every claim of "done" = backed by a real test order or a screenshot. Evidence, not hope.

## 9. How Claude (me) helps at each step
- Port your prototype components into Liquid sections.
- Set up the theme structure, PDP, collection, cart, content pages.
- Write the QA checklist runs, the legal pages, the client message about payment KYC.
- Debug anything, review before launch. Ask me at every phase — you're not doing this alone.
