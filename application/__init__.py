from flask import Flask

app = Flask(__name__)

from application import forum_views
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application.forum import forum_models
from application.forum import forum_views
db.create_all()
