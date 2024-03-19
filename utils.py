import os
import uuid
import sqlite3
from datetime import timedelta

def convert(segments,file_name):

    srt_dir = os.path.join(os.getcwd(),'srt_files')
    os.makedirs(srt_dir, exist_ok=True)

    uuid_file = uuid.uuid4()
    srtFileName = file_name.replace(".mp3",'_' + str(uuid_file) + '.srt')
    srtFileName = os.path.join(srt_dir, srtFileName)

    with open(srtFileName, 'w', encoding='utf-8') as srtFile:
        print("ok")

    Finaltext = []

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment.start)))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment.end)))+',000'
        text = segment.text
        segmentId = segment.id
        line = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        segmentId = segment.id+1
        Finaltext.append(segment.text)
        print(line)

        with open(srtFileName, 'a', encoding='utf-8') as srtFile:
            srtFile.write(line)

    saveDataBase(str(uuid_file),srtFileName)

    return str(uuid_file), ''.join(Finaltext)

def saveDataBase(uuid_file,srtFileName):
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
    print(uuid)
    print(path)
    con.close()
    return path[0]