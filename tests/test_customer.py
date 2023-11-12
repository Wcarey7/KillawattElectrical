import pytest
from app import db
from app.models.customer import Customer, Telephone, Email
from app.models.address import Address


def test_add_customer(client, auth, app):
    auth.login()

    # Test that viewing the page renders without template errors
    assert client.get("/customer/add/").status_code == 200

    response = client.post("/customer/add/", data={
        "name": "Dev",
        "street": "123 Dev St",
        "city": "Lancaster",
        "state": "CA",
        "zip": "93536",
        "phone_number": "(661)810-8496",
        "email": "dev@example.com",
    }, follow_redirects=True)

    # Test that successful add customer redirects to the customer home
    assert response.request.path == "/customer/"

    # Test that the customer was inserted into the database
    with app.app_context():
        select_name = db.select(Customer).filter_by(name="Dev")
        customer = db.session.execute(select_name).scalar()
        assert customer is not None

        select_address = db.select(Address).filter_by(street="123 Dev St")
        address = db.session.execute(select_address).scalar()
        assert address is not None

        select_telephone = db.select(Telephone).filter_by(phone_number="6618108496")
        telephone = db.session.execute(select_telephone).scalar()
        assert telephone is not None

        select_email = db.select(Email).filter_by(email="dev@example.com")
        email = db.session.execute(select_email).scalar()
        assert email is not None


def test_update_customer(client, auth, app):
    auth.login()
    pass


def test_delete_customer(client, auth, app):
    auth.login()

    response = client.post("/customer/1/delete/", follow_redirects=True)
    assert response.request.path == "/customer/"

    with app.app_context():
        assert db.session.get(Customer, 1) is None
