import os                                                   # Used to get the environment variables
from alpha_vantage.timeseries import TimeSeries             # Used for stock prices
import time                                                 # Used to pause the loop for 60 seconds
import smtplib                                              # Used to send email alerts


# The main function
def main():
    ticker = str(input("Enter the stock ticker: "))         # Get the stock ticker from the user
    loop, interval = set_settings()                         # Call the function that gets the users settings

    market_open = True                                      # Initialize market_open to true
    while market_open:                                      # While the market is open
        market_open = calc_price(ticker, interval)          # Calculate and display the stock price
        if loop != "y":                                     # If the user does not want to loop
            break                                           # Break the loop
        elif market_open:                                   # Else if the market is open
            time.sleep(interval)                            # Pause for the interval to wait for update


# Function that sets the users settings
def set_settings():
    loop = str(input("Would you like to continue "          # Determine if user would like to get
                     "getting the price while/if "          # the stock price until the
                     "the market is open? (y/n): "))        # end of the day

    print("Menu for how often the price updates:")          # Beginning of price update menu
    print("1. Update price every hour")                     # Display option 1
    print("2. Update price every 30 minutes")               # Display option 2
    print("3. Update price every 15 minutes")               # Display option 3
    print("4. Update price every 5 minutes")                # Display option 4
    print("5. Update price every minute")                   # Display option 5
    choice = int(input("Enter interval: "))                 # Prompt user to enter his/her choice

    if choice == 1:                                         # If the user chose 1
        interval = 3600                                     # Set the interval to 3,600 seconds
    elif choice == 2:                                       # If the user chose 2
        interval = 1800                                     # Set the interval to 1,800 seconds
    elif choice == 3:                                       # If the user chose 3
        interval = 900                                      # Set the interval to 900 seconds
    elif choice == 4:                                       # If the user chose 4
        interval = 300                                      # Set the interval to 300 seconds
    else:                                                   # By default
        interval = 60                                       # Set the interval to 60 seconds

    return loop, interval                                   # Return the settings


# Function that calculates the current price of a stock
def calc_price(ticker, interval):
    api_key = os.environ.get("ALPHAVANTAGE_API")            # My API key for www.alphavantage.co in environment var
    ts = TimeSeries(key=api_key, output_format="json")      # Create an object ts, of the class TimeSeries

    wait_time = reformat_interval(interval)                 # Reformat the interval so that it works with the API

    data, meta_data = ts.get_intraday(symbol=ticker,        # Get the price of the stock for each minute
                                      interval=wait_time)   # Pass the wait time that the user chose

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

    check_percent_change(percent_change, ticker)            # Check the percent change to see if email is needed

    return market_open                                      # Return true if the market is open, false otherwise


# Function that fixes the interval time to work with the
# alpha vantage API
def reformat_interval(interval):
    if interval == 3600:                                    # If the interval was 3,600 seconds
        return "60min"                                      # Return 60min as string
    elif interval == 1800:                                  # If the interval is 1,800 seconds
        return "30min"                                      # Return 30min as string
    elif interval == 900:                                   # If the interval is 900 seconds
        return "15min"                                      # Return 15min as string
    elif interval == 300:                                   # If the interval is 300 seconds
        return "5min"                                       # Return 5min as string
    else:                                                   # If the interval is anything else
        return "1min"                                       # Return 1min as string


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


# Function that emails the user if the market has
# moved a predetermined amount
def check_percent_change(percent_change, ticker):
    if abs(percent_change) > 0.1:                           # If the percent change is greater than 0.1%
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:   # Send an email alert
            # Please note that to get an app password, you must have gmail two factor authentication on and go to
            # app passwords in settings -> security for the sender's gmail account
            email_address = os.environ.get("EMAIL_ADDRESS")     # Set email_address to the sender's email address
            email_password = os.environ.get("EMAIL_PASSWORD")   # Set email_password to the sender's app password

            smtp.ehlo()                                     # Extended hello (SMTP protocol)
            smtp.starttls()                                 # Encryption
            smtp.ehlo()                                     # Extended hello (SMTP protocol)
            smtp.login(email_address, email_password)       # Login to the sender email

            subject = "Market Change Alert!"                # Set the email's subject
            if percent_change > 0:                          # If the percent change is positive
                body = "The stock " + ticker +\
                             " has gone up by " +\
                             str(percent_change) + "%"      # Set the message body to this message
            else:                                           # Else the percent change must be negative
                body = "The stock " + ticker +\
                             " has gone down by " +\
                             str(percent_change) + "%"      # Set the message body to this message

            msg = 'Subject: ' + subject + '\n\n'            # Create the email message
            msg += body.format(subject, body)               #
            recipient = os.environ.get("EMAIL_RECIPIENT")   # Set the recipient address
            smtp.sendmail(email_address, recipient, msg)    # Send the email


main()                                                      # Call the main function
