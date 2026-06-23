import asyncio
from playwright.async_api import async_playwright

FORECAST_URL = "https://www.weather2day.co.il/forecast"

async def test_selection():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=False)
    page = await browser.new_page()
    
    await page.goto(FORECAST_URL, wait_until="networkidle")
    print("1. Opened page")
    
    # Enter city
    city_he = "ירושלים"
    input_field = page.locator("#city_search_forecast")
    await input_field.click()
    await input_field.fill(city_he)
    await page.evaluate("""
        const input = document.querySelector('#city_search_forecast');
        if (input) {
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    """)
    print("2. Entered ירושלים")
    await page.wait_for_timeout(1500)
    
    # Select using force click
    target_selector = f"form#weather-location + ul li a:has-text(\"{city_he}\")"
    try:
        await page.click(target_selector, force=True)
        print("4. Clicked target with force=True")
    except Exception as e:
        print(f"4. Failed force click: {e}")
        print("   Trying keyboard fallback...")
        try:
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")
            print("   Keyboard selection executed")
        except Exception as e2:
            print(f"   Keyboard fallback failed: {e2}")
    
    await page.wait_for_timeout(3000)
    print(f"5. URL after selection: {page.url}")
    title = await page.title()
    print(f"6. Title: {title}")
    
    # Check if we got forecast data
    body_text = await page.inner_text("body")
    if "ירושלים" in body_text and ("יום" in body_text or "תחזית" in body_text or "מעלות" in body_text):
        print("✓ SUCCESS: Forecast page loaded for Jerusalem")
    else:
        print("✗ Page content check - checking...")
        print("First 1000 chars:", body_text[:1000])
    
    await browser.close()
    await pw.stop()

asyncio.run(test_selection())


