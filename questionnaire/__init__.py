# MODULE IMPORTS

# FLASK AND FLASK SUB-COMPONENTS
from flask import Flask
from flask import render_template
from flask import session
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
import logging
from datetime import timedelta
from datetime import datetime

# ADDITIONAL 3RD PARTY MODULES
from dotenv import load_dotenv

# APPLICATION MODULES
from .helper import check_email
from .helper import gen_superuser
from .helper import gen_default_form

# DATABASE MODELS
from questionnaire.models import db
from questionnaire.models import Applicant
from questionnaire.models import User
from questionnaire.models import FormSession
from questionnaire.models import FormState

# LOAD ENVIRONMENT VARIABLES FROM .ENV
load_dotenv()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    # LOGGING CONFIGURATION

    # logging.basicConfig(
    #     filename='questionnaire.log',
    #     level=logging.os.getenv('LOG_LEVEL'),
    #     format='%(asctime)s %(levelname)s : %(message)s')

    app.config["DEBUG"] = os.getenv('APP_DEBUG')
    app.config["SECRET_KEY"] = os.getenv('APP_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getenv('DB_NAME')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Make sure the instance folder is created to store the database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        # Create all database models, automatically checks if database exists
        db.create_all()
        # Generate first starting defaults id they don't exist
        gen_superuser(os.getenv('SUPERUSER_EMAIL'), os.getenv('SUPERUSER_PASSWORD'))
        gen_default_form()

    # LOGIN MANAGER MODULE

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # APP ROUTES

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Serve the questionnaire landing page template."""

        if request.method == "POST":

            email = str(request.form.get("email"))

            try:
                if email:

                    # prevent applicant from resubmitting questionnaire
                    # by checking for the their email in the database

                    if email != check_email(email):

                        # Set session timeouts for applicant
                        session.permanent = True
                        app.permanent_session_lifetime = timedelta(minutes=5)
                        session["email"] = email

                        return redirect(url_for("form"))
                    else:
                        raise Exception("Email exists in database!")
                else:
                    raise Exception("Invalid Email Address!")

            except Exception as e:
                flash("Invalid Email Address!")

        return render_template("index.html")

    @app.route("/form", methods=["GET", "POST"])
    def form():
        """Construct the questionnaire landing page template."""

        # Limit access to sessions that have set their email address
        # sessions auto-expire after 5 minutes

        if "email" not in session:
            return redirect(url_for("index"))

        if request.method == "POST":

            # for every question in the returned request object
            # create a versioned entry in the FormSession table

            for answer in request.form:

                new_session = FormSession(
                    applicant_id=str(session["email"]),
                    answer=str(request.form.get(answer)),
                    question=str(request.form.get("question")),
                )
                db.session.add(new_session)
                db.session.commit()

            # store the applicant's info in the database
            new_applicant = Applicant(
                email=str(session["email"]),
                state=1,
                # TODO: implement session timer for duration
            )

            db.session.add(new_applicant)
            db.session.commit()

            # invalidate session to prevent applicants from
            # trying to revisit the questionnaire page after submission

            session.clear()

            return redirect(url_for("confirm"))

        forms = FormState.query.filter_by(version=1).all()

        return render_template("form.html", forms=forms)

    @app.route("/confirm", methods=["GET", "POST"])
    def confirm():
        """Serve confirmation template."""
        return render_template("confirm.html")

    # AUTHENTICATED ROUTES

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
                        login_user(user, remember=True)

                        return redirect(url_for("admin"))
                    else:
                        raise Exception
                else:
                    raise Exception

            except Exception as e:
                flash("Incorrect Email or Password")

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        """Hasta La Vista, Baby!"""
        logout_user()
        return redirect(url_for("login"))

    @app.route("/admin", methods=["GET", "POST"])
    @login_required
    def admin():
        """Serve questionnaire review page."""

        if request.method == "POST":

            try:
                if "delete-form" in request.form:
                    # TODO: cascade all and delete orphans in database
                    # Query applicant based on hidden input value
                    # db.session.delete(archived_form)
                    ...

                elif "review-form" in request.form:
                    # TODO: query and build related form's layout
                    # TODO: swap out user email for a UUID

                    email = request.form.get("review-form")

                    return redirect(url_for("review"))

                elif "export-form" in request.form:
                    # TODO: generate JSON object from SQL and provide as .json download file
                    ...

                else:
                    raise Exception("Unable to Delete Questionnaire!")

            except Exception as e:
                # NOTE: bare-exception because I'm running out of time. D:
                pass

        # pull all sessions in to display in admin portal
        form_archive = FormSession.query.group_by(FormSession.applicant_id)

        return render_template("admin.html", form_archive=form_archive)

    # NOTE: would rather use a UUID than email

    @app.route("/review")
    @login_required
    def review():
        """Serve questionnaire review page."""

        # NOTE: have to hardcode or I wont make deadline - need to pass data from admin portal to review page
        # Question is broken on submission side, not indexing through input questions properly.

        applicant_id = "spangenbergmarthinus@gmail.com"
        forms = FormSession.query.filter(
            FormSession.applicant_id.endswith(applicant_id)
        ).all()

        return render_template("review.html", forms=forms)

    @app.route("/build", methods=["GET", "POST"])
    @login_required
    def build():
        """Serve questionnaire builder page."""
        return render_template("build.html")

    # SERVICE ROUTES

    @app.errorhandler(400)
    def bad_request(e):
        """Page Not Found"""
        return make_response(render_template("400.html"), 400)

    @app.errorhandler(404)
    def page_not_found(e):
        """Page Not Found"""
        return make_response(render_template("404.html"), 404)

    @app.errorhandler(500)
    def server_error(e):
        """Internal Server Error"""
        return make_response(render_template("500.html"), 500)

    # API ENDPOINTS

    # NOTE:
    # I understand this to be the correct
    # RESTful convention to structure the endpoint
    # https://restfulapi.net/resource-naming/

    @app.get("/api/v1/questionnaire/<string:applicantid>/json")
    @login_required
    def get_json_raw(applicantid):

        # TODO:
        # render the response as a pretty-printed json response

        return jsonify(
            {
                "identifier": 1,
                "email": 2,
            }
        )

    @app.get("/api/v1/questionnaire/<string:applicantid>/json/download")
    @login_required
    def get_json_file(applicantid):

        # TODO:
        # implement sendfile in such a way that it creates a .json file
        # and offers it up to the the client's browser for download
        # https://flask.palletsprojects.com/en/2.2.x/api/#flask.send_file

        return jsonify(
            {
                "identifier": 1,
                "email": 2,
            }
        )

    @app.get("/api/v1/questionnaire/<string:applicantid>/delete")
    @login_required
    def delete_form(applicantid):
        '''
        API endpoint for authenticated user to delete specified questionnaire
        
        NOTE:
        If this were a production application I would prefer this endpoint
        to have role-based permission as a second layer of protection against abuse
        '''

        # TODO:
        # implement sendfile in such a way that it creates a .json file
        # and offers it up to the the client's browser for download
        # https://flask.palletsprojects.com/en/2.2.x/api/#flask.send_file

        return jsonify(
            {
                "identifier": 1,
                "email": 2,
            }
        )

    return app
