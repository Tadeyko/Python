from .base import Base
from extensions import db
from app.account.models import User

class Account(Base):
    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page(self):
        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        response = self.client.get('/account/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_logout(self):
        response = self.client.get('/account/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_post(self):
        response = self.client.post('/account/register', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='testpassword',
        ), follow_redirects=True)
            
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
