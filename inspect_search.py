import requests

url = 'https://www.weather2day.co.il/forecast'
r = requests.get(url, timeout=15)
print('status', r.status_code)
text = r.text
idx = text.find('id="city_search_forecast"')
print('input idx', idx)
if idx != -1:
    print(text[idx-200:idx+200])
else:
    print('input not found')

# show surrounding markup for potential list element
li_idx = text.find('<li')
print('first <li idx', li_idx)
print(text[li_idx:li_idx+400])
