# This file contains the EmailNotif class
import smtplib                                              # Used to send email alerts


class EmailNotif:
    def __init__(self, recipient, sender, password):        # The constructor
        self.recipient = recipient                          # Set the recipient data field
        self.sender = sender                                # Set the sender data field
        self.password = password                            # Set the password data field

    def send_email(self, ticker, price, change):            # Method that sends the email alert
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()                                     # Extended hello (SMTP protocol)
            smtp.starttls()                                 # Encryption
            smtp.ehlo()                                     # Extended hello (SMTP protocol)
            smtp.login(self.sender, self.password)          # Login to the sender email
            subject = "Market Change Alert!"                # Set the email's subject
            if change > 0:                                  # If the percent change is positive
                body = "The stock " + ticker +\
                        " has gone up by " +\
                        str(change) + "% and is " \
                        "currently trading at $" +\
                        str(price)                          # Set the message body to this message
            else:                                           # Else the percent change must be negative
                body = "The stock " + ticker + \
                        " has gone down by " + \
                        str(change) + "% and is " \
                        "currently trading at $" +\
                        str(price)                          # Set the message body to this message

            msg = 'Subject: ' + subject + '\n\n'            # Create the email message
            msg += body.format(subject, body)               #
            smtp.sendmail(self.sender, self.recipient, msg) # Send the email
