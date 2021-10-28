from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# REST Get Parameters
ARG_KEY = 'key'

def containsRequiredArgs(request):
    params = request.args
    key = params.get(ARG_KEY)
    if not key:
        return False
    return True

def verify(request):
    params = request.args
    key = params.get(ARG_KEY)
    if not key:
        return 
    if(key == '1234'): # Will add reading of file with acceptable API keys
        return True
    return False

@app.route('/', methods=['GET'])
def home():
    return '''<html><head><title>KyAPI</title></head><h1>KyAPI</h1>
<p>Kyle's simple API server. Must supply path and API key for access.</p></html>'''

@app.route('/print', methods=['GET'])
def print():
    if containsRequiredArgs(request):
        if verify(request):
            return '''API Key accepted'''
        return '''API Key invalid'''
    return '''API key not provided'''

if __name__ == '__main__':
    app.run()