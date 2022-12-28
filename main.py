# Get the arguments from the user (refresh time, failsafe time, base, currency)
# 
# Get the endpoint names by using endpoint.keys() (print the number of combinations (or log for future reference))
# Create a table for each broker/endpoint
# Create the book table
# 
# Initialize the last update datetime variable
# Iterate while current_time=last_update + refresh_period (seconds)
#
#   Refreshing and DB Handling:
#   Iterate over the endpoints/broker
#   Create a database entry to the broker/endpoint table
#   Update the book table for the current endpoint/broker

#   Trading:
#   Perform the difference on the different combinations
#   Find the maximum difference
#   If the entry pair for the maximum difference both have a timestamp of that indicates that it was updated:
#       Perform the trade if it is within a failsafe period (s) from the update time
#       Log the trade time

# Logic for API and Database Integration
from database import Book
from api import API

book = Book()
client = API("BTC","USD")

BROKERS = {
    "coinbase": client.coinbase,
    "kraken": client.kraken
}

# Populate the book for the first time
for broker in BROKERS.keys():
    data = BROKERS[broker]()
    book.createBroker(broker)
    book.insertBroker(broker,data)

# Refresh the book
for broker in BROKERS.keys(): book.insertBroker(broker,BROKERS[broker]())

book_data = book.view(asdict=True) # By converting this ones response to a dict, we reduce the time complexity when calculating the diff in amounts (profit margin)

# Find the most profitable trade (highest profit margin)
highest = [0,{}]
for selling_broker in book_data:
    ask = book_data[selling_broker]['ask']
    buyers = [buyer_broker for buyer_broker in book_data if buyer_broker!=selling_broker]
    for buyer in buyers:
        margin = book_data[buyer]['bid']-ask
        difference = {
            "seller": selling_broker,
            "buyer": buyer,
            "sell_price": ask,
            "buy_price": book_data[buyer]['bid'],
            "margin": margin 
        }
        if margin>=highest[0]: highest[1]=difference