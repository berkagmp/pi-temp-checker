import subprocess
from datetime import datetime
from mysql.connector import MySQLConnection
import pymongo
import pytz
import datetime

import config


def insertMySQL(array):
  cpu = float(array[1])
  gpu = float(array[2][0:array[2].find("'")])

  query = "INSERT INTO temp(cpu, gpu) VALUES(%s, %s)"
  args = (cpu, gpu,)

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


def insertMongoDB(array):
    cpu = float(array[1])
    gpu = float(array[2][0:array[2].find("'")])

    timezone = pytz.timezone(config.timezone)
    aware_datetime = timezone.localize(datetime.datetime.now())

    print(aware_datetime.isoformat())

    myclient = pymongo.MongoClient(config.mongo_client)
    mydb = myclient[config.database]
    mycol = mydb[config.collection]

    data = {"cpu": cpu, "gpu": gpu,
            "created_at": aware_datetime.replace(tzinfo=pytz.UTC)}

    x = mycol.insert_one(data)


temp = subprocess.check_output(['temp'])
# temp = "2020-09-06 18:11:34/44.7/45.0'C"

array = str(temp).split('/')

insertMySQL(array)
insertMongoDB(array)
