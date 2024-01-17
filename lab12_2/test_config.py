import os

WTF_CSRF_ENABLED = False
SECRET_KEY = b"secret"
baseDir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False 
TESTING = True