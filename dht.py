import subprocess
from mysql.connector import MySQLConnection

import config
import notification

import sentry_sdk
sentry_sdk.init(
    "https://63fb277c6fad4fefb7f0aa01eea20850@o456682.ingest.sentry.io/5450003",
    traces_sample_rate=1.0
)

MAX_TEMPERATURE = config.MAX_TEMPERATURE
MAX_HUMIDITY = config.MAX_HUMIDITY

ADDRESS = config.EMAIL_ADDRESS


def insertMySQL(temp, humidity):
  query = "INSERT INTO soap_room(temp, humidity) VALUES(%s, %s)"
  args = (temp, humidity,)

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


def dht():
  # Read temperature, humidity from DHT11
  data = subprocess.check_output(['dht']).decode()
  array = str(data).split('/')

  temperature = array[0]
  humidity = array[1]

  # Insert Temp and Humidity to DB
  insertMySQL(temperature, humidity)

  # Notification
  if(float(temperature) > MAX_TEMPERATURE or float(humidity) > MAX_HUMIDITY):
    recipient = ADDRESS
    subject = 'Soap Room Alert'
    body = 'Temperature = ' + \
        str(temperature) + " C / " + 'Humidity = ' + str(humidity) + ' %'

    notification.insert_email(recipient, None, subject, body)


if __name__ == "__main__":
    dht()
