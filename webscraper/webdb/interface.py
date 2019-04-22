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
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "START_TIMESTAMP REAL,"
               "END_TIMESTAMP REAL"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS REQUESTS ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "URI_ID INTEGER,"
               "SESSION_ID INTEGER,"
               "RESPONSE_ID INTEGER"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS RESPONSES ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "STATUS_CODE INTEGER,"
               "TIMESTAMP REAL,"
               "CONTENT_TYPE_ID INTEGER,"
               "CONTENT_ID INTEGER"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS CONTENT_CACHE ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "CONTENT BLOB"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS CONTENT_TYPE_CACHE ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
               "CONTENT_TYPE TEXT"
               ");")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS URI_CACHE ("
               "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
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
           "WHERE id = :session_id;")

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
    try:
        (last_response, last_content_id) = extract_last_response_of_request(
            cursor, request)

        if (response.content != last_response.content):
            module_logger.debug("The received response content is new.")
            content_id = cache.insert_content(cursor, response.content)
        else:
            module_logger.debug(
                "The received response content was stored beforehand. Using this instead.")

            content_id = last_content_id

    except ResponseNotFound:
        module_logger.debug(
            "This is the first time the request %s was perfomed.", request)

        content_id = cache.insert_content(cursor, response.content)

    sql = ("INSERT INTO RESPONSES ("
           "STATUS_CODE,"
           "TIMESTAMP,"
           "CONTENT_TYPE_ID,"
           "CONTENT_ID"
           ") VALUES (?,?,?,?);")

    content_type_id = cache.create_or_get_content_type_id(
        cursor,
        response.content_type
    )

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


def list_metadata_for_request(cursor, request):
    """ Listet alle gespeicherten Metadaten auf, die unter der 
    gegebenen request in der Tabelle REQUESTS gespeichert wurden.

    Arguments:
        cursor -- Datenbank Cursor
        request - request 

    Returns:
        Eine Liste von Dictionaries die die gefunden Metadaten enthalten.
    """

    sql = ("SELECT SESSION_ID, RESPONSE_ID FROM REQUESTS "
           "WHERE "
           "URI_ID = :uri_id;")

    try:
        uri_id = cache.get_id_of_uri(
            cursor,
            request.scheme,
            request.netloc,
            request.path,
            request.params,
            request.query,
            request.fragment
        )
    except UriNotFound:
        return []

    params = {
        'uri_id': uri_id
    }

    cursor.execute(sql, params)
    metadata_list = [{
        'session_id': x[0],
        'response_id': x[1]
    } for x in cursor.fetchall()]

    return metadata_list

def get_content_type_list(cursor):
    sql = ("SELECT CONTENT_TYPE FROM CONTENT_TYPE_CACHE;")
    
    cursor.execute(sql)
    content_types = [x[0] for x in cursor.fetchall() ]
    return content_types


def get_session_list(cursor):
    sql = ("SELECT "
           "ID,"
           "START_TIMESTAMP,"
           "END_TIMESTAMP "
           "FROM SESSIONS;")

    cursor.execute(sql)
    session_list = [{
        'id': x[0],
        'session': Session.from_timestamps(x[1], x[2])
    } for x in cursor.fetchall()]

    return session_list

def get_request_list_of_session_id(cursor, session_id):
    sql = ("SELECT "
           "ID "
           "FROM REQUESTS "
           "WHERE SESSION_ID = :session_id"
           ";")

    sqlparams = {
        'session_id' : session_id
    }
    cursor.execute(sql, sqlparams)

    request_list = []
    for x in cursor.fetchall():
        request_id = x[0]
        request, (session_id, response_id) = get_request_by_id(cursor, request_id)
        request_list.append(
            (request, 
                {
                    'session_id' : session_id, 
                    'request_id' : request_id, 
                    'response_id' : response_id
                }
            )
        )
    
    return request_list

def get_request_by_id(cursor, request_id):
    sql = ("SELECT "
            "URI_ID,"
            "SESSION_ID,"
            "RESPONSE_ID "
           "FROM REQUESTS WHERE id = :request_id;")

    param = {'request_id': request_id}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    uri_id = x[0]
    session_id = x[1]
    response_id = x[2]

    uri = cache.get_uri(cursor,uri_id )

    response = Request(
        scheme = uri['scheme'],
        netloc = uri['netloc'],
        path = uri['path'],
        params  = uri['params'],
        query = uri['query'],
        fragment = uri['fragment']
    )

    return (response, (session_id, response_id))

def get_response_by_id(cursor, rid):
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
           "FROM RESPONSES WHERE id = :rid;")

    param = {'rid': rid}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    content_id = x[3]

    response = Response(
        status_code=x[0],
        date=datetime.fromtimestamp(x[1]),
        content_type=cache.get_content_type(cursor, x[2]),
        content=cache.get_content(cursor, content_id)
    )

    module_logger.debug(
        "Extracted %s with id = %i from RESPONSES. "
        "Corresponding content_id is %i.", str(response), rid, content_id)

    return (response, content_id)


def extract_last_response_of_request(cursor, request):
    """ Extrahiert die letzte unter dem gegeben request gespeicherte response.

    Arguments:
        cursor -- Datenbank Cursor
        request -- Der request unter dem die response gesucht werden soll.

    Returns:
        Es wird ein tuple zurückgegeben. Das erste Element ist die
        gefundene response das zweite die content_id der gefundenen
        response. 

    Raises:
        ResponseNotFound - If no last response for request was found.
    """

    dataset = list_metadata_for_request(cursor, request)

    if len(dataset) == 0:
        module_logger.debug(
            'For request %s no meta data was found in REQUESTS.', request)
        raise ResponseNotFound()

    last_response_id = dataset[-1]['response_id']

    module_logger.debug(
        'For request %s a meta data list was found in REQUESTS.', request)
    module_logger.debug(
        "The last meta data entry in this list has the response_id=%i.", last_response_id)

    return get_response_by_id(cursor, last_response_id)


def extract_response_by_request(cursor, session_id, request):

    uri_id = cache.get_id_of_uri(
        cursor,
        request.scheme,
        request.netloc,
        request.path,
        request.params,
        request.query,
        request.fragment
    )

    sql = ("SELECT RESPONSE_ID FROM REQUESTS "
           "WHERE "
           "URI_ID =:uri_id AND "
           "SESSION_ID =:session_id;")

    params = {
        'uri_id': uri_id,
        'session_id': session_id
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()
    response_id = x[0]

    return get_response_by_id(cursor, response_id)
