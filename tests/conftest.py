# TEST FRAMEWORK
import pytest

# PACKAGE CONTEXT
from questionnaire import create_app

# PACKAGE MODELS
from questionnaire.models import Applicant
from questionnaire.models import User
from questionnaire.models import FormSession
from questionnaire.models import FormState

@pytest.fixture(scope='module')
def applicant():
    """fixture to create a test applicant"""
    new_applicant = Applicant(email='test@example.com', state=0, duration=42)
    return new_applicant

@pytest.fixture(scope='module')
def test_client():
    """fixture to create a flask app instance for testing"""
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        yield testing_client