def test_index_route(test_client):
    """
    GIVEN the flask application
    WHEN the index route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = test_client.get('/')
    assert response.status_code == 200

def test_index_render(test_client):
    """
    GIVEN the flask application
    WHEN the index route is requested via GET
    THEN check for valid response.data indicating successful template render
    """
    response = test_client.get('/')
    assert b'Questionnaire' in response.data