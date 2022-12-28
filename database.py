import sqlite3
import datetime

class Book:
    # Initalize the connection, cursor, and create a table for the book
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        # Create a table for the book
        self.c.execute("CREATE TABLE book (broker text, time text, bid real, ask real)")
        self.conn.commit()
        return

    # Create a table for the endpoint/broker
    def createBroker(self, broker): 
        # Create a table for the broker
        self.c.execute(f'CREATE TABLE {broker}(time text,bid real,ask real)')
        self.conn.commit()
        # Create a entry for the broker in the book with None for bid and ask
        self.c.execute("INSERT INTO book VALUES (?,?,?,?)",(broker, str(datetime.datetime.now().isoformat()),None,None))
        self.conn.commit()
        return

    # Insert data into the endpoint/broker table
    def insertBroker(self, broker, data): 
        now = str(datetime.datetime.now().isoformat())
        self.c.execute(f'INSERT INTO {broker} VALUES (?,?,?)',(now, data['bid'], data['ask']))
        self.conn.commit()
        # Update the book
        self.c.execute(f'UPDATE book SET time=?,bid=?,ask=? WHERE broker="{broker}"',(now,data['bid'],data['ask']))
        self.conn.commit()
        return

    # get/view the book's data
    def view(self):
        self.c.execute('SELECT * FROM book')
        data = self.c.fetchall()
        print(data)
        return data

    # Close the cursor and the connection
    def close(self):
        try:
            self.conn.close()
            self.c.close()
        except Exception as e:
            print("Failed to close connection and cursor.")
            print(str(e))
        return

# Order Book Concept:
# To actually tade the initial amount (order book functionality)
# Buy the initial amount worth of the coin at the ask price
# Sell the number of coins for the bid price
# Update the balance and log the trade