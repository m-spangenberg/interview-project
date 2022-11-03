from sqlalchemy_utils import ChoiceType
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "CX_MARTHINUS_BA_DB"

db = SQLAlchemy()

# Database Models
class Applicant(db.Model):
    """applicant table"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)

class User(db.Model, UserMixin):
    """superuser table for user authentication"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FormData(db.Model):
    """from representation table used for view generation"""
    id = db.Column(db.Integer, primary_key=True)
    #user response

class Questions(db.Model):
    """question structure table used by form builder"""
    FIELDS = [
        ('input', 'input'),
        ('textarea', 'textarea'),
        ('select', 'select'),
        ('radio', 'radio'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(64), default='Question #')
    prompt = db.Column(db.String(256))
    field = db.Column(ChoiceType(FIELDS))

class Session(db.Model):
    """per applicant session statistics"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    state = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default="0")