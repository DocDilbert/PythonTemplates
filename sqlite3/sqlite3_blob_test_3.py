"""
Einfügen von zufällig generieten Dateien in eine sqllite3 Datenbank und 
Wiederherstellung derselbigen. Die Daten in der Datenbank werden
im gzip Format gespeichert. Es werden nur neue Daten gespeichert.
"""

import sqlite3
import create_binary_file as cbf
import os
import filecmp
import zlib
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

def insert_file(cursor, filename):
    """ Fügt die Datei mit dem Namen filename einer sqlite3 Datenbank hinzu.
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der zu lesenden Datei
    
    Returns:
        [int] --  Die id unter welche der blob in der Datenbank gespeichert wurde.
    """

    with open(filename, 'rb') as input_file:
        ablob=input_file.read()
        ablob_gz = zlib.compress(ablob)
        return insert_blob(cursor, filename, ablob_gz)

def list_dataset_for_filename(cursor, filename):
    """Listet alle gespeicherten Datensätze in der Datenbank auf die 
    unter filename gespeichert wurden
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der Datei
    
    Returns:
        Eine Liste von Dictionaries die die gefundenen Einträge enthalten.
    """

    sql = "SELECT ID, DATETIME, STORAGE_ID FROM BLOBS WHERE BLOBNAME = :filename"
    param = {'filename': filename}
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
    dataset = list_dataset_for_filename(cursor, blobname)
    
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

    ablob_gz = extract_blob_from_storage(cursor, storage_id)
    ablob = zlib.decompress(ablob_gz)

    return filename_db, opaque, ablob

def extract_file(cursor, blobid, filename):
    """ Extrahiert eine Datei aus einer Datenbank. Die extrahiert Datei
    wird über die file_id identifziert und in Dateisystem gespeichert.
    
    Arguments:
        cursor -- Datenbank Cursor
        blobid -- Die id des Blobs der extrahiert werden soll.
        filename -- Der Dateiname unter dem die extrahierte Datei gespeichert werden soll
    """

    (filename_db, _ , blob) = extract_blob(cursor, blobid)

    print("Extracting file with id {} from database. Stored filename is \"{}\". It will be stored in \"{}\"."
        .format(blobid, filename_db, filename ))

    with open(filename, 'wb') as output_file:
        output_file.write(blob)

def main(seed):
    conn = create_or_open_db("blob.db")
    TESTFILE1 = "testfile1.bin"
    TESTFILE2 = "testfile2.bin"
    TESTFILE3 = "testfile3.bin"

    TESTFILE1_DB = "testfile1_lite.bin"
    TESTFILE2_DB = "testfile2_lite.bin"
    TESTFILE3_DB = "testfile3_lite.bin"

    cbf.create_random_file(None,    1024, TESTFILE1) # A seed of None is equal to use system time
    cbf.create_random_file(seed+7,  2048, TESTFILE2)
    cbf.create_random_file(seed+13, 1024*10, TESTFILE3)

    cursor = conn.cursor()
    
    fid1 = insert_file(cursor, TESTFILE1)
    fid2 = insert_file(cursor, TESTFILE2)
    fid3 = insert_file(cursor, TESTFILE3)

    conn.commit()

    extract_file(cursor, fid1, TESTFILE1_DB)
    extract_file(cursor, fid2, TESTFILE2_DB)
    extract_file(cursor, fid3, TESTFILE3_DB)

    if (filecmp.cmp(TESTFILE1, TESTFILE1_DB, shallow=False)):
        print("{} == {}".format(TESTFILE1, TESTFILE1_DB))
    else:
        print("!!! {} != {} !!!".format(TESTFILE1, TESTFILE1_DB))
    
    if (filecmp.cmp(TESTFILE2, TESTFILE2_DB, shallow=False)):
        print("{} == {}".format(TESTFILE2, TESTFILE2_DB))
    else:
        print("!!! {} != {} !!!".format(TESTFILE2, TESTFILE2_DB))
    
    if (filecmp.cmp(TESTFILE3, TESTFILE3_DB, shallow=False)):
        print("{} == {}".format(TESTFILE3, TESTFILE3_DB))
    else:
        print("!!! {} != {} !!!".format(TESTFILE3, TESTFILE3_DB))
    
    list_dataset_for_filename(cursor, TESTFILE1)
    
if __name__ == "__main__":
    main(123)