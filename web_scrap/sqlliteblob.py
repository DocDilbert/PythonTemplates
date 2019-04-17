"""
Modul zum hinzufügen von http(s) requests und responses in eine sqllite3 Datenbank. Die 
requests und responses werden versioniert.
"""

import sqlite3
import os
import logging
from urllib.parse import urlparse, urlunparse

module_logger = logging.getLogger('main.sqliteblob')

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

        sql = ("CREATE TABLE IF NOT EXISTS REQUESTS ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "TIMESTAMP TEXT,"
                    "SCHEME TEXT,"
                    "NETLOC TEXT,"
                    "PATH TEXT,"
                    "PARAMS TEXT,"
                    "QUERY TEXT,"
                    "FRAGMENT TEXT,"
                    "RESPONSE_ID INTEGER);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = ("CREATE TABLE IF NOT EXISTS RESPONSES ("
                    "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "CONTENT_TYPE TEXT,"
                    "CONTENT BLOB);")

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

    else:
        module_logger.info("Tables exists.")

    return conn


def insert_request_and_response(cursor, timestamp, request, content_type, content):
    """ Fügt einen http(s) request und die dazugehörige response der Datenbank hinzu. 

    Es wird überprüft ob unter dem gleichen requesr bereits eine response gespeichert wurde.
    Falls ja, wird diese response auf Gleichheit mit der empfangenen überprüft und 
    gegebenfalls die alten response verwendet.

    Arguments:
        cursor -- Datenbank Cursor
        timestamp - Zeitstempel des scraps
        response - 
        content_type - Art des hinzugefügten Inhalts
        content - Inhalt der response
    
    Returns:
        [int] --  Die id unter welche der request in der Datenbank gespeichert wurde.
    """
    
    url = request['url']
    last_response = extract_last_response_of_request(cursor, url)
    
    if not last_response or (last_response and (content != last_response['content'])):
        module_logger.debug("The response is new. Insert it into RESPONSES.")

        sql =("INSERT INTO RESPONSES ("
                "CONTENT_TYPE,"
                "CONTENT"
               ") VALUES (?, ?);")

        cursor.execute(sql, [
            content_type,
            sqlite3.Binary(content)
        ])
        response_id = int(cursor.lastrowid)
        module_logger.debug("sql: INSERT INTO RESPONSES with id=%i", response_id)
    else:
        response_id = last_response['id']
        module_logger.debug(
            "The received response and the one which is stored under id=%i are equal. "
            "Using the stored response instead.",response_id)

    sql = ("INSERT INTO REQUESTS ("
                "TIMESTAMP,"
                "SCHEME," 
                "NETLOC,"
                "PATH,"
                "PARAMS,"
                "QUERY,"
                "FRAGMENT,"
                "RESPONSE_ID"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?)")

    scheme, netloc, path, params,query, fragment = urlparse(url)
    cursor.execute(sql, [
        timestamp,
        scheme, 
        netloc, 
        path, 
        params, 
        query, 
        fragment, 
        response_id
    ])

    lastrowid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT INTO REQUESTS with id=%i", lastrowid)

    return lastrowid

def list_all_requests_for_url(cursor, url):
    """ Listet alle gespeicherten request datensätze auf, die unter der 
    gegebenen url gespeichert wurden.

    Arguments:
        cursor -- Datenbank Cursor
        url - request url

    Returns:
        Eine Liste von Dictionaries die die gefunden requests enthalten.
    """

    sql = ("SELECT ID, TIMESTAMP, RESPONSE_ID FROM REQUESTS "
                "WHERE "
                "SCHEME = :scheme AND "
                "NETLOC = :netloc AND "
                "PATH = :path AND "
                "PARAMS = :params AND "
                "QUERY = :query AND "
                "FRAGMENT =:fragment")

    scheme, netloc, path, params, query, fragment = urlparse(url)
    params = {
        'scheme': scheme,
        'netloc' : netloc,
        'path' : path,
        'params' : params,
        'query' : query,
        'fragment': fragment
    }

    cursor.execute(sql, params)
    data = [{
            'id': x[0],
            'timestamp': x[1],
            'response_id':x[2]
        } for x in cursor.fetchall()]

    return data


def extract_response_by_id(cursor, id):
    """ Extrahiert die unter der id in der Datenbank abgelegte response.

    Arguments:
        cursor -- Datenbank Cursor
        id -- Die id der gewünschten response

    Returns:
        Die response die unter id gespeichert wurde.
    """

    module_logger.debug("Extract response with id = %i from RESPONSES.", id)
    sql = "SELECT CONTENT_TYPE, CONTENT FROM RESPONSES WHERE id = :id"
    param = {'id': id}
    cursor.execute(sql, param)
    x = cursor.fetchone()
    
    return {
        'id' : id,
        'content_type' : x[0],
        'content' : x[1]
    }


def extract_last_response_of_request(cursor, url):
    """ Extrahiert die letzten unter url gespeicherte response.

    Arguments:
        cursor -- Datenbank Cursor
        url -- Die url unter dem die response gesucht werden soll

    Returns:
        Die letzte unter url gespeicherte response.
        Falls keine response gefunden wird, wird None zurückgegeben.
    """
    dataset = list_all_requests_for_url(cursor, url)

    if len(dataset) == 0:
        module_logger.debug('Found no request in REQUESTS with url "%s"', url)
        return None
    else:
        module_logger.debug('Found request(s) in REQUESTS with url "%s"', url)
        module_logger.debug("The last request in this list has the response_id=%i.", dataset[-1]['response_id'])
        
    last_response_id = dataset[-1]['response_id']
    return extract_response_by_id(cursor, last_response_id)


def extract_request_by_id(cursor, blobid):
    """ Extrahiert einen Blob aus der sqllite3 Datenbank. Die extrahiert Datei
    wird über die blobid identifziert.

    Arguments:
        cursor -- Datenbank Cursor
        blobid -- Die id des Blobs der extrahiert werden soll.

    Returns:
        [(blobname, opaque, blob)] 
            blobname -- Der Name unter dem der blob gespeichert ist.
            opaque -- Die gespeicherten beliebigen Datem-
            blob -- Der eigentlich Blob als bytearray.
    """

    sql = "SELECT BLOBNAME, OPAQUE, RESPONSE_ID FROM BLOBS WHERE id = :id"
    param = {'id': blobid}
    cursor.execute(sql, param)
    filename_db, opaque, storage_id = cursor.fetchone()

    blob = extract_response_by_id(cursor, storage_id)

    return filename_db, opaque, blob
