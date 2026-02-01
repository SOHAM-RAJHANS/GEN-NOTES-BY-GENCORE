import os
from playwright.sync_api import sync_playwright

def verify_app():
    print("Starting verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Absolute path to index.html
        file_path = os.path.abspath("index.html")
        url = f"file://{file_path}"
        print(f"Navigating to {url}")

        # Navigate
        page.goto(url)

        # Inject API Key to bypass modal (Mock key)
        print("Injecting API Key...")
        page.evaluate("localStorage.setItem('gen_notes_api_key', 'test_key_123')")
        page.reload() # Reload to pick up key

        # Wait for Header to appear (indicating App loaded)
        try:
            page.wait_for_selector("header", timeout=10000)
            print("Header found.")
        except Exception as e:
            print("Header not found, dumping content...")
            print(page.content()[:500])
            browser.close()
            return

        # Wait for the specific RippleButton (Sidebar Toggle)
        # It contains an SVG (PanelLeft)
        # Verify it has 'relative' and 'overflow-hidden' classes
        toggle_btn = page.locator("header button").first
        classes = toggle_btn.get_attribute("class")
        print(f"Button classes: {classes}")

        if "relative" in classes and "overflow-hidden" in classes:
            print("VERIFIED: RippleButton classes found on Header button.")
        else:
            print("WARNING: RippleButton classes MISSING.")

        # Screenshot
        page.screenshot(path="verification.png")
        print("Screenshot saved to verification.png")

        browser.close()

if __name__ == "__main__":
    verify_app()
