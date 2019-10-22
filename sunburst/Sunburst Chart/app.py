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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/sunburst.sqlite"
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

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run()
