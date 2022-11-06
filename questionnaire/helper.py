from flask import current_app

from questionnaire.models import db
from questionnaire.models import FormSession
from questionnaire.models import Applicant
from questionnaire.models import FormState
from questionnaire.models import User

from werkzeug.security import generate_password_hash

from random import choice
from random import randrange


def del_applicant(applicantid: str) -> None:
    '''delete the applicant and all their associated data from the database'''
    try:
        if applicantid:
            with current_app.app_context():

                applicant = Applicant.query.filter_by(email=applicantid).first()
                db.session.delete(applicant)
                db.session.commit()

        raise Exception('no valid applicant id supplied')

    except Exception as e:
        current_app.logger.error('%s -- failed to delete applicant data', e)


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


def gen_applicants(count: int) -> None:
    '''
    generate dummy applicants
    '''

    domains = ['bigmail', 'yeehaw', 'icebox', 'ycloud', 'neutron', 'inlook', 'lmao', 'windex']
    tlds = ['com', 'org', 'io', 'net', 'mail', 'spam']
    f_names = ['test', 'spam', 'leetcoder', 'dbdude', 'htmlmao', 'howto']
    l_names = ['magic', 'box', 'hunter', 'cool', 'super', 'bingbong']

    try:
        with current_app.app_context():

            if Applicant.query.first() is None:

                for _ in range(count):
                    email = f'{choice(f_names)}{choice(l_names)}@{choice(domains)}.{choice(tlds)}'
                    state = 1
                    duration = randrange(5, 120, 1)

                    db.session.add(
                        Applicant(
                            email=email,
                            state=state,
                            duration=duration,
                        )
                    )

                db.session.commit()

            else:
                raise Exception('applicant pool is already pre-populated')

    except Exception as e:
        current_app.logger.error('%s -- failed to populate default applicant pool', e)


def gen_sessions() -> None:
    '''
    generate dummy sessions for available applicants
    '''
    try:
        with current_app.app_context():

            if FormSession.query.first() is None:

                applicants = Applicant.query.all()

                for applicant in applicants:

                    db.session.add(
                        FormSession(
                            applicant_id=applicant.id,
                            answer="This is just some dummy text so there's something to look at.",
                            question="This is just here so the form is populated"
                        )
                    )

                db.session.commit()

            else:
                raise Exception('session is already pre-populated')

    except Exception as e:
        current_app.logger.error('%s -- failed to populate default session data', e)
