import { test, expect } from '@playwright/test';

test('RippleButton and UI check', async ({ page }) => {
  // Inject API Key
  await page.addInitScript(() => {
    localStorage.setItem('gen_notes_api_key', 'test-key');
  });

  await page.goto('http://localhost:8000/index.html');

  // Wait for the app to load
  await expect(page.locator('text=GenNotes')).toBeVisible();

  // Check if Sidebar Toggle (RippleButton) is working
  // Initial state is open
  const sidebarToggle = page.locator('button[title="Close Sidebar"]');
  await expect(sidebarToggle).toBeVisible();

  await sidebarToggle.click();

  // Expect title to change to "Open Sidebar"
  const closedSidebarToggle = page.locator('button[title="Open Sidebar"]');
  await expect(closedSidebarToggle).toBeVisible();

  // Check Toast Styling
  // The app shows a security warning toast on mount.
  const toastText = page.locator('text=SECURITY NOTICE');
  await expect(toastText).toBeVisible();

  // Navigate up to the toast container div
  const toast = toastText.locator('xpath=../..');
  // Verify Glassmorphism 3.0 classes
  await expect(toast).toHaveClass(/backdrop-blur-2xl/);
  await expect(toast).toHaveClass(/bg-slate-900\/60/);
});
