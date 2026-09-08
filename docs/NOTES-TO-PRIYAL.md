# Notes & open questions — GummyChums

_The single parked list. Everything not-yet-done lives here: questions for Priyal, decisions taken on her behalf, and the tasks still on Mehal's plate. Nothing else should hold a to-do list._

**Launch: 19 Sep 2026** · Last updated: 8 Sep 2026

---

# PART 1 — For Priyal

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

### 1. Prices and GST — one decision, not two

All three products sit at **₹399**, which was placeholder test data from the original store setup — not a price anyone chose.

**The real question isn't "what's the price", it's "is that what the customer pays, or what you keep?"** Those give very different numbers, because GST has to come from somewhere.

Shopify has GST at **18%** (CGST 9% + SGST 9%), applied automatically when the India market was created. Right now it's set to **add** tax on top of the listed price, so a live checkout today looks like this:

> Melatonin Gummies ₹399 · Shipping ₹49 · **Estimated taxes ₹71.82** · **Total ₹519.82**

That contradicts the product page, which says **"Inclusive of all taxes"** — the customer sees ₹399 and is charged ₹470.82 for the gummies. That has to change before launch.

**Three ways it can work.** One pouch, delivered, at the ₹49 shipping tier:

| | Listed | GST | Shipping | **Customer pays** | **You keep** (per pouch) |
|---|---|---|---|---|---|
| **A. Price includes GST** *(recommended)* | ₹399 | ₹60.86 *(inside)* | ₹49 | **₹448** | **₹338.14** |
| **B. GST added on top** *(current — contradicts the site)* | ₹399 | ₹71.82 *(added)* | ₹49 | **₹519.82** | ₹399.00 |
| **C. Includes GST, priced to keep ~₹399** | ₹470 | ₹71.69 *(inside)* | ₹49 | **₹519** | ₹398.31 |

**A** is the Indian norm — MRP on packaged goods is tax-inclusive, and it's what the site already promises. But note it takes **₹60.86 per pouch** out of what you keep versus the ₹399 you may have had in mind.

**C** is A with the maths done backwards: if ₹399 is what you want to *keep*, the listed price needs to be about **₹470** (₹499 would keep ₹422.88).

**B** is where the store sits today. It's legal, but showing ₹399 and charging ₹470.82 reads as a bait-and-switch and will cost you conversions.

**Need from you:**
1. **Should the listed price include GST, or be added at checkout?** (We recommend included.)
2. **What should each of the three products be listed at** — and is that number what the customer pays, or what you keep?
3. **Is 18% the right GST slab?** Please confirm with your CA — Shopify assumed it. Nutraceuticals and food supplements fall into different slabs by classification, and a wrong rate is a filing problem, not just a display one. Also worth asking whether **shipping charges** should be taxed (currently they aren't).

### 2. Shipping rates — provisional

Checkout now works. Customers currently pay, by cart weight (each pouch is 0.15 kg):

| Cart weight | Customer pays | Roughly |
|---|---|---|
| 0 – 0.5 kg | ₹49 | 1–3 packs |
| 0.5 – 1 kg | ₹69 | 4–6 packs |
| 1 kg + | ₹99 | 7+ packs |

**These are our estimates, not yours** — they approximate Shiprocket's surface pricing so margin roughly holds.

**Need:** your actual Shiprocket rate card, or a decision to keep these. Also worth deciding: a **free-shipping threshold** (e.g. free over ₹699) lifts average order value, but you'd absorb the courier cost on those orders. Currently not offered.

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

### 5. Product photography

Still using illustrated gummy graphics. They look good, but real photos convert better and are the biggest visual upgrade left. Ideally per flavour: pouch on a clean background, a loose-gummy shot, and one lifestyle/in-hand shot.

This also fixes social sharing — with no product photos, WhatsApp and Instagram shares currently fall back to the wordmark.

### 6. Real customer reviews

The homepage now has a review wall, currently filled with **placeholder text, every card stamped "SAMPLE"**.

⚠️ **These cannot go live as-is.** Publishing invented reviews as real customer feedback is deceptive and breaches Indian consumer-review rules (BIS IS 19000). The badges are deliberately loud so this can't ship unnoticed.

**Options:** collect genuine reviews from early testers before launch; or launch with the section removed and add it once real reviews arrive. Either is fine — inventing them is not.

### 7. Founder note

The "Why we exist" section is text only. There's a slot ready for a **photo + one-line quote + your name** — it stays hidden until filled. Readers trust a face. Something in your own words about why you started Nirmay is all it needs.

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
| M3 | **Publish the theme** | Online Store → Themes → GummyChums Build → Publish | Still a draft, so "View Online Store" shows Dawn's Horizon theme |
| M4 | **Payment gateway setup** | Settings → Payments | Follows Priyal's KYC (item 3) |

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
