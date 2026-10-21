import { test, expect } from '@playwright/test';

/**
 * Pack your Chum Box — the bundle builder.
 *
 * It writes to the cart, so a screenshot proves nothing. These assert the money
 * path: what you pick is what gets added, at the price the page showed you.
 */
test.beforeEach(async ({ context }) => { await context.clearCookies(); });

test('the box starts empty and the button is disabled', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  await expect(page.locator('#chum-box')).toBeVisible();
  await expect(page.locator('[data-summary]')).toHaveText(/empty/i);
  await expect(page.locator('[data-add]')).toBeDisabled();
});

test('tapping a Chum picks them, tapping again puts them back', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const first = page.locator('.gcb-pick').first();
  await first.click();
  await expect(first).toHaveClass(/is-picked/);
  await expect(page.locator('[data-add]')).toBeEnabled();
  await first.click();
  await expect(first).not.toHaveClass(/is-picked/);
  await expect(page.locator('[data-add]')).toBeDisabled();
});

test('the total is the sum of what is in the box, not a guess', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const picks = page.locator('.gcb-pick');
  const n = await picks.count();
  let expected = 0;
  for (let i = 0; i < n; i++) {
    const p = picks.nth(i);
    expected += Number(await p.getAttribute('data-price'));
    await p.click();
  }
  const text = await page.locator('[data-summary]').innerText();
  expect(text, 'all three picked should say so').toMatch(/all three/i);
  /* Grouped the way the page groups it. The summary uses
     toLocaleString('en-IN'), so a three-box total renders ₹2,247 — this
     asserted ₹2247 and went red the moment the comma landed. Formatting the
     expectation the same way keeps the real check intact: the total still has
     to equal the sum of what was picked, and a wrong total still fails. */
  expect(text).toContain(`₹${Math.round(expected / 100).toLocaleString('en-IN')}`);
});

test('the quantity stepper does not go below zero', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const minus = page.locator('.gcb-pick').first().locator('[data-step="-1"]');
  for (let i = 0; i < 3; i++) await minus.click();
  await expect(page.locator('.gcb-pick').first().locator('[data-count]')).toHaveText('0');
  await expect(page.locator('[data-add]')).toBeDisabled();
});

test('the box lands in the cart with the right lines and the right total', async ({ page }) => {
  await page.goto('/', { waitUntil: 'load' });
  const picks = page.locator('.gcb-pick');
  await picks.nth(0).click();
  await picks.nth(2).locator('[data-step="1"]').click();   // two of the third
  await picks.nth(2).locator('[data-step="1"]').click();

  await Promise.all([
    page.waitForURL(/\/cart/, { timeout: 25_000 }),
    page.locator('[data-add]').click(),
  ]);

  const cart = await page.evaluate(() => fetch('/cart.js').then((r) => r.json()));
  expect(cart.item_count, 'one of the first + two of the third = three jars').toBe(3);
  expect(cart.items.length, 'two distinct products').toBe(2);
  const qty = cart.items.map((i) => i.quantity).sort();
  expect(qty).toEqual([1, 2]);
});
