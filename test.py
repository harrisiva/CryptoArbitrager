import requests
import json

BASE = 'BTC'
CURRENCY = 'USD'

INPUTS = {
    "Coinbase": "{}-{}".format(BASE,CURRENCY),
    "Kraken": "{}{}".format(BASE,CURRENCY)
}

ENDPOINTS:dict = {
    "Coinbase": {"buy": "https://api.coinbase.com/v2/prices/{}/buy","sell":"https://api.coinbase.com/v2/prices/{}/sell"}, #Input format (BTC-USD)
    "Kraken": "https://api.kraken.com/0/public/Depth?pair={}"
}

# To receive responses from brokers in the required format, use these functions
def coinbase(): return {
    "bid": float((requests.get(ENDPOINTS["Coinbase"]["buy"].format(INPUTS["Coinbase"])).json())['data']['amount']),
    "ask": float((requests.get(ENDPOINTS["Coinbase"]["sell"].format(INPUTS["Coinbase"])).json())['data']['amount']),
}

def kraken():
    response = requests.get(ENDPOINTS["Kraken"].format(INPUTS["Kraken"])).json()
    pair = list(response['result'].keys())[0]
    bids_volume = ([float(sets[1]) for sets in response['result'][pair]['bids']]) 
    asks_volume = ([float(sets[1]) for sets in response['result'][pair]['asks']])
    return {
        "bid":[float(sets[0])for sets in response['result'][pair]['asks']][asks_volume.index(max(asks_volume))],
        "ask": [float(sets[0])for sets in response['result'][pair]['bids']][bids_volume.index(max(bids_volume))]
}
