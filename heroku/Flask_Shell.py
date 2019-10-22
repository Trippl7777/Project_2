import os

import pandas as pd
import numpy as np

from graph1 import graph1
from graph2 import graph2

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.sql import func

app = Flask(__name__)

#################################################
# Database Setup
#################################################

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/crime_pop.sqlite"
app.config["SQLALCHEMY_BINDS"] = {
    'sunburst':     'sqlite:///db/sunburst.sqlite',
    'combined':     'sqlite:///db/db.sqlite'
}

db = SQLAlchemy(app)

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)
class combined(db.Model):
    # __tablename__ = 'combined'
    __bind_key__ = 'combined'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30))
    code = db.Column(db.String(10))
    startdate = db.Column(db.String(30))#(db.DateTime)
    starttime = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    mapping = db.Column(db.String(50))
    weather = db.Column(db.String(50))

    def __repr__(self):
        return '<CrimeWeather %r>' % (self.name)

class crime_pop(db.Model):
    # __tablename__ = 'crime_pop' 
    __bind_key__ = 'crime_pop'
    City = db.Column(db.String(30), primary_key=True)
    Year = db.Column(db.Integer)
    Month = db.Column(db.Integer)
    DayofWeek = db.Column(db.String(15))
    StartTime = db.Column(db.Integer)
    MapCrime = db.Column(db.String(40))
    MapWeather = db.Column(db.String(50))
    Population = db.Column(db.Integer)
    Count = db.Column(db.Integer)

class sunburst(db.Model):
    # __tablename__ = 'sunburst'
    __bind_key__ = 'sunburst'
    id = db.Column(db.Integer, primary_key=True)
    Ids = db.Column(db.String(50))
    Labels = db.Column(db.String(50))
    Parents = db.Column(db.String(50))
    Values = db.Column(db.String(50))

    def __repr__(self):
        return '<sunburst %r>' % (self.name)

chart = "Year"
crime = "All"
weather = "All"

@app.route("/")
def welcome():
    """List all available api routes."""
    # return (
    #     f"Available Routes:<br/>"
    #     f"/plot1<br/>"
    #     f"/plot2<br/>"
    #     f"/callsunburst<br/>"
    #     f"/api<br/>"
    #     f"/api/<cityname> (denver,atlanta,boston)"
    # )
    return render_template("index.html")

@app.route("/plot1")
def plot1():
    """Return the homepage."""
    return render_template("plot1.html")

@app.route("/plot2")
def plot2():
    """Return the homepage."""
    return render_template("plot2.html")

@app.route("/chartroute")
def chartroute():
    """Return a list of selector names."""
    selectors = ["Year", "Month", "DayofWeek", "StartTime"]
    
    return jsonify(selectors)

@app.route("/callsunburst")
def callsunburst():
    return render_template("sunburst.html")

@app.route("/sunburst")
def Sunny():
    results = db.session.query(sunburst.Ids, sunburst.Labels, sunburst.Parents, sunburst.Values).all()

    ids = [result[0] for result in results]
    labels = [result[1] for result in results]
    parents = [result[2] for result in results]
    values = [result[3] for result in results]

    sunburst_data = {
        "ids": ids,
        "labels": labels,
        "parents": parents,
        "values": values}

    return jsonify(sunburst_data)

@app.route("/crimeroute")
def crimeroute():
    """Return a list of selector names."""
    selectors = ["All", "Auto-Theft", "Other", "Property", "Theft", "Violation", "Violence"]
    
    return jsonify(selectors)

@app.route("/weatherroute")
def weatherroute():
    """Return a list of selector names."""
    selectors = ["All", "Clear", "Mostly Cloudy", "Overcast", "Partly Cloudy", "Rain", "Snow"]

    return jsonify(selectors)

@app.route("/cityroute")
def cityroute():
    """Return a list of selector names."""
    selectors = ["All", "atlanta", "boston", "chicago", "denver", "los_angeles"]

    return jsonify(selectors)

@app.route("/measureroute")
def measureroute():
    """Return a list of selector names."""
    selectors = ["Percentage", "Per Capita", "Count"]

    return jsonify(selectors)

@app.route("/samples/<sample>")
def samples1(sample):
    """Return summarized data by selected sample."""
    data = {}
    print(sample)
    words = sample.split("1")

    if (words[0] == "first") :
        data = graph1(sample, db.session)
    else :
        data = graph2(sample, db.session)

    return data

# API
@app.route("/api")
def crimeweather():
    result = db.session.query(combined.city,combined.code,combined.startdate,combined.starttime,
    combined.latitude,combined.longitude,combined.mapping,combined.weather).first()
    
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

@app.route("/api/<city>") # City filter test path
def crimeweather_state(city):
    results = db.session.query(combined.city,combined.code,combined.startdate,combined.starttime,
    combined.latitude,combined.longitude,combined.mapping,combined.weather).filter(combined.city == city).all() #.first()

    # Uncomment these and comment the duplicates below if .all() is selected
    city = [result[0] for result in results]
    code = [result[1] for result in results]
    date = [result[2] for result in results]
    time = [result[3] for result in results]
    lat = [result[4] for result in results]
    lon = [result[5] for result in results]
    mapping = [result[6] for result in results]
    weather = [result[7] for result in results]

    # city = result[0]
    # code = result[1]
    # date = result[2]
    # time = result[3]
    # lat = result[4]
    # lon = result[5]
    # mapping = result[6]
    # weather = result[7]

    crimeweather_data = [{
        "location":{
            "city":city,
            "lat":lat,
            "lon":lon
        },
        "crime":{
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

@app.route("/api/data")
# !!!WARNING!!! Navigating to this path may cause a timeout/overload error.
#   If you want subqueries, please filter the data before in order to possibly avoid these errors!
def crimeweather_full():
    results = db.session.query(combined.city,combined.code,combined.startdate,combined.starttime,
    combined.latitude,combined.longitude,combined.mapping,combined.weather).all()

    city = [result[0] for result in results]
    code = [result[1] for result in results]
    date = [result[2] for result in results]
    time = [result[3] for result in results]
    lat = [result[4] for result in results]
    lon = [result[5] for result in results]
    mapping = [result[6] for result in results]
    weather = [result[7] for result in results]

    crimeweather_data = [{
        "location":{
            "city":city,
            "lat":lat,
            "lon":lon
        },
        "crime":{
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



if __name__ == "__main__":
    app.run()
