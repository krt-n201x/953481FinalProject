from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(100))
    foodTitle = db.Column(db.String(100))
    foodPicture = db.Column(db.String(100))