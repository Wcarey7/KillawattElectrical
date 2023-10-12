import pytest
from flask_login import current_user
from flask import g, session
from app import db
from app.models.user import User


def test_default_user_exists(app):
    with app.app_context():
        select = db.select(User).filter_by(username="test")
        user = db.session.execute(select).scalar()
        assert user is not None
        assert user.email == "test@example.com"


def test_register(client, app):
    # Test that viewing the page renders without template errors
    assert client.get("/auth/register").status_code == 200

    # Test that successful registration redirects to the login page
    response = client.post("/auth/register", data={
        "username": "wade",
        "email": "wade@example.com",
        "password": "foo",
        "password2": "foo",
    }, follow_redirects=True)
    assert response.request.path == "/auth/login"

    # Test that the user was inserted into the database
    with app.app_context():
        select = db.select(User).filter_by(username="wade")
        user = db.session.execute(select).scalar()
        assert user is not None


@pytest.mark.parametrize(
    ("username", "email", "password", "password2", "message"),
    (
        ("", "testemail@mail.com", "password", "password", "Please provide a valid username."),
        ("a", "testemail@mail.com", "", "", "Please provide a valid password."),
        ("test", "testemail@mail.com", "password", "password", "Username already in use. Please choose a different username."),
        ("test1", "test@example.com", "password", "password", "Email already registered. Please use a different email."),
        ("test2", "test2email@mail.com", "test", "dog", "Passwords do not match"),
    ),
)
def test_register_validate_input(client, username, email, password, password2, message):
    response = client.post(
        "/auth/register", data={"username": username, "email": email, "password": password, "password2": password2}
    )
    assert message in response.text


@pytest.mark.parametrize(
    "route",
    ("/customer/", "/customer/add/", "/customer/search", "/customer/1/", "/customer/1/edit/", "/customer/1/delete/"))
def test_login_required(client, route):
    response = client.post(route, follow_redirects=True)
    assert response.request.path == "/auth/login"


def test_login(client, auth):
    # Test that viewing the page renders without template errors
    assert client.get("/auth/login").status_code == 200

    # Test that successful login redirects to the index page
    response = auth.login()
    assert response.request.path == "/"

    # Login request set the _user_id in the session
    # Check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["_user_id"] == "1"
        assert g._login_user.username == "test"
        assert current_user.username == "test"


def test_access_protected_view(client, auth):
    auth.login()

    with client:
        assert client.get("/customer/").status_code == 200


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "_user_id" not in session
