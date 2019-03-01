from application import db
from sqlalchemy import event

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default = db.func.current_timestamp(),onupdate = db.func.current_timestamp())
