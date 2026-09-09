# Notes & open questions — GummyChums

_The single parked list. Everything not-yet-done lives here: questions for Priyal, decisions taken on her behalf, and the tasks still on Mehal's plate. Nothing else should hold a to-do list._

**Launch: 19 Sep 2026** · Last updated: 9 Sep 2026

---

# PART 1 — For Priyal

## ⚡ Priyal replied 9 Sep — what's settled, what's still open

**Settled and actioned:**

| Answer | Status |
|---|---|
| Prices **₹699 Melatonin · ₹599 Brain Booster · ₹599 Eye Care**, GST-inclusive | ✅ live on the store |
| Shipping tiers ₹49 / ₹69 / ₹99 confirmed | ✅ already live |
| Free shipping threshold **₹999** (not ₹699 — a single Melatonin shouldn't qualify) | ✅ live & verified |
| Reviews: **hide until genuine ones exist** | ✅ section disabled, content kept |
| FSSAI: keep manufacturer's licence for now | ✅ unchanged |
| Both KYCs started 9 Sep | ⏳ with her |
| Photos + founder note coming | ⏳ with her |

**Still open:** GST **rate** — her CA is confirming the slab, expected 10 Sep.

### ✅ Tax-inclusive pricing is on and verified

Verified end to end on a real checkout: one Melatonin totals **₹748.00** (₹699 + ₹49 shipping), with GST inside the price rather than added on top. The store no longer charges ₹824.82 for a ₹699 product.

---

## 📮 Round 3 — sent 9 Sep, awaiting reply

### R5. Delivery charges — the ₹69/₹99 tiers are unreachable 🔴

**Tested on the live store with real carts.** Because products are ₹599–₹699, two packs already exceed the ₹999 free-shipping threshold — so only **single-pack orders ever pay for delivery**.

| Basket | Packs | Weight | Value | Customer pays |
|---|---|---|---|---|
| 1 Melatonin | 1 | 0.15 kg | ₹699 | ₹49 |
| 1 Brain Booster | 1 | 0.15 kg | ₹599 | ₹49 |
| Melatonin + Brain | 2 | 0.30 kg | ₹1,298 | **₹0** |
| All three | 3 | 0.45 kg | ₹1,897 | **₹0** |
| 2 of each | 6 | 0.90 kg | ₹3,794 | **₹0** |
| 3 of each | 9 | 1.35 kg | ₹5,691 | **₹0** |
| 10 packs | 10 | 1.50 kg | ₹6,990 | **₹0** |

An order must reach ~4 packs to leave the 0–0.5 kg band, but only 2 packs to clear ₹999. So the ₹69 and ₹99 rates are **structurally unreachable** — they exist but can never be charged.

**Weight cap is impossible.** Tested `deliveryProfileUpdate` with both a price and a weight condition on one rate; Shopify rejects it:

> *"Method definition cannot save conditions with different fields (total_weight and total_price)."*

So "free over ₹999 but only under 1kg" cannot be built. The mutation failed cleanly — no stray rate was created.

**Priyal's absorbed cost per free order** (estimates until her rate card arrives): 2–3 packs ≈ ₹45–70 · 6 packs ≈ ₹65–95 · 9–10 packs ≈ ₹90–120.

**Four options put to her:** (1) leave as-is · (2) same outcome, remove the dead ₹69/₹99 rates so checkout shows one option not two · (3) raise the threshold to ₹1,999 so weight tiers become live again · (4) drop free shipping entirely. **Recommended: 2** — at launch a second pouch is worth more than ₹50 of absorbed delivery.


### R2. GST rate — needed from the CA 🔴

Prices are live and GST-inclusive. Shopify currently assumes **18%** (CGST 9% + SGST 9%), which it applied automatically. Nothing else is blocked by this, but the wrong rate is a filing problem rather than a display one, so it needs confirming before the first real order.

**Need:** the slab the CA confirms for nutraceutical gummies.

### R3. Should shipping charges carry GST? 🔴

Separate setting, currently **off** — shipping is being charged with no GST on it. In India, shipping usually attracts GST at the same rate as the goods being shipped.

**Need:** the CA's answer on this too. One checkbox either way.

### R4. Discount codes — for approval before we create them

Priyal mentioned a 10% launch discount, up to 15% for campaigns, a 5% first-time welcome code, and bundles later. Proposed setup below. **Nothing has been created yet.**

| Code | What | When | Limits |
|---|---|---|---|
| `LAUNCH10` | 10% off everything | 19–30 Sep | One per customer, no minimum |
| `WELCOME5` | 5% off first order | ongoing | One per customer, first order only |
| *(campaign 15%)* | 15% off | per campaign | Held until a campaign is defined |

**What each does to the margin** (GST-inclusive, at 18%):

| | List | After discount | GST inside | **Priyal keeps** |
|---|---|---|---|---|
| Melatonin, no code | ₹699 | ₹699 | ₹106.63 | ₹592.37 |
| Melatonin, `LAUNCH10` | ₹699 | ₹629.10 | ₹95.97 | **₹533.13** |
| Melatonin, 15% campaign | ₹699 | ₹594.15 | ₹90.63 | **₹503.52** |
| Brain/Eye, no code | ₹599 | ₹599 | ₹91.37 | ₹507.63 |
| Brain/Eye, `LAUNCH10` | ₹599 | ₹539.10 | ₹82.24 | **₹456.86** |
| Brain/Eye, 15% campaign | ₹599 | ₹509.15 | ₹77.67 | **₹431.48** |

**Three things to decide:**

1. **Should codes stack?** Recommend **no** — `LAUNCH10` + `WELCOME5` together would be ~15% off, which is campaign-level discounting given away by accident. Shopify lets us block combining.
2. **Do codes stack with free shipping over ₹999?** Free shipping is a shipping rate rather than a discount, so it applies independently — a ₹1398 order with `LAUNCH10` pays ₹1258.20 and still ships free. Worth being deliberate about, since that's ~₹189 of discount plus ₹49 of absorbed shipping on one order.
3. **Exact dates for `LAUNCH10`** — 19–30 Sep assumed.

---

## 📮 Round 2 — asked after the 8 Sep email

### R1. Do we actually want Cash on Delivery at launch? 🔴

You confirmed COD earlier and the site currently advertises it — marquee, product pages, cart, FAQ. **But it has never been switched on in Shopify**, so it wouldn't appear at checkout anyway. Before enabling it, worth a genuine second look, because COD is not free:

**What it costs you**

- Shiprocket charges roughly **₹35–40 per COD order** on top of shipping
- COD orders are **returned undelivered far more often** than prepaid — and on an RTO you pay shipping *both ways* and get the stock back, often unsellable
- Cash is remitted on a **weekly cycle**, so your money is tied up longer than a prepaid order
- Refunds are slower and messier — bank transfer via Shiprocket rather than a straight reversal

**What it buys you**

- A large share of first-time Indian shoppers simply **will not prepay** an unfamiliar brand. For a launch with no reviews and no track record, COD is often the difference between a first order and no order.
- Removing it will cost conversions; the question is whether it costs more than the returns do.

**Three sensible options:**

| | What it means |
|---|---|
| **A. COD on, free** | Maximum conversion, you absorb ~₹35–40 plus the RTO risk on every COD order |
| **B. COD on, with a ₹30–50 fee** | Covers the cost and gently nudges people toward prepaying. Common for Indian D2C |
| **C. Prepaid only at launch** | Cleanest cash flow and no RTO losses, but loses first-time buyers who don't trust a new brand yet |

A fourth combination worth considering: **COD on, plus a small discount for prepaid** (e.g. ₹25 off) — that shifts behaviour without punishing anyone.

**Need:** which of these? It's a one-setting change either way, so it can wait for a proper answer rather than a quick one.

---

## 🔴 Blockers — needed before launch

### 1. GST rate — the only pricing item left

Prices are set and live: **₹699 / ₹599 / ₹599, GST-inclusive** (her 9 Sep decision).

**Still needed:** the GST **slab** her CA confirms — expected 10 Sep. Shopify currently assumes 18% (CGST 9% + SGST 9%). Also worth confirming whether **shipping charges** should carry GST; they currently don't.

The *inclusive* half is done and verified — see the banner at the top of this file. Only the rate is outstanding.

### 2. Shipping ✅ done — rate card still welcome

Tiers confirmed and live: **₹49** (1–3 packs) · **₹69** (4–6) · **₹99** (7+), plus **free shipping over ₹999**. Verified: a ₹699 cart still pays ₹49; a ₹1398 cart ships free.

Priyal will still send the real Shiprocket rate card so we can cross-check the tiers against her actual costs.

---

## 🟠 Waiting on you — accounts & assets

### 3. Payment gateway KYC ⚠️ most likely to move the launch date

Razorpay / Shopify Payments needs PAN, GST and bank details, and takes **2–5 business days** to approve. It's someone else's queue, not something we can speed up. **If this hasn't started, start it today.**

### 4. Shiprocket account + KYC ⚠️

Same shape of risk — **24–72 hours** to approve. Only you can do these:

- Create the Shiprocket account
- Submit KYC (PAN, GST, bank details, address proof)
- Load the shipping wallet with a starting balance

*(Full walkthrough in Part 3 below.)*

### 5. Product photography ⏳ shoot being arranged

Confirmed 9 Sep — pouch on a clean background, loose gummies, and a lifestyle shot per flavour. Send them over and we'll replace the illustrated placeholders and the social-share fallback in one pass.

### 6. Real customer reviews ✅ resolved — hidden until genuine

Priyal agreed on 9 Sep: no invented reviews. The section is **disabled** on the homepage; the sample content stays in the file so it can be switched back on in one line.

**To re-enable:** collect 5–10 genuine reviews from early testers, replace the sample blocks in the theme editor, turn off the "Sample" badge, and set `disabled` to false in `templates/index.json`.

### 7. Founder note ⏳ she's writing it

Confirmed 9 Sep — photo, name and a short personal line. The slot is built and stays hidden until filled.

Worth knowing: the brand book names her personal arc (lactose intolerance, becoming vegetarian, a period of anxiety and medication) as the emotional root of "wellness shouldn't feel clinical". **We deliberately did not publish any of that** — it's her medical history and hers to share or not. If she wants it in, this is the place.

### 8. Legal review of the policies

Three are now **live on the site** (Terms, Returns & Refunds, Shipping); Privacy is currently Shopify's auto-managed version. All written specifically for Nirmay, not templates — **but no lawyer has read them.** For a consumables business taking COD across India, that review is worth doing before launch.

### 9. NaN Jaune font licence

You confirmed you're buying the web licence. Send the files when you have them and we'll swap from the current Manrope fallback to the real brand typeface.

---

## 🟡 Decided on your behalf — confirm or overrule

Each was needed to keep building, and each is easy to change.

| # | Decision | Why | Note |
|---|---|---|---|
| 10 | **Pack size = 30 gummies** | Melatonin label says "Serving Per Container: 30"; your email said 15 | **Confirm before packaging goes to print** — it's your manufacturing spec |
| 11 | **Return window = 7 days** from delivery (48h for damaged/wrong items) | A refund policy can't publish without a number | Standard for Indian consumables |
| 12 | **One gummy per day** | Every nutrition label says "Serving Size: 1 Gummy"; site had said two | Corrected everywhere |
| 13 | **FSSAI line = manufacturer's licence** (Biovencer, 10017051002083) | Nirmay's own licence still pending | **Swap the moment yours arrives** |
| 14 | **"Free shipping over ₹699" removed** | Never confirmed, and contradicts weight-based pricing | Was in five places |
| 15 | **Delivery shown as 3–10 working days** | Your stated range | Checkout shows 5–8 business days, which sits inside it |

---

## 🔵 Worth a decision, not urgent

### 16. COD handling fee

*(Superseded by R1 above — kept for the numbers.)* Shiprocket charges ~₹35–40 per COD order, and COD orders are returned undelivered far more often than prepaid. Both costs land on your margin. Many Indian D2C brands add a ₹30–50 COD fee, or offer a small prepaid discount instead. Currently COD is free to the customer — fine to launch that way, just know it's a real cost.

### 17. Post-launch feature wishlist

You asked for reviews, WhatsApp support, loyalty and gift options.

- **Live now:** WhatsApp support (floating button + footer), review wall (needs real content)
- **Fast-follow, week after launch:** loyalty programme, gift options

Better to launch on time with a few things working well than to risk the date on all of them.

---

# PART 2 — On Mehal's plate

Things still to do, or that need doing in the Shopify admin.

## 🔴 Blocking launch

| # | Task | Where | Note |
|---|---|---|---|
| M1 | **COD — decide, then act** | Settings → Payments → Manual payment methods | ⏸ On hold pending Priyal (R1). The site advertises COD in four places; if the answer is no, that copy has to come out too |
| M2 | **Privacy policy** — decide auto vs ours | Admin → Policies → Privacy | Terms, Refund and Shipping are **published and live**. Privacy is still Shopify's auto-managed one; ours names the actual processors (Shiprocket, Klaviyo, analytics) |
| M3 | 🔴 **Publish the theme** | Online Store → Themes → GummyChums Build → ⋯ → Publish | Still `role: unpublished` — verified via `Shopify.theme`. The plain URL serves Horizon. Separately, the store password is still on (Online Store → Preferences → Restrict store access) |
| M4 | **Payment gateway setup** | Settings → Payments | Follows Priyal's KYC — she started it 9 Sep |
| M15 | **Discount codes** | Discounts | Drafted in R4 — awaiting Priyal's approval before creating |

## 🟡 Before launch

| # | Task | Where |
|---|---|---|
| M5 | **Require a phone number at checkout** — Indian couriers need one to attempt delivery | Settings → Checkout → Customer contact method |
| M6 | **Backup Region → India** (now selectable, since the US market was deleted) | Settings → General → Store defaults |
| M7 | **Abandoned checkout emails**, send after 1 hour | Settings → Checkout |
| M8 | **Order ID prefix `GC`** — makes Shiprocket support calls easier | Settings → General → Order ID |
| M9 | **GA4 + Meta Pixel** — fresh accounts, then integrate | Needs accounts created first |
| M10 | **Connect Klaviyo** to the store for the launch-day blast | Klaviyo dashboard |
| M11 | **Delete 2 Klaviyo test entries** (`waitlist.test@…`, `waitlist.test2@…`) — they'd receive the launch email | Klaviyo dashboard |
| M12 | **Real test order** end-to-end, then refund it | Password-protected paid store |
| M13 | **Point DNS** gummychums.com / .in from Vercel to Shopify | At launch only |

## ✅ Done

Site build (home, product, collection, cart, search, 404), launch reel section, review wall, certifications section, WhatsApp support, sticky mobile buy bar, Buy-it-now, payment trust chips, per-day pricing, favicon and social-share fallback, all four policies drafted, and the full India store configuration — shipping zone, tax region, currency format, weights, timezone, fulfillment location.

**Fixed along the way:** checkout rejected every Indian address (no India shipping zone); all text rendering at ~62% of intended size; two headings invisible against dark backgrounds; the hero gummy not covering tall screens; all collection gummies rendering one colour; four dead policy links; the "Rs. 399.00" price format; and a product description mangled into unreadable text.

---

# PART 3 — Shiprocket setup

_Written for someone who has never used it. Nothing here is irreversible._

## What it is

A **courier aggregator** — it doesn't deliver anything itself. It sits between the store and ~17 courier companies (Delhivery, Bluedart, Ekart, XpressBees…) and picks the cheapest or fastest for each order. One dashboard, one bill, one support line instead of five courier contracts.

**The flow once set up:** customer orders → order syncs to Shiprocket → you click "Ship Now", pick a courier, print the label → courier collects → tracking flows back into Shopify and the customer gets emails.

**Cost:** no monthly fee on the free plan. You pre-load a wallet and pay per shipment — roughly ₹25–40 per 500g surface, plus ~₹35–40 on each COD order.

## Steps

**1. Account** (Priyal) — shiprocket.in → Sign Up, using the business email and WhatsApp number. Free plan to start; paid tiers mainly buy cheaper rate slabs at volume, not a launch-week concern.

**2. KYC** (Priyal) — Settings → Company → KYC. Upload PAN (proprietor's), GST certificate, bank details (this is where COD money is remitted — double-check account number and IFSC), and address proof. **24–72 hours to approve.**

**3. Pickup address** — Settings → Company → Pickup Addresses → Add New. Use the Jaipur pickup address and nickname it something obvious like `Jaipur-Main`; that's the label you pick when creating shipments. Confirm couriers actually service the PIN code for pickup.

**4. Connect Shopify** (Mehal) — Shiprocket → Channels → Add New Channel → Shopify. Use the **real** store, not the dev store. Set order sync to automatic, sync **only paid orders**, and turn **auto-update tracking to Shopify ON** — that's what makes the customer's tracking link work.

**5. COD** — two separate switches. In **Shopify**: Settings → Payments → Manual payment methods → Cash on Delivery (item M1 above). In **Shiprocket**: enabled per shipment; they collect the cash and remit to your bank, typically weekly.

**6. Returns** — returns route entirely through Shiprocket, so there's no bank-detail form on the site. Settings → Return Settings: enable returns and set the window to match the site (currently 7 days). A return creates a reverse pickup; once inspected, refund from the Shopify order page.

## Pre-launch tests

On the real store while it's still password-protected:

- [ ] Place a real prepaid order with your own card
- [ ] Confirm it appears in Shiprocket within minutes
- [ ] Create the shipment, pick a courier, generate the label (cancel before pickup)
- [ ] Confirm the tracking number flows back into the Shopify order
- [ ] Confirm the customer email has a working tracking link
- [ ] Refund it in Shopify, confirm the refund email arrives
- [ ] Repeat once with **COD**
- [ ] Check the whole flow on a phone

## Things that bite people

**Wallet runs dry mid-day.** Labels can't be generated and orders silently pile up. Load a buffer before launch and set a low-balance alert.

**Weight discrepancies.** Shiprocket re-weighs at their hub and bills the difference weeks later. Weigh a finished, packed parcel — pouch plus box plus filler — not just the product.

**RTO (Return to Origin).** Undelivered orders come back and you pay both legs. COD returns far more often than prepaid. Watch this in month one; a high rate is the argument for a COD fee.

**Serviceability gaps.** Not every PIN code is deliverable, and COD serviceability is narrower than prepaid. Spot-check a few remote codes so you know what to tell a customer who asks.

**Dev store vs real store.** Reconnect the channel against the real domain before launch.

---

## Quick reference

| Thing | Value |
|---|---|
| Business | Nirmay (sole proprietorship, Priyal Ojha) |
| Pickup PIN | 302019 (Jaipur, Rajasthan) |
| Support email | nirmay.co.in@gmail.com |
| WhatsApp | +91 73000 39307 |
| Per-pouch weight | 0.15 kg |
| Pack size | 30 gummies |
| Manufacturer | Biovencer Healthcare Pvt Ltd · FSSAI 10017051002083 |
| Delivery promise | 3–10 working days, pan-India |
| Return window | 7 days (pending confirmation) |
| Preview link | `?preview_theme_id=165560844500` |

---

## ✅ Decision log

| Date | Decision | Who |
|---|---|---|
| 7 Sep 2026 | Launch moved 14 → **19 Sep** | Priyal |
| 7 Sep 2026 | Returns route entirely through **Shiprocket** — no bank-detail form on the site | Mehal |
| 7 Sep 2026 | Pack size **30** (pending confirm — item 10) | Mehal |
| 7 Sep 2026 | COD **enabled** pan-India | Priyal |
| 8 Sep 2026 | COD **re-opened as a question** (R1) — never switched on in Shopify; Mehal wants the cost weighed first | Mehal |
| 7 Sep 2026 | Delivery **3–10 working days**, pan-India only | Priyal |
| 7 Sep 2026 | Buying the real **NaN Jaune** licence | Priyal |
| 7 Sep 2026 | Analytics: fresh **GA4 + Meta Pixel** | Priyal |
| 7 Sep 2026 | Add **WhatsApp** (7300039307) alongside Instagram | Priyal |
| 8 Sep 2026 | Return window **7 days** — publish now, confirm later | Mehal |
| 8 Sep 2026 | India shipping zone created, US zone/market/location removed — **checkout unblocked and verified** | Mehal |
| 8 Sep 2026 | Checkout transit time **5–8 business days** (only 3–5 or 5–8 offered; 5–8 sits inside the site's 3–10) | Mehal |
| 8 Sep 2026 | Launch reel added to the homepage as a video section | Mehal |
| 8 Sep 2026 | Review wall built with **sample content, badged** until real reviews exist | Mehal |
| 9 Sep 2026 | Prices **₹699 Melatonin · ₹599 Brain Booster · ₹599 Eye Care**, GST-inclusive | Priyal |
| 9 Sep 2026 | Shipping tiers **₹49/₹69/₹99 confirmed**; free shipping at **₹999** (not ₹699 — a single Melatonin shouldn't qualify) | Priyal |
| 9 Sep 2026 | Reviews **hidden until genuine** — no invented testimonials | Priyal |
| 9 Sep 2026 | Both KYCs started | Priyal |
| 9 Sep 2026 | Planned promos: 10% launch · up to 15% campaigns · 5% first-time welcome · bundles later | Priyal |
