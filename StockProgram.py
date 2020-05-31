import pandas as pd                                         # Used for displaying stock prices
from alpha_vantage.timeseries import TimeSeries             # Used for stock prices


# The main function
def main():
    ticker = str(input("Enter the stock ticker: "))         # Get the stock ticker from the user
    calc_price(ticker)                                      # Calculate and display the stock price


# Function that calculates the current price of a stock
def calc_price(ticker):
    api_key = "Insert Key Here"                             # API key for https://www.alphavantage.co/
    ts = TimeSeries(key=api_key, output_format="pandas")    # Create an object ts, of the class TimeSeries

    data, meta_data = ts.get_intraday(symbol=ticker,        # Get the price of the stock for each minute
                                    interval="1min",        # One minute is the smallest interval allowed
                                    outputsize="compact")   # Compact will show only the last 100 minutes

    close_data = data["4. close"]                           # Set the last price of each minute to closeData
    last_price = close_data[0]                              # Get the final price of the most recent minute
    percent_change = close_data.pct_change()                # Get the percent change from each minute to the next
    last_change = percent_change[0]                         # Get the last percent change

    last_change = str(last_change)                          # Convert last_change to a string
    last_price = str(last_price)                            # Convert last_price to a string

    print(ticker)                                           # Print the stock ticker
    print("Last Price: " + last_price)                      # Print the last price
    print("Percent Change: " + last_change)                 # Print the percent change


main()                                                      # Call the main function
