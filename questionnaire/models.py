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
    session statistics for applicants
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
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
    answers to questionnaire sessions
    """
    id = db.Column(db.Integer, primary_key=True)


class FormSession(db.Model):
    """
    version of questionnaire accessed by applicant
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    history_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

class FormHistory(db.Model):
    """
    history of all questionnaires
    """
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    #state = db.relationship('FormState')

class FormState(db.Model):
    """
    structure of the questionnaire
    """
    id = db.Column(db.Integer, primary_key=True)
    #history_id = db.Column(db.Integer, db.ForeignKey('formhistory.id'))
    #question = db.relationship('FormQuestion')

class FormQuestion(db.Model):
    """
    questions available to form
    """
    id = db.Column(db.Integer, primary_key=True)
    #state_id = db.Column(db.Integer, db.ForeignKey('formstate.id'))
    question = db.Column(db.String(256))
    #choice = db.relationship('FormChoice')

class FormChoice(db.Model):
    """
    choices available to form questions
    """
    id = db.Column(db.Integer, primary_key=True)
    #question_id = db.Column(db.Integer, db.ForeignKey('formquestion.id'))

    # TODO: perform choice validation to protect integrity
    choice_type = db.Column(db.String(16))