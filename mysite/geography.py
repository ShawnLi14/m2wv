from flask_sqlalchemy import SQLAlchemy
from flask_app import db

class Geography(db.Model):

    __tablename__ = "geography"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(15))
    state_code = db.Column(db.String(2))
    place = db.Column(db.String(10))
    state_id = db.Column(db.String(10))
    place_id = db.Column(db.String(10))