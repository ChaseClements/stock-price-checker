# This file contains the StockChecker class

from yahoo_fin import stock_info as si                  # Yahoo finance is used to check the prices
import requests                                         # Needed to use yahoo_fin
import requests_html                                    # Needed to use yahoo_fin


class StockChecker:                                     # The StockChecker class
    def __init__(self, ticker):                         # Constructor, the ticker is passed as an argument
        self.ticker = ticker.upper()                    # Set the ticker attribute
        self.__update_price()                           # Set the price of the stock

    def display_stock(self):                            # Method that displays the stock's current price
        self.__update_price()                           # Get the latest price
        print("Ticker: " + str(self.ticker))            # Print the ticker
        print("Price: $" + str(self.price))             # Print the price

    def __update_price(self):                           # Method that updates the stock price (Private)
        self.price = si.get_live_price(self.ticker)     # Get the price from yahoo finance
        self.price = round(self.price, 2)               # Round it to two decimals

    def get_price(self):                                # Method that returns the price of a stock
        self.__update_price()                           # Call the method that updates the price
        return self.price                               # Return the updated price
