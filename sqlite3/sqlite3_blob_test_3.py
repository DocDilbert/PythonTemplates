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
from sqlliteblob import insert_blob, extract_blob, create_or_open_db

def insert_file(cursor, filename):
    """ Fügt die Datei mit dem Namen filename einer sqlite3 Datenbank hinzu.
    
    Arguments:
        cursor -- Datenbank Cursor
        filename -- Name der zu lesenden Datei
    
    Returns:
        [int] -- Die id unter welche der blob in der Datenbank gespeichert wurde.
    """

    with open(filename, 'rb') as input_file:
        ablob=input_file.read()
        ablob_gz = zlib.compress(ablob)
        return insert_blob(cursor, filename, ablob_gz)

def extract_file(cursor, blobid, filename):
    """ Extrahiert eine Datei aus einer Datenbank. Die extrahiert Datei
    wird über die file_id identifziert und in Dateisystem gespeichert.
    
    Arguments:
        cursor -- Datenbank Cursor
        blobid -- Die id des Blobs der extrahiert werden soll.
        filename -- Der Dateiname unter dem die extrahierte Datei gespeichert werden soll
    """

    (filename_db, _ , blob_gz) = extract_blob(cursor, blobid)
    blob = zlib.decompress(blob_gz)
    
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

    
if __name__ == "__main__":
    main(123)