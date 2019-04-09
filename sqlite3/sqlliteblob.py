"""
Modul zum hinzfügen von Blobs in eine sqllite3 Datenbank. Die 
eingefügten Blobs werden versioniert.
"""

import sqlite3
import os
import datetime



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
        print("Creating schemas")

        sql = """CREATE TABLE IF NOT EXISTS BLOBS(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 BLOBNAME TEXT,
                 DATETIME TEXT,
                 OPAQUE TEXT,
                 STORAGE_ID INTEGER);"""

        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS BLOB_STORAGE(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 CONTENT BLOB);"""

        conn.execute(sql) 

    else:
        print("Schema exists")
    return conn

def insert_blob(cursor, blobname, blob, opaque=""):
    """ Fügt einen Blob unter den Namen blobname einer sqllite3 Datenbank hinzu. 

    Es wird überprüft ob unter den gleichen Namen bereits Daten gespeichert wurden.
    Falls ja, werden die Daten nicht erneut hinzugefügt sondern die alten Daten
    verwendet.
    
    Arguments:
        cursor -- Datenbank Cursor
        blobname -- Name des Blobs
        blob -- Der eigentliche Blob
        opaque -- Beliebige Daten als String gepackt
    
    Returns:
        [int] --  Die id unter welche der blob in der Datenbank gespeichert wurde.
    """
    
    (storage_id, ablob_last) = extract_last_bytestream_from_storage(cursor, blobname)
    
    if (blob != ablob_last):
        print("New content found for blob \"{}\"".format(blobname))
        sql="INSERT INTO BLOB_STORAGE (CONTENT) VALUES(?);"
        cursor.execute(sql,[sqlite3.Binary(blob)])
        storage_id = int(cursor.lastrowid)

    sql="INSERT INTO BLOBS (BLOBNAME, DATETIME, OPAQUE, STORAGE_ID) VALUES(?, ?, ?, ?);"
    dt = datetime.datetime.now().isoformat()
    cursor.execute(sql,[blobname, dt, opaque, storage_id]) 

    return int(cursor.lastrowid)


def list_dataset_for_blobname(cursor, blobname):
    """Listet alle gespeicherten Datensätze in der Datenbank auf die 
    unter filename gespeichert wurden
    
    Arguments:
        cursor -- Datenbank Cursor
        blobname -- Name unter dem der gesuchte blob gespeichert ist.
    
    Returns:
        Eine Liste von Dictionaries die die gefundenen Einträge enthalten.
    """

    sql = "SELECT ID, DATETIME, STORAGE_ID FROM BLOBS WHERE BLOBNAME = :filename"
    param = {'filename': blobname}
    cursor.execute(sql, param)
    data = [
        {
            'id' : x[0], 
            'datatime' : x[1], 
            'storage_id':x[2]
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

    sql = "SELECT CONTENT FROM BLOB_STORAGE WHERE id = :id"
    param = {'id': storage_id}
    cursor.execute(sql, param)
    return cursor.fetchone()[0]

def extract_last_bytestream_from_storage(cursor, blobname):
    """ Extrahiert den letzten unter blobname gespeicherten blob.
    
    Arguments:
        cursor -- Datenbank Cursor
        blobname -- Der Name des blobs der gesucht wird.
    
    Returns:
        Ein tuple welches die storage_id sowie das bytearray des gefundenen
        blobs enthält. Falls kein blob gefunden wird (-1, None) zurückgegeben.
    """
    dataset = list_dataset_for_blobname(cursor, blobname)
    
    if len(dataset)==0:
        return (-1, None)
    
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
