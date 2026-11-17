"""Print the executed HTML using an installed Chromium browser."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.goto((root / 'reports' / 'wifi_room_classification.html').as_uri(), wait_until='load')
    page.evaluate('document.fonts.ready')
    page.pdf(path=str(root / 'reports' / 'wifi_room_classification.pdf'),
             print_background=True, prefer_css_page_size=True)
    page.screenshot(path=str(root / '.verification' / 'report_preview.png'), full_page=False)
    browser.close()
print('PDF saved.')
