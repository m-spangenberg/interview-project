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
    email = db.Column(db.String(64), unique=True, nullable=False)
    stats = db.relationship('ApplicantStats', back_populates='applicant', uselist=False)

class ApplicantStats(db.Model):
    """
    session statistics for applicants
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")
    applicant = db.relationship('Applicant', back_populates='stats')

class User(db.Model, UserMixin):
    """
    users table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FormTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256))
    input = db.Column(db.String(16))

# class FormData(db.Model):
#     """
#     answers provided by the applicant during the questionnaire session
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
#     answer = db.Column(db.Integer)
#     session_id = db.Column(db.Integer, db.ForeignKey('form_session.id'))

# class FormSession(db.Model):
#     """
#     state of the the applicant's session
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
#     data_id = db.Column(db.Integer, db.ForeignKey('form_data.id'))
#     state_version = db.Column(db.Integer, db.ForeignKey('form_state.version'))

# class FormState(db.Model):
#     """
#     state of the questionnaire
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     version = db.Column(db.Integer)
#     question_id = db.Column(db.Integer, db.ForeignKey('form_question.id'))

# class FormQuestion(db.Model):
#     """
#     questions available to form
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String(256))
#     input_id = db.Column(db.Integer, db.ForeignKey('form_input.id'))
    

# class FormInput(db.Model):
#     """
#     input types available to form questions
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     input_type = db.Column(db.String(16))