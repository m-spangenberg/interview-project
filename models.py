from os import path
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "forms.db"
DB_LOCATION = "data/db/"

db = SQLAlchemy()


def create_database(app):
    """Perform a check to see if the database exists"""
    if not path.exists(DB_LOCATION + DB_NAME):
        db.create_all(app=app)
