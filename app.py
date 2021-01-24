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


#         jobsInCity = []
# city = "Noida"
# for i in range (len(df)):
#     if city in df.iloc[i]['Location']:
#         jobsInCity.append(df.iloc[i]) 



#         rolesInCity = {}
# for i in range (len(jobsInCity)):
#     if (jobsInCity[i]['Role'] in rolesInCity):
#         rolesInCity[jobsInCity[i]['Role']] += 1
#     else:
#         rolesInCity[jobsInCity[i]['Role']] = 1


# role = "Software Developer"
# jobs = []
# for i in range (len(jobsInCity)):
#     if role in jobsInCity[i]['Role']:
#         jobs.append(jobsInCity[i])


# jobs is all the jobs of the chosen role in the chosen city

#rolesInCity is a list of all the roles in the chosen city


#jobsInCity is a list of all the jobs in the city
        jobsInCity = []
        # breh
        # need to match cities info with our query value
        for i in range (len(data)):
            if query in data.iloc[i]['Location']:
                jobsInCity.append(df.iloc[i])
        # we need to find the most frequent jobs with appropriate city match
        rolesInCity = []
        for i in range (len(jobsInCity)):
            if (jobsInCity[i]['Role'] in rolesInCity):
                rolesInCity[jobsInCity[i]['Role']] += 1
            else:
                rolesInCity[jobsInCity[i]['Role']] = 1

        # find the top 5 common roles 
        rolesInCity.sort(reverse = True)
        top5Roles = rolesInCity[:5]

        # find the number of jobs available to each role in the city
        # jobs = []
        # count = 0
        # role = top5Roles[count]

        # for i in range (len(top5Roles)):
        #     if role in jobsInCity[i]['Role']:
        #         count += 1
        #         jobs.append(jobsInCity[i])
        
        # find the average salary for each role in the city
        
        # salaries = []
        # for i in range(len(jobsInCity)):
            

        results = ["Textiles Manager", "Supply Chain Analyst", "Telemarketer"]
        return render_template('results.html', query=query.capitalize(), results=results)
    else:
        return redirect((url_for('splash')))
    
@app.route('/explore/<query>/<focus>')
def explore(query=None, focus=None):
    if query is not None and focus is not None:
        # breh
        results = ["Textiles Manager", "Supply Chain Analyst", "Telemarketer"]
        return render_template('explore.html', query=query.capitalize(), focus=focus)
    else:
        return redirect((url_for('results', query=query)))