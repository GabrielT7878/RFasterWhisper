from flask import Flask, jsonify, request, jsonify, json, send_file
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from audio_extract import extract_audio
from repository import getSrtFile
from service import *
import os

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'cache')
os.makedirs(uploads_dir, exist_ok=True)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e.name)), 404


@app.route('/audio',methods=["POST"])
def uploadAudio():
    try:
        file = request.files['file']
        file_path = os.path.join(uploads_dir, secure_filename(file.filename))
        file.save(file_path)
       
        result = transcribe(file_path,file.filename)
        os.remove(file_path)
        return result
    except:
        raise Exception("Error while executing the transcribe routine")
    
@app.route('/video',methods=["POST"])
def uploadVideo():
    try:
        file = request.files['file']
        video_file_path = os.path.join(uploads_dir, secure_filename(file.filename))
        file.save(video_file_path)
        audio_file_path = video_file_path.split('.')[0] + '.mp3'
        extract_audio(input_path=video_file_path, output_path=audio_file_path)
        os.remove(video_file_path)
        result = transcribe(audio_file_path,file_name=audio_file_path.split('/')[-1])
        os.remove(audio_file_path)
        return result
    except:
        raise Exception("Error while executing the transcribe routine")
    

@app.route('/<uuid>',methods=["GET"])
def srtFile(uuid):
    path = getSrtFile(uuid)
    return send_file(path,as_attachment=True)

app.run(port=8080,host="0.0.0.0",debug=True)

