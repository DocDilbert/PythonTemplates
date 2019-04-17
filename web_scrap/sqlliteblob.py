"""
Modul zum hinzufügen von Blobs in eine sqllite3 Datenbank. Die 
eingefügten Blobs werden versioniert.
"""

import sqlite3
import os
import datetime
import logging
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

        sql = """CREATE TABLE IF NOT EXISTS RESPONSE_CONTENT_STORAGE(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 CONTENT BLOB);"""

        module_logger.debug("conn.execute(%s)", sql)
        conn.execute(sql)

    else:
        module_logger.info("Tables exists.")

    return conn


def insert_request(cursor, scheme, netloc, path, params, query, fragment, content_type, content):
    """ Fügt einen Blob unter den Namen blobname einer sqllite3 Datenbank hinzu. 

    Es wird überprüft ob unter den gleichen Namen bereits Daten gespeichert wurden.
    Falls ja, werden die Daten nicht erneut hinzugefügt sondern die alten Daten
    verwendet.

    Arguments:
        cursor -- Datenbank Cursor
        

    Returns:
        [int] --  Die id unter welche der blob in der Datenbank gespeichert wurde.
    """

    (storage_id, last_content) = extract_last_blob(cursor, scheme, netloc, path, params, query, fragment)

    if (content != last_content):
        module_logger.debug("The content is new. Insert it into RESPONSE_CONTENT_STORAGE.")

        sql = "INSERT INTO RESPONSE_CONTENT_STORAGE (CONTENT) VALUES (?);"
        cursor.execute(sql, [sqlite3.Binary(content)])
        module_logger.debug("sql: INSERT INTO RESPONSE_CONTENT_STORAGE")
        storage_id = int(cursor.lastrowid)
    
    else:
        module_logger.debug(
            "The content was inserted beforehand. Using this blob instead.")

    sql = """INSERT INTO REQUESTS (
                DATETIME,
                SCHEME,
                NETLOC,
                PATH,
                PARAMS,
                QUERY,
                FRAGMENT,
                CONTENT_TYPE,
                STORAGE_ID
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    dt = datetime.datetime.now().isoformat()

    
    cursor.execute(sql, [
        dt,
        scheme, 
        netloc, 
        path, 
        params, 
        query, 
        fragment, 
        content_type,
        storage_id
    ])
    module_logger.debug("sql: INSERT INTO REQUESTS")
    lastrowid = int(cursor.lastrowid)
    module_logger.debug(
        "The request was inserted with into REQUESTS with id=%i", lastrowid)
    return lastrowid


def list_dataset_for_uri(cursor, scheme, netloc, path, params, query, fragment):
    """Listet alle gespeicherten Datensätze in der Datenbank auf die 
    unter filename gespeichert wurden

    Arguments:
        cursor -- Datenbank Cursor
        blobname -- Name unter dem der gesuchte blob gespeichert ist.

    Returns:
        Eine Liste von Dictionaries die die gefundenen Einträge enthalten.
    """

    sql = """ SELECT ID, DATETIME, CONTENT_TYPE, STORAGE_ID FROM REQUESTS
                WHERE 
                SCHEME = :scheme AND
                NETLOC = :netloc AND
                PATH = :path AND
                PARAMS = :params AND
                QUERY = :query 
          """

    params = {
        'scheme': scheme,
        'netloc' : netloc,
        'path' : path,
        'params' : params,
        'query' : query
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


def extract_blob_from_storage(cursor, storage_id):
    """ Extrahiert den unter der storage_id in der Datenbank abgelegten blob.

    Arguments:
        cursor -- Datenbank Cursor
        storage_id -- Die Storage id des gewünschten blobs.

    Returns:
        Der blob der unter storage_id gespeichert wurde. Dieser wird
        als bytearray zurückgegeben.
    """
    module_logger.debug("Extract blob with storage_id=%i from RESPONSE_CONTENT_STORAGE.", storage_id)
    sql = "SELECT CONTENT FROM RESPONSE_CONTENT_STORAGE WHERE id = :id"
    param = {'id': storage_id}
    cursor.execute(sql, param)
    return cursor.fetchone()[0]


def extract_last_blob(cursor, scheme, netloc, path, params, query, fragment):
    """ Extrahiert den letzten unter blobname gespeicherten blob.

    Arguments:
        cursor -- Datenbank Cursor
        blobname -- Der Name des blobs der gesucht wird.

    Returns:
        Ein tuple welches die storage_id sowie das bytearray des gefundenen
        blobs enthält. Falls kein blob gefunden wird (-1, None) zurückgegeben.
    """
    dataset = list_dataset_for_uri(cursor, scheme, netloc, path, params, query, fragment)

    if len(dataset) == 0:
        module_logger.debug("Found no request with uri\n"+
            "\tscheme = %s\n"+
            "\tnetloc = %s\n"+
            "\tpath = %s\n"+
            "\tparams = %s\n" +
            "\tquery = %s\n"+
            "\tfragment = %s in REQUESTS.", scheme, netloc, path,params,query,fragment)
        return (-1, None)
    else:
        module_logger.debug("Found request with uri\n"+
            "\tscheme = %s\n"+
            "\tnetloc = %s\n"+
            "\tpath = %s\n"+
            "\tparams = %s\n" +
            "\tquery = %s\n"+
            "\tfragment = %s in REQUESTS.", scheme, netloc, path,params,query,fragment)
        
        module_logger.debug("The last one has the storage_id %i.", dataset[-1]['storage_id'])
        
    laststorageid = dataset[-1]['storage_id']
    return laststorageid, extract_blob_from_storage(cursor, laststorageid)


def extract_blob(cursor, blobid):
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

    blob = extract_blob_from_storage(cursor, storage_id)

    return filename_db, opaque, blob
