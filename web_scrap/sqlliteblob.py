"""
Modul zum hinzufügen von Blobs in eine sqllite3 Datenbank. Die 
eingefügten Blobs werden versioniert.
"""

import sqlite3
import os
import datetime
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

        sql = """CREATE TABLE IF NOT EXISTS REQUESTS(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    DATETIME TEXT,
                    SCHEME TEXT,
                    NETLOC TEXT,
                    PATH TEXT,
                    PARAMS TEXT,
                    QUERY TEXT,
                    FRAGMENT TEXT,
                    CONTENT_TYPE TEXT,
                    STORAGE_ID INTEGER);"""

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS RESPONSES(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 CONTENT BLOB);"""

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

    else:
        module_logger.info("Tables exists.")

    return conn


def insert_request_and_response(cursor, url, content_type, content):
    """ Fügt einen Blob unter den Namen blobname einer sqllite3 Datenbank hinzu. 

    Es wird überprüft ob unter den gleichen Namen bereits Daten gespeichert wurden.
    Falls ja, werden die Daten nicht erneut hinzugefügt sondern die alten Daten
    verwendet.

    Arguments:
        cursor -- Datenbank Cursor
        

    Returns:
        [int] --  Die id unter welche der blob in der Datenbank gespeichert wurde.
    """
    
    (response_id, last_content) = extract_last_response(cursor, url)

    if (content != last_content):
        module_logger.debug("The response is new. Insert it into RESPONSES.")

        sql = "INSERT INTO RESPONSES (CONTENT) VALUES (?);"
        cursor.execute(sql, [sqlite3.Binary(content)])
        response_id = int(cursor.lastrowid)
        module_logger.debug("sql: INSERT INTO RESPONSES with id=%i", response_id)
        
    
    else:
        module_logger.debug(
            "The response was inserted into RESPONSES beforehand. Using this response instead.")

    sql = ("INSERT INTO REQUESTS ("
                "DATETIME,"
                "SCHEME," 
                "NETLOC,"
                "PATH,"
                "PARAMS,"
                "QUERY,"
                "FRAGMENT,"
                "CONTENT_TYPE,"
                "STORAGE_ID"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)")

    dt = datetime.datetime.now().isoformat()

    scheme, netloc, path, params,query, fragment = urlparse(url)
    cursor.execute(sql, [
        dt,
        scheme, 
        netloc, 
        path, 
        params, 
        query, 
        fragment, 
        content_type,
        response_id
    ])

    lastrowid = int(cursor.lastrowid)
    module_logger.debug("sql: INSERT INTO REQUESTS with id=%i", lastrowid)

    return lastrowid

def list_all_requests_for_url(cursor, url):
    """Listet alle gespeicherten requests datensätze auf die 
    unter der gegebenen uri gespeichert wurden.

    Arguments:
        cursor -- Datenbank Cursor
        scheme - uri scheme
        netloc - uri netloc
        path - uri path
        params - uri params
        query - uri query
        fragment - uri fragment

    Returns:
        Eine Liste von Dictionaries die die gefundenen Einträge enthalten.
    """

    sql = ("SELECT ID, DATETIME, CONTENT_TYPE, STORAGE_ID FROM REQUESTS "
                "WHERE "
                "SCHEME = :scheme AND "
                "NETLOC = :netloc AND "
                "PATH = :path AND "
                "PARAMS = :params AND "
                "QUERY = :query AND "
                "FRAGMENT =:fragment")

    scheme, netloc, path, params,query, fragment = urlparse(url)
    params = {
        'scheme': scheme,
        'netloc' : netloc,
        'path' : path,
        'params' : params,
        'query' : query,
        'fragment': fragment
    }

    cursor.execute(sql, params)
    data = [
        {
            'id': x[0],
            'datetime': x[1],
            'content_type' : x[2],
            'storage_id':x[3]
        }
        for x in cursor.fetchall()]

    return data


def extract_response_by_id(cursor, id):
    """ Extrahiert die unter der id in der Datenbank abgelegte response.

    Arguments:
        cursor -- Datenbank Cursor
        id -- Die id der gewünschten response

    Returns:
        Die response die unter id gespeichert wurde. Diese wird
        als bytearray zurückgegeben.
    """

    module_logger.debug("Extract response with storage_id=%i from RESPONSES.", id)
    sql = "SELECT CONTENT FROM RESPONSES WHERE id = :id"
    param = {'id': id}
    cursor.execute(sql, param)
    return cursor.fetchone()[0]


def extract_last_response(cursor, url):
    """ Extrahiert den letzten unter blobname gespeicherten blob.

    Arguments:
        cursor -- Datenbank Cursor
        url -- Die url unter dem die response gesucht werden soll

    Returns:
        Ein tuple welches die storage_id sowie das bytearray des gefundenen
        blobs enthält. Falls kein blob gefunden wird (-1, None) zurückgegeben.
    """
    dataset = list_all_requests_for_url(cursor, url)

    if len(dataset) == 0:
        module_logger.debug('Found no request in REQUESTS with url "%s"', url)
        return (-1, None)
    else:
        module_logger.debug('Found request(s) in REQUESTS with url "%s"', url)
        module_logger.debug("The last one has the storage_id %i.", dataset[-1]['storage_id'])
        
    laststorageid = dataset[-1]['storage_id']
    return laststorageid, extract_response_by_id(cursor, laststorageid)


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

    sql = "SELECT BLOBNAME, OPAQUE, STORAGE_ID FROM BLOBS WHERE id = :id"
    param = {'id': blobid}
    cursor.execute(sql, param)
    filename_db, opaque, storage_id = cursor.fetchone()

    blob = extract_response_by_id(cursor, storage_id)

    return filename_db, opaque, blob
