const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 900 } });
  for (let n = 1; n <= 5; n++) {
    await p.goto('file:///home/claude/hrid-website/brand/hero-src/render.html?n=' + n); await p.waitForFunction(() => document.title === 'done');
    await p.screenshot({ path: `/home/claude/hrid-website/site/assets/hero/banner-${n}.jpg`, type: 'jpeg', quality: 80 });
  }
  await b.close();
})();
