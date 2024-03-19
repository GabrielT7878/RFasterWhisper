from flask import Flask, jsonify, request, jsonify, json, send_file
from faster_whisper_transcribe import transcribe
from werkzeug.utils import secure_filename
from utils import *

import os

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'cache')
os.makedirs(uploads_dir, exist_ok=True)



@app.route('/',methods=["POST"])
def upload():
    global file_path

    try:
        file = request.files['file']
        file_path = os.path.join(uploads_dir, secure_filename(file.filename))
        file.save(file_path)
        uuid, text = transcribe(file_path,file.filename)

        os.remove(file_path)
        return jsonify(uuid=uuid,text=text)
    except:

        raise Exception("Error While executing the transcribe routine")
    

@app.route('/<uuid>',methods=["GET"])
def srtFile(uuid):
    print(uuid)
    path = getSrtFile(uuid)
    return send_file(path,as_attachment=True)

app.run(port=8080,host="0.0.0.0",debug=True)

