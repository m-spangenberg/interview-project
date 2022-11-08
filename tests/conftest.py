import os
import pytest
from questionnaire import create_app
from questionnaire.models import Applicant
from questionnaire.models import User
from questionnaire.models import FormSession
from questionnaire.models import FormState
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="module")
def app():
    """fixture to create a flask app instance for testing"""
    app = create_app()
    app.config.update({"TESTING": os.getenv("APP_TESTING")})
    app.config["LOGIN_DISABLED"] = True

    with app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope="module")
def applicant():
    """fixture to create a test applicant"""
    new_applicant = Applicant(email="test@example.com", state=0, duration=42)
    return new_applicant


@pytest.fixture(scope="module")
def superuser():
    """fixture to create a test superuser"""
    user = User(email="superuser@example.com", password="hashedpasswordplaceholder")
    return user


@pytest.fixture(scope="module")
def session_form():
    """fixture to create a test session"""
    sesh = FormSession(applicant_id=1, answer="42")
    return sesh


@pytest.fixture(scope="module")
def session_state():
    """fixture to create a test state"""
    sesh_state = FormState(
        version=1, question="the meaning of life?", input_type="select", choice="42;1;0"
    )
    return sesh_state
