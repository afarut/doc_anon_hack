from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from app import routes


@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))
