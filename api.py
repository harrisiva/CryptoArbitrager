import requests, json

class API:
    def __init__(self,base,currency):
        self.base = base
        self.currency = currency

        # Details of different crypto API's endpoints for requests
        self.INPUTS = {
            "Coinbase": "{}-{}".format(self.base,self.currency),
            "Kraken": "{}{}".format(self.base,self.currency)
        }

        self.ENDPOINT_URLS:dict = {
            "Coinbase": {"buy": "https://api.coinbase.com/v2/prices/{}/buy","sell":"https://api.coinbase.com/v2/prices/{}/sell"}, #Input format (BTC-USD)
            "Kraken": "https://api.kraken.com/0/public/Depth?pair={}"
        }
        return
    
    def coinbase(self): 
        data = {
            "bid": float((requests.get(self.ENDPOINT_URLS["Coinbase"]["buy"].format(self.INPUTS["Coinbase"])).json())['data']['amount']),
            "ask": float((requests.get(self.ENDPOINT_URLS["Coinbase"]["sell"].format(self.INPUTS["Coinbase"])).json())['data']['amount']),
        }
        return data

    def kraken(self):
        response = requests.get(self.ENDPOINT_URLS["Kraken"].format(self.INPUTS["Kraken"])).json()
        pair = list(response['result'].keys())[0]
        bids_volume = ([float(sets[1]) for sets in response['result'][pair]['bids']]) 
        asks_volume = ([float(sets[1]) for sets in response['result'][pair]['asks']])
        return {
            "bid":[float(sets[0])for sets in response['result'][pair]['asks']][asks_volume.index(max(asks_volume))],
            "ask": [float(sets[0])for sets in response['result'][pair]['bids']][bids_volume.index(max(bids_volume))]
    }
