from os import getenv
import mysql.connector


def __open__():
    connection = mysql.connector.connect(
        user="gps",
        password=getenv("DB_PASSWD"),
        host="localhost",
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
