from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Database Models
class Applicant(db.Model):
    """
    applicants table
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")
    session = db.relationship(
        "FormSession", backref="applicant", lazy=True, cascade="all, delete"
    )


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
    """

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey("applicant.id"))
    answer = db.Column(db.String(1024))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state_id = db.Column(db.Integer, db.ForeignKey("form_state.id"))


class FormState(db.Model):
    """
    state of the questionnaire
    """

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    question = db.Column(db.String(256))
    input_type = db.Column(db.String(32))
    choice = db.Column(db.String(64))
    session = db.relationship("FormSession", backref="session", lazy=True)
