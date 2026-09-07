# Shiprocket + Shopify — step-by-step setup

_Written for someone who has never touched Shiprocket. Follow it top to bottom. Nothing here is irreversible; you can change every setting later._

## What Shiprocket actually is (30 seconds)

Shiprocket is a **courier aggregator**. It doesn't deliver anything itself — it sits between your store and ~17 courier companies (Delhivery, Bluedart, Ekart, XpressBees…) and picks the cheapest/fastest one for each order. You get one dashboard, one bill, one support line instead of contracts with five couriers.

**The flow, once set up:**

1. Customer orders on your Shopify store
2. The order syncs into Shiprocket automatically
3. You click "Ship Now" → pick a courier → print the label
4. Courier picks up from your address
5. Tracking updates flow back into Shopify, and the customer gets emails

**What it costs:** no monthly fee on the free plan. You pay per shipment, deducted from a wallet you pre-load. Rates start around ₹25–40 per 500g for surface delivery, plus a COD fee (~₹35–40 or 1.5% of order value, whichever is higher) on COD orders.

---

## Who does what

Some of this needs **Priyal** (it's her business identity and bank account). Some is yours.

| Step | Who | Why |
|---|---|---|
| Create Shiprocket account | **Priyal** | Tied to her business + bank |
| Submit KYC | **Priyal** | Needs her PAN / GST / bank |
| Add pickup address | Either | Just an address form |
| Connect Shopify ↔ Shiprocket | **You** | Needs Shopify admin |
| Configure Shopify shipping rates | **You** (done — see below) | Store settings |
| Load wallet money | **Priyal** | Her card/UPI |
| Test order end-to-end | **You** | Pre-launch QA |

> ⚠️ **Start Priyal's KYC now.** It takes 24–72 hours to approve and you cannot ship a single real order until it clears. This is the same class of risk as the payment-gateway KYC — it's someone else's queue, not your code.

---

## Step 1 — Create the account (Priyal)

1. Go to **shiprocket.in** → **Sign Up**
2. Use the business email (`nirmay.co.in@gmail.com`) and the WhatsApp number (7300039307)
3. Choose the **free plan** to start. You can upgrade later; the paid tiers mainly buy cheaper rate slabs at volume, which is not a launch-week concern.

## Step 2 — KYC (Priyal)

In **Settings → Company → KYC**, upload:

- **PAN card** (proprietor's, since Nirmay is a sole proprietorship)
- **GST certificate**
- **Bank account details** — this is where COD money gets remitted, so double-check the account number and IFSC
- **Address proof** for the pickup location

Approval is typically 24–72 hours. You'll get an email.

## Step 3 — Pickup address

**Settings → Company → Pickup Addresses → Add New**

Use the Jaipur business address:

```
Nirmay
Sodala Police Station, Hawa Sadak Road
Ramnagar Extension, Civil Lines
Jaipur, Rajasthan 302019
Phone: 7300039307
```

Nickname it something obvious like `Jaipur-Main` — this is the label you pick when creating shipments.

**Verify serviceability:** Shiprocket will confirm couriers actually do pickups from that PIN code (302019 is a Jaipur metro PIN, so this should be fine). If pickup isn't available, you'd have to drop parcels at a courier hub — worth knowing before launch, not after.

## Step 4 — Connect Shopify (you)

1. In Shiprocket: **Channels → Add New Channel → Shopify**
2. Enter the store URL: `gummychums.myshopify.com` (use the **real** store, not the dev store, when you do this for production)
3. Approve the app install on the Shopify side
4. Set **order sync** to automatic

**Settings that matter:**

- **Sync only Paid orders** — otherwise abandoned/pending orders clutter the queue
- **Auto-update tracking to Shopify: ON** — this is what makes the customer's tracking link work
- **Order tags:** leave default

## Step 5 — Shopify shipping rates (you)

⚠️ **This is separate from Shiprocket and easy to miss.** Shiprocket charges *you*; Shopify charges *your customer*. They are two different numbers and Shiprocket does not automatically set what the customer pays at checkout.

The dev store shipped with a **United States** zone and USD rates — a leftover default that would have blocked Indian checkout entirely. The replacement is an **India** zone with weight-based rates:

| Cart weight | Customer pays | Roughly |
|---|---|---|
| 0 – 0.5 kg | ₹49 | 1–3 pouches |
| 0.5 – 1 kg | ₹69 | 4–6 pouches |
| 1 kg + | ₹99 | 7+ pouches |

Each pouch is set to **0.15 kg** in Shopify, so these bands work out automatically.

> **These rate numbers still need Priyal's confirmation.** They approximate Shiprocket's surface rates, but she may want to absorb shipping into the product price, offer free shipping over a threshold, or charge differently for metro vs non-metro. Once she has her actual rate card, adjust in **Shopify Admin → Settings → Shipping and delivery**.

## Step 6 — Cash on Delivery

Two separate switches:

**In Shopify** — Settings → Payments → Manual payment methods → **Cash on Delivery (COD)**. This is what shows COD at checkout.

**In Shiprocket** — COD is enabled per-shipment when you create it. Shiprocket collects the cash from the customer and remits it to the bank account from Step 2, typically on a weekly cycle (faster on paid plans).

**Consider a COD fee.** Shiprocket charges you ~₹35–40 per COD order, and COD has a much higher return-to-origin rate than prepaid. Many Indian D2C stores add a ₹30–50 COD handling fee to offset this, or offer a small discount for prepaid instead. Worth raising with Priyal — right now COD is free to the customer and that cost lands entirely on her margin.

## Step 7 — Returns

Priyal decided returns route **entirely through Shiprocket**, so there is no bank-detail form on the site to build or maintain.

In Shiprocket: **Settings → Return Settings** — enable returns and set the window to match the site's policy (currently drafted as **7 days**; confirm with Priyal).

When a customer requests a return, you create a **Return Order** in Shiprocket, which schedules a reverse pickup. Once the parcel is back and inspected, you refund from the Shopify order page.

## Step 8 — Test before launch

Do this on the **real store while it's still password-protected**:

- [ ] Place a real order (prepaid) with your own card
- [ ] Confirm it appears in Shiprocket within a few minutes
- [ ] Create the shipment, pick a courier, generate the label (you can cancel before pickup)
- [ ] Confirm the tracking number flows back into the Shopify order
- [ ] Confirm the customer email contains a working tracking link
- [ ] Refund the order in Shopify and confirm the refund email arrives
- [ ] Repeat once with **COD** to confirm that path works too
- [ ] Check the whole flow on a phone

---

## Things that bite people

**Wallet runs dry mid-day.** Shiprocket deducts per shipment from a pre-loaded wallet. If it hits zero, you cannot generate labels and orders silently pile up. Load a buffer before launch day and set a low-balance alert.

**Weight discrepancies.** Shiprocket re-weighs parcels at their hub. If your declared weight is lower than actual, they bill the difference and it appears as a surprise deduction weeks later. Weigh a finished, packed parcel — pouch plus box plus filler — and use that real number, not the product weight alone.

**RTO (Return to Origin).** Undelivered orders come back to you and you pay both legs of shipping. COD orders RTO far more often than prepaid. Watch this rate in the first month; if it's high, that's the argument for a COD fee or prepaid discount.

**Serviceability gaps.** Not every PIN code is deliverable, and COD serviceability is narrower than prepaid. Shiprocket has a PIN-code checker — worth spot-checking a few remote codes so you know what to tell a customer who asks.

**The dev store vs the real store.** Everything above should ultimately point at the **paid production store**. Connecting Shiprocket to the dev store is fine for a dry run, but remember to redo the channel connection against the real domain before launch.

---

## Quick reference

| Thing | Value |
|---|---|
| Business | Nirmay (sole proprietorship, Priyal Ojha) |
| Pickup PIN | 302019 (Jaipur, Rajasthan) |
| Support email | nirmay.co.in@gmail.com |
| WhatsApp | +91 73000 39307 |
| Per-pouch weight | 0.15 kg |
| Delivery promise on site | 3–10 working days, pan-India |
| Return window on site | 7 days (⚠️ pending Priyal's confirmation) |
