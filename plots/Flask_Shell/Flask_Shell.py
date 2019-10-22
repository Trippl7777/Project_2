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

app = Flask(__name__)

#################################################
# Database Setup
#################################################

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/crime.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

class Sunburst(db.Model):
    __tablename__ = 'sunburst'

    id = db.Column(db.Integer, primary_key=True)
    Ids = db.Column(db.String(50))
    Labels = db.Column(db.String(50))
    Parents = db.Column(db.String(50))
    Values = db.Column(db.String(50))

    def __repr__(self):
        return '<Sunburst %r>' % (self.name)


chart = "Year"
crime = "All"
weather = "All"

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/plot1<br/>"
        f"/plot2<br/>"
        f"/plot3"
    )

@app.route("/plot1")
def plot1():
    """Return the homepage."""
    return render_template("plot1.html")

@app.route("/plot2")
def plot2():
    """Return the homepage."""
    return render_template("plot2.html")

@app.route("/plot3")
def plot3():
    """Return the homepage."""
    return render_template("plot3.html")

@app.route("/sunburst")
def Sunny():

    results = db.session.query(Sunburst.Ids, Sunburst.Labels, Sunburst.Parents, Sunburst.Values).all()

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

if __name__ == "__main__":
    app.run()