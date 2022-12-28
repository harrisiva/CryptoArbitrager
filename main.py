from database import Book
from api import API
import datetime, argparse
import functions

#TODO: Get the arguments from the user (refresh time, failsafe time, base, currency)

REFRESH = 5 # Refresh time interval in seconds

book = Book() # Initialize a DB connection, cusor, and create a table for the book
client = API("BTC","USD") # Initialize a object containing methods that provide data from different brokers for the given base and currency

BROKERS = { # Initialize a dictionary of BROKERS and their function (that returns bid and ask) from the client instance
    "coinbase": client.coinbase,
    "kraken": client.kraken
}

# Populate the book for the first time by creating a table for each broker/endpoint
refreshed = datetime.datetime.now() # Store the time of the database population/update
for broker in BROKERS.keys():
    data = BROKERS[broker]()
    book.createBroker(broker)
    book.insertBroker(broker,data)

# Perform the first trade if required
print(functions.mostprofitable(book.view(asdict=True)))

while True:
    if datetime.datetime.now()>=(refreshed+datetime.timedelta(seconds=REFRESH)):
        
        # Refresh the brokers data (also updates the book)
        for broker in BROKERS.keys(): book.insertBroker(broker,BROKERS[broker]())
        
        # Find the most profitable trade (highest profit margin)
        print(functions.mostprofitable(book.view(asdict=True)))