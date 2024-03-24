import sqlite3

def save(uuid_file,srtFileName):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO SrtFile VALUES (?,?)",[str(uuid_file),srtFileName])
    con.commit()
    con.close()

def getSrtFile(uuid):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute("SELECT path FROM SrtFile WHERE uuid = ?",(uuid,))
    path = res.fetchone()
    con.close()
    return path[0]