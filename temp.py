import subprocess
from datetime import datetime
from mysql.connector import MySQLConnection

import config


def insertDB(array):
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


temp = subprocess.check_output(['temp'])
# temp = "2020-09-06 18:11:34/44.7/45.0'C"

array = str(temp).split('/')
insertDB(array)
