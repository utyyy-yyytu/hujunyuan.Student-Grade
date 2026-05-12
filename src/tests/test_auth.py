import unittest
from src.app import app
from src.models.user import User
from src.models.database import db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_register_success(self):
        res = self.client.post('/register', json={
            'username': 'testuser',
            'password': '123456'
        })
        self.assertEqual(res.status_code, 201)

    def test_register_duplicate(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': '123456'
        })
        res = self.client.post('/register', json={
            'username': 'testuser',
            'password': '654321'
        })
        self.assertEqual(res.status_code, 400)

    def test_login_success(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': '123456'
        })
        res = self.client.post('/login', json={
            'username': 'testuser',
            'password': '123456'
        })
        self.assertEqual(res.status_code, 200)

    def test_login_failure(self):
        res = self.client.post('/login', json={
            'username': 'nobody',
            'password': 'wrong'
        })
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()