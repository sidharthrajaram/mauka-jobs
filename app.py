from flask import Flask
from flask import request, jsonify, redirect, url_for, render_template
import pandas as pd

app = Flask(__name__)
data = pd.read_csv('FilteredData.csv')

@app.route('/')
def splash():
    return render_template('splash_a.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        print(request.form['query'])
        return redirect((url_for('results', query=request.form['query'])))
    return redirect((url_for('splash')))

@app.route('/results/')
@app.route('/results/<query>')
def results(query=None):
    if query is not None:
        # breh
        # need to match cities info with our query value
        
        # we need to find the most frequent jobs with appropriate city match


        results = ["Textiles Manager", "Supply Chain Analyst", "Telemarketer"]
        return render_template('results.html', query=query.capitalize(), results=results)
    else:
        return redirect((url_for('splash')))
    
@app.route('/explore/<query>/<focus>')
def explore(query=None, focus=None):
    if query is not None and focus is not None:
        # breh
        query_jobs = ["Job 1", "Job 2", "Job 3"]
        materials = ["YT 123","Khan","blah"]
        return render_template('explore.html', 
                               query=query.capitalize(), 
                               focus=focus, 
                               jobs=query_jobs, 
                               materials=materials)
    else:
        return redirect((url_for('results', query=query)))
