from flask_testing import TestCase
from app import create_app

class Base(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app