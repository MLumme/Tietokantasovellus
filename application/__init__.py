from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

if(os.environ.get("HEROKU")):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application.forum import forum_models, forum_views
from application.auth import auth_models, auth_views
from application.utils import utils_views
from application.auth.auth_models import User
from os import urandom
from flask_login import LoginManager

app.config["SECRET_KEY"] = urandom(32)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "auth_login"
loginManager.login_message = "Login to access."

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()
