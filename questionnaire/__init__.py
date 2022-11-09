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
from werkzeug.security import check_password_hash

# USER AUTHENTICATION MODULE
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user

# STANDARD LIBRARY
import os
import logging
from datetime import timedelta

# ADDITIONAL 3RD PARTY MODULES
from dotenv import load_dotenv

# APPLICATION MODULES
from .helper import check_email
from .helper import del_applicant
from .helper import gen_applicants
from .helper import gen_superuser
from .helper import gen_default_form
from .helper import gen_sessions
from .helper import chucky

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
    if not os.getenv("APP_DEBUG"):
        logging.basicConfig(
            filename="questionnaire.log",
            level=logging.os.getenv("LOG_LEVEL"),
            format="%(asctime)s %(levelname)s : %(message)s",
        )

    app.config["DEBUG"] = os.getenv("APP_DEBUG")
    app.config["SECRET_KEY"] = os.getenv("APP_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getenv('DB_NAME')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("TRACK_MODS")
    app.config["TEMPLATES_AUTO_RELOAD"] = os.getenv("APP_TEMPLATE_RELOAD")

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
        gen_superuser(os.getenv("SUPERUSER_EMAIL"), os.getenv("SUPERUSER_PASSWORD"))
        gen_default_form()
        gen_applicants(10)
        gen_sessions()

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

            except Exception:
                # a bare exception, yes
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

            applicant = Applicant.query.filter_by(email=session["email"]).first()

            for count, answer in enumerate(request.form):

                session_answer = FormSession(
                    applicant_id=int(applicant.id),
                    answer=str(request.form.get(answer)),
                    state_id=int(count + 1),
                )

                db.session.add(session_answer)
                db.session.commit()

            # change the state of the applicant's questionnaire to true

            applicant.state = 1
            db.session.commit()

            # invalidate session to prevent applicants from
            # trying to revisit the questionnaire page after submission

            session.clear()

            return redirect(url_for("confirm"))

        # TODO: modify query to return the newest version of the form
        forms = FormState.query.filter_by(version=1).all()

        # store the applicant's info in the database on load
        # set state to false so we know the questionnaire isn't completed

        new_applicant = Applicant(
            email=str(session["email"]),
            state=0,
            duration=50,
        )

        db.session.add(new_applicant)
        db.session.commit()

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

            except Exception:
                # a bare exception, yes
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
        form_archive = FormSession.query.group_by(FormSession.applicant_id)
        return render_template("admin.html", form_archive=form_archive)

    @app.route("/build", methods=["GET", "POST"])
    @login_required
    def build():
        """Serve questionnaire builder page."""

        # pass most current version of the questionnaire on page load
        val = FormState.query.order_by(FormState.version.desc()).first()
        form_state = FormState.query.filter_by(version=val.version).all()
        new_version = int(val.version) + 1

        return render_template("build.html", new_version=new_version, form_state=form_state)

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

    @app.get("/api/v1/questionnaire/<string:applicantid>/review")
    @login_required
    def review(applicantid):
        """Serve questionnaire review page."""
        applicant = Applicant.query.filter_by(id=applicantid).first()
        questions = FormSession.query.filter_by(applicant_id=applicantid).all()

        return render_template("review.html", questions=questions, applicant=applicant)

    @app.get("/api/v1/questionnaire/<string:applicantid>/json")
    @login_required
    def get_json(applicantid):
        """Return the applicant's session as a json dump"""

        return jsonify(chucky(applicantid))

    @app.get("/api/v1/questionnaire/<string:applicantid>/delete")
    @login_required
    def delete_applicant(applicantid):
        """delete the applicants data"""
        del_applicant(applicantid)

        return redirect(url_for("admin"))

    return app
