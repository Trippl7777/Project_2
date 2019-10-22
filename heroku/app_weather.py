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
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('HEROKU_POSTGRESQL_BLUE_URL', '') or "sqlite:///crime_pop.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

class CrimeWeather(db.Model):
    __tablename__ = 'combined'
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
    __tablename__ = 'crime_pop' 
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
def samples(sample):
    """Return summarized data by selected sample."""
    data = {}
    words = sample.split("1")
    weather = ["base", "Clear", "Mostly Cloudy", "Overcast", "Partly Cloudy", "Rain", "Snow"]
    
    for i in range(len(weather)):
        if (weather[i] == "base") :

            #CHRIS' WORK
            # stmt1 = "SELECT crime_pop." + (words[0]) +", SUM(crime_pop.Count), AVG(crime_pop.Population) FROM crime_pop"
            # stmt5 = " GROUP BY crime_pop." + words[0]
            # stmt6 = " ORDER BY crime_pop." + words[0]
            # stmt = stmt1 + stmt5 + stmt6

            # df = pd.read_sql_query(stmt, db.session.bind)
            # df = pd.read_sql_query(stmt, db.session.query)




#------------ my interpretation

            stmt1 = "crime_pop." + words[0] +",func.sum(crime_pop.Count),func.avg(crime_pop.Population)"
            stmt5 = ".group_by(crime_pop." + words[0]+ ")"
            stmt6 = ".order_by(crime_pop." + words[0]+ ").all()"
            stmt = stmt1 + stmt5 + stmt6

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
            # results2 = ()
            for result in results:
                
                result = list(result)
                print(result)
                results1.append(result)
            #     for r in result:
            #         r = round(r,1)
            #         print(r)
            #         results2.append(r)
            #     results1.append(results2)
            df = pd.DataFrame(results1)   

            #         if type(r) == 'decimal.Decimal':
            #             print("found decimal")
            #             r = float(r)
            print (results1)
            # df = pd.read_sql_query(results, db.session.bind)
            # df = pd.read_json(jsonify(results))
            print("==================")
            print(df)
            print(df[0])

            # df = pd.read_sql_query(stmt, db.session.bind)
            # print(df)
            df["ratio"] = df.iloc[:,1] * 0
            data.update({weather[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})

        # else:
        #     stmt1 = "SELECT crime_pop." + words[0] +", SUM(crime_pop.Count), AVG(crime_pop.Population) FROM crime_pop"
        #     stmt2 = " WHERE crime_pop.MapWeather = " + "'" + weather[i] + "'"
            
        #     if (words[1] == "All"):
        #         stmt3 = ""
        #     else:
        #         stmt3 = " AND MapCrime = '" + words[1] + "'"
            
        #     if (words[2] == "All"):
        #         stmt4 = ""
        #     else:
        #         stmt4 = " AND City = '" + words[2] + "'"
            
        #     stmt5 = " GROUP BY crime_pop." + words[0]
        #     stmt6 = " ORDER BY crime_pop." + words[0]
        #     stmt = stmt1 + stmt2 + stmt3 + stmt4 + stmt5 + stmt6

        #     df = pd.read_sql_query(stmt, db.session.query)
#------------ my interpretation
            # stmt1 = "SELECT crime_pop." + words[0] +", SUM(crime_pop.Count), AVG(crime_pop.Population) FROM crime_pop"
            # stmt2 = " WHERE crime_pop.MapWeather = " + "'" + weather[i] + "'"


            # df = db.session.query(stmt)
            # print(df)

            # measure = words[3]
            # if (measure == "Percentage") :
            #     divisor = df["SUM(crime_pop.Count)"].sum()
            # elif (measure == "Per Capita") :
            #     divisor = df["AVG(crime_pop.Population)"].sum() / 1000
            # else :
            #     divisor = 1
 
            # df["ratio"] = df.iloc[:,1] / divisor            
            # data.update({weather[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,3].tolist()}})

    return jsonify(data)

#-------JULIAN
@app.route("/api")
def crimeweather():
    result = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
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
    result = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
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
    results = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
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
