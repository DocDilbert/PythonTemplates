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
from webtypes.response_content import ResponseContent

module_logger = logging.getLogger('sqliteblob.sqliteblob')

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
                    "START_DATETIME TEXT,"
                    "END_DATETIME TEXT);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS REQUESTS ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "SCHEME TEXT,"
                    "NETLOC TEXT,"
                    "PATH TEXT,"
                    "PARAMS TEXT,"
                    "QUERY TEXT,"
                    "FRAGMENT TEXT,"
                    "SESSION_ID INTEGER,"
                    "RESPONSE_ID INTEGER);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS RESPONSES ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "STATUS_CODE INTEGER,"
                    "DATE TEXT,"
                    "CONTENT_TYPE TEXT,"
                    "CONTENT_ID INTEGER);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)
        
        sql = ("CREATE TABLE IF NOT EXISTS RESPONSE_CONTENT ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "CONTENT BLOB);")

        
        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

    else:
        module_logger.info("Tables exists.")

    return conn

def insert_session(cursor, session):
    sql =("INSERT INTO SESSIONS ("
            "START_DATETIME,"
            "END_DATETIME"
          ") VALUES (?, ?);")

    cursor.execute(sql, [
        session.start_datetime,
        session.end_datetime
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into SESSIONS. Row id is %i.", session, rid)
    return rid

def update_session(cursor, session_id, session):
    sql =("UPDATE SESSIONS SET "
            "START_DATETIME = :start_datetime, "
            "END_DATETIME = :end_datetime "
          "WHERE id = :session_id;")

    params = {
        'session_id' : session_id,
        'start_datetime': session.start_datetime,
        'end_datetime' : session.end_datetime,
    }
    cursor.execute(sql, params)
    
    module_logger.debug("sql: UPDATE session (id=%i) with %s.", session_id, session)


def insert_response_content(cursor, response_content):
    sql =("INSERT INTO RESPONSE_CONTENT ("
            "CONTENT"
          ") VALUES (?);")

    cursor.execute(sql, [
        sqlite3.Binary(response_content.compress())
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into RESPONSE_CONTENT. Row id is %i.", response_content, rid)
    
    return rid

def insert_response(cursor, response, content_id):
    sql =("INSERT INTO RESPONSES ("
            "STATUS_CODE,"
            "DATE,"
            "CONTENT_TYPE,"
            "CONTENT_ID"
            ") VALUES (?,?,?,?);")

    cursor.execute(sql, [
        response.status_code,
        response.date,
        response.content_type,
        content_id
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into RESPONSES. Row id is %i.", response, rid)
    return rid

def insert_request_and_response(cursor, session_id, request, response, response_content):
    """ Fügt einen http(s) request und die dazugehörige response der Datenbank hinzu. 

    Es wird überprüft ob unter dem gleichen requesr bereits eine response gespeichert wurde.
    Falls ja, wird diese response auf Gleichheit mit der empfangenen überprüft und 
    gegebenfalls die alten response verwendet.

    Arguments:
        cursor -- Datenbank Cursor
        session_id - Id der Session
        response - 
        content_type - Art des hinzugefügten Inhalts
        content - Inhalt der response
    
    Returns:
        [int] --  Die id unter welche der request in der Datenbank gespeichert wurde.
    """
    
    (last_response, last_content_id) = extract_last_response_of_request(cursor, request)
    
    if not last_response:
        module_logger.debug("This is the first time the request %s was perfomed.", request)

        content_id = insert_response_content(cursor, response_content)
        response_id = insert_response(cursor, response, content_id)
    else:
        stored_response_content = extract_response_content_by_id(cursor, last_content_id)

        if (response_content.content != stored_response_content.content):
            module_logger.debug("The received response content is new.")
            content_id = insert_response_content(cursor, response_content)
        else:
            module_logger.debug("The received response content was stored beforehand. Using this instead.")
            content_id = last_content_id

        response_id = insert_response(cursor, response, content_id)
        
    sql = ("INSERT INTO REQUESTS ("
                "SCHEME," 
                "NETLOC,"
                "PATH,"
                "PARAMS,"
                "QUERY,"
                "FRAGMENT,"
                "SESSION_ID,"
                "RESPONSE_ID"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?);")

    cursor.execute(sql, [
        request.scheme, 
        request.netloc, 
        request.path, 
        request.params, 
        request.query, 
        request.fragment, 
        session_id,
        response_id
    ])

    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into REQUESTS. Row id is %i.", request, rid)
    return rid

def list_metadata_for_request(cursor, request):
    """ Listet alle gespeicherten Metadaten auf, die unter der 
    gegebenen request in der Tabelle REQUESTS gespeichert wurden.

    Arguments:
        cursor -- Datenbank Cursor
        url - request url

    Returns:
        Eine Liste von Dictionaries die die gefunden Metadaten enthalten.
    """

    sql = ("SELECT SESSION_ID, RESPONSE_ID FROM REQUESTS "
                "WHERE "
                "SCHEME = :scheme AND "
                "NETLOC = :netloc AND "
                "PATH = :path AND "
                "PARAMS = :params AND "
                "QUERY = :query AND "
                "FRAGMENT =:fragment;")

    params = {
        'scheme': request.scheme,
        'netloc' : request.netloc,
        'path' : request.path,
        'params' : request.params,
        'query' : request.query,
        'fragment': request.fragment
    }

    cursor.execute(sql, params)
    metadata_list = [{
        'session_id': x[0],
        'response_id': x[1]
    } for x in cursor.fetchall()]

    return metadata_list

def list_all_sessions(cursor):
    sql = ("SELECT "
                "ID,"
                "START_DATETIME,"
                "END_DATETIME "
           "FROM SESSIONS;")

    params = {}

    cursor.execute(sql, params)
    session_list = [{
        'id': x[0],
        'session': Session(start_datetime = x[1], end_datetime=x[2])
    } for x in cursor.fetchall()]

    return session_list

def extract_response_content_by_id(cursor, rid):
    """ Extrahiert das unter der rid in der Tabelle RESPONSE_CONTENT 
    abgelegten ResponseContent Objekt.

    Arguments:
        cursor -- Datenbank Cursor
        id -- Die id des gewünschten response content

    Returns:
        Ein befülltes ResponseContent Objekt.
    """
    sql = ("SELECT "
                "CONTENT "
            "FROM RESPONSE_CONTENT WHERE id = :rid;")
    param = {'rid': rid}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    response_content = ResponseContent.from_decompress(x[0])

    module_logger.debug(
        "Extracted %s with id = %i from RESPONSE_CONTENT.", str(response_content), rid) 

    return response_content

def extract_response_by_id(cursor, rid):
    """ Extrahiert das unter der rid in der Tabelle RESPONSES 
    abgelegte Response Objekt sowie die zugehöre content id.

    Arguments:
        cursor -- Datenbank Cursor
        rid -- Die id der gewünschten response

    Returns:
        Ein Tuple bestehend aus der gefundenen Response und der zu
        dieser Response zugehörigen content_id.
    """

    
    sql = ("SELECT "
                "STATUS_CODE,"
                "DATE,"
                "CONTENT_TYPE,"
                "CONTENT_ID "
            "FROM RESPONSES WHERE id = :rid;")
    param = {'rid': rid}
    cursor.execute(sql, param)
    x = cursor.fetchone()
    response = Response(
        status_code=x[0],
        date=x[1],
        content_type=x[2]
    )
    content_id =  x[3]
    module_logger.debug(
        "Extracted %s with id = %i from RESPONSES. "
        "Corresponding content_id is %i.", str(response), rid, content_id) 

    return (response, content_id)


def extract_last_response_of_request(cursor, request):
    """ Extrahiert die letzten unter url gespeicherte response.

    Arguments:
        cursor -- Datenbank Cursor
        request -- Der request unter dem die response gesucht werden soll.

    Returns:
        Es wird ein tuple zurückgegeben. Das erste Element ist die
        gefundene response das zweite die content_id der gefundenen
        response. Wird kein Element gefunden wird (None, -1) zurückgegeben
    """

    dataset = list_metadata_for_request(cursor, request)

    if len(dataset) == 0:
        module_logger.debug('For request %s no meta data was found in REQUESTS.', request)
        return (None, -1)
    else:
        module_logger.debug('For request %s a meta data list was found in REQUESTS.', request)
        module_logger.debug("The last meta data entry in this list has the response_id=%i.", dataset[-1]['response_id'])
        
    last_response_id = dataset[-1]['response_id']
    return extract_response_by_id(cursor, last_response_id)


def extract_response_by_request(cursor, session_id, request):

    sql = ("SELECT RESPONSE_ID FROM REQUESTS "
                "WHERE "
                "SCHEME = :scheme AND "
                "NETLOC = :netloc AND "
                "PATH = :path AND "
                "PARAMS = :params AND "
                "QUERY = :query AND "
                "FRAGMENT =:fragment AND "
                "SESSION_ID =:session_id;")

    params = {
        'scheme': request.scheme,
        'netloc' : request.netloc,
        'path' : request.path,
        'params' : request.params,
        'query' : request.query,
        'fragment': request.fragment,
        'session_id': session_id
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()
    response_id = x[0]
    response, response_content_id = extract_response_by_id(cursor, response_id)
    response_content = extract_response_content_by_id(cursor, response_content_id)

    return response, response_content


def info(cursor):
    sql = ("SELECT count(*) FROM SESSIONS;")    
    cursor.execute(sql)
    x = cursor.fetchone()
    session_count = x[0]

    sql = ("SELECT count(*) FROM REQUESTS;")    
    cursor.execute(sql)
    x = cursor.fetchone()
    request_count = x[0]

    sql = ("SELECT count(*) FROM RESPONSES;")    
    cursor.execute(sql)
    x = cursor.fetchone()
    response_count = x[0]

    sql = ("SELECT count(*) FROM RESPONSE_CONTENT;")    
    cursor.execute(sql)
    x = cursor.fetchone()
    response_content_count = x[0]


    return {
        'session_count' : session_count,
        'request_count' : request_count,
        'response_count' : response_count,
        'response_content_count' : response_content_count
    }