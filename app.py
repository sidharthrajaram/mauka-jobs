from flask import Flask
from flask import request, jsonify, redirect, url_for, render_template
import pandas as pd
import re
from googleapiclient.discovery import build
import requests

my_api_key = "AIzaSyCK6ggQxTBGVDUe2AhiivaU5fK0pgREjoE"
YT_SEARCH_ID = "9c71e23e36e197d73"

app = Flask(__name__)
data = pd.read_csv('FilteredData.csv')

# google custom search engine method
def search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


# retrieves cleaned up urls from google search or YT search depending on cse ID parameter
def get_urls(search_term, cse=YT_SEARCH_ID):
    results = search(search_term, my_api_key, cse, num=3)
    urls = []
    for result in results:
        url = result["formattedUrl"]
        urls.append(url)
    return urls

def get_materials(search_term, cse=YT_SEARCH_ID):
    
    query = search_term
    # using the first page
    page = 1
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={my_api_key}&cx={YT_SEARCH_ID}&q={query}"
    data = requests.get(url).json()
    search_items = data.get("items")[:1]
    return search_items

# create url for youtube search based on parsed query
def generate_youtube_url(split_query):
    query = '+'.join(split_query)
    url = str(get_urls(query, cse=YT_SEARCH_ID)[1])
    return url


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

# jobs is all the jobs of the chosen role in the chosen city

#rolesFreqInCity is a list of all the roles in the chosen city

#jobsInCity is a list of all the jobs in the city
        jobsInCity = []
        # breh
        # need to match cities info with our query value
        for i in range (len(data)):
            if query.lower() in data.iloc[i]['Location'].lower():
                jobsInCity.append(data.iloc[i])
        # we need to find the most frequent jobs with appropriate city match
        rolesFreqInCity = {}
        for i in range (len(jobsInCity)):
            if (jobsInCity[i]['Role'] in rolesFreqInCity):
                rolesFreqInCity[jobsInCity[i]['Role']] += 1
            else:
                rolesFreqInCity[jobsInCity[i]['Role']] = 1

        # find the top 5 common roles 
        #rolesFreqInCity.sort(reverse = True)

        sortedVals = sorted(rolesFreqInCity.items(), key=lambda i: i[1], reverse=True)
        top5Roles = sortedVals[:8]
        
        sum_of_top5 = 0
        for role in top5Roles:
            for i in range (len(jobsInCity)):
                if (type(jobsInCity[i]['Role']) == str) and role[0] in jobsInCity[i]['Role']:
                    sum_of_top5 += 1
            

        results = []
        for role in top5Roles:
            sum = 0
            valid_salaries = 0

            for i in range (len(jobsInCity)):
                # print(data.iloc[i]['Job Title'])
                # print(data.iloc[i]['Location'])
                # print(type(data.iloc[i]['Role']))
                if (type(jobsInCity[i]['Role']) == str):
                    if role[0] in jobsInCity[i]['Role']:
                        salary = jobsInCity[i]['Job Salary']
                        if salary > 0:
                            sum += salary
                            valid_salaries += 1
                        
            print(sum_of_top5)
            popularity = 20
            avg = "Not available"
            if valid_salaries > 0:
                avg = int(sum/valid_salaries)
                avg = "INR " + str(avg)
            if sum_of_top5 > 0:
                popularity = int(100*role[1]/sum_of_top5)
            
            if popularity < 33:
                popularity += 30
                
            
            
            result = {"role":role[0], "num":role[1], "avg":avg, "popularity":popularity}
            results.append(result)

        return render_template('results.html', query=query.capitalize(), results=results)
    else:
        return redirect((url_for('splash')))
    
    
def most_popular_skills(skills_dict, top=8):
    sortedSkills = sorted(skills_dict.items(), key=lambda i: i[1], reverse=True)
    topSkills = sortedSkills[:top]
    return topSkills
    
@app.route('/explore/<query>/<focus>')
def explore(query=None, focus=None):
    if query is not None and focus is not None:
        # breh
        
        query_jobs = []
        skills_dict = {}
        city = query.capitalize()
        for i in range (len(data)):
            if city in data.iloc[i]['Location'] and focus in data.iloc[i]['Role']:
                raw_skills = data.iloc[i]["Key Skills"]
                skills = raw_skills.replace('[','')
                skills = skills.replace(']','')
                skills = skills.replace('\'', '')
                skills_split = skills.split(', ')
                for skill in skills_split:
                    if skill in skills_dict:
                        skills_dict[skill] += 1
                    else:
                        skills_dict[skill] = 1
                        
                pay = data.iloc[i]['Job Salary']
                if int(pay) > 0:
                    pay = "INR " + str(pay)
                else:
                    pay = "Not available"
                    
                job = {"title":data.iloc[i]["Job Title"],
                       "location":city,
                       "pay": pay,
                       "skills":skills}
                query_jobs.append(job)
                if len(query_jobs) > 4:
                    break
        
        materials = []
        popular_skills = most_popular_skills(skills_dict)

        for skill in popular_skills:
            materials += get_materials(skill[0])
            
        
        return render_template('explore.html', 
                               query=query.capitalize(), 
                               focus=focus, 
                               jobs=query_jobs, 
                               materials=materials)
    else:
        return redirect((url_for('results', query=query)))