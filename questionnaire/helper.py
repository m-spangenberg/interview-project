from questionnaire.models import db
from questionnaire.models import Applicant


def check_email(email: str) -> str:
    """return a matching email address from the Applicant table"""
    try:
        email_check = Applicant.query.filter_by(email=email).first()
        if email_check.email is not None:
            email_exists = str(email_check.email)
    except AttributeError:
        email_exists = None

    return email_exists
