import unittest
import unittest
import os
import json
from flask import Flask
from server import app, db


class ServerTest(unittest.TestCase):
    """Tests behavior of the API."""

    def setUp(self):
        """Test Setup."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        self.app = app.test_client()
        self.app.secret_key = 1
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_user_creation(self):
        """Tests user creation with valid card number."""
        user = {
            'card_number': 1,
            'employee_id': 111,
            'full_name': 'Steve Rogers',
            'email': 'cap@email.com',
            'mobile_number': 12345,
            'pin': 1111,
            'card_balance': 0
        }
        response = self.app.post('/user/new', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Steve Rogers! Your current card balance is &#163;0.', response.data)

    def test_user_retrieval(self):
        """Tests user retrieval with valid card number."""
        user = {
            'card_number': 1,
            'employee_id': 111,
            'full_name': 'Steve Rogers',
            'email': 'cap@email.com',
            'mobile_number': 12345,
            'pin': 1111,
            'card_balance': 0
        }
        self.app.post('/user/new', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        response = self.app.get('/user/1', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back Steve Rogers! Your current card balance is &#163;0.', response.data)

    def test_user_retrieval_unregistered_user(self):
        """Tests user retrieval with an invalid card number."""
        user = {
            'card_number': 2,  # This card number is not registered.
            'employee_id': 111,
            'full_name': 'Steve Rogers',
            'email': 'cap@email.com',
            'mobile_number': 12345,
            'pin': 1111,
            'card_balance': 0
        }
        response = self.app.get('/user/2', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No card found for that number in the system. Please register your card.', response.data)

    def test_user_editing(self):
        """Tests editing a user with a valid card number."""
        user = {
            'card_number': 1,
            'employee_id': 111,
            'full_name': 'Steve Rogers',
            'email': 'cap@email.com',
            'mobile_number': 12345,
            'pin': 1111,
            'card_balance': 0
        }
        self.app.post('/user/new', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        response = self.app.put('/user/1', headers={'Content-Type': 'application/json'},
                                data=json.dumps({'card_balance': 25}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your card balance is now &#163;25.', response.data)

    def test_user_deletion(self):
        """Tests deleting a user with a valid card number."""
        user = {
            'card_number': 1,
            'employee_id': 111,
            'full_name': 'Steve Rogers',
            'email': 'cap@email.com',
            'mobile_number': 12345,
            'pin': 1111,
            'card_balance': 0
        }
        self.app.post('/user/new', headers={'Content-Type': 'application/json'}, data=json.dumps(user))
        response = self.app.delete('/user/1', headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account for card number 1 has been deleted.', response.data)


if __name__ == '__main__':
    unittest.main()
