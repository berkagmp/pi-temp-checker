import smtplib
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

from mysql.connector import MySQLConnection
import config

import sentry_sdk
sentry_sdk.init(
    "https://63fb277c6fad4fefb7f0aa01eea20850@o456682.ingest.sentry.io/5450003",
    traces_sample_rate=1.0
)

ADDRESS = config.EMAIL_ADDRESS
PASSWORD = config.EMAIL_PASSWORD
HOST = config.EMAIL_HOST
PORT = config.EMAIL_PORT

DB_CONFIG = config.db_config


def delete_email(id):
    query = "DELETE FROM email_queue WHERE id = %s"
    args = (id,)

    try:
        conn = MySQLConnection(**DB_CONFIG)

        cursor = conn.cursor()
        cursor.execute(query, args)
    except Exception as exception:
        print('Exception: %s' % exception)
    finally:
        cursor.close()
        conn.close()


def get_email_queue():
    query = "SELECT id, recipient, cc, subject, body, created_at FROM email_queue"

    conn = MySQLConnection(**DB_CONFIG)

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
    except Exception as exception:
        print('Exception: %s' % exception)
    finally:
        cursor.close()
        conn.close()

    return result


def send_email(email):
    recipient = email[1]
    subject = email[3]
    created_at = email[5].strftime("%Y/%m/%d, %H:%M:%S")
    message = email[4] + "\n\n" + created_at

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
    msg['To'] = recipient
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()


def email_sender():
  email_data = get_email_queue()

  for email in email_data:
    try:
      send_email(email)
      delete_email(email[0])
    except Exception as exception:
      print('Exception: %s' % exception)
      pass


if __name__ == "__main__":
    email_sender()
