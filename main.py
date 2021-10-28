from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, Api
import os.path
import logging

app = Flask(__name__)
api = Api(app)

# REST Get Parameters
ARG_KEY = 'key'

# FILE Names and paths
KEYFILE_FILE = 'keys.txt'

def createDefaultFiles():
    if not keyFileExists:
        fp = open(KEYFILE_FILE, 'w')
        defaultKey = input("No keys file detected! Please enter first API key: ")
        fp.write(defaultKey)
        fp.close()

def containsRequiredArgs(request):
    params = request.args
    key = params.get(ARG_KEY)
    if not key:
        return False
    return True

def getDictOfKeys():
    with open(KEYFILE_FILE) as f:
        keys = f.read().splitlines()
        return keys

def verify(request):
    params = request.args
    key = params.get(ARG_KEY)

    keyFileExists = os.path.exists(KEYFILE_FILE)
    if keyFileExists:
        keys = getDictOfKeys()
        if key not in keys:
            return False
        else: # Will add reading of file with acceptable API keys
            return True
    else:
        error = '''API Key File {} was not found, rejecting all requests'''.format(KEYFILE_FILE)
        app.logger.info(error)
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
    keyFileExists = os.path.exists(KEYFILE_FILE)
    createDefaultFiles()
    app.run(debug=True)