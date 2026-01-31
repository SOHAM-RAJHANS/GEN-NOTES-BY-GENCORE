import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Inject API Key to bypass modal
        page.add_init_script("localStorage.setItem('gen_notes_api_key', 'dummy-key');")

        # Load local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for React to mount and Header to appear
        page.wait_for_selector("header", state="visible")

        # Allow animations to settle (Glassmorphism, particles)
        page.wait_for_timeout(2000)

        # Take screenshot of the whole page
        page.screenshot(path="verification/ui_verification.png")

        print("Screenshot taken.")
        browser.close()

if __name__ == "__main__":
    run()
