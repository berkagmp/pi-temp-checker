import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

ADDRESS = config.EMAIL_ADDRESS
PASSWORD = config.EMAIL_PASSWORD
HOST = config.EMAIL_HOST
PORT = config.EMAIL_PORT


def send_email(body):
    message = 'TEST Email'

    # set up the SMTP server
    s = smtplib.SMTP(host=HOST, port=PORT)
    s.starttls()
    s.login(ADDRESS, config.PASSWORD)

    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    # message = message_template.substitute(PERSON_NAME=name.title())

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From'] = ADDRESS
    msg['To'] = ADDRESS
    msg['Subject'] = body

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
