from flask import Flask
from flask import request, jsonify, redirect, url_for, render_template
import pandas

app = Flask(__name__)

@app.route('/')
def splash():
    return 'Hello, World!'

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        print(request.form['query'])
        return redirect((url_for('results', query=request.form['query'])))
    return redirect((url_for('splash')))

@app.route('/results/')
@app.route('/results/<query>')
def results(query=None, advanced=True):
    if query is not None:
        return query
    else:
        return "no query"