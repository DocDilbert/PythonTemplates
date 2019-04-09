"""
Einfügen von zufällig generieten Dateien in eine sqllite3 Datenbank und 
Wiederherstellung derselbigen.
"""

import sqlite3
import create_binary_file as cbf
import os
import filecmp

def create_or_open_db(db_file):
    """
    Erstellt oder öffnet eine sqllite3 Datenbank. 
    Liefert eine Connection zurück.
    """
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print("Creating schema")

        sql = """CREATE TABLE IF NOT EXISTS FILES(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 FILE BLOB,
                 FILENAME TEXT);"""

        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
    else:
        print("Schema exists")
    return conn

def insert_file(cursor, filename):
    """ Fügt eine Datei der Datenbank hinzu
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der Datei
    
    Returns:
        Die id unter welche die Datei in der Datenbank gespeichert wurde.
    """
    with open(filename, 'rb') as input_file:
        ablob=input_file.read()
        sql="INSERT INTO FILES (FILE, FILENAME) VALUES(?, ?);"
        cursor.execute(sql,[sqlite3.Binary(ablob), filename]) 
        return int(cursor.lastrowid)

def extract_file(cursor, file_id, filename):
    """ Extrahiert eine Datei aus einer Datenbank. Die extrahiert Datei
    wird über eine id identifziert.
    
    Arguments:
        cursor -- Datenbank Cursor
        file_id -- Die id der Datei die extrahiert werden soll
        filename -- Der Dateiname unter dem die extrahierte Datei gespeichert werden soll
    """
    sql = "SELECT FILE, FILENAME FROM FILES WHERE id = :id"
    param = {'id': file_id}
    cursor.execute(sql, param)
    ablob, filename_db = cursor.fetchone()
    
    print("Extracting file with id {} from database. Stored filename is \"{}\". It will be stored in \"{}\"."
        .format(file_id, filename_db, filename ))

    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    return filename

def main(seed):
    try:
        # Verzeichnis erstellen
        os.mkdir("database")
    except FileExistsError:
        # Falls es schon existiert mache weiter
        pass

    conn = create_or_open_db("blob.db")
    TESTFILE1 = "testfile1.bin"
    TESTFILE2 = "testfile2.bin"
    TESTFILE3 = "testfile3.bin"

    TESTFILE1_DB = "testfile1_lite.bin"
    TESTFILE2_DB = "testfile2_lite.bin"
    TESTFILE3_DB = "testfile3_lite.bin"

    cbf.create_random_file(seed,    1024, TESTFILE1)
    cbf.create_random_file(seed+7,  2048, TESTFILE2)
    cbf.create_random_file(seed+13, 4096, TESTFILE3)

    cursor=conn.cursor()
    
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
        
    
if __name__ == "__main__":
    main(123)