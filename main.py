"""
Print anything to a DotMatrix printer and log from REST
Initially written by Kyle Mikolajczyk (@kylemikableh)
"""


import os.path
import platform
import subprocess
from strenum import StrEnum
from flask import Flask
from flask import request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# REST Get Parameters
ARG_KEY = 'key'
ARG_PRINT_DATA = 'pdata'

# FILE Names and paths
KEYFILE_FILE = 'keys.txt'
PRINTLOG_FILE = 'print.log'
TEMPPRINT_FILE = 'tempprint.txt'


class Platform(StrEnum):
    """
    Class for enums of Platforms to detect
    """
    LINUX = "Linux"
    MAC = "Darwin"
    WINDOWS = "Windows"


def create_default_files():
    """
    Generate default files for the API server
    :return:
    """
    if not os.path.exists(KEYFILE_FILE):
        fp = open(KEYFILE_FILE, 'w', encoding="utf8")  # pylint: disable=invalid-name,consider-using-with
        default_key = input("No keys file detected! Please enter first API key: ")
        fp.write(default_key)
        fp.close()
    if not os.path.exists(PRINTLOG_FILE):
        fp = open(PRINTLOG_FILE, 'x', encoding="utf8")  # pylint: disable=invalid-name,consider-using-with
        fp.close()
    if not os.path.exists(TEMPPRINT_FILE):
        fp = open(TEMPPRINT_FILE, 'x', encoding="utf8")  # pylint: disable=invalid-name,consider-using-with
        fp.close()


def contains_required_args(request_passed):
    """
    Check if the request contains an API key
    :param request_passed: the URL request
    :return: True if contains the key, False otherwise
    """
    params = request_passed.args
    key = params.get(ARG_KEY)
    if not key:
        return False
    return True


def get_dict_of_keys():
    """
    Grab all valid API keys from file
    :return: dict of string of keys
    """
    with open(KEYFILE_FILE, encoding="utf8") as key_file:
        keys = key_file.read().splitlines()
        return keys


def verify(request_passed):
    """
    Verify that the key passed is valid
    :param request_passed: URL request passed
    :return: True if key is valid
    """
    params = request_passed.args
    key = params.get(ARG_KEY)

    key_file_exists = os.path.exists(KEYFILE_FILE)
    if key_file_exists:
        keys = get_dict_of_keys()
        if key not in keys:
            return False
        return True
    error = '''API Key File {} was not found,
     rejecting all requests'''.format(KEYFILE_FILE)  # pylint: disable=consider-using-f-string
    app.logger.error(error)  # pylint: disable=no-member
    return False


def format_for_dot_matrix(data):
    """
    Format the data for the DotMatrix printer
    :param data: String data to print to printer
    :return: Correctly formatted data for printer
    """
    return data


def print_to_locations():
    """
    Send print data to printing locations
    :return: String of status
    """
    params = request.args
    data = params.get(ARG_PRINT_DATA)
    if not data:
        return '''Did not recieve any print data. Not printing.'''
    app.logger.info('''Recieved print data: {}'''.format(data))  # pylint: disable=no-member,consider-using-f-string
    formatted_data = format_for_dot_matrix(data)
    if os.path.exists(PRINTLOG_FILE):
        app.logger.info('''Printing to logfile recieved print data''')  # pylint: disable=no-member
        log_file = open(PRINTLOG_FILE, 'a', encoding="utf8")  # pylint: disable=consider-using-with
        log_file.write(formatted_data + "\n")
        log_file.close()
    else:
        app.logger.error('''Missing print file, please restart server.''')  # pylint: disable=no-member
    #
    print_status = print_to_printer(formatted_data)
    app.logger.error('''Print status: {}'''.format(print_status))  # pylint: disable=no-member
    return '''Recieved print data: {}.<br> Printer status:<br>{}'''.format(data, print_status)  # pylint: disable=consider-using-f-string


def print_to_printer(data):
    """
    Print to printer
    :return:
    """
    log_file = open(TEMPPRINT_FILE, 'w', encoding="utf8")  # pylint: disable=consider-using-with
    log_file.write('\n')  # Fix for CUPS not printing the first line
    log_file.write(data)
    log_file.close()
    current_platform = platform.system()
    app.logger.error('''Printing to printer with os: {}'''.format(current_platform))  # pylint: disable=no-member
    if current_platform == Platform.WINDOWS:
        os.startfile(PRINTLOG_FILE, "print")
        return '''Platform detected: WINDOWS'''
    if current_platform == Platform.MAC:
        return '''Platform detected: MAC'''
    if current_platform == Platform.LINUX:
        cmd = '''lp -o raw {}'''.format(TEMPPRINT_FILE)
        subprocess.run(
            cmd, shell=True)
        return '''Platform detected: LINUX'''
    return '''Did not find platform: {}'''.format(Platform.MAC)


@app.route('/', methods=['GET'])
def home():
    """
    Default home landing page. Shouldn't do anything, might add documentation or something
    :return:
    """
    return '''<html><head><title>KyAPI</title></head><h1>KyAPI</h1>
<p>Kyle's simple API server. Must supply path and API key for access.</p></html>'''


@app.route('/print', methods=['GET'])
def print_request():
    """
    The print path
    :return: String to return to browser, e.g. HTML
    """
    if contains_required_args(request):
        if verify(request):
            # We have been verified, now do function
            return print_to_locations()
        return '''API Key invalid'''
    return '''API key not provided'''


if __name__ == '__main__':
    create_default_files()
    logFileLocation = os.path.abspath(PRINTLOG_FILE)
    print('''Log file is located at: {}'''.format(logFileLocation))  # pylint: disable=consider-using-f-string
    keysFileLocation = os.path.abspath(KEYFILE_FILE)
    print('''Key file is located at: {}'''.format(keysFileLocation))  # pylint: disable=consider-using-f-string
    app.run('0.0.0.0', port=5000, debug=True)
