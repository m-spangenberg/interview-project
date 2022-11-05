from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "CX_MARTHINUS_BA_DB"

db = SQLAlchemy()

# Database Models
class Applicant(db.Model):
    """
    applicants table
    """
    email = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")

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
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String, db.ForeignKey('applicant.email'))
    answer = db.Column(db.String(1024))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state_id = db.Column(db.Integer, db.ForeignKey('form_state.version'))
    state = db.relationship('FormState', backref='parents')

class FormState(db.Model):
    """
    state of the questionnaire
    many-to-one relationship with FormSession referencing FormState version
    """
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    question = db.Column(db.String(256))
    input_type = db.Column(db.String(32))
    choice = db.Column(db.String(64))