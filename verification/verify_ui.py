from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})

        print("Navigating...")
        page.goto("http://localhost:8080/index.html")

        # Wait for toast
        try:
            page.wait_for_selector(".fixed.bottom-6", timeout=5000)
            print("Toast container found.")
        except:
            print("Toast container not found immediately.")

        # Simulate mouse movement for UniverseCursorFX
        print("Moving mouse...")
        for i in range(10):
            page.mouse.move(100 + i * 50, 100 + i * 50)
            time.sleep(0.1)

        # Take screenshot
        output_path = "verification/ui_check.png"
        page.screenshot(path=output_path)
        print(f"Screenshot saved to {output_path}")
        browser.close()

if __name__ == "__main__":
    run()
