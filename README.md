# CryptoArbitrageur
## Overview
This program automates the price arbitrage trading model for crypto currencies using a SQLite3 database and a component based architecture that follow OOP principles.
## Design
There are three main components for this program.
- Book: Contains the DB tables for the book (the last updated bid and ask price for multiple brokers).
- API: Using the request library, this component provides the bid and ask price from various crypto currency brokers.
- Trade: This component takes the users inputs, updates balances and logs trades.
## Data Limitations
Since the program is still under developement, price data is currently limited to Kraken and Coinbase. Due to the type of software architecture used, scaling the program to contain other brokers is relatively easy (coming soon).
## Tutorial
To run the program:
```
python main.py -r 5 -b BTC -c USD -ib 10000
```
- Refresh Rate (r) is the refresh time for the database.
- Base (b) is the base currency/crypto.
- Currency (c) is the exchange currency.
- Initial Balance (ib) is the initial balance of the user.

To view other flags:
```
python main.py -h
```
---
This program was developed in ***<6 hours***