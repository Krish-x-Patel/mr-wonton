// Quick checks for the Mr. Wonton site. Run: python3 -m http.server 8765 & node tools/check.js
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765/';
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL:', m); } };
(async () => {
  const b = await chromium.launch();
  for (const vp of [{ width: 1280, height: 800, n: 'desktop' }, { width: 375, height: 740, n: 'phone' }, { width: 320, height: 640, n: 'small' }]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(BASE, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(800);
    ok(errs.length === 0, vp.n + ' page errors: ' + errs.join('; '));
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    ok(sw <= vp.width, `${vp.n} horizontal scroll ${sw} > ${vp.width}`);
    ok(await p.$('meta[name=robots][content*=noindex]') !== null, 'noindex missing');
    const bad = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h)));
    ok(bad.length === 0, 'broken in-page links: ' + bad);
    const small = await p.evaluate(() => [...document.querySelectorAll('.btn,.chips a')].filter(e => e.offsetParent && e.getBoundingClientRect().height < 42).length);
    ok(small === 0, vp.n + ' small tap targets: ' + small);
    ok(await p.$$eval('a[href^="tel:"]', a => a.every(x => x.getAttribute('href') === 'tel:+17705914288')), 'tel links');
    ok(await p.$$eval('a[target=_blank]', a => a.every(x => x.rel.includes('noopener'))), 'noopener');
    ok(await p.locator('#status').textContent() !== '', 'status text');
    if (vp.n !== 'small') await p.screenshot({ path: `/tmp/claude-0/-home-user/df94f082-9dbb-5ab1-a96f-40f1adfb84f8/scratchpad/shot-${vp.n}.png`, fullPage: false });
    await p.close();
  }
  // Open/closed logic at fixed Eastern times
  const cases = [
    ['2026-11-23T12:00:00', /^Closed today\. Opens tomorrow at 11 am$/, 'Monday, closed'],
    ['2026-11-24T10:00:00', /^Closed now\. Opens today at 11 am$/, 'Tuesday, 11 am to 9:30 pm'],
    ['2026-11-24T13:00:00', /^Open now, until 9:30 pm$/, null],
    ['2026-11-28T21:45:00', /^Open now, until 10 pm$/, null],
    ['2026-11-22T21:45:00', /^Closed now\. Opens Tuesday at 11 am$/, null],
    ['2026-11-27T22:30:00', /^Closed now\. Opens tomorrow at 11 am$/, null],
  ];
  for (const [t, re, today] of cases) {
    const p = await b.newPage();
    await p.addInitScript(`window.__NOW=${JSON.stringify(t)}`);
    await p.goto(BASE, { waitUntil: 'domcontentloaded' });
    const s = await p.locator('#status').textContent();
    ok(re.test(s), `status at ${t}: "${s}"`);
    if (today) ok((await p.locator('#today').textContent()) === today, `today at ${t}`);
    await p.close();
  }
  // Legal page
  const p = await b.newPage(); await p.goto(BASE + 'legal.html');
  for (const id of ['privacy', 'terms', 'accessibility', 'allergens']) ok(await p.$('#' + id) !== null, 'legal #' + id);
  ok(!(await p.content()).toLowerCase().includes('falafel'), 'leftover Falafel text');
  await b.close();
  console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})();
