from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()