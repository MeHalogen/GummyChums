# Make the store correct for Indian customers — exact steps

_The store was created from a Shopify dev-store template and still carries **US defaults** in six places. One of them blocks checkout completely. None of these are in the theme — they're all Shopify admin settings, and four of them cannot be changed by any API, only by hand._

**Time needed: ~15 minutes.** Do them in this order.

---

## What's wrong (audited 8 Sep 2026)

| # | Setting | Currently | Should be | If left alone |
|---|---|---|---|---|
| 1 | Shipping zone | United States, USD rates | India, INR rates | 🔴 **No Indian customer can check out** |
| 2 | Tax region | United States only | India (GST) | GST not calculated or recorded |
| 3 | Currency format | `Rs. {{amount}}` | `₹{{amount_no_decimals}}` | Checkout + emails show "Rs. 399.00" |
| 4 | Weight unit | **lb** | **kg** | Wrong unit on every new product |
| 5 | Timezone | America/New_York | Asia/Kolkata | Order times off by ~10.5 hours |
| 6 | Store phone | empty | +91 73000 39307 | Missing from invoices & notifications |

> The theme already forces ₹ on the storefront, so the site *looks* right. But **checkout, order confirmation emails, invoices and admin reports all use these store settings** — the theme can't reach them. That's why this matters.

---

## 1. Shipping zone 🔴 THE BLOCKER

**Right now Shopify rejects every Indian address at checkout** with `Country/region not supported`. Verified live. Nothing else on this list matters until this is fixed.

**Settings → Shipping and delivery → General shipping rates → Manage**

1. Find the existing **"Domestic"** zone (it contains United States). Click **⋯ → Delete zone**.
2. **Create zone** → name it `India` → search and tick **India** → Done.
3. Inside the India zone, **Add rate** → **Set up your own rates**:
   - Name: `Standard Delivery (3–10 working days)`
   - Price: `49`
   - Click **Add conditions → Based on item weight** → `0` kg to `0.5` kg
   - Save
4. **Add rate** again: same name, price `69`, weight `0.5` kg to `1` kg
5. **Add rate** once more: same name, price `99`, weight `1` kg and up

Each pouch is 0.15 kg, so a 1–3 pack order lands in the ₹49 band.

> ⚠️ **These rate numbers are provisional.** They approximate Shiprocket's surface pricing so margin roughly holds, but Priyal hasn't given her actual rate card yet — that's blocker #1 in `NOTES-TO-PRIYAL.md`. Set these now to unblock checkout; adjust the three numbers when she answers. Changing them later takes 30 seconds.

**Verify:** add something to cart, start checkout, enter a Jaipur address (PIN 302019). You should see the ₹49 rate, not an error.

---

## 2. GST / taxes

**Settings → Taxes and duties**

Only United States is configured. Add India:

1. Under **Countries/regions**, click **India** (or add it if not listed)
2. Set the GST rate that applies to your products

**Two things to get right, and they interact:**

- **Priyal is GST-registered** (GST number was provided for KYC), so GST must be collected and recorded properly for her filings.
- The product pages say **"Inclusive of all taxes"** — the standard for Indian packaged goods, where MRP includes GST. For that to be true, tick:

  **Settings → Taxes and duties → "All prices include tax"** ✅

  With this on, Shopify treats ₹399 as GST-inclusive and back-calculates the tax component rather than adding it on top. Leave it off and a customer would be charged ₹399 **plus** GST at checkout — which contradicts the page and reads as a bait-and-switch.

> **Confirm the actual GST rate with Priyal's CA before entering it.** Nutraceuticals and food supplements fall into different slabs depending on classification, and picking the wrong one creates a filing problem, not just a display one. This is the one item on this page I'd not guess at.

---

## 3. Currency format

**Settings → General → Store defaults → Currency** → click **Change formatting**

Replace all four fields:

| Field | Value |
|---|---|
| HTML with currency | `₹{{amount_no_decimals}} INR` |
| HTML without currency | `₹{{amount_no_decimals}}` |
| Email with currency | `₹{{amount_no_decimals}} INR` |
| Email without currency | `₹{{amount_no_decimals}}` |

`amount_no_decimals` gives `₹399` instead of `₹399.00`, which is how Indian stores price. If you ever need paise shown, use `{{amount}}` instead.

---

## 4. Weight unit

**Settings → General → Store defaults → Unit system**

- Unit system: **Metric**
- Default weight unit: **kg**

The three existing products already carry correct 0.15 kg weights, so nothing needs re-entering. This just stops new products defaulting to pounds — which would silently break the weight-based shipping rates from step 1.

---

## 5. Timezone

**Settings → General → Store defaults → Timezone**

Set to **(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi**.

Currently New York, so every order timestamp is ~10.5 hours out. That makes "orders today" wrong, throws off daily reports, and would misfire any scheduled discount or launch-timed campaign.

---

## 6. Store phone

**Settings → General → Store details**

Add `+91 73000 39307`. It appears on invoices and some customer notifications, and couriers ask for it.

---

## Also worth doing for Indian customers

These aren't broken, just worth setting deliberately.

**Checkout — require a phone number.**
Settings → Checkout → Customer contact method → **Phone number required** (or ask for both email and phone).
Indian courier partners need a phone number to attempt delivery; an address alone often isn't enough. This single setting prevents a meaningful share of failed deliveries.

**Enable Cash on Delivery.**
Settings → Payments → Manual payment methods → **Cash on Delivery (COD)**.
The site advertises COD in the marquee, on product pages and in the FAQ — but it won't appear at checkout until this is switched on.

**Abandoned checkout emails.**
Settings → Checkout → Abandoned checkouts → send after **1 hour**.
Cheapest recovered revenue available; it's off by default.

**Order ID prefix.**
Settings → General → Order ID → prefix `GC`.
Orders read `GC1001` instead of `#1001` — easier when talking to Shiprocket support about a specific order.

---

## Final check once you're done

- [ ] Add to cart → checkout with a **Jaipur address (302019)** → shipping shows **₹49**, no error
- [ ] Price at checkout reads **₹399**, not "Rs. 399.00"
- [ ] **COD** appears as a payment option
- [ ] Checkout asks for a **phone number**
- [ ] Place a test order → the timestamp in Admin matches **IST**
- [ ] Order confirmation email shows **₹** and the right total
- [ ] Repeat the whole thing **on a phone**

---

## Why I couldn't do these for you

The shipping zone (#1) is scriptable and the script is ready — but applying it trips this session's safety check on store-settings changes, so it needs a permission rule or your hand on the wheel.

Items #2–#6 aren't scriptable at all. Shopify's Shop resource is **read-only** over the Admin API — a write returns `HTTP 406` (I tested it). Currency format, weight unit, timezone and tax configuration have no API mutation in any version. Any tool claiming otherwise is changing something else.
