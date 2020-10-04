from mysql.connector import MySQLConnection

import config
import sentry_sdk
sentry_sdk.init(
    "https://63fb277c6fad4fefb7f0aa01eea20850@o456682.ingest.sentry.io/5450003",
    traces_sample_rate=1.0
)


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
