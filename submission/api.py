import requests
import json
import datetime as dt
import os
import time

# obtain CoinGecko demo-api key -> the part where your api key must be registered
# it can be either be hardcoded in or use the environment vairable.
key = os.environ.get("API")

# flag argument -> sort cryptocurrency ratio of price change to current price
# top argument -> sort cryptocurrency by the top 5
def get_ids_info (ids: str, flag = False, top = False):
    ids = str(ids)
    req = requests.get(url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=sgd&ids={ids.lower()}", headers={"x-cg-demo-api-key": os.environ.get("API"), "accept": "application/json"})
    req_t = req.text
    parsed = json.loads(req_t)

    if parsed == []:
        return f"{ids} does not exist in the database!"
    
    else:
        data = parsed[0]
        return (data.get("name"), data.get("price_change_percentage_24h"), data.get("low_24h"), data.get("high_24h"), data.get("current_price"), data.get("circulating_supply"), data.get("market_cap"), data.get("market_cap_change_percentage_24h"))

def get_all_info():
    req = requests.get(url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=sgd", headers={"x-cg-demo-api-key": os.environ.get("API"), "accept": "application/json"})
    req = req.text
    parsed = json.loads(req)
    r_value = []

    for data in parsed:
        r_value.append([data.get("name"), data.get("price_change_percentage_24h"), data.get("low_24h"), data.get("high_24h"), data.get("current_price")])

    return sorted(r_value, key=lambda x: x[1], reverse=True)[:3]

# frm & to arguments: start and end points for the api to extract historical data in that time range
def get_historical(ids: str, frm: tuple[int, int, int], to: tuple[int, int, int]):
    frm_dt = dt.datetime(frm[0], frm[1], frm[2])
    to_dt = dt.datetime(to[0], to[1], to[2])

    frm_ux = time.mktime(frm_dt.timetuple())
    to_ux = time.mktime(to_dt.timetuple())
    req = requests.get(url=f"https://api.coingecko.com/api/v3/coins/{ids.lower()}/market_chart/range?vs_currency=sgd&from={frm_ux}&to={to_ux}", headers={"x-cg-demo-api-key": os.environ.get("API"), "accept": "application/json"})
    req_t = req.text
    parsed = json.loads(req_t)

    x_values = [data[0] for data in parsed['prices']]
    y_values = [data[1] for data in parsed['prices']]

    return (x_values, y_values, frm, to, ids)

#json.dumps(get_posts(flag=True, top=True), indent=4)
