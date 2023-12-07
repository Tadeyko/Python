from flask import Flask
from extensions import *

from .api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix="/api")

    return app