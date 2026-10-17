/** Every page a customer can reach, with what must be true of each. */
export const ROUTES = [
  { path: '/',                           name: 'home',        must: /Chums/i },
  { path: '/collections/all',            name: 'catalogue',   must: /gumm/i },
  { path: '/products/brain-booster-gummies', name: 'product-brain', must: /Brain Booster/i },
  { path: '/products/melatonin-gummies', name: 'product-sleep', must: /Melatonin/i },
  { path: '/products/eye-care-gummies',  name: 'product-eye',  must: /Eye Care/i },
  { path: '/cart',                       name: 'cart',        must: /bag|cart/i },
  { path: '/pages/story',                name: 'story',       must: /./ },
  { path: '/pages/contact',              name: 'contact',     must: /./ },
  { path: '/policies/refund-policy',     name: 'refund',      must: /refund|return/i },
  { path: '/policies/privacy-policy',    name: 'privacy',     must: /privacy/i },
  { path: '/policies/shipping-policy',   name: 'shipping',    must: /ship/i },
  { path: '/policies/terms-of-service',  name: 'terms',       must: /terms/i },
];

/**
 * Noise that is not ours.
 *
 * The big one is third-party by ORIGIN, not by wording: `shopify theme dev`
 * serves the storefront from 127.0.0.1 while Shopify's own scripts still come
 * from cdn.shopify.com, so the browser blocks them as cross-origin. On the real
 * domain they are same-origin and load fine. Filtering those by their source
 * host rather than by message text keeps genuine first-party errors failing.
 *
 * WebKit needs its own entries: it reports the same CORS block as a pageerror
 * with no source URL, so the host filter cannot see it and only the wording
 * identifies it.
 *
 * LIMITATION worth knowing: every one of these was judged against
 * `shopify theme dev`. They are all platform calls that behave differently on
 * the real domain, where they are same-origin. Re-run this suite against the
 * live storefront once the password comes off, with GC_BASE set to it — if any
 * of these are still firing there, they are real and this list is hiding them.
 */
const THIRD_PARTY_HOSTS = [/cdn\.shopify\.com/, /shopifycloud/, /shopifysvc\.com/, /google-analytics/, /googletagmanager/];

export const IGNORED_CONSOLE = [
  /favicon/i,
  /origin_trials/i,
  /blocked by CORS policy/i,                        // Chromium's wording
  /Cross-origin script load denied/i,               // WebKit's wording for the same block
  /sf_private_access_tokens/i,                      // Shopify's own storefront-API call; 400s through the dev proxy
  /net::ERR_FAILED/i,            // the paired failure of that same blocked request
  /web-pixel/i,
  /Content Security Policy/i,
];

export const fromThirdParty = (url) => !!url && THIRD_PARTY_HOSTS.some((r) => r.test(url));
export const ignorable = (text) => IGNORED_CONSOLE.some((r) => r.test(text));
