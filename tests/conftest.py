import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.user import User
from app.models.customer import Customer, Telephone, Email
from app.models.address import Address


user1_pass = generate_password_hash("test")


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test."""
    # Create the app with common test config
    app = create_app('testing')

    # Create the database and load test data
    # Set _password to pre-generated hashes, since hashing for each test is slow
    with app.app_context():
        db.create_all()

        # Create initial test User and insert into test database
        user = User(username="test", email="test@example.com", password=user1_pass)
        db.session.add(user)
        db.session.commit()

        # Create initial test Customer and insert into test database
        test_customer = Customer(name="Test Customer")
        test_address = Address(street="3333 West",
                               city="Palmdale",
                               state="CA",
                               zip="93536",
                               )

        test_phone = Telephone(phone_number="6618934876")
        test_email = Email(email="testcustomer@example.com")

        test_customer.addresses.append(test_address)
        test_customer.phone_numbers.append(test_phone)
        test_customer.emails.append(test_email)

        db.session.add(test_customer)
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
