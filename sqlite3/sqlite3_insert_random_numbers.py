# Inserts random numbers into database
#  
import sqlite3 as lite
import random 

con = lite.connect('./database/test.db')

with con:

    cur = con.cursor()     

    cur.execute("CREATE TABLE IF NOT EXISTS RandomNumbers(randn integer)")
    sql = "INSERT INTO RandomNumbers VALUES (?)"
    print(sql)
    cur.execute(sql, (random.randint(0, 5), ))


