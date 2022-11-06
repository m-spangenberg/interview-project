from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Database Models
class Applicant(db.Model):
    """
    applicants table
    related to FormSession table (1..1)
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")
    session = db.relationship('FormSession', backref="applicant", lazy=True)


class User(db.Model, UserMixin):
    """
    superusers table
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))


class FormSession(db.Model):
    """
    state of the the applicant's session
    maximum answer VARCHAR set to 1024
    related to Applicant table (1..1)
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String, db.ForeignKey("applicant.id"))
    answer = db.Column(db.String(1024))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # NOTE: last minute band-aid
    question = db.Column(db.String(256))


class FormState(db.Model):
    """
    state of the questionnaire
    """
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    question = db.Column(db.String(256))
    input_type = db.Column(db.String(32))
    choice = db.Column(db.String(64))
