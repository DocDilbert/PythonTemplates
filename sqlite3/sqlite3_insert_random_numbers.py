# Inserts random numbers into database
#  
import sqlite3 as lite
import random 
import os


try:
    # Verzeichnis erstellen
    os.mkdir("database")
except FileExistsError:
    # Falls es schon exisitiert mache weiter
    pass

con = lite.connect('./database/test.db')

with con:

    cur = con.cursor()     
    # To create a new table in SQLite, you use CREATE TABLE
    #
    # To create a table you specify the following attributes:
    #
    # * The name of the table: you are not allowed to create a table with the name 
    #   starting with sqlite_ because these names are reserved for SQLite’s internal use. 
    #   In addition, you cannot create a table that already exists in the current database. 
    #   To avoid this, you can use an optional clause IF NOT EXISTS to instruct SQLite to 
    #   create a new table if the table does not exist, otherwise, just ignore the statement.
    #
    # * The database to which table belongs. It may be the main database, temp database 
    #   or any attached database.
    #
    # * The name of each column, its data type, and an optional constraint. SQLite 
    #   supports PRIMARY KEY, UNIQUE, NOT NULL, and CHECK constraints.
    #
    # * The primary key of the table: is a column or a group of columns that uniquely identifies 
    #   a row in the table. In case the primary key consists of multiple columns, you need to 
    #   use table constraint instead of PRIMARY KEY column constraint.
    #
    # * The WITHOUT ROWID table. By default, a row in a table has an implicit column, 
    #   which can be referred to as the rowid, oid or _rowid_ column. The rowid column 
    #   stores a 64-bit signed integer key that uniquely identifies the row inside the table. If you don’t want SQLite creates the rowid column, you can specify the WITHOUT ROWID option in the CREATE TABLE statement. A table that contains a rowid column called a rowid table.
        
    cur.execute("CREATE TABLE IF NOT EXISTS RandomNumbers(randn integer)")
    sql = "INSERT INTO RandomNumbers VALUES (?)"
    print(sql)
    cur.execute(sql, (random.randint(0, 5), ))


