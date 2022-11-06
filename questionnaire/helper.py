from flask import current_app

from questionnaire.models import db
from questionnaire.models import Applicant
from questionnaire.models import FormState
from questionnaire.models import User

from werkzeug.security import generate_password_hash


def check_email(email: str) -> str:
    """return a matching email address from the Applicant table"""
    try:
        email_check = Applicant.query.filter_by(email=email).first()
        if email_check.email is not None:
            email_exists = str(email_check.email)
    except AttributeError:
        current_app.logger.info('login attempt by processed applicant: %s', email)
        email_exists = None

    return email_exists


def gen_superuser(email: str, password: str) -> None:
    '''
    check if db is empty
    check if user does not exists
    generate superuser in database

    NOTE:
    because of how Flask handles the application context this will fire
    off an exception if automatic template reloading is on in flasks config.
    '''
    try:
        with current_app.app_context():
            if User.query.first() is None:
                if not User.query.filter_by(email=email).first():

                    password = generate_password_hash(password)
                    superuser = User(email=email, password=password)
                    db.session.add(superuser)
                    db.session.commit()
                else:
                    raise Exception('superuser already exists')
            else:
                raise Exception('database is not empty')

    except Exception as e:
        current_app.logger.error('%s -- failed to generate superuser', e)

def gen_default_form() -> None:
    '''
    generate default questions form
    
    NOTE:
    because of how Flask handles the application context this will fire
    off an exception if automatic template reloading is on in flasks config.
    '''
    try:
        with current_app.app_context():

            if FormState.query.first() is None:

                db.session.add(
                    FormState(
                        version=1,
                        question="Where did you hear from us, and what do you think will make\
                                you a great asset to the BCX Business Application Department?",
                        input_type="input",
                        choice=None,
                    )
                )
                db.session.add(
                    FormState(
                        version=1,
                        question="How many software solutions did you write in your life?",
                        input_type="select",
                        choice="1 to 5;6 -25;26 -100;101 +",
                    )
                )
                db.session.add(
                    FormState(
                        version=1,
                        question="Was it fun building a website for an interview?",
                        input_type="radio",
                        choice="yes;no",
                    )
                )

                db.session.commit()
            else:
                raise Exception('form is already pre-populated')

    except Exception as e:
        current_app.logger.error('%s -- failed to populate default form', e)
