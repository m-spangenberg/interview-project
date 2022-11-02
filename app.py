# MODULE IMPORTS

# FLASK AND FLASK SUB-COMPONENTS
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import flash
from flask import make_response
from flask import redirect
from flask import url_for
from flask import send_from_directory
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest
from markupsafe import escape

# USER AUTHENTICATION MODULE
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

# DATABASE MODULE
from flask_sqlalchemy import SQLAlchemy

# STANDARD LIBRARY
from datetime import datetime

# APPLICATION
from models import db
from models import DB_NAME
from models import DB_LOCATION
from models import Applicant
from models import User


# FLASK AND DATABASE INITIALIZATION
app = Flask(__name__)
app.secret_key = b"thisIsNotAProductionApp"
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_LOCATION}/{DB_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

# with app.app_context():
#     db.create_all()

# LOGIN MANAGER MODULE
# login_manager = LoginManager()
# login_manager.login_view = 'login'
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


# APP ROUTES
@app.route("/")
@app.route("/index")
def index():
    '''Serve landing page template.'''
    return render_template("index.html", user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    '''Page Not Found'''
    return make_response(render_template("404.html"), 404)


@app.errorhandler(500)
def server_error(e):
    '''Internal Server Error'''
    return make_response(render_template("500.html"), 500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)