# Making the new store match the old one

Everything here was exported from the old store (`gummychums-k3kwkntm`) today.
Products are already done. These are the remaining pieces.

---

## 1. Pages — Content → Pages → Add page

The handles must match exactly; the theme and nav link to them.

| Title | Handle | Body |
|---|---|---|
| Our Story | `story` | **leave empty** — the content comes from the theme template |
| Contact | `contact` | **leave empty** — same |
| Your Privacy Choices | `data-sharing-opt-out` | paste `pages/data-sharing-opt-out.html` |

Shopify builds the handle from the title, so "Our Story" gives `our-story` — **edit
the handle by hand to `story`** or the nav breaks.

---

## 2. Policies — Settings → Policies

Paste each file in. Use the HTML/source view so the markup survives.

| Policy | File |
|---|---|
| Refund policy | `policies/refund-policy.html` |
| Privacy policy | `policies/privacy-policy.html` |
| Terms of service | `policies/terms-of-service.html` |
| Shipping policy | `policies/shipping-policy.html` |

The privacy policy is the long one (18k chars) and names the real processors —
Shiprocket, Klaviyo, analytics. Do not let Shopify's auto-generated one replace it.

---

## 3. Navigation — Content → Menus → Main menu

The theme links to these. Two items only:

- **Shop** → `/collections/all`
- **Story** → `/pages/story`

Footer menus are rendered by the theme itself, not by Shopify menus, so there is
nothing to rebuild there.

---

## 4. Still outstanding

- **Product photos** — all three have `images=0`. Biggest remaining gap.
- **Razorpay** — in review. Until it clears there is no way to take money.
- **Cookie banner** — Settings → Customer privacy (DPDP Act).
- **FSSAI licence number on invoices** — Settings → Notifications.
- **Footer certificate logos** — Theme editor → Footer → Affiliated certificates.
