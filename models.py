from app import db
from datetime import datetime


# Database Models
class BloaterSuit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)


class KarateGi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)


class BloaterHead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)
