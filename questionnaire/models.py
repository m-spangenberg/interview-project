from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "CX_MARTHINUS_BA_DB"

db = SQLAlchemy()

# Database Models
class Applicant(db.Model):
    """
    applicants table

    NOTE:
    applicants have a cascading one-to-one relationship with their stats
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    stats = db.relationship('ApplicantStats', back_populates='applicant', uselist=False)

class ApplicantStats(db.Model):
    """
    session statistics for applicants

    NOTE:
    stats only track whether the user completed the form, when it was completed,
    and how long it took to complete. Retries are not logged.
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

    NOTE:
    added this table for the sake of having a functional login but did not implement
    a role-based permission system.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FormData(db.Model):
    """
    answers provided by the applicant during the questionnaire session
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    answer = db.Column(db.Integer)
    session_id = db.Column(db.Integer, db.ForeignKey('form_session.id'))


class FormSession(db.Model):
    """
    an inner-join table that displays the state of the questionnaire accessed
    by the applicant joined with the data they provided during their session

    NOTE:
    the session serves as a join table linking applicant answers and the
    specific form structure (questions) they engaged with.
    """
    id = db.Column(db.Integer, primary_key=True)
    #applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    #history_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

class FormHistory(db.Model):
    """
    history of all revisions to the questionnaire
    """
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('form_session.id'))
    state = db.relationship('FormState')

class FormState(db.Model):
    """
    active state of the questionnaire presented to the applicant
    """
    id = db.Column(db.Integer, primary_key=True)
    timer = db.Column(db.Integer, default="300")
    history_id = db.Column(db.Integer, db.ForeignKey('form_history.id'))
    question = db.relationship('FormQuestion')

class FormQuestion(db.Model):
    """
    questions available to form
    """
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('form_state.id'))
    question = db.Column(db.String(256))
    choice = db.relationship('FormInputs')

class FormInputs(db.Model):
    """
    input types available to form questions

    NOTE:
    I decided to make input the generic text field choice because of UI/UX considerations.
    """
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('form_question.id'))

    # TODO: perform choice validation to protect integrity
    input_type = db.Column(db.String(16))