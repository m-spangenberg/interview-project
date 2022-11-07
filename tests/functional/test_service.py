def test_404_route(test_client):
    """
    GIVEN the flask application
    WHEN the 404 route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = test_client.get('/404')
    assert response.status_code == 200

def test_500_route(test_client):
    """
    GIVEN the flask application
    WHEN the 500 route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = test_client.get('/500')
    assert response.status_code == 200