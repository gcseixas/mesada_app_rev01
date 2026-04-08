import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
load_dotenv()

database_url = os.getenv('DATABASE_URL', 'sqlite:///mesada.db')
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'feab4390c1432bea3243c0282fda2aef')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login" # type: ignore
login_manager.login_message_category = 'alert-info'

from app.routes import *
