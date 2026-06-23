from playwright.sync_api import sync_playwright

city_he = 'ירושלים'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('https://www.weather2day.co.il/forecast', wait_until='networkidle')
    page.wait_for_timeout(1000)
    page.click('#city_search_forecast')
    page.fill('#city_search_forecast', city_he)
    page.evaluate("const input = document.querySelector('#city_search_forecast'); if (input) input.dispatchEvent(new Event('input', { bubbles: true }));")
    page.wait_for_timeout(1000)

    suggestions = page.locator('form#weather-location + ul li a')
    print('suggestion count:', suggestions.count())
    for i in range(min(10, suggestions.count())):
        el = suggestions.nth(i)
        print(i, el.inner_text().strip(), el.get_attribute('href'))

    target = page.locator('form#weather-location + ul li a', has_text=city_he).first
    print('target exists', target.count())
    if target.count() > 0:
        target.click()
        page.wait_for_timeout(3000)
        print('url after click', page.url)
        print('title after click', page.title())
        print('body snippet', page.content()[:2000])
    else:
        print('target not found')
    b.close()
