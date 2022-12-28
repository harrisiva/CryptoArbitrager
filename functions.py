def mostprofitable(data): # Finds the most profitable trade (highest profit margin)
    highest = [0,{}]
    for selling_broker in data:
        ask = data[selling_broker]['ask']
        buyers = [buyer_broker for buyer_broker in data if buyer_broker!=selling_broker]
        for buyer in buyers:
            margin = data[buyer]['bid']-ask
            difference = {
                "seller": selling_broker,
                "buyer": buyer,
                "sell_price": ask,
                "buy_price": data[buyer]['bid'],
                "margin": margin 
            }
            if margin>=highest[0]: highest[1]=difference