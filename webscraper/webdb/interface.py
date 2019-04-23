"""
Modul zum hinzufügen von http(s) requests und responses in eine sqllite3 Datenbank. Die 
requests und responses werden versioniert.
"""

import sqlite3
import os
import logging
from urllib.parse import urlparse, urlunparse

from webtypes.session import Session
from webtypes.response import Response
from webtypes.request import Request
from datetime import datetime

import webdb.cache as cache
import bz2

from webdb.exceptions import (
    UriNotFound,
    ResponseNotFound
)

module_logger = logging.getLogger('webdb.interface')


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


def insert_session(cursor, session):
    sql = ("INSERT INTO SESSIONS ("
           "START_TIMESTAMP,"
           "END_TIMESTAMP"
           ") VALUES (?, ?);")

    cursor.execute(sql, [
        session.start_datetime.timestamp(),
        -1.0,  # endtime unkmown
    ])

    rid = int(cursor.lastrowid)
    module_logger.debug(
        "sql: INSERT %s into SESSIONS. Row id is %i.", session, rid)
    return rid


def update_session(cursor, session_id, session):
    sql = ("UPDATE SESSIONS SET "
           "START_TIMESTAMP = :start_timestamp, "
           "END_TIMESTAMP = :end_timestamp "
           "WHERE SESSION_ID = :session_id;")

    params = {
        'session_id': session_id,
        'start_timestamp': session.start_datetime.timestamp(),
        'end_timestamp': session.end_datetime.timestamp()
    }
    cursor.execute(sql, params)

    module_logger.debug(
        "sql: UPDATE session (id=%i) with %s.", session_id, session)


def insert_request(cursor, request, session_id, response_id):
    uid = cache.create_or_get_uri_id(
        cursor,
        request.scheme,
        request.netloc,
        request.path,
        request.params,
        request.query,
        request.fragment
    )

    sql = ("INSERT INTO REQUESTS ("
           "URI_ID,"
           "SESSION_ID,"
           "RESPONSE_ID"
           ") VALUES(?, ?, ?);")

    cursor.execute(sql, [
        uid,
        session_id,
        response_id
    ])

    rid = int(cursor.lastrowid)
    module_logger.debug(
        "sql: INSERT %s into REQUESTS. Row id is %i.", request, rid)
    return rid


def insert_response(cursor, request, response):

    content_type_id = cache.create_or_get_content_type_id(
        cursor,
        response.content_type
    )

    content_id = cache.create_or_get_content_id(
        cursor,
        request,
        response.content
    )
    sql = ("INSERT INTO RESPONSES ("
           "STATUS_CODE,"
           "TIMESTAMP,"
           "CONTENT_TYPE_ID,"
           "CONTENT_ID"
           ") VALUES (?,?,?,?);")

    cursor.execute(sql, [
        response.status_code,
        response.date.timestamp(),
        content_type_id,
        content_id
    ])

    rid = int(cursor.lastrowid)
    module_logger.debug(
        "sql: INSERT %s into RESPONSES. Row id is %i.", response, rid)

    return rid


def insert_request_and_response(cursor, session_id, request, response):
    """ Fügt einen http(s) request und die dazugehörige response der Datenbank hinzu. 

    Es wird überprüft ob unter dem gleichen request bereits eine response gespeichert wurde.
    Falls ja, wird diese response auf Gleichheit mit der empfangenen überprüft und 
    gegebenfalls die alten response verwendet.

    Arguments:
        cursor -- Datenbank Cursor
        session_id - Id der Session
        response - 
        response_content - 

    Returns:
        [int] --  Die id unter welche der request in der Datenbank gespeichert wurde.
    """

    response_id = insert_response(
        cursor,
        request,
        response
    )

    request_id = insert_request(
        cursor,
        request,
        session_id,
        response_id
    )
    return request_id


def get_content_types(cursor):
    sql = ("SELECT CONTENT_TYPE FROM CONTENT_TYPE_CACHE;")

    cursor.execute(sql)
    content_types = [x[0] for x in cursor.fetchall()]
    return content_types


def get_sessions(cursor):
    sql = ("SELECT "
           "SESSION_ID,"
           "START_TIMESTAMP,"
           "END_TIMESTAMP "
           "FROM SESSIONS;")

    cursor.execute(sql)
    session_list = [(
        Session.from_timestamps(x[1], x[2]),
        {
            'session_id': x[0]
        }
    ) for x in cursor.fetchall()]

    return session_list


def get_request_where_request_id(cursor, request_id):
    sql = ("SELECT "
           "URI_ID,"
           "SESSION_ID,"
           "RESPONSE_ID "
           "FROM REQUESTS WHERE REQUEST_ID = :request_id;")

    param = {'request_id': request_id}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    uri_id = x[0]
    session_id = x[1]
    response_id = x[2]

    uri = cache.get_uri_where_uri_id(cursor, uri_id)

    response = Request(
        scheme=uri['scheme'],
        netloc=uri['netloc'],
        path=uri['path'],
        params=uri['params'],
        query=uri['query'],
        fragment=uri['fragment']
    )

    return (
        response, 
        {
            'session_id': session_id,
            'response_id':  response_id
        }    
    )


def get_response_where_response_id(cursor, response_id):
    """ Extrahiert das unter der rid in der Tabelle RESPONSES 
    abgelegte Response Objekt sowie die zugehöre content id.

    Arguments:
        cursor -- Datenbank Cursor
        rid -- Die id der gewünschten response

    Returns:
        Ein Tuple bestehend aus der gefundenen response und der zu
        dieser Response zugehörigen content_id.
    """

    sql = ("SELECT "
           "STATUS_CODE,"
           "TIMESTAMP,"
           "CONTENT_TYPE_ID,"
           "CONTENT_ID "
           "FROM RESPONSES WHERE RESPONSE_ID = :rid;")

    param = {'rid': response_id}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    content_id = x[3]

    response = Response(
        status_code=x[0],
        date=datetime.fromtimestamp(x[1]),
        content_type=cache.get_content_type_where_content_type_id(cursor, x[2]),
        content=cache.get_content_where_content_id(cursor, content_id)
    )

    module_logger.debug(
        "Extracted %s with id = %i from RESPONSES. "
        "Corresponding content_id is %i.", str(response), response_id, content_id)

    return (
        response,
        {
            'content_id': content_id
        }
    )
