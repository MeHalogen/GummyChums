# Notes to Priyal — open decisions & running log

_The single place where every decision that needs Priyal lives. Add to the top of each section as things come up; move items to **Logged decisions** at the bottom once she answers, with the date._

**Launch: 19 Sep 2026** · Last updated: 8 Sep 2026

---

## Where things stand

The store is **built and working**. All three products are live with real ingredient and nutrition information from your labels, the certifications are on the site, the policies are drafted, and — as of today — **checkout works for Indian customers**.

What's left is mostly **information from you** rather than build work. The three things below marked 🔴 are what we genuinely can't finish without you.

**Done and working:**

- Homepage, product pages, story, FAQ, footer — full site, mobile and desktop
- All 3 products live: real ingredients, nutrition per gummy, 30-gummy pack size
- Certifications section built from your GMP / FSSC 22000 / FSSAI documents
- Cash on Delivery, WhatsApp support, shipping and returns information
- Privacy, Terms, Returns & Refunds and Shipping policies — drafted, pending legal review
- Store configured for India: currency, timezone, weights, shipping zone, tax region

---

## 🔴 Blockers — needed before launch

### 1. Shipping rates — provisional, needs your rate card

**Checkout is now working.** The store had no India shipping zone at all, so Shopify was rejecting every Indian address. That's fixed and verified.

Customers currently pay, by cart weight (each pouch is 0.15 kg):

| Cart weight | Customer pays | Roughly |
|---|---|---|
| 0 – 0.5 kg | ₹49 | 1–3 packs |
| 0.5 – 1 kg | ₹69 | 4–6 packs |
| 1 kg + | ₹99 | 7+ packs |

**These numbers are our estimate, not yours.** They approximate Shiprocket's surface pricing so margin roughly holds. **What we need:** your actual Shiprocket rate card, or a decision to keep these. Changing them takes about a minute.

Also worth deciding: a **free-shipping threshold** (e.g. free over ₹699) lifts average order value, but you'd absorb the courier cost on those orders. Currently not offered.

### 2. GST rate for the products

The store has **no India tax region configured** — only United States, left over from the dev-store template. GST isn't being calculated or recorded on any order, which matters for your filings since Nirmay is GST-registered.

The product pages say **"Inclusive of all taxes"**, so the store needs to treat ₹399 as GST-inclusive and back-calculate the tax, rather than adding it on top at checkout.

**What we need:** the **GST rate** that applies to these products, confirmed with your CA. Nutraceuticals and food supplements sit in different slabs depending on classification, and this affects your returns — not something we should guess at. Setup steps are ready in `docs/INDIA-STORE-SETTINGS.md`; we just need the number.

---

### 3. Product prices

All three products currently sit at **₹399** on the live preview. That number was placeholder test data from the original store setup — **not a price anyone chose**. It's now showing publicly on the preview link and drives the "≈ ₹13/day" line on every product card.

**What we need:** the real price for each of the three SKUs. If they differ per product, all the better — the site handles it automatically.

---

## 🟡 Decisions made on your behalf — please confirm or overrule

These were needed to keep building. Each is a reasonable default, and each is easy to change.

### 4. Pack size = 30 gummies

Your email said 15, but the Melatonin nutrition label PDF says "Serving Per Container: 30", and all three labels say one gummy per day. We went with **30** and it's now on the site and in the product descriptions.

**Confirm before packaging goes to print** — this is your manufacturing spec, not ours.

### 5. Return window = 7 days from delivery

