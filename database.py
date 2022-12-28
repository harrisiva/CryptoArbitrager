import sqlite3
import datetime
from test import coinbase

conn = sqlite3.connect(":memory:")
c:sqlite3.Cursor = conn.cursor()

# Use endpoints.keys() to get the different endpoints for which we need to create a table

# for time, ISO8601 strings "YYYY-MM-DD HH:MM:SS.SSS"

# Two types of tables
# One table per broker that contains the entry time for bid and ask 

endpoint = 'coinbase'

# Create a table for the endpoint/broker
c.execute(f'CREATE TABLE {endpoint}(time text,bid real,ask real)')
conn.commit()

coinbase_data = coinbase()


# Insert data into the endpoint/broker table
c.execute(f'INSERT INTO {endpoint} VALUES (?,?,?)',(str(datetime.datetime.now().isoformat()), coinbase_data['bid'], coinbase_data['ask']))

# Select the most recent data for the given endpoint/broker
c.execute(f'SELECT * FROM {endpoint} ORDER BY time DESC')
recent_data = c.fetchone()

# Create the book table
c.execute("CREATE TABLE book (broker text, time text, bid real, ask real)")
conn.commit()

# Insert a broker into the table
c.execute("INSERT INTO book VALUES (?,?,?,?)",(endpoint, str(datetime.datetime.now().isoformat()), recent_data[1], recent_data[2]))
conn.commit()

# Get the book (last refresh) entry for a broker
c.execute(f'SELECT * FROM book WHERE broker="{endpoint}"')
first_data = c.fetchone()
print(first_data)


bid = coinbase_data['bid']
ask = coinbase_data['ask']

# Update data for a endpoint/broker in the book
c.execute(f'UPDATE book SET time=?,bid=?,ask=? WHERE broker="{endpoint}"',(str(datetime.datetime.now().isoformat()),bid,ask))
conn.commit()

# Get the latest entry for an endpoint/broker
c.execute(f'SELECT * FROM book WHERE broker="{endpoint}"')
second_data = c.fetchone()
print(second_data)


# Just get the cheapest ask and the most expensive ask
# Find the diff between each bid and ask
# Find the greatest diff from ^
# That is the profit margin on trading each unit of the base (coin)


# To actually tade the initial amount (order book functionality)
# Buy the initial amount worth of the coin at the ask price
# Sell the number of coins for the bid price
# Update the balance and log the trade

conn.close()