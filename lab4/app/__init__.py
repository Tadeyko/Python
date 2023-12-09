from flask import Flask

app = Flask(__name__)
app.secret_key = b"secret"

from app import views