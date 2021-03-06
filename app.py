from flask import Flask, render_template, request, jsonify
import sqlite3, requests
import re

conn = sqlite3.connect('cognitev.db')
db = conn.cursor()
db.execute('CREATE TABLE IF NOT EXISTS campaign(id INTEGER PRIMARY KEY, Name TEXT UNIQUE, Country TEXT, '
           'Budget INTEGER, Goal TEXT, URL TEXT ,Category TEXT)')


app = Flask(__name__)


#campaings = datasets
#countries = data/labels
#values = count of every campaign

db.execute('SELECT DISTINCT Category FROM campaign')
datasets = db.fetchall() #category
db.execute('SELECT Country, Category, count(category) AS value FROM campaign Group by Category,Country')
values = db.fetchall() #data
db.execute('SELECT DISTINCT Country FROM campaign')
labels = db.fetchall() #countries
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        name = request.form['inputName']
        country = request.form['inputCountry']
        budget = request.form['inputBudget']
        goal = request.form['inputGoal']
        url = request.form['inputURL']
        category = request.form['inputCategory']
        if len(category) < 1:
            req = 'https://ngkc0vhbrl.execute-api.eu-west-1.amazonaws.com/api/?url='+url
            resp = requests.get(req)
            jresp = resp.json()
            category = jresp['category']['name']
        db_resp = db.execute('INSERT INTO campaign (Name, Country, Budget, Goal, URL ,category) VALUES(?,?,?,?,?,?)',
                             (name, country, budget, goal, url, category))
        conn.commit()
        if not db_resp:
            return 'db error'
        else:
            return 'success'


@app.route('/bar')
def bar():
    bar_labels=[]
    bar_values=[]

    for label in labels:
        new_label=""
        for c in label:
            new_label += c
        bar_labels.append(str(new_label))
    bar_values=values
    return render_template('bar_chart.html', title='Analysis by country and category', max=17000, labels=bar_labels, values=bar_values)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)