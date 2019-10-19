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

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/crime.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

chart = "Year"
crime = "All"
weather = "All"

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

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

@app.route("/samples/<sample>")
def samples(sample):
    """Return summarized data by selected sample."""
    data = {}
    words = sample.split("1")
    cities = ["base", "atlanta", "boston", "chicago", "denver", "los_angeles"]
    for i in range(len(cities)):
        if (cities[i] == "base") :
            stmt1 = "SELECT " + words[0] +", SUM(Count) FROM crime"
            stmt5 = " GROUP BY " + words[0]
            stmt6 = " ORDER BY " + words[0]
            stmt = stmt1 + stmt5 + stmt6
            print(stmt)
            df = pd.read_sql_query(stmt, db.session.bind)
            df["ratio"] = df.iloc[:,1] * 0
            data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,2].tolist()}})

        else:
            stmt1 = "SELECT " + words[0] +", SUM(Count) FROM crime"
            stmt2 = " WHERE City = " + "'" + cities[i] + "'"
            
            if (words[1] == "All"):
                stmt3 = ""
            else:
                stmt3 = " AND MapCrime = '" + words[1] + "'"
            
            if (words[2] == "All"):
                stmt4 = ""
            else:
                stmt4 = " AND MapWeather = '" + words[2] + "'"
            
            stmt5 = " GROUP BY " + words[0]
            stmt6 = " ORDER BY " + words[0]
            stmt = stmt1 + stmt2 + stmt3 + stmt4 + stmt5 + stmt6
            print(stmt)
            df = pd.read_sql_query(stmt, db.session.bind)
            df["ratio"] = df.iloc[:,1] / df["SUM(Count)"].sum()
            data.update({cities[i] : {"xAxis": df.iloc[:,0].tolist(), "yAxis": df.iloc[:,2].tolist()}})

    return jsonify(data)

if __name__ == "__main__":
    app.run()
