from database import Book
from api import API
from trade import Trade
import datetime, argparse
import functions
#TODO: Add logging

parser = argparse.ArgumentParser()
parser.add_argument("-r",type=int,help="Refresh rate for updating database's price data in seconds. Default is 30 seconds.")
parser.add_argument("-b",type=str,help="Base currency as a string. (E.X. BTC)", required=True)
parser.add_argument("-c",type=str,help="Currenct for exchange as a string. (E.X. USD)", required=True)
parser.add_argument("-ib",type=float, help="Initial Balance", required=True)
args = parser.parse_args()

REFRESH = args.r if args.r else 30 # Refresh time interval in seconds
BASE = args.b
CURRENCY = args.c
BALANCE = args.ib

trade = Trade(BASE,CURRENCY,BALANCE)
book = Book() # Initialize a DB connection, cusor, and create a table for the book
client = API(trade.base,trade.currency) # Initialize a object containing methods that provide data from different brokers for the given base and currency

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
trade.place(functions.mostprofitable(book.view(asdict=True))[1],view=True)

while True:
    if datetime.datetime.now()>=(refreshed+datetime.timedelta(seconds=REFRESH)):
        
        # Refresh the brokers data (also updates the book)
        for broker in BROKERS.keys(): book.insertBroker(broker,BROKERS[broker]())
        refreshed = datetime.datetime.now()

        # Find the most profitable trade (highest profit margin)
        trade.place(functions.mostprofitable(book.view(asdict=True))[1],view=True)