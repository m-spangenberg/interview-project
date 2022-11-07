def test_new_applicant(applicant):
    '''
    GIVEN the Applicant model
    WHEN a new applicant is created
    THEN check that the email, state and duration is set
    see: https://en.wikipedia.org/wiki/Given-When-Then
    '''
    assert applicant.email == 'test@example.com'
    assert applicant.state == 0
    assert applicant.duration != 0