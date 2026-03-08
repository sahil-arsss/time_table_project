from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100))

    role = db.Column(db.String(50))

    subject = db.Column(db.String(50))


class Timetable(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    room = db.Column(db.String(50))

    day = db.Column(db.String(50))

    period = db.Column(db.String(10))

    department = db.Column(db.String(50))   # CS, Civil, ECE

    subject = db.Column(db.String(100))     # OS, CN, DSA

    professor = db.Column(db.String(100))