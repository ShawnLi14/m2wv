from flask_sqlalchemy import SQLAlchemy
from flask_app import db

class Ratings(db.Model):

    __tablename__ = "ratingsNew"

    place = db.Column(db.String(20))
    placeid = db.Column(db.String(10), primary_key = True)
    schools = db.Column(db.Integer)
    safety = db.Column(db.Integer)
    outdoors = db.Column(db.Integer)
    cultural = db.Column(db.Integer)
    urban = db.Column(db.Integer)
    rural = db.Column(db.Integer)
    description = db.Column(db.String(10000))
    ascend = db.Column(db.Boolean, default=False)
    url = db.Column(db.String(100))


