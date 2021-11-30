from genericpath import exists
from sys import path
from flask import Flask
from flask import request, jsonify
from flask_restful import Resource, Api
import os.path
import logging

app = Flask(__name__)
api = Api(app)

# REST Get Parameters
ARG_KEY = 'key'
ARG_PRINT_DATA = 'pdata'

# FILE Names and paths
KEYFILE_FILE = 'keys.txt'
PRINTLOG_FILE = 'print.log'


def createDefaultFiles():
    if not os.path.exists(KEYFILE_FILE):
        fp = open(KEYFILE_FILE, 'w')
        defaultKey = input("No keys file detected! Please enter first API key: ")
        fp.write(defaultKey)
        fp.close()
    if not os.path.exists(PRINTLOG_FILE):
        fp = open(PRINTLOG_FILE, 'x')
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
        else:  # Will add reading of file with acceptable API keys
            return True
    else:
        error = '''API Key File {} was not found, rejecting all requests'''.format(KEYFILE_FILE)
        app.logger.info(error)
    return False


def formatForDotMatrix(data):
    return data


def printToPrinter():
    params = request.args
    data = params.get(ARG_PRINT_DATA)
    if not data:
        return '''Did not recieve any print data. Not printing.'''
    app.logger.info('''Recieved print data: {}'''.format(data))
    formattedData = formatForDotMatrix(data)
    if os.path.exists(PRINTLOG_FILE):
        app.logger.info('''Printing to logfile recieved print data''')
        fp = open(PRINTLOG_FILE, 'a')
        fp.write(formattedData + "\n")
        fp.close()
    else:
        app.logger.error('''Missing print file, please restart server.''')
    return '''Recieved print data: {}'''.format(data)


@app.route('/', methods=['GET'])
def home():
    return '''<html><head><title>KyAPI</title></head><h1>KyAPI</h1>
<p>Kyle's simple API server. Must supply path and API key for access.</p></html>'''


@app.route('/print', methods=['GET'])
def printRequest():
    if containsRequiredArgs(request):
        if verify(request):
            # We have been verified, now do function
            return printToPrinter()
        return '''API Key invalid'''
    return '''API key not provided'''


if __name__ == '__main__':
    createDefaultFiles()
    logFileLocation = os.path.abspath(PRINTLOG_FILE)
    print('''Log file is located at: {}'''.format(logFileLocation))
    app.run(debug=True)
