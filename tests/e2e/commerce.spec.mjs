import { test, expect } from '@playwright/test';

/**
 * The money path. Everything up to — and deliberately stopping at — checkout.
 *
 * These tests never complete a purchase and never enter payment details. The
 * assertion is that a customer CAN reach Shopify's checkout with the right item
 * at the right price; what happens inside checkout is Shopify's, and exercising
 * it would mean putting card numbers into a form.
 */

const PRODUCT = '/products/brain-booster-gummies';

/** Rupee amounts on a page, normalised to integers. */
const prices = (text) =>
  [...text.matchAll(/₹\s?([\d,]+)/g)].map((m) => Number(m[1].replace(/,/g, '')));

test.beforeEach(async ({ context }) => { await context.clearCookies(); });

test('a customer can add to bag and reach checkout', async ({ page }) => {
  await page.goto(PRODUCT, { waitUntil: 'load' });

  const buy = page.locator('#gp-buy');
  await expect(buy, 'the product page has no visible buy button').toBeVisible();
  await expect(buy).toBeEnabled();

  /* "Add to bag" posts with fetch and stays on the page — navigating straight
     after the click races the request. The confirmation line is the signal that
     the add actually landed. */
  await buy.click();
  await expect(page.locator('#gp-added'), 'no "In your bag" confirmation after adding')
    .toBeVisible({ timeout: 15_000 });

  await page.goto('/cart', { waitUntil: 'load' });

  /* Assert on structure, not on prose. An earlier version of this test matched
     /cart is empty/ — but this theme says "Your bag", so it passed on an empty
     cart and proved nothing. */
  await expect(page.locator('.gck-empty'), 'the cart is empty after adding a product')
    .toHaveCount(0);
  await expect(page.locator('.gck-row'), 'no line items in the cart').toHaveCount(1);
  await expect(page.locator('.gck-row').first()).toContainText(/Brain Booster/i);

  const checkout = page.locator('button[name="checkout"]');
  await expect(checkout, 'no checkout control on a cart that has items').toBeVisible();
  await expect(checkout).toBeEnabled();
});

test('"Buy it now" goes to checkout, not nowhere', async ({ page }) => {
  await page.goto(PRODUCT, { waitUntil: 'load' });
  const now = page.locator('#gp-now');
  await expect(now, 'no "Buy it now" control').toBeVisible();

  /* Stop at the checkout boundary: assert we are sent there, never go through
     it. Completing a purchase would mean entering payment details. */
  const [req] = await Promise.all([
    page.waitForRequest((r) => /\/checkout/.test(r.url()), { timeout: 20_000 }).catch(() => null),
    now.click(),
  ]);
  const url = page.url();
  expect(req || /\/checkout|\/cart/.test(url),
    `"Buy it now" did not head for checkout — landed on ${url}`).toBeTruthy();
});

test('the price a customer sees never changes between pages', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const home = prices(await page.locator('body').innerText());

  await page.goto(PRODUCT, { waitUntil: 'load' });
  const product = prices(await page.locator('body').innerText());

  expect(home.length, 'no prices found on the homepage').toBeGreaterThan(0);
  expect(product.length, 'no price found on the product page').toBeGreaterThan(0);

  // The product's own price must be one the homepage advertised for it.
  expect(home, `homepage prices ${home} do not contain the product price ${product[0]}`)
    .toContain(product[0]);
});

test('the + control raises the quantity that gets submitted', async ({ page }) => {
  await page.goto(PRODUCT, { waitUntil: 'load' });
  const qty = page.locator('#gp-qty');
  await expect(qty).toHaveCount(1);
  const before = Number(await qty.inputValue());
  /* Target the increment specifically. Taking "the first button in the group"
     picked the decrement, which cannot go below 1 — so the test failed while
     the control worked. */
  const plus = page.locator('[data-qty="up"], [data-qty-up], .gp-qty button:last-of-type').first();
  if (!(await plus.count())) test.skip(true, 'no quantity stepper on this product');
  await plus.click();
  await expect(qty).not.toHaveValue(String(before), { timeout: 5_000 });
  expect(Number(await qty.inputValue())).toBeGreaterThan(before);
});

test('the cart survives a reload', async ({ page }) => {
  await page.goto(PRODUCT, { waitUntil: 'load' });
  await page.locator('#gp-buy').click();
  await expect(page.locator('#gp-added')).toBeVisible({ timeout: 15_000 });
  await page.goto('/cart', { waitUntil: 'load' });
  await page.reload({ waitUntil: 'load' });
  await expect(page.locator('.gck-empty'), 'the cart emptied on reload').toHaveCount(0);
});

test('every in-site link resolves', async ({ page, request }) => {
  await page.goto('/', { waitUntil: 'load' });
  const hrefs = await page.evaluate(() =>
    [...new Set([...document.querySelectorAll('a[href^="/"]')].map((a) => a.getAttribute('href')))]
      .filter((h) => !h.startsWith('//') && !h.includes('#')));
  const dead = [];
  for (const h of hrefs) {
    const r = await request.get(h, { maxRedirects: 5 });
    if (r.status() >= 400) dead.push(`${r.status()} ${h}`);
  }
  expect(dead, 'links on the homepage that go nowhere').toEqual([]);
});
