# import dependencies
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import sqlite3
import numpy as np

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

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
    mapping = db.Column(db.String(50))
    weather = db.Column(db.String(50))

    def __repr__(self):
        return '<CrimeWeather %r>' % (self.name)

# create route that renders index.html template
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api for a test api statement.<br/>"
        f"/api/[INSERT CITY HERE] for a test api statement specifying city name."
    )

# ========== NEW API CODE ==========
@app.route("/api")
def crimeweather():
    results = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).limit(10).all()
    
    crimeweather_data = []
    for result in results:
        city = result[0]
        code = result[1]
        date = result[2]
        time = result[3]
        lat = result[4]
        lon = result[5]
        mapping = result[6]
        weather = result[7]

        crimeweather_data.append({
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
        })

    return jsonify(crimeweather_data)

@app.route("/api/<city>") # City filter test path
def crimeweather_state(city):
    results = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).filter(CrimeWeather.city == city).limit(5).all()

    crimeweather_data = []
    for result in results:

        city = result[0]
        code = result[1]
        date = result[2]
        time = result[3]
        lat = result[4]
        lon = result[5]
        mapping = result[6]
        weather = result[7]
       
        crimeweather_data.append({
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
        })

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
    crimeweather_data = []

    # The following will jsonify all the data. DO NOT UNCOMMENT AND RUN IF YOU NAVIGATE TO THIS PATH
    # crimeweather_data = [{
    #     "location":{
    #         "city":city,
    #         "lat":lat,
    #         "lon":lon
    #     },
    #     "crime":{
    #         "mapping":mapping,
    #         "code":code
    #     },
    #     "time":{
    #         "date":date,
    #         "hour":time
    #     },
    #     "weather":weather
    # }]

    return jsonify(crimeweather_data)

if __name__ == "__main__":
    app.run(debug=True)
