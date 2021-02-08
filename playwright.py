from playwright.sync_api import sync_playwright

def run(playwright):
    # chromium = playwright.chromium # or "firefox" or "webkit".
    browser = playwright.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://seznam.cz")
    page.fill('input[name="q"]')
    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

