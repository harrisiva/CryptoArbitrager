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

brokers = {
    "coinbase": client.coinbase,
    "kraken": client.kraken
}

# Populate the book for the first time
for broker in brokers.keys():
    data = brokers[broker]()
    book.createBroker(broker)
    book.insertBroker(broker,data)

book_data = book.view(asdict=True) # By converting this ones response to a dict, we reduce the time complexity when calculating the diff in amounts (profit margin)

# Get the max diff between the combinations of bid and asks
# The number of brokers is the len of book_data
# Each book_data item contains the bid and ask
# Get the natural difference of each book_data and use this to set the initial desired diff data
#   each time when setting the disired diff, take the bid and ask amount and broker data as well
# For each broker, get the diff of their bid with all other asks, their ask with all other bids

print("Number of brokers:", len(brokers))
# for each broker
#   get the bid and ask price data
#   iterate over the other brokers
#   
