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
    app.run()
