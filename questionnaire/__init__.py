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
import os
from datetime import datetime

# RELATIVE PACKAGE
from questionnaire.models import db
from questionnaire.models import DB_NAME
from questionnaire.models import Applicant
from questionnaire.models import User


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(
        __name__,
        instance_relative_config=True,
    )
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = b"thisIsNotAProductionApp"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Check that the apps instance folder is created
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # LOGIN MANAGER MODULE
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # APP ROUTES
    @app.route("/")
    def index():
        """Serve the questionnaire landing page template."""
        return render_template("index.html")

    # APPLICANT PORTAL ROUTES
    @app.route("/form")
    #NOTE: only allow users who have entered their email address to access this page
    def form():
        """Serve the questionnaire landing page template."""
        return render_template("form.html")

    @app.route("/confirm", methods=['GET', 'POST'])
    def confirm():
        '''Serve account template.'''
        return render_template("confirm.html")

    # ADMIN PORTAL ROUTES
    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Serve admin portal's login page template."""
        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            try:
                if user:
                    if check_password_hash(user.password, password):
                        login_user(user, remember=remember)
                        # Set user as online
                        current_user.state = True
                        db.session.commit()
                        return redirect(url_for("review"))
                    else:
                        raise Exception
                else:
                    raise Exception

            except Exception as e:
                flash("Incorrect email or password")

        else:
            return render_template("login.html")
    
    @app.route("/logout")
    @login_required
    def logout():
        '''Hasta La Vista, Baby!'''
        logout_user()
        return redirect(url_for('login'))

    @app.route("/admin", methods=['GET', 'POST'])
    @login_required
    def admin():
        '''Serve questionnaire review page.'''
        return render_template("admin.html")

    @app.route("/review", methods=['GET', 'POST'])
    @login_required
    def review():
        '''Serve questionnaire review page.'''
        return render_template("review.html")

    @app.route("/build", methods=['GET', 'POST'])
    @login_required
    def build():
        '''Serve questionnaire builder page.'''
        return render_template("build.html")

    # SERVICE ROUTES
    @app.errorhandler(404)
    def page_not_found(e):
        """Page Not Found"""
        return make_response(render_template("404.html"), 404)

    @app.errorhandler(500)
    def server_error(e):
        """Internal Server Error"""
        return make_response(render_template("500.html"), 500)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
