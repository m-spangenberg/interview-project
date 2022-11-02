from markupsafe import escape
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, DB_NAME, DB_LOCATION, create_database
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    flash,
    make_response,
    redirect,
    url_for,
    send_from_directory,
)

# FLASK CONFIGURATION
app = Flask(__name__)
app.secret_key = b"thisIsNotAProductionApp"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_LOCATION}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DATABASE INITIALIZATION
db.init_app(app)
create_database(app)

# APP ROUTES
