from playwright.sync_api import sync_playwright
p = sync_playwright().start()
try:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('https://www.weather2day.co.il/forecast', wait_until='networkidle')
    print('title:', page.title())
    inp = page.query_selector('#city_search_forecast')
    print('input exists', inp is not None)
    if inp:
        print('input html:', inp.get_attribute('outerHTML'))
    page.click('#city_search_forecast')
    page.fill('#city_search_forecast', 'ירושלים')
    page.wait_for_timeout(3000)
    items = page.query_selector_all('li')
    print('li count', len(items))
    for i, item in enumerate(items[:20]):
        print('li', i, repr(item.inner_text().strip()))
    page.screenshot(path='search.png')
    print('screenshot saved search.png')
    b.close()
finally:
    p.stop()
