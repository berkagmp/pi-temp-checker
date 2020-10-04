from mysql.connector import MySQLConnection

import config


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
