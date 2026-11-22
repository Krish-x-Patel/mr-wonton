# Mr. Wonton

Chinese takeout on Canton Road. 3595 Canton Rd, Suite 328, Marietta, GA 30066 · (770) 591-4288

To change a price or menu item, edit the `MENU` (or `TRAYS`) list in `tools/build.py`, then run `python3 tools/build.py` from this folder. It rebuilds `index.html`, so prices stay the same everywhere on the page. Page design and text live in `tools/template.html`.

To check the site: `python3 -m http.server 8765` in this folder, then `node tools/check.js` (needs Playwright).

Prices come from Mr. Wonton's own online ordering page, copied Nov 22, 2026. The site is unlisted (noindex) until the owner approves it.
