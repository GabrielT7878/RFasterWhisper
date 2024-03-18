from flask import Flask, jsonify, request
from faster_whisper_transcribe import transcribe
from werkzeug.utils import secure_filename

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
        text = transcribe(file_path)
        return text
        
    except:
        #os.remove(file_path)
        raise Exception("Error While executing the transcribe routine")

app.run(port=8080,host="0.0.0.0",debug=True)

