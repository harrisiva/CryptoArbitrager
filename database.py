import sqlite3
import datetime
from test import coinbase

conn = sqlite3.connect(":memory:")
c:sqlite3.Cursor = conn.cursor()

# Use endpoints.keys() to get the different endpoints for which we need to create a table

# for time, ISO8601 strings "YYYY-MM-DD HH:MM:SS.SSS"

# Two types of tables
# One table per broker that contains the entry time for bid and ask 
# One table with the most recent data for each broker

endpoint = 'coinbase'
c.execute(f'CREATE TABLE {endpoint}(time text,bid real,ask real)')
conn.commit()

coinbase_data = coinbase()
print(str(datetime.datetime.now().isoformat()))
c.execute(f'INSERT INTO {endpoint} VALUES (?,?,?)',(str(datetime.datetime.now().isoformat()), coinbase_data['bid'], coinbase_data['ask']))

c.execute(f'SELECT * FROM {endpoint} ORDER BY time DESC')
print(c.fetchall())
# Just get the cheapest ask and the most expensive ask
# Find the diff between each bid and ask
# Find the greatest diff from ^
# That is the profit margin on trading each unit of the base (coin)


# To actually tade the initial amount (order book functionality)
# Buy the initial amount worth of the coin at the ask price
# Sell the number of coins for the bid price
# Update the balance and log the trade

conn.close()