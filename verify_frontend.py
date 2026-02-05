import os
import time
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Load Page
        print("Loading page...")
        page.goto("http://localhost:3000/index.html")

        # 2. Inject API Key
        print("Injecting key...")
        page.evaluate("localStorage.setItem('gen_notes_api_key', 'test_key')")
        page.reload()

        # 3. Wait for App to load (Header)
        print("Waiting for header...")
        page.wait_for_selector("header")

        # 4. Check for Sidebar Button (RippleButton)
        # It has title "Close Sidebar" initially (sidebarOpen=true)
        btn = page.get_by_title("Close Sidebar")
        if btn.is_visible():
            print("Sidebar button found.")
            # Hover to trigger hover styles
            btn.hover()
            time.sleep(0.5)

            # Click to trigger ripple
            # Note: Ripple animation is fast (600ms), catching it in screenshot might be hard,
            # but we can verify the UI didn't crash.
            btn.click()
            time.sleep(0.2)
        else:
            print("Sidebar button NOT found.")

        # 5. Screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification_ripple.png")

        browser.close()

if __name__ == "__main__":
    verify()
