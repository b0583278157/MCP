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
    target = page.query_selector('form#weather-location + ul li a:has-text("ירושלים")')
    print('target', target is not None)
    if target:
        style = page.evaluate('el => ({display: getComputedStyle(el).display, visibility: getComputedStyle(el).visibility, opacity: getComputedStyle(el).opacity, offsetHeight: el.offsetHeight, offsetWidth: el.offsetWidth, boundingClientRect: el.getBoundingClientRect().toJSON(), parentDisplay: getComputedStyle(el.parentElement).display, parentVisibility: getComputedStyle(el.parentElement).visibility, ulDisplay: getComputedStyle(el.closest("ul")).display, ulVisibility: getComputedStyle(el.closest("ul")).visibility})', target)
        print('style', style)
        print('href', target.get_attribute('href'))
        print('outer', target.evaluate('el => el.outerHTML'))
    else:
        print('no target')
    print('ul outer HTML', page.query_selector('form#weather-location + ul').evaluate('el => el.outerHTML.slice(0,500)'))
    b.close()
