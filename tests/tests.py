# Referenced from: https://blog.miguelgrinberg.com/post/how-to-write-unit-tests-in-python-part-3-web-applications
import unittest
from app import create_app, db
from app.models.user import User
from config import TestConfig
from flask import current_app


class UserAuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.client = None

    def populate_db(self):
        user = User(username='wade', email='wade@example.com')
        user.set_password('foo')
        db.session.add(user)
        db.session.commit()

    def login(self):
        self.client.post('/auth/login', data={
            'username': 'wade',
            'password': 'foo',
        })

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    # Any page but Home requires User to be logged in,
    # path after redirect should be to login page.
    def test_customer_page_redirect(self):
        response = self.client.get('/customer', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'

    def test_password_hashing(self):
        u = User(username='wade', email='wade@gmail.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'wade',
            'email': 'wade@example.com',
            'password': 'foo',
            'password2': 'foo',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/auth/login'  # Redirected to login

        # login with new user
        response = self.client.post('/auth/login', data={
            'username': 'wade',
            'password': 'foo',
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Logged in as: <b>wade</b>' in html      # TODO: Better spot to test HTML templates receives data. Username formatting is too variable

    def test_register_user_mismatched_passwords(self):
        response = self.client.post('/auth/register', data={
            'username': 'wade',
            'email': 'wade@example.com',
            'password': 'foo',
            'password2': 'bar',
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Passwords do not match' in html


if __name__ == '__main__':
    unittest.main()
