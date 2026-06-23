from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('https://www.weather2day.co.il/forecast', wait_until='networkidle')
    print('title:', page.title())

    print('input selector exists', page.query_selector('#city_search_forecast') is not None)
    print('input info', page.eval_on_selector('#city_search_forecast', 'el => ({outerHTML: el.outerHTML, id: el.id, className: el.className, name: el.name, type: el.type})'))

    page.click('#city_search_forecast')
    page.fill('#city_search_forecast', 'ירושלים')
    page.wait_for_timeout(3000)

    print('find li matching ירושלים or תל אביב or צפת')
    matches = page.evaluate('''() => {
        const out = [];
        document.querySelectorAll('li').forEach((el, i) => {
            const txt = el.innerText.trim();
            if (txt.includes('ירושלים') || txt.includes('תל אביב') || txt.includes('צפת')) {
                out.push({
                    i,
                    text: txt,
                    className: el.className,
                    parent: el.parentElement ? {tag: el.parentElement.tagName, className: el.parentElement.className, id: el.parentElement.id} : null,
                    outer: el.outerHTML.slice(0,200)
                });
            }
        });
        return out;
    }''')
    print(matches)

    print('ul containers after form#weather-location')
    ul_info = page.evaluate('''() => {
        const out = [];
        const els = document.querySelectorAll('form#weather-location + ul, form#weather-location ul, form#weather-location ~ ul');
        els.forEach((el, i) => {
            out.push({
                index: i,
                tag: el.tagName,
                id: el.id,
                className: el.className,
                itemCount: el.querySelectorAll('li').length,
                firstItems: Array.from(el.querySelectorAll('li')).slice(0,5).map(li => li.innerText.trim())
            });
        });
        return out;
    }''')
    print(ul_info)

    print('list containers near input')
    containers = page.evaluate('''() => {
        const input = document.querySelector('#city_search_forecast');
        const out = [];
        let node = input;
        for (let i = 0; i < 6 && node; i++) {
            node = node.parentElement;
            if (!node) break;
            out.push({level: i+1, tag: node.tagName, id: node.id, className: node.className, inner: node.innerHTML.slice(0,200)});
        }
        return out;
    }''')
    print(containers)

    page.screenshot(path='search_screenshot.png')
    print('screenshot written to search_screenshot.png')
    b.close()
