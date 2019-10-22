# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################


# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_BLUE_URL', '') #or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

# from .models import CrimeWeather
#import models

# ==========
class CrimeWeather(db.Model):
    __tablename__ = 'combined'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30))
    code = db.Column(db.String(10))
    startdate = db.Column(db.String(30))#(db.DateTime)
    starttime = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # crime_desc = db.Column(db.String())
    mapping = db.Column(db.String(50))
    weather = db.Column(db.String(50))

    def __repr__(self):
        return '<CrimeWeather %r>' % (self.name)

# ==========

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index2.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    # if request.method == "POST":
    #     name = request.form["petName"]
    #     lat = request.form["petLat"]
    #     lon = request.form["petLon"]

    #     pet = Pet(name=name, lat=lat, lon=lon)
    #     db.session.add(pet)
    #     db.session.commit()
    #     return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api")
def crimeweather():
    result = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).first()#.all()

  

    city = result[0]
    code = result[1]
    date = result[2]
    time = result[3]
    lat = result[4]
    lon = result[5]
    mapping = result[6]
    weather = result[7]


    crimeweather_data = [{
        "location":{
            "city":city,
            "lat":lat,
            "lon":lon
        },
        "crime":{
            # "crime_desc":crime_desc,
            "mapping":mapping,
            "code":code
        },
        "time":{
            "date":date,
            "hour":time
        },
        "weather":weather
    }]

    return jsonify(crimeweather_data)

@app.route("/index2")
def index2():
    """Return the homepage."""
    return render_template("index2.html")

@app.route("/names")
def names():
    """Return a list of selector names."""
    selectors = ["Year", "Month", "DayofWeek", "StartTime"]
    #print(selectors)
    return jsonify(selectors)

@app.route("/samples/<sample>")
def samples(sample):
    """Return summarized data by selected sample."""
    data = {}
    cities = ["atlanta", "boston", "chicago", "denver", "los_angeles"]
    for i in range(len(cities)):
        stmt1 = "SELECT " + sample +", SUM(Count) FROM crime"
        stmt2 = " WHERE City = " + "'" + cities[i] + "'"
        stmt3 = " GROUP BY " + sample
        stmt = stmt1 + stmt2 + stmt3
        df = pd.read_sql_query(stmt, db.session.bind)
        df["ratio"] = df.iloc[:,1] / df["SUM(Count)"].sum()
        print(cities[i])
        data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,2].tolist()}})

    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
