from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False)
    browser = p.firefox.launch(headless=False)
    # browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://seznam.cz")
    search_field = page.query_selector('div.search-form input[name=q].input')
    search_field.fill("chata")
    search_field.press('Enter')
    sleep(3)
    print(page.title())
    browser.close()
