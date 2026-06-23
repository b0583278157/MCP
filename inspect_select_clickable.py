from playwright.sync_api import sync_playwright

city_he = 'ירושלים'
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('https://www.weather2day.co.il/forecast', wait_until='networkidle')
    page.click('#city_search_forecast')
    page.fill('#city_search_forecast', city_he)
    page.evaluate("const input = document.querySelector('#city_search_forecast'); if (input) input.dispatchEvent(new Event('input', { bubbles: true }));")
    page.wait_for_timeout(1500)

    li = page.query_selector('form#weather-location + ul li:has(a:has-text("ירושלים"))')
    print('li exists', li is not None)
    if li:
        box = li.bounding_box()
        print('li box', box)
        style = page.evaluate('el => ({display: getComputedStyle(el).display, visibility: getComputedStyle(el).visibility, opacity: getComputedStyle(el).opacity, offsetHeight: el.offsetHeight, offsetWidth: el.offsetWidth})', li)
        print('li style', style)
        a = li.query_selector('a')
        print('a exists', a is not None)
        if a:
            print('a box', a.bounding_box())
            style_a = page.evaluate('el => ({display: getComputedStyle(el).display, visibility: getComputedStyle(el).visibility, opacity: getComputedStyle(el).opacity, offsetHeight: el.offsetHeight, offsetWidth: el.offsetWidth})', a)
            print('a style', style_a)
        print('trying li click by JS')
        page.evaluate('(el) => el.click()', li)
        page.wait_for_timeout(2000)
        print('after js click url', page.url)
        print('title', page.title())
        print('content starts', page.content()[:500])
    b.close()
