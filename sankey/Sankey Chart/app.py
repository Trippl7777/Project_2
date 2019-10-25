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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/sankey.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

class Sankey(db.Model):
    __tablename__ = 'sankey'

    id = db.Column(db.Integer, primary_key=True)
    City = db.Column(db.String(20))
    Start = db.Column(db.String(50))
    End = db.Column(db.String(50))
    Values = db.Column(db.String(50))

    def __repr__(self):
        return '<Sankey %r>' % (self.name)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/sankey")
def Sandy():

    results = db.session.query(Sankey.City, Sankey.Start, Sankey.End, Sankey.Values).all()

    #Get values from sqlite file
    df = pd.DataFrame({})
    df['city'] = [result[0] for result in results]
    df['start'] = [result[1] for result in results]
    df['end'] = [result[2] for result in results]
    df['values'] = [result[3] for result in results]

    #Make column names to list, remove first column name 'city' as it's purpose was to act as the key value for dictionary.
    city_dt = df['city'].unique().tolist()
    col = df.columns.to_list()
    col.remove('city')

    city_dt = city_dt
    dt = {}

    #De-panda's the the dataframe into a dictionary for jsonifable structure.
    for x in city_dt:

        out = {}
        xx = df.loc[df['city'] == x]
        yy = xx[['start','end','values']]
        for y in col:
            out[y] = yy[y].to_list()
        dt[x] = out

    # print(dt)
    return jsonify(dt)

# USED FOR DROPDOWN
# Make route with city's names/ slection options
@app.route("/sancity")
def citychange():
    """Return a list of selector names."""

    cities = ['All', 'Atlanta', 'Boston', 'Chicago', 'Denver', 'Los Angeles']

    return jsonify(cities)


if __name__ == "__main__":
    app.run()
