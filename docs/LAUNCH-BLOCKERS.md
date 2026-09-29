# Launch blockers — GummyChums

Live theme: `GummyChums v2 (rebrand)` #166241829076. Store is password-gated, so
nothing below is public yet. Each item says who it needs.

---

## 1. Product photography — PRIYAL
All three products have **no image** (`img=NO` on Brain Booster, Eye Care,
Melatonin). Consequences while that is true:

- Product pages have no photo.
- The Chum cards fall back to the figurine illustrations.
- Shared links use the generic brand card, not the product.

Mehal is waiting on the founder to send them. Once they land, upload in
Shopify admin → Products → each product → Media. Nothing needs re-coding;
the theme already prefers the real photo wherever one exists.

## 2. Store plan — MEHAL
The Admin API reports `plan_name: basic`, `plan_display_name: "Basic App
Development"`, `checkout_api_supported: false`. That pattern is what a partner
**development store** looks like, and a development store cannot take real
payments until it is transferred to a paid plan.

Check Settings → Plan. If it is a development store, this blocks everything
else — the site can look finished and still be unable to take an order.

## 3. Payment claims — DONE, pending reinstatement
Every claim naming a payment method has been removed from the storefront
(marquee, cart, product page, FAQ). "Secure checkout" is kept, since that is
true regardless.

Restore the specific methods only once Priyal confirms what is actually enabled
at Settings → Payments. The removed blocks are in git at the commit that
removed them, and `gc-product.liquid` carries a comment pointing here.

## 4. Invented reviews — NEEDS A DECISION
`sections/gc-reviews.liquid` ships six default testimonials with names
(Ananya, Rohan, Meera, Kabir, Ishita, Aditya) and the section is on the live
homepage. The store has zero orders, so these are fabricated.

This is the same problem as the payment claims: the site stating something that
is not true. In India it also falls under the CCPA guidelines on fake reviews.

Options: remove the section until real reviews exist; keep it and leave it
empty; or replace with something honest ("be our first Chum"). Needs Mehal or
Priyal to choose — it is brand content, not a bug.

## 5. Cookie consent — MEHAL (admin only)
No banner is active. Enable at Settings → Customer privacy → Cookie banner.
Cannot be done from the theme: Shopify's banner is the one that integrates with
the Customer Privacy API and actually gates tracking. There is also an
unpublished "Your Privacy Choices" page that should be published alongside it.

Relevant because you sell into India under the DPDP Act.

## 6. Admin API token — MEHAL (admin only)
The custom app's token has **15 scopes, 7 of them writes** (`write_orders`,
`write_discounts`, `write_inventory`, `write_products`, …) and `read_orders` /
`read_all_orders`. Nothing in the repo uses it except ad-hoc introspection.

`read_customers` is correctly denied, but `/orders.json` returns 200 — so it
reads customer names, emails, phones and addresses through order records the
moment a sale happens.

Reduce to reads only, and add `read_script_tags` so app-injected JavaScript can
be audited. Changing scopes forces a reinstall and issues a new token.

## 7. Analytics — MEHAL
A GA4 Measurement ID field now exists in the theme editor under "Analytics".
Blank means no third-party script loads at all. Paste the ID when ready — no
code change needed. Do it after the cookie banner, not before.

---

_Kept current by Claude. Last updated 29 Sep 2026._
