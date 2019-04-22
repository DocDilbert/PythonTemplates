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
from datetime import datetime
module_logger = logging.getLogger('sqliteblob.sqliteblob')

class UriNotFound(Exception):
    pass

class ResponseNotFound(Exception):
    pass

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
                    "END_TIMESTAMP REAL);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS REQUESTS ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "URI_ID INTEGER,"
                    "SESSION_ID INTEGER,"
                    "RESPONSE_ID INTEGER);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS RESPONSES ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "STATUS_CODE INTEGER,"
                    "TIMESTAMP REAL,"
                    "CONTENT_TYPE_ID INTEGER,"
                    "CONTENT_ID INTEGER);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)
        
        sql = ("CREATE TABLE IF NOT EXISTS RESPONSE_CONTENTS ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "CONTENT BLOB);")

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

def extract_content_type_from_cache(cursor, content_type_id):
    sql = ("SELECT "
              "CONTENT_TYPE "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE id = :content_type_id;")

    params = {
        'content_type_id' : content_type_id
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()

    content_type= x[0]
    module_logger.debug("Extracted content_type=%s with id %i.", content_type, content_type_id )

    return content_type

def insert_or_get_content_type_from_cache(cursor, content_type):
    sql = ("SELECT "
              "ID "
           "FROM CONTENT_TYPE_CACHE "
           "WHERE CONTENT_TYPE = :content_type;")

    params = {
        'content_type' : content_type
    }

    cursor.execute(sql, params)
    x = cursor.fetchone()
    if x:
        content_type_id = x[0]
        module_logger.debug("Found content_type=%s. Id is %i", content_type, content_type_id )
    else:
        
        sql =("INSERT INTO CONTENT_TYPE_CACHE ("
                "CONTENT_TYPE"
              ") VALUES (?);")
        cursor.execute(sql, [
            content_type
        ])
        content_type_id = int(cursor.lastrowid)
        module_logger.debug("The content_type=%s is new. Inserting it. Id is %i", content_type, content_type_id )

    return content_type_id

def get_uri_from_cache(cursor, uri_id):
    sql = ("SELECT "
                "SCHEME,"
                "NETLOC,"
                "PATH,"
                "PARAMS,"
                "QUERY,"
                "FRAGMENT "
           "FROM URI_CACHE "
           "WHERE id = :uri_id;")

    sql_params = {
        'uri_id' : uri_id
    }

    cursor.execute(sql, sql_params)
    x = cursor.fetchone()
    if x:
        return {
            'scheme' : x[0],
            'netloc' : x[1],
            'path' : x[2],
            'params' : x[3],
            'query' : x[4],
            'fragment' : x[5],
        }
    else:
        raise UriNotFound()


def get_uri_id_from_cache(cursor, scheme, netloc, path, params, query, fragment):
    sql = ("SELECT "
              "ID "
           "FROM URI_CACHE "
           "WHERE "
                "SCHEME = :scheme AND "
                "NETLOC = :netloc AND "
                "PATH   = :path AND "
                "PARAMS = :params AND "
                "QUERY = :query AND "
                "FRAGMENT = :fragment"                
            ";")

    sql_params = {
        "scheme" : scheme,
        "netloc" : netloc,
        "path" : path,
        "params" : params,
        "query" : query,
        "fragment" : fragment
    }

    cursor.execute(sql, sql_params)
    x = cursor.fetchone()
    if x:
        return x[0]
    else:
        raise UriNotFound()
    
def insert_or_get_uri_from_cache(cursor, scheme, netloc, path, params, query, fragment):
    try:
        uri_id = get_uri_id_from_cache(cursor, scheme, netloc, path, params, query, fragment )
        module_logger.debug("Found uri. Id is %i", uri_id )
        return uri_id

    except UriNotFound:
        sql =("INSERT INTO URI_CACHE ("
                "SCHEME, "
                "NETLOC, "
                "PATH, "
                "PARAMS, "
                "QUERY, "
                "FRAGMENT "
              ") VALUES (?, ?, ?, ?, ?, ?);")

        cursor.execute(sql, [
            scheme,
            netloc,
            path,
            params,
            query,
            fragment
        ])
        uri_id = int(cursor.lastrowid)
        module_logger.debug("The uri is new. Inserting it. Id is %i", uri_id )
        return uri_id
    

def insert_session(cursor, session):
    sql =("INSERT INTO SESSIONS ("
            "START_TIMESTAMP,"
            "END_TIMESTAMP"
          ") VALUES (?, ?);")

    cursor.execute(sql, [
        session.start_datetime.timestamp(),
        -1.0, # endtime unkmown
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into SESSIONS. Row id is %i.", session, rid)
    return rid


def update_session(cursor, session_id, session):
    sql =("UPDATE SESSIONS SET "
            "START_TIMESTAMP = :start_timestamp, "
            "END_TIMESTAMP = :end_timestamp "
          "WHERE id = :session_id;")

    params = {
        'session_id' : session_id,
        'start_timestamp': session.start_datetime.timestamp(),
        'end_timestamp' : session.end_datetime.timestamp()
    }
    cursor.execute(sql, params)
    
    module_logger.debug("sql: UPDATE session (id=%i) with %s.", session_id, session)

def insert_request(cursor, request, session_id, response_id):
    uri_id= insert_or_get_uri_from_cache(
        cursor,
        request.scheme, 
        request.netloc, 
        request.path, 
        request.params, 
        request.query, 
        request.fragment
    )
    sql = ( "INSERT INTO REQUESTS ("
                "URI_ID,"
                "SESSION_ID,"
                "RESPONSE_ID"
            ") VALUES(?, ?, ?);")

    cursor.execute(sql, [
        uri_id,
        session_id,
        response_id
    ])

    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into REQUESTS. Row id is %i.", request, rid)
    return rid


def insert_response(cursor, response, content_id):
    sql =  ("INSERT INTO RESPONSES ("
               "STATUS_CODE,"
               "TIMESTAMP,"
               "CONTENT_TYPE_ID,"
               "CONTENT_ID"
            ") VALUES (?,?,?,?);")

    content_type_id = insert_or_get_content_type_from_cache(cursor, response.content_type)
    cursor.execute(sql, [
        response.status_code,
        response.date.timestamp(),
        content_type_id,
        content_id
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into RESPONSES. Row id is %i.", response, rid)
    return rid

def insert_response_content(cursor, response_content):
    sql =("INSERT INTO RESPONSE_CONTENTS ("
            "CONTENT"
          ") VALUES (?);")

    content_compressed=sqlite3.Binary(response_content.compress())

    module_logger.debug("Compression of content reduced the file size to %.3f %% of the original size.",
        len(content_compressed)/len(response_content.content)*100.0)
    cursor.execute(sql, [
        content_compressed
    ])
    
    rid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT %s into RESPONSE_CONTENTS. Row id is %i.", response_content, rid)
    
    return rid

def insert_request_and_response(cursor, session_id, request, response, response_content):
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
    
    try:
        (_, last_content_id) = extract_last_response_of_request(cursor, request)
        stored_response_content = extract_response_content_by_id(cursor, last_content_id)

        if (response_content.content != stored_response_content.content):
            module_logger.debug("The received response content is new.")
            content_id = insert_response_content(cursor, response_content)
        else:
            module_logger.debug("The received response content was stored beforehand. Using this instead.")
            content_id = last_content_id

        response_id = insert_response(cursor, response, content_id)

    except ResponseNotFound:
        module_logger.debug("This is the first time the request %s was perfomed.", request)

        content_id = insert_response_content(cursor, response_content)
        response_id = insert_response(cursor, response, content_id)
    
    rid = insert_request(
        cursor, 
        request,
        session_id,
        response_id
    )
    return rid

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
        uri_id = get_uri_id_from_cache(cursor, 
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

def list_all_sessions(cursor):
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

def extract_response_content_by_id(cursor, rid):
    """ Extrahiert das unter der rid in der Tabelle RESPONSE_CONTENTS 
    abgelegten ResponseContent Objekt.

    Arguments:
        cursor -- Datenbank Cursor
        id -- Die id des gewünschten response content

    Returns:
        Ein befülltes ResponseContent Objekt.
    """
    sql = ("SELECT "
                "CONTENT "
           "FROM RESPONSE_CONTENTS WHERE id = :rid;")
    param = {'rid': rid}
    cursor.execute(sql, param)
    x = cursor.fetchone()

    response_content = ResponseContent.from_decompress(x[0])

    module_logger.debug(
        "Extracted %s with id = %i from RESPONSE_CONTENTS.", str(response_content), rid) 

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

    
    sql = ( "SELECT "
                "STATUS_CODE,"
                "TIMESTAMP,"
                "CONTENT_TYPE_ID,"
                "CONTENT_ID "
            "FROM RESPONSES WHERE id = :rid;")
    
    param = {'rid': rid}
    cursor.execute(sql, param)
    x = cursor.fetchone()
    
    response = Response(
        status_code=x[0],
        date=datetime.fromtimestamp(x[1]),
        content_type=extract_content_type_from_cache(cursor, x[2])
    )
    content_id =  x[3]

    module_logger.debug(
        "Extracted %s with id = %i from RESPONSES. "
        "Corresponding content_id is %i.", str(response), rid, content_id) 

    return (response, content_id)


def extract_last_response_of_request(cursor, request):
    """ Extrahiert die letzten unter request gespeicherte response.

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
        module_logger.debug('For request %s no meta data was found in REQUESTS.', request)
        raise ResponseNotFound()
    else:
        module_logger.debug('For request %s a meta data list was found in REQUESTS.', request)
        module_logger.debug("The last meta data entry in this list has the response_id=%i.", dataset[-1]['response_id'])
        
    last_response_id = dataset[-1]['response_id']
    return extract_response_by_id(cursor, last_response_id)


def extract_response_by_request(cursor, session_id, request):

    uri_id = get_uri_id_from_cache(cursor, 
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
    response, RESPONSE_CONTENTS_id = extract_response_by_id(cursor, response_id)
    RESPONSE_CONTENTS = extract_response_content_by_id(cursor, RESPONSE_CONTENTS_id)

    return response, RESPONSE_CONTENTS


def compute_content_size(cursor):
    sql = ("SELECT sum(length(CONTENT)) FROM RESPONSE_CONTENTS;")
    cursor.execute(sql)
    x = cursor.fetchone()
    content_size = x[0]
    return content_size

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

    sql = ("SELECT count(*) FROM RESPONSE_CONTENTS;")    
    cursor.execute(sql)
    x = cursor.fetchone()
    RESPONSE_CONTENTS_count = x[0]


    return {
        'session_count' : session_count,
        'request_count' : request_count,
        'response_count' : response_count,
        'RESPONSE_CONTENTS_count' : RESPONSE_CONTENTS_count
    }