# PiPrint API
## About
Welcome to PiPrint API. This project, under the MIT License, is a Python Flask server that allows anyone to send REST requests for printing to a printer of their choice. 
## Why?
The idea for the program was created when I acquired an OKIData Microline 186 9 Pin DotMatrix printer. The goal for this printer was to have a constantly printing "log" that prints line-by-line as it receives requests.  I hoped to find a program that could do this for me, so that I could send alert and information data from any other program and the result will be a central log for all programs in my apartment. 
## How to use
### Development Mode (All Operating Systems)
1) You must have Python 3.7 or later [installed](https://www.python.org/)
2) Download the project
3) After downloading the project, you must run the `requirements.txt` through Python's PIP to install the required modules: 
```
pip install -r requirements.txt
```
4) Next, you will run the program:
```
python3 main.py
```
5) The program will next prompt the user to give some config details, follow the prompt
6) At this point, the development server will be running and the required files will be generated (`keys.txt`,`print.log`, and `temmprint.txt`)
7) The prompt will give you a URL to access the website, follow the link
8) At this point you are now on the program! You must now navigate to the url: `/print`
9) Here, it will warn you that there is no API key. You must supply the API key at the end of the url using the format: `/print?key=[KEY]` where `[KEY]` is you key you created during the setup.
10) Now, it should warn you that you have not given any data. This is the last step! Append the data to the end of the URL: `/print?key=[KEY]&pdata=[DATA]` where `[DATA]` is the text you want printed to the log file and printer. For example:
```
/print?key=12345678abcd&pdata=Hello%20World!
```
11) NOTE: To add a space to printed data, you must use the URL space of `%20` in the URL wherever a whitespace is wanted.