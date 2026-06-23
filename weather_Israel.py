from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
import requests
import re

mcp = FastMCP("weather-Israel")

FORECAST_URL = "https://www.weather2day.co.il/forecast"

# =========================
# STATE
# =========================
STATE = {
    "pw": None,
    "browser": None,
    "page": None,
    "step": "INIT"
}

# =========================
# HEBREW CITY NAMES DICTIONARY
# =========================
CITY_NAMES_HE = {
    "jerusalem": "ירושלים",
    "tel aviv": "תל אביב",
    "haifa": "חיפה",
    "beer sheva": "באר שבע",
    "be'er sheva": "באר שבע",
    "ashdod": "אשדוד",
    "ashkelon": "אשקלון",
    "netanya": "נתניה",
    "holon": "חולון",
    "bnei brak": "בני ברק",
    "bene brak": "בני ברק",
    "petah tikva": "פתח תקוה",
    "petach tikva": "פתח תקוה",
    "rishon lezion": "ראשון לציון",
    "rishon le-zion": "ראשון לציון",
    "bat yam": "בת ים",
    "ramat gan": "רמת גן",
    "givatayim": "גבעתיים",
    "herzliya": "הרצליה",
    "kfar saba": "כפר סבא",
    "raanana": "ראש העין",
    "modiin": "מודיעין",
    "lod": "לוד",
    "ramla": "רמלה",
    "nahariya": "נהריה",
    "akko": "עכו",
    "acre": "עכו",
    "safed": "צפת",
    "tiberias": "טבריה",
    "bethlehem": "בית לחם",
    "jericho": "יריחו",
    "nablus": "נבלוס",
    "dead sea": "ים המלח",
    "sea of galilee": "כנרת",
    "eilat": "אילת",
    "mitzpe ramon": "מצפה רמון",
    "beersheba": "באר שבע",
    "sakhnin": "סח'נין",
    "umm al-fahm": "אום אל-פחם",
    "tamra": "תמרה",
    "rahat": "רהט",
}

# =========================
# TRANSLATION (NOMINATIM + FALLBACKS)
# =========================
async def translate_to_hebrew(city: str) -> str:
    city_lower = city.lower().strip()

    if city_lower in CITY_NAMES_HE:
        return CITY_NAMES_HE[city_lower]

    hebrew_re = re.compile(r"[\u0590-\u05FF]")

    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": city,
                "format": "json",
                "limit": 1,
                "accept-language": "he",
            },
            headers={"User-Agent": "mcp-weather"},
            timeout=5,
        )

        if r.ok:
            data = r.json()
            if data:
                item = data[0]
                display = item.get("display_name", "")
                if display and hebrew_re.search(display):
                    return display.split(",")[0].strip()

    except Exception:
        pass

    return city


# =========================
# 1. OPEN BROWSER
# =========================
@mcp.tool()
async def open_weather_forecast_israel():
    global STATE

    STATE["pw"] = await async_playwright().start()
    STATE["browser"] = await STATE["pw"].chromium.launch(headless=False)
    STATE["page"] = await STATE["browser"].new_page()

    await STATE["page"].goto(FORECAST_URL, wait_until="networkidle")

    STATE["step"] = "OPENED"

    return "Browser opened and ready."


# =========================
# 2. ENTER CITY
# =========================
@mcp.tool()
async def enter_weather_forecast_city_israel(city: str):
    global STATE

    if STATE["step"] != "OPENED":
        return "ERROR: Browser not open."

    page = STATE["page"]
    city_he = await translate_to_hebrew(city)

    input_field = page.locator("#city_search_forecast")
    await input_field.wait_for(timeout=10000)

    await input_field.click()
    await input_field.fill(city_he)
    await page.evaluate("""
        const input = document.querySelector('#city_search_forecast');
        if (input) {
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    """)

    try:
        await page.locator("form#weather-location + ul li").first.wait_for(timeout=5000)
    except:
        await page.wait_for_timeout(1500)

    STATE["step"] = "CITY_ENTERED"
    STATE["city_he"] = city_he

    return f"City entered: {city_he}"


# =========================
# 3. SELECT CITY + GET FORECAST
# =========================
@mcp.tool()
async def select_weather_forecast_city_israel():
    page = STATE["page"]
    
    # המתן לצעות להופיע
    await page.wait_for_timeout(500)
    
    # השתמש בניווט מקלדת לבחירה (ArrowDown + Enter)
    # זה עובד אפילו כשהאלמנטים אפס-גודל
    await page.keyboard.press("ArrowDown")
    await page.keyboard.press("Enter")
    
    # המתן לדף התחזית לטעון
    await page.wait_for_timeout(2500)
    
    return await page.inner_text("body")

# =========================
# RUN SERVER
# =========================
def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()