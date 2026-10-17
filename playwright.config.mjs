import { defineConfig, devices } from '@playwright/test';

/**
 * The storefront runs locally under `shopify theme dev` (port 9292). That server
 * is started by Mehal, not by this config — it needs Shopify auth, so Playwright
 * must not try to own its lifecycle.
 *
 * WebKit carries the mobile and tablet projects deliberately: the founder's own
 * device is an iPhone, every jitter report in this project came from Safari, and
 * Chromium would have reported those pages as fine.
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  /* `shopify theme dev` is a local proxy to Shopify — every request goes over
     the network and it rate-limits under load. At 4 workers pages that pass
     alone failed in the suite, which is the proxy buckling, not the site. Two
     workers and one retry keep genuine failures visible while flakes show up
     as flakes rather than as bugs. */
  workers: 2,
  retries: 1,
  reporter: [['list'], ['json', { outputFile: '.playwright/report.json' }]],
  timeout: 45_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: process.env.GC_BASE ?? 'http://127.0.0.1:9292',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'mobile',  use: { ...devices['iPhone 14'] } },
    { name: 'tablet',  use: { ...devices['iPad (gen 7) landscape'], viewport: { width: 820, height: 1180 } } },
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
  ],
});
