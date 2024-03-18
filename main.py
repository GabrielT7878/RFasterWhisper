from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/',methods=["GET"])
def home():
    return "Hello Python Api"

app.run(port=8080,host="0.0.0.0",debug=True)

