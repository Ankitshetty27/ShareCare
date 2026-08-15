from . import db

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer)
    ngo_name = db.Column(db.String(100))
    status = db.Column(db.String(20))
