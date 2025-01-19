from os import getenv
#import mysql.connector
import mariadb

def __open__():
    connection = mariadb.connect(
        user="gps",
        password=getenv("DB_PASSWD"),
        host="192.168.0.65",
        database="gpstracker",
    )
    cursor = connection.cursor(dictionary=True)

    return (connection, cursor)


def __close__(connection, cursor):
    connection.close()
    cursor.close()


def query(query, data=[], insert=False):
    (connection, cursor) = __open__()
    cursor.execute(query, data)
    data = cursor.fetchall()

    if insert:
        connection.commit()

    __close__(connection, cursor)

    return data
