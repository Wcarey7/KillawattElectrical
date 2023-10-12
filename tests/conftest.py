import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.user import User
from config import TestConfig


user1_pass = generate_password_hash("test")


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test."""
    # Create the app with common test config
    app = create_app(TestConfig)

    # Create the database and load test data
    # Set _password to pre-generated hashes, since hashing for each test is slow
    with app.app_context():
        db.create_all()
        user = User(username="test", email="test@example.com", password=user1_pass)
        db.session.add(user)
        db.session.commit()

    yield app


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self.client = client

    def login(self, username="test", password="test"):
        return self.client.post(
            "/auth/login", data={"username": username, "password": password}, follow_redirects=True
        )

    def logout(self):
        return self.client.get("/auth/logout")


@pytest.fixture(scope="module")
def auth(client):
    return AuthActions(client)
