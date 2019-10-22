import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup
#################################################

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') 
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/crime.sqlite"


# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crime.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# app.config['SQLALCHEMY_BINDS'] = {'crime_db': 'SQLALCHEMY_DATABASE_URI',
#                                     'main_db': os.environ.get('HEROKU_POSTGRESQL_BLUE_URL', '') #or "sqlite:///db.sqlite"
#                                 }

db = SQLAlchemy(app)

# ==========
class CrimeWeather(db.Model):
    __tablename__ = 'combined'
    __bind_key__ = 'main_db'
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

class CrimeDB(db.Model):
    # __tablename__ = 'combined'
    __bind_key__ = 'crime_db'


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index2.html")

@app.route("/names")
def names():
    """Return a list of selector names."""
    selectors = ["Year", "Month", "DayofWeek", "StartTime"]
    #print(selectors)
    return jsonify(selectors)

# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return summarized data by selected sample."""
#     data = {}
#     cities = ["atlanta", "boston", "chicago", "denver", "los_angeles"]
#     for i in range(len(cities)):
#         stmt1 = "SELECT " + sample +", SUM(Count) FROM crime"
#         stmt2 = " WHERE City = " + "'" + cities[i] + "'"
#         stmt3 = " GROUP BY " + sample
#         stmt = stmt1 + stmt2 + stmt3
#         df = pd.read_sql_query(stmt, db.session.bind)
#         df["ratio"] = df.iloc[:,1] / df["SUM(Count)"].sum()
#         print(cities[i])
#         data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,2].tolist()}})

#     print(data)
#     return jsonify(data)

# --------- ADDING JULIANS WORK
@app.route("/api")
def crimeweather():
    result = main_db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).first()
    
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
    result = main_db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).filter(CrimeWeather.city == city).first()#.all()

    # Uncomment these and comment the duplicates below if .all() is selected
    # city = [result[0] for result in results]
    # code = [result[1] for result in results]
    # date = [result[2] for result in results]
    # time = [result[3] for result in results]
    # lat = [result[4] for result in results]
    # lon = [result[5] for result in results]
    # mapping = [result[6] for result in results]
    # weather = [result[7] for result in results]

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

@app.route("/api/data") 
# !!!WARNING!!! Navigating to this path may cause a timeout/overload error.
#   If you want subqueries, please filter the data before in order to possibly avoid these errors!
def crimeweather_full():
    results = main_db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).all()

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
