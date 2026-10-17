import { test, expect } from '@playwright/test';
import { ROUTES, ignorable, fromThirdParty } from './_routes.mjs';

/**
 * One pass over every customer-reachable page, at every viewport.
 *
 * These are the failures that actually cost a sale: a page that errors, a page
 * that scrolls sideways on a phone, an asset that 404s, a script that throws.
 * None of them show up in a unit test and all of them show up to a customer.
 */
for (const route of ROUTES) {
  test.describe(route.name, () => {

    test(`${route.name}: loads, renders, and says the right thing`, async ({ page }) => {
      const res = await page.goto(route.path, { waitUntil: 'domcontentloaded' });
      expect(res?.status(), `${route.path} returned ${res?.status()}`).toBeLessThan(400);
      await expect(page.locator('body')).toBeVisible();
      const text = await page.locator('body').innerText();
      expect(text, `${route.path} is missing its expected content`).toMatch(route.must);
      expect(text, `${route.path} shows a Liquid error`).not.toMatch(/Liquid error|translation missing/i);
    });

    test(`${route.name}: does not scroll sideways`, async ({ page }, testInfo) => {
      await page.goto(route.path, { waitUntil: 'load' });
      await page.waitForTimeout(400);
      const over = await page.evaluate(() => {
        const d = document.documentElement;
        if (d.scrollWidth <= d.clientWidth) return null;
        // name the widest offender, so a failure is actionable
        let worst = null;
        for (const el of document.querySelectorAll('body *')) {
          const r = el.getBoundingClientRect();
          if (r.right > d.clientWidth + 1 && (!worst || r.right > worst.right)) {
            worst = { right: Math.round(r.right), tag: el.tagName, cls: String(el.className).slice(0, 80) };
          }
        }
        return { scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, worst };
      });
      expect(over, `horizontal overflow at ${testInfo.project.name}: ${JSON.stringify(over)}`).toBeNull();
    });

    test(`${route.name}: no console errors and no broken assets`, async ({ page }) => {
      const errors = [];
      const broken = [];
      page.on('console', (m) => {
        if (m.type() !== 'error') return;
        const where = m.location()?.url ?? '';
        /* The URL must be filtered too, not just the text. A failed subresource
           reports as "Failed to load resource: ... 400 ..." with the endpoint
           only in location() — so matching on text alone let every one of these
           through and failed every tablet page. */
        if (ignorable(m.text()) || ignorable(where)) return;
        if (fromThirdParty(where)) return;               // not ours to fix
        errors.push(`${m.text()}  @${where || 'inline'}`);
      });
      page.on('pageerror', (e) => { if (!ignorable(String(e))) errors.push(`pageerror: ${e}`); });
      page.on('response', (r) => {
        if (r.status() >= 400 && new URL(r.url()).host.includes('127.0.0.1') && !ignorable(r.url())) {
          broken.push(`${r.status()} ${r.url()}`);
        }
      });
      await page.goto(route.path, { waitUntil: 'load' });
      await page.waitForTimeout(800);
      expect(errors, `console errors on ${route.path}`).toEqual([]);
      expect(broken, `broken assets on ${route.path}`).toEqual([]);
    });

    test(`${route.name}: every image actually loaded`, async ({ page }) => {
      await page.goto(route.path, { waitUntil: 'load' });
      await page.waitForTimeout(800);
      const bad = await page.evaluate(() =>
        [...document.images]
          .filter((i) => i.loading !== 'lazy' || i.getBoundingClientRect().top < innerHeight * 2)
          .filter((i) => i.complete && i.naturalWidth === 0)
          .map((i) => i.currentSrc || i.src));
      expect(bad, `images failed to decode on ${route.path}`).toEqual([]);
    });

    test(`${route.name}: images that convey meaning have alt text`, async ({ page }) => {
      await page.goto(route.path, { waitUntil: 'load' });
      const missing = await page.evaluate(() =>
        [...document.images]
          .filter((i) => !i.closest('[aria-hidden="true"]'))
          .filter((i) => !i.hasAttribute('alt'))
          .map((i) => (i.currentSrc || i.src).split('/').pop()));
      expect(missing, `images with no alt attribute on ${route.path}`).toEqual([]);
    });
  });
}

/* The brand font ships to every visitor on every page. It was a 163 KB TTF; the
   WOFF2 is 53 KB for byte-identical glyph coverage. This asserts the small one
   is what the page actually asks for, because a stray edit to the @font-face
   would silently cost 110 KB on every load and nothing else would notice. */
test('the page requests the small font, not the large one', async ({ page }) => {
  const fonts = [];
  page.on('request', (r) => { if (/Manrope-Variable/.test(r.url())) fonts.push(r.url()); });
  await page.goto('/', { waitUntil: 'load' });
  await page.waitForTimeout(1200);
  expect(fonts.some((u) => u.endsWith('.ttf')),
    `the 163 KB TTF was requested: ${fonts.join(', ')}`).toBe(false);
});
