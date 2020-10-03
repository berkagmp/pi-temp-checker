import subprocess
from mysql.connector import MySQLConnection

import config
import notification

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


def readDHT():
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
    subject = 'SOAP ROOM ALERT'
    body = 'Temperature = ' + \
        str(temperature) + " C / " + 'Humidity = ' + str(MAX_HUMIDITY) + ' %'

    notification.insert_email(recipient, None, subject, body)


readDHT()
