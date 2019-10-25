from .app import db


class CrimeWeather(db.Model):
    __tablename__ = 'crimeweather'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    code = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    time = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    crime_desc = db.Column(db.String())
    mapping = db.Column(db.String(64))
    weather = db.Column(db.String(30))

    def __repr__(self):
        return '<CrimeWeather %r>' % (self.name)
