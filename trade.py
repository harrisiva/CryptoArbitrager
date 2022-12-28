import datetime

#TODO: Use a SQL Table for storing the trades data
class Trade:
    def __init__(self,base,currency,balance):
        self.base,self.currency, self.balance, self.quantity = base,currency,balance,0 
        self.log = []
        return
    
    def place(self, data, view=False):
        
        # Purchase transaction
        self.quantity = self.balance/data["sell_price"]
        purchase = data["sell_price"]*self.quantity
        self.balance=self.balance-purchase

        # Sale transaction
        sale = self.quantity*data["buy_price"]
        self.quantity = self.quantity-self.quantity
        self.balance = self.balance+sale

        trade = {
            "time": datetime.datetime.now().isoformat(),
            "purchase": purchase,
            "sale": sale,
            "balance": self.balance,
            "data": data
        }
        self.log.append(trade)
        if view==True: print(trade)
        return