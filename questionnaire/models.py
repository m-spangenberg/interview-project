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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)

class ApplicantStats(db.Model):
    """
    session statistics for applicant
    """
    id = db.Column(db.Integer, primary_key=True)
    # applicant_id = 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")

class User(db.Model, UserMixin):
    """
    users table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FormData(db.Model):
    """
    answers to applicant's questionnaire session
    """
    id = db.Column(db.Integer, primary_key=True)


class FormSession(db.Model):
    """
    version of questionnaire accessed by applicant
    """
    id = db.Column(db.Integer, primary_key=True)


class FormState(db.Model):
    """
    structure of the questionnaire
    """
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(64), default='Question #')
    prompt = db.Column(db.String(256))
    #field = db.Column(ChoiceType(FIELDS))

class FormQuestion(db.Model):
    """
    questions available to form
    """
    id = db.Column(db.Integer, primary_key=True)


class FormChoice(db.Model):
    """
    choices available to form questions
    """
    id = db.Column(db.Integer, primary_key=True)
