from alpha_vantage.timeseries import TimeSeries             # Used for stock prices


# The main function
def main():
    ticker = str(input("Enter the stock ticker: "))         # Get the stock ticker from the user
    market_open = True                                      # Initialize market_open to true
    while market_open:                                      # While the market is open
        market_open = calc_price(ticker)                    # Calculate and display the stock price


# Function that calculates the current price of a stock
def calc_price(ticker):
    api_key = "Insert Key Here"                             # My API key for https://www.alphavantage.co/
    ts = TimeSeries(key=api_key, output_format="json")      # Create an object ts, of the class TimeSeries

    data, meta_data = ts.get_intraday(symbol=ticker,        # Get the price of the stock for each minute
                                    interval="1min",        # One minute is the smallest interval allowed
                                    outputsize="compact")   # Compact will show only the last 100 minutes

    current_time = str(next(iter(data)))                    # Get the time of the last stock price update
    market_open = is_market_open(current_time)              # Determine if the market is open

    close_price = float(data[current_time]["4. close"])     # Get the close of the minute price (the last price)
    open_price = float(data[current_time]["1. open"])       # Get the open of the minute price

    percent_change = (close_price - open_price)/open_price  # Get the decimal change in price
    percent_change = percent_change * 100                   # Turn the decimal to a percent
    percent_change = round(percent_change, 3)               # Round the percent change to 3 digits

    print(ticker)                                           # Print the stock ticker
    print("Last Price: $" + str(close_price))               # Print the last price
    print("Percent Change: " + str(percent_change) + "%")   # Print the percent change

    return market_open                                      # Return true if the market is open, false otherwise


# Function that determines if the market is open, given the
# last time a stock price was updated
def is_market_open(current_time):
    start_index = 0                                         # Initialize the starting index of the string to 0
    end_index = 0                                           # Initialize the ending index of the string to 0
    for i in range(len(current_time)):                      # Iterate through the string
        if current_time[i] == " ":                          # If the current character is a space
            start_index = (i + 1)                           # Then the next char is where we want to start
        elif current_time[i] == ":":                        # Else if the current character is a colon
            end_index = i                                   # That is where we want to end
            break                                           # We also want to end the loop here

    current_hour = current_time[start_index:end_index]      # Get the hour from the current_time (it is a substring)
    if current_hour == "16":                                # If the hour is 16
        return False                                        # Then the market is closed
    else:                                                   # Otherwise
        return True                                         # The market is open


main()                                                      # Call the main function