You said you'd get back to us on this. A refund policy can't be published without a number, so we drafted **7 days** (with 48 hours for damaged/wrong items, matching the courier's claim window). Standard for Indian consumables.

### 6. Dosage copy = one gummy per day

The site briefly said "two gummies a day". Every nutrition label says "Serving Size: 1 Gummy", so we corrected it everywhere.

### 7. FSSAI line = manufacturer's licence

Nirmay's own FSSAI licence is still pending, so the footer currently cites Biovencer's (10017051002083) with the manufacturer's name and address, as required. **Swap to Nirmay's licence the moment it comes through.**

### 8. Shipping claims removed

The site previously said "Free shipping over ₹699" in five places. That was never confirmed and contradicts weight-based pricing, so it's gone. If you *do* want a free-shipping threshold, that's the second question in item 1.

---

## 🟠 Waiting on you — assets & access

### 9. Product photography

Still using illustrated gummy graphics as placeholders. They look good, but real product shots convert better and are the single biggest visual upgrade left. Ideally: pouch on a clean background, a loose-gummy shot, and one lifestyle/in-hand shot per flavour.

### 10. Founder note for the story section

The "Why we exist" section is currently text only. There's a slot ready for a **photo + one-line quote + your name** — it stays hidden until you fill it. Readers trust a face; this is a small thing that punches above its weight.

Something in your own words about why you started Nirmay is all it needs.

### 11. Shiprocket account + KYC

Full walkthrough is in `docs/SHIPROCKET-SETUP.md`. The parts only you can do:

- Create the Shiprocket account
- Submit KYC (PAN, GST, bank details, address proof) — **takes 24–72 hours to approve**
- Load the shipping wallet with a starting balance

**Start the KYC now.** Like the payment gateway, this is someone else's approval queue and it's the kind of thing that quietly eats a launch date.

### 12. Payment gateway KYC

Same shape of risk — Razorpay/Shopify Payments needs PAN, GST and bank details and takes 2–5 business days. **If this isn't already started, it's the most likely thing to move the 19th.**

### 13. Legal review of the policies

Four policies are drafted from your real business details (Privacy, Terms, Returns & Refunds, Shipping) and are ready to publish. They're solid drafts written specifically for Nirmay — not templates — **but they haven't been reviewed by a lawyer.** For a consumables business taking COD across India, that review is worth doing before launch.

---

## 🔵 Worth a decision, not urgent

### 14. COD handling fee

Shiprocket charges roughly ₹35–40 per COD order, and COD orders are returned undelivered far more often than prepaid ones. Both costs land on your margin. Many Indian D2C brands add a ₹30–50 COD fee, or offer a small prepaid discount instead.

Currently COD is free to the customer. Fine to launch that way — just know it's a real cost.

### 15. NaN Jaune font licence

You confirmed you're buying the web licence. Once you have the files, send them over and we'll swap the site from the current Manrope fallback to the real brand typeface.

### 16. Post-launch feature wishlist

You asked for reviews, WhatsApp support, loyalty and gift options. Realistic sequencing:

- **Launch-feasible:** WhatsApp support (✅ already live — floating button and footer link), product reviews
- **Fast-follow, week after launch:** loyalty programme, gift options

Better to launch on time with four things working well than to risk the date on eight.

---

## ✅ Logged decisions

| Date | Decision | Who |
|---|---|---|
| 7 Sep 2026 | Launch moved 14 → **19 Sep** | Priyal |
| 7 Sep 2026 | Returns/refunds route entirely through **Shiprocket** — no bank-detail form on the site | Mehal |
| 7 Sep 2026 | Pack size **30** (pending Priyal's confirm — item 4) | Mehal |
| 7 Sep 2026 | COD **enabled** pan-India | Priyal |
| 7 Sep 2026 | Delivery promise **3–10 working days**, pan-India only | Priyal |
| 7 Sep 2026 | Font: buying the real **NaN Jaune** licence, not swapping to a free alternative | Priyal |
| 7 Sep 2026 | Analytics: fresh **GA4 + Meta Pixel** | Priyal |
| 7 Sep 2026 | Add **WhatsApp** (7300039307) alongside Instagram | Priyal |
| 8 Sep 2026 | Return window **7 days** — publish now, confirm later | Mehal |
| 8 Sep 2026 | India shipping zone created, US zone/market/location removed — **checkout unblocked and verified** (₹49/₹69/₹99 by weight) | Mehal |

---

## 📋 Work log

### 8 Sep 2026 — Store set up for India (checkout fixed)

**We found and fixed a problem that would have stopped the store taking orders on launch day.**

The Shopify store was originally created from a template configured for the United States, and several of those settings were still in place. Most seriously, **India had never been added as a place the store ships to** — so when an Indian customer reached checkout and entered their address, Shopify rejected it outright. No order could have been completed.

This wasn't visible from browsing the site; everything looked normal until you actually tried to pay. We caught it while setting up shipping.

Fixed today:

| What | Was | Now |
|---|---|---|
| Ships to | United States only | **India** |
| Shipping rates | US dollars | **₹49 / ₹69 / ₹99** by weight |
| Ships from | A US address | **Your Jaipur address** |
| Order timestamps | New York time | **India time (IST)** |
| Product weights | Pounds | **Kilograms** |
| Store phone | Missing | **+91 73000 39307** |

**Tested and confirmed working** — a Jaipur delivery address now returns a correct shipping charge at every order size, from a single pouch to a bulk order.

Also completed this week: fixed the dosage information to match your labels (one gummy per day), removed shipping claims that weren't accurate, added the certifications section from your GMP/FSSC/FSSAI documents, added WhatsApp support, and drafted all four store policies.

**What we need from you next** — the three 🔴 items at the top of this document, plus starting the two KYC processes (payment gateway and Shiprocket), which take several days to approve and are the most likely thing to delay the launch date.
