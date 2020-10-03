import smtplib
from mysql.connector import MySQLConnection
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

ADDRESS = config.EMAIL_ADDRESS
PASSWORD = config.EMAIL_PASSWORD
HOST = config.EMAIL_HOST
PORT = config.EMAIL_PORT


def insert_email(recipient, cc, subject, body):
    query = "INSERT INTO email_queue(recipient, cc, subject, body) VALUES(%s, %s, %s, %s)"
    args = (recipient, cc, subject, body, )

    db_config = config.db_config

    conn = MySQLConnection(**db_config)

    try:
        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Exception as exception:
        print('Exception: %s' % exception)
        conn.rollback()
    finally:
        cursor.close()


def send_email(subject, message):
    # set up the SMTP server
    s = smtplib.SMTP(host=HOST, port=PORT)
    s.starttls()
    s.login(ADDRESS, PASSWORD)

    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    # message = message_template.substitute(PERSON_NAME=name.title())

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From'] = ADDRESS
    msg['To'] = ADDRESS
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
