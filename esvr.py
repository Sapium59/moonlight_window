import sys, os
sys.path.insert(1,os.path.dirname(__file__))
print(sys.path)


import requests
from flask import Flask, request, render_template, send_from_directory, send_file
from moonlight_window import moonlight_window

app = Flask(__name__)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='output', filename=filename)


@app.route('/download/<path:url>')
def download_file(url):
    response = requests.get("https://" + url)
    with open('temp_file.png', 'wb') as f:
        f.write(response.content)
    return send_file(os.path.basename(url), as_attachment=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    input_string = request.form['input']
    font = request.form['font']
    # do something with the input string to produce the output
    res = moonlight_window(input_string, font)
    if res == "Success!":
        return render_template(
            'result_success.html', 
            result=input_string,
            )
    else:
        return render_template(
            'result_fail.html', 
            result=res,
            )
