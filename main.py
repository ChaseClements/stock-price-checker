# The file contain the main function

from StockChecker import StockChecker                           # Import the class that checks stock prices
from EmailNotifications import EmailNotif                       # Import the class that sends email notifications
from datetime import datetime                                   # Import datetime to get current time
import time                                                     # Import time to sleep
import pytz                                                     # Import to set the timezone to EST


# The main function
def main():
    print("Welcome to the stock checker program!")              # Welcome the user to the program
    end = 0                                                     # Initialize end to 0
    while end != -1:                                            # While end is not -1
        option = display_menu()                                 # Call the function that displays the menu
        if option == 1:                                         # If the option is 1
            look_up_price()                                     # Look up the price of a stock
        elif option == 2:                                       # Else if the option is 2
            continual_lookup()                                  # Continually lookup the price of a stock
        elif option == 3:                                       # Else if the option is 3
            email_notifs()                                      # Continually look up and send email notifications
        end = int(input("Enter -1 to quit the program, "        # Ask user if he/she would like to end the program
                        "or any other integer to continue: "))  #


# The function that displays a menu of options to the user
def display_menu():
    choice = 0                                                  # Initialize the choice to 0 to enter the loop
    while choice < 1 or choice > 3:                             # While the choice is not one of the options
        print()                                                 # Print a blank line
        print("Stock Checker Menu")                             # Print a welcome statement to the user
        print("1. Look up the price of a stock")                #
        print("2. Enter continual price lookup mode")           #
        print("3. Enter email notifications mode")              #
        choice = int(input("Enter your choice: "))              # Prompt the user to enter his/her choice
    return choice                                               # Return the choice to main


# Function that looks up the price of a stock
def look_up_price():
    print()                                                     # Print a blank line
    ticker = str(input("Enter the stock ticker: "))             # Prompt the user to enter a ticker
    stock = StockChecker(ticker)                                # Create the StockChecker object
    stock.display_stock()                                       # Display the stock and it's price


# Function that sets up the email updates
def set_email_updates():
    print()                                                     # Print a blank line
    choice = int(input("If you would like an explanation "      # Allow user to get an explanation of how to set
                       "of how to set up email alerts, "        # up email alerts if he/she likes
                       "enter 1, otherwise enter "              #
                       "any integer: "))                        #
    if choice == 1:                                             # If the user entered 1
        explain_email()                                         # Explain how to set up email notifications

    recipient = input("Enter the email of the recipient: ")     # Prompt user for the recipient email
    sender = input("Enter the email of the sender: ")           # Prompt user for the sender's email
    password = input("Enter the app password of the sender: ")  # Prompt user for the sender's app password

    emailnotif = EmailNotif(recipient, sender, password)        # Create the EmailNotif object

    return emailnotif                                           # Return the emailnotif object


# Function that explains to the user how to set up email alerts
def explain_email():
    print("To set up email alerts, you need to go to "          # Explain to user how to set up email alerts
          "myaccount.google.com")                               #
    print("Click on the security tab on the left and turn on"   #
          " 2-Step Verification")                               #
    print("Finally, generate an app password for the account")  #


# Function that continually looks up the price of a certain stock
# while the market is open
def continual_lookup():
    market_is_open = market_open()                              # Find out if the market is open
    if not market_is_open:                                      # If the market is not open
        print()                                                 # Print a blank line
        print("Error, the market is not open")                  # Print an error
        return                                                  # Return to main

    print()                                                     # Print a blank line
    print("Welcome to continual price lookup mode!")            # Welcome the user to this function
    print("To exit the mode you have to exit the program, or"   # Tell user how to exit
          " wait until the end of the trading day")             #

    ticker = input("Enter a ticker to continually look up: ")   # Get the ticker from the user
    stock = StockChecker(ticker)                                # Create the stock checker object

    while market_open():                                        # While the market is open
        stock.display_stock()                                   # Display the stock
        time.sleep(2)                                           # Wait 2 seconds (chosen due to api limits)


# Function that monitors the market and sends emails
def email_notifs():
    market_is_open = market_open()                              # Find out if the market is open
    if not market_is_open:                                      # If the market is not open
        print()                                                 # Print a blank line
        print("Error, the market is not open")                  # Print an error
        return                                                  # Return to main

    email_notif = set_email_updates()                           # Call function to set up updates before proceeding
    print()                                                     # Print a blank line
    print("Welcome to email notifications mode!")               # Welcome the user to email notifications mode
    print("To exit the mode you have to exit the program, or"   # Tell user how to exit
          " wait until the end of the trading day")             #

    interval = int(input("Enter the number of seconds to"       # Prompt user for the number of seconds to wait in
                         " wait between price updates: "))      # between price updates
    max_change = float(input("Enter the percent change "        # Prompt user for the percent change needed to receive
                             "necessary within each interval "  # an email
                             "in order to receive an email: "))
    display = str(input("Enter y to display the stock "         # Ask user if he/she would like the information
                        "information on console as well: "))    # displayed on the console as well

    ticker = input("Enter a ticker to watch: ")                 # Get the ticker from the user
    ticker = ticker.upper()                                     # Make the ticker upper case
    stock = StockChecker(ticker)                                # Create the StockChecker object
    last_price = stock.get_price()                              # Get the price

    while market_open():                                        # While the market is open
        print()                                                 # Print a blank line
        time.sleep(interval)                                    # Wait to get the stock price
        new_price = stock.get_price()                           # Get the new stock price
        change = ((new_price - last_price)/last_price) * 100    # Calculate the percent change

        if abs(change) > abs(max_change):                       # If the change is greater than the max change allowed
            email_notif.send_email(ticker, new_price, change)   # Send the email

        if display == "y":                                      # If the user would like the stock info displayed
            print("Ticker: " + str(ticker))                     # Print the ticker
            print("Price: $" + str(new_price))                  # Print the price

        last_price = new_price                                  # Set the last price to the new price


# Function that determines if the market is open
def market_open():
    est = pytz.timezone('America/New_York')                     # Set the time zone to EST
    current_time = datetime.now(est)                            # Get the current time in EST
    current_hour = int(current_time.hour)                       # Get the current hour

    if 16 > current_hour >= 9:                                  # While the market is open
        if current_hour == 9 and int(current_time.minute) < 30: # If it is past 9 but not yet 9:30 in NYC
            return False                                        # Return false
        else:                                                   # Else: current time is between 9:30 and 4:00
            return True                                         # Return True
    else:
        return False                                            # Return false


main()
