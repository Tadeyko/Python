import os

baseDir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False 