import dbconfig
if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

from flask import Flask
from flask import render_template
from flask import request

import json
import dateparser
import datetime

app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in', 'grabble']

@app.route("/")
def home(error_message=None):
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print(e)
        crimes = None
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()

@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    try:
        category = request.form.get("category")
        if category not in categories:
            return home()
        date = format_date(request.form.get("date"))
        if not date:
            return home("Error! Use format date yyyy-mm-dd")
        longitude = float(request.form.get("longitude"))
        latitude = float(request.form.get("latitude"))
        description = request.form.get("description")
        DB.add_crime(category, date, longitude, latitude, description)
    except Exception as e:
        print(e)
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None




if __name__ == "__main__":
    app.run(port=5000, debug=True)