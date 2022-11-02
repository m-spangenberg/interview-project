from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "CX_YOUR_FIRSTNAME_BA_DB.db"
DB_LOCATION = "data/database/"

db = SQLAlchemy()

# Database Models
class Applicant(db.Model):
    """applicant table"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)

class User(db.Model):
    """user table"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)

# class Form(db.Model):

# class Session(db.Model):
