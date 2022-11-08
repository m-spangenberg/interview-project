def test_new_applicant(applicant):
    """
    GIVEN the Applicant model
    WHEN a new applicant is created
    THEN check that fixture data is set
    see: https://en.wikipedia.org/wiki/Given-When-Then
    """
    assert applicant.email == "test@example.com"
    assert applicant.state == 0
    assert applicant.duration != 0


def test_new_superuser(superuser):
    """
    GIVEN the User model
    WHEN a new superuser is created
    THEN check that fixture data is set
    """
    assert superuser.email == "superuser@example.com"


def test_new_session(session_form):
    """
    GIVEN the FormSession model
    WHEN a new session is created
    THEN check that fixture data is set
    """
    assert session_form.answer == str(42)


def test_new_state(session_state):
    """
    GIVEN the FormState model
    WHEN a new state is created
    THEN check that fixture data is set
    """
    assert session_state.question == "the meaning of life?"
    assert session_state.choice == "42;1;0"
