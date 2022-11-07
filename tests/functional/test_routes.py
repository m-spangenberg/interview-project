def test_index_route(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = app.get('/')
    assert response.status_code == 200

def test_login_route(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = app.get('/login')
    assert response.status_code == 200

def test_confirm_route(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for a valid 200 OK response
    """
    response = app.get('/confirm')
    assert response.status_code == 200

# TODO:
# Set up superuser in conftest.py for testing authenticated views

# def test_review_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/review')
#     assert response.status_code == 200

# def test_form_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/form')
#     assert response.status_code == 200

# def test_build_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/build')
#     assert response.status_code == 200

# def test_admin_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/admin')
#     assert response.status_code == 200

# def test_404_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/404')
#     assert response.status_code == 200

# def test_500_route(test_client):
#     """
#     GIVEN the flask application
#     WHEN the route is requested via GET
#     THEN check for a valid 200 OK response
#     """
#     response = test_client.get('/500')
#     assert response.status_code == 200