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
        Eine sqlite3 Datenbank connection
    """
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print("Creating schemas")

        sql = """CREATE TABLE IF NOT EXISTS FILES(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 FILENAME TEXT,
                 DATETIME TEXT,
                 STORAGE_ID INTEGER);"""

        conn.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS FILE_STORAGE(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 FILE BLOB);"""

        conn.execute(sql) 

    else:
        print("Schema exists")
    return conn

def insert_file(cursor, filename):
    """ Fügt eine Datei der Datenbank hinzu. 

    Es wird überprüft ob unter den gleichen Namen bereits Daten gespeichert wurden.
    Falls ja, werden die Daten nicht erneut hinzugefügt sondern die Referenz auf
    die alten Daten verwendet.
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der Datei
    
    Returns:
        Die id unter welche die Datei in der Datenbank gespeichert wurde.
    """

    
    with open(filename, 'rb') as input_file:
        ablob=input_file.read()
        ablob_gz = zlib.compress(ablob)
        (storage_id, ablob_last) = extract_last_bytestream_from_storage(cursor, filename)
        
        if (ablob_gz != ablob_last):
            print("New content found for file \"{}\"".format(filename))
            sql="INSERT INTO FILE_STORAGE (FILE) VALUES(?);"
            cursor.execute(sql,[sqlite3.Binary(ablob_gz)])
            storage_id = int(cursor.lastrowid)

        sql="INSERT INTO FILES (FILENAME, DATETIME, STORAGE_ID) VALUES(?, ?, ?);"
        dt = datetime.datetime.now().isoformat()
        cursor.execute(sql,[filename, dt, storage_id]) 


        return int(cursor.lastrowid)

def list_dataset_for_filename(cursor, filename):
    """Listet alle Einträge in der Datenbank auf die unter filename gespeichert wurden
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der Datei
    
    Returns:
        Eine Liste von Dictionaries die die gefundenen Einträge enthalten.
    """

    sql = "SELECT ID, DATETIME, STORAGE_ID FROM FILES WHERE FILENAME = :filename"
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

    sql = "SELECT FILE FROM FILE_STORAGE WHERE id = :id"
    param = {'id': storage_id}
    cursor.execute(sql, param)
    return cursor.fetchone()[0]

def extract_last_bytestream_from_storage(cursor, filename):
    """ Extrahiert den letzten unter filename gespeicherten blob.
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Der Dateiname für den der letzte blob gesucht wird.
    
    Returns:
        Ein tuple welches die storage_id sowie das bytearray des gefundenen
        blobs enthält. Falls kein blob gefunden wird wird (-1, None) zurückgegeben.
    """
    dataset = list_dataset_for_filename(cursor, filename)
    
    if len(dataset)==0:
        return (-1, None)
    
    laststorageid = dataset[-1]['storage_id']
    return (laststorageid, extract_blob_from_storage(cursor, laststorageid))
    
def extract_file(cursor, file_id, filename):
    """ Extrahiert eine Datei aus einer Datenbank. Die extrahiert Datei
    wird über die file_id identifziert.
    
    Arguments:
        cursor -- Datenbank Cursor
        file_id -- Die id der Datei die extrahiert werden soll
        filename -- Der Dateiname unter dem die extrahierte Datei gespeichert werden soll
    """

    sql = "SELECT FILENAME, STORAGE_ID FROM FILES WHERE id = :id"
    param = {'id': file_id}
    cursor.execute(sql, param)
    filename_db, storage_id = cursor.fetchone()

    ablob_gz = extract_blob_from_storage(cursor, storage_id)
    ablob = zlib.decompress(ablob_gz)

    print("Extracting file with id {} from database. Stored filename is \"{}\". It will be stored in \"{}\"."
        .format(file_id, filename_db, filename ))

    with open(filename, 'wb') as output_file:
        output_file.write(ablob)

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