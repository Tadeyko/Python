from flask import Flask
from extensions import *

from .resume.blueprint import resume
from .tasks.blueprint import tasks
from .cookie.blueprint import cookie
from .account.blueprint import bp
from .posts.blueprint import postsBp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
       app.register_blueprint(resume, url_prefix="/")
       app.register_blueprint(tasks, url_prefix="/tasks")
       app.register_blueprint(cookie, url_prefix="/cookie")
       app.register_blueprint(bp, url_prefix="/account")
       app.register_blueprint(postsBp, url_prefix="/posts")

    return app