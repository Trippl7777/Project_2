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
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.sql import func

app = Flask(__name__)

#################################################
# Database Setup
#################################################

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crime_pop.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sunburst.sqlite"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('HEROKU_POSTGRESQL_BLUE_URL', '') or "sqlite:///crime_pop.sqlite"
app.config["SQLALCHEMY_BINDS"] = {
    'crime_pop':        'sqlite:///crime_pop.sqlite',
    'combined':     'sqlite:///db.sqlite'
}

db = SQLAlchemy(app)

# reflect an existing database into a new model
# Base = automap_base()
# reflect the tables
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

class sunburst(db.Model):
    __tablename__ = 'sunburst'
    id = db.Column(db.Integer, primary_key=True)
    Ids = db.Column(db.String(50))
    Labels = db.Column(db.String(50))
    Parents = db.Column(db.String(50))
    Values = db.Column(db.String(50))

    def __repr__(self):
        return '<sunburst %r>' % (self.name)

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

chart = "Year"
crime = "All"
weather = "All"

@app.route("/")
def index():
    """Return the homepage."""
    # return render_template("index_pop.html")
    return render_template("index.html")

@app.route("/chart")
def chart():
    return render_template("index_pop.html")

@app.route("/weather")
def weather():
    return render_template("index_weather.html")

@app.route("/chartroute")
def chartroute():
    """Return a list of selector names."""
    selectors = ["Year", "Month", "DayofWeek", "StartTime"]
    
    return jsonify(selectors)

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

@app.route("/measureroute")
def measureroute():
    """Return a list of selector names."""
    selectors = ["Percentage", "Per Capita", "Count"]

    return jsonify(selectors)

@app.route("/samples/<sample>")
def samples(sample):
    """Return summarized data by selected sample."""
    data = {}
    words = sample.split("1")

    cities = ["base", "atlanta", "boston", "chicago", "denver", "los_angeles"]
    for i in range(len(cities)):
        if (cities[i] == "base") :
            # stmt1 = "SELECT " + words[0] +", SUM(Count), AVG(Population) FROM crime_pop"
            # stmt5 = " GROUP BY " + words[0]
            # stmt6 = " ORDER BY " + words[0]
            # stmt = stmt1 + stmt5 + stmt6

            # df = pd.read_sql_query(stmt, db.session.bind)

            if words[0] == "Year":
                # df = pd.read_sql_query("(crime_pop.Year, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.Year).order_by(crime_pop.Year).all()", db.session.query)
                results = db.session.query(crime_pop.Year, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.Year).order_by(crime_pop.Year).all()#.as_scalar()
            elif words[0] == "Month":
                # df = pd.read_sql_query("(crime_pop.Month, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.Month).order_by(crime_pop.Month).all()", db.session.query)
                results = db.session.query(crime_pop.Month, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.Month).order_by(crime_pop.Month).all()
            elif words[0] == "DayofWeek":
                # df = pd.read_sql_query("(crime_pop.DayofWeek, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.DayofWeek).order_by(crime_pop.DayofWeek).all()", db.session.query)
                results = db.session.query(crime_pop.DayofWeek, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.DayofWeek).order_by(crime_pop.DayofWeek).all()
            else:
                # df = pd.read_sql_query("(crime_pop.StartTime, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.StartTime).order_by(crime_pop.StartTime).all()", db.session.query)
                results = db.session.query(crime_pop.StartTime, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).group_by(crime_pop.StartTime).order_by(crime_pop.StartTime).all()
            # print (results)

            results1 = []
            for result in results:
                result = list(result)
                print(result)
                results1.append(result)
            df = pd.DataFrame(results1)
            
            df["ratio"] = df.iloc[:,1] * 0
            print(df[0])
            print(df[2])
            # print(df[3])
            # data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})
            data.update({cities[i] : {"xAxis": df[0].tolist(), "yAxis": df[2].tolist()}})

            print(data)

        # else:
        #     stmt1 = "SELECT " + words[0] +", SUM(Count), AVG(Population) FROM crime_pop"
        #     stmt2 = " WHERE City = " + "'" + cities[i] + "'"
              # group_by(crime_pop.Year).order_by(crime_pop.Year).all()#.as_scalar()

        #     if (words[1] == "All"):
        #         stmt3 = ""
        #     else:
        #         stmt3 = " AND MapCrime = '" + words[1] + "'"
            
        #     if (words[2] == "All"):
        #         stmt4 = ""
        #     else:
        #         stmt4 = " AND MapWeather = '" + words[2] + "'"
            
        #     stmt5 = " GROUP BY " + words[0]
        #     stmt6 = " ORDER BY " + words[0]
        #     stmt = stmt1 + stmt2 + stmt3 + stmt4 + stmt5 + stmt6

        #     df = pd.read_sql_query(stmt, db.session.bind)
            
            # results = db.session.query(crime_pop.Year, func.sum(crime_pop.Count), (func.avg(crime_pop.Population))).filter(crime_pop.City = cities[i])

        #     measure = words[3]
        #     if (measure == "Percentage") :
        #         divisor = df["SUM(Count)"].sum()
        #     elif (measure == "Per Capita") :
        #         divisor = df["AVG(Population)"].sum() / 1000
        #     else :
        #         divisor = 1
 
        #     df["ratio"] = df.iloc[:,1] / divisor            
        #     data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})

    return jsonify(data)

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

if __name__ == "__main__":
    app.run()
