def test_index_render(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for valid response.data indicating successful template render
    """
    response = app.get("/")
    assert b"Questionnaire" in response.data


def test_login_render(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for valid response.data indicating successful template render
    """
    response = app.get("/login")
    assert b"Admin Portal" in response.data


def test_404_render(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for valid response.data indicating successful template render
    """
    response = app.get("/notarealresource")
    assert response.status_code == 404
    assert b"PAGE NOT FOUND" in response.data


def test_admin_render(app):
    """
    GIVEN the flask application
    WHEN the route is requested via GET
    THEN check for valid response.data indicating successful template render
    """
    response = app.get("/admin", follow_redirects=True)

    assert b"Admin Portal" in response.data
