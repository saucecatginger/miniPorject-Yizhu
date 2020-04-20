import requests
from pprint import pprint

eq_url_template = 'https://apis.is/earthquake/is'

my_latitude = '63.976'
my_longitude = '-21.949'
my_depth = 1.1

eq_url = eq_url_template.format(lat = my_latitude, lng = my_longitude)

resp = requests.get(eq_url)
if resp.ok:
    eq = resp.json()
else:
    print(resp.reason)

pprint(eq)

date_url_template = 'https://apis.is/earthquake/is'

resp = requests.get(date_url_template.format(depth = my_depth))
if resp.ok:
    date_json = resp.json()
else:
    print(resp.reason)

dates = {categ["url"]:categ["name"] for categ in date_json}

date_category_stats = dict.fromkeys(dates.keys(), 0)
date_category_stats.pop("all-crime")

for date in eq:
	date_category_stats[date["category"]] += 1

pprint(date_category_stats)
