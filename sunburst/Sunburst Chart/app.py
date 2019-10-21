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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/db.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

class CrimeWeather(db.Model):
    __tablename__ = 'combine'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30))
    mapping = db.Column(db.String(50))
    weather = db.Column(db.String(50))

    def __repr__(self):
        return '<CrimeWeather %r>' % (self.name)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/sunburst")
def crimeweather():

    #Just take the needed columns for the sqlite file, reduces process time.
    results = db.session.query(CrimeWeather.city, CrimeWeather.mapping, CrimeWeather.weather).all()

    #May not be in jupyter notebook/lab, but dataframes are still very useful.
    data = pd.DataFrame({})
    data['City'] = [result[0] for result in results]
    data['Mapping'] = [result[1] for result in results]
    data['Weather'] = [result[2] for result in results]

    city_ls = data['City'].unique()
    # weat = data['Weather'].unique()
    parents = []
    labels = []
    ids = []
    values = []

    #Create sunburst chart's necessary labels, ids, parents, values. Make small changes in accordance with professionalism; eg formatting.
    for x in city_ls:
        xc = x.capitalize().replace('Los_angeles','Los Angeles')
        parents.append('')
        labels.append(xc)
        ids.append(f'Weather-{xc}')
        loop_df = data.loc[data['City'] == x]
        values.append((loop_df['City'].value_counts())[x])


    for x in city_ls:
        xc = x.capitalize().replace('Los_angeles','Los Angeles')
        loop_df = data.loc[data['City'] == x]
        mapping_ls = loop_df['Mapping'].unique()
        weather_ls = pd.Series(loop_df['Weather'].unique()).dropna().tolist()

        for y in weather_ls:
            parents.append(f'Weather-{xc}')
            xx = loop_df['Weather'].value_counts()
            values.append(xx[y])
            ids.append(f'{xc}-{y}')
            labels.append(y)

        for y in weather_ls:
            yy = loop_df.loc[loop_df['Weather'] == y]
            
            for z in mapping_ls:
                parents.append(f'{xc}-{y}')
                ids.append(f'{y}-{z}')
                try:
                    zz = yy['Mapping'].value_counts()
                    values.append(zz[z])
                    labels.append(z)
                except:
                    values.append(0)
                    labels.append('')

    #jsonsify errors out with values as numpy int64, convert to str, then reconvert to number in js
    values = [str(x) for x in values]
    # weat = [str(x) for x in weat]

    #Enter lists into dictionaty format for jsonify
    sunburst_data = {
        "ids": ids,
        "labels": labels,
        "parents": parents,
        "values": values}
        # ,'weather': weat}

    return jsonify(sunburst_data)

if __name__ == "__main__":
    app.run()
