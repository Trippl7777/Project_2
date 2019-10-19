# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import sqlite3

# Flask Setup
app = Flask(__name__)

# Database Setup
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

# ========== OLD FLASK TEMPLATE CODE

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


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

# ========== NEW API CODE ==========
@app.route("/api")
def crimeweather():
    result = db.session.query(CrimeWeather.city,CrimeWeather.code,CrimeWeather.startdate,CrimeWeather.starttime,
    CrimeWeather.latitude,CrimeWeather.longitude,CrimeWeather.mapping,CrimeWeather.weather).first()#.all()

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

@app.route("/api/<city>")
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
    app.run(debug=True)
