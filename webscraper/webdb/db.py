import sqlite3
import os
import logging
module_logger = logging.getLogger('webdb.db')

def open_db_readonly(db_file):
    uri = "file:./{}?mode=ro".format(db_file)
    conn = sqlite3.connect(uri, uri=True)
    return conn

def create_or_open_db(db_file):
    """ Erstellt oder öffnet eine sqlite3 Datenbank. 

    Arguments:
        db_file -- Name der Datenbank

    Returns:
        Eine sqlite3 Datenbank connection.
    """
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)

    if db_is_new:
        module_logger.info("Creating tables...")

        sql = ("CREATE TABLE IF NOT EXISTS SESSIONS ("
               "SESSION_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "START_TIMESTAMP REAL,"
               "END_TIMESTAMP REAL"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS REQUESTS ("
               "REQUEST_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "URI_ID INTEGER,"
               "SESSION_ID INTEGER,"
               "RESPONSE_ID INTEGER"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS RESPONSES ("
               "RESPONSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "STATUS_CODE INTEGER,"
               "TIMESTAMP REAL,"
               "CONTENT_TYPE_ID INTEGER,"
               "CONTENT_ID INTEGER"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS CONTENT_CACHE ("
               "CONTENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "CONTENT BLOB"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS CONTENT_TYPE_CACHE ("
               "CONTENT_TYPE_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "CONTENT_TYPE TEXT"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS URI_CACHE ("
               "URI_ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "SCHEME TEXT,"
               "NETLOC TEXT,"
               "PATH TEXT,"
               "PARAMS TEXT,"
               "QUERY TEXT,"
               "FRAGMENT TEXT"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)
    else:
        module_logger.info("Tables exists.")

    return conn

