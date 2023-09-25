from flask_sqlalchemy import SQLAlchemy         # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
from flask_login import LoginManager            # https://flask-login.readthedocs.io/en/latest/
from flask_migrate import Migrate               # https://flask-migrate.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow       # https://flask-marshmallow.readthedocs.io/en/latest/
from flask_moment import Moment                 # https://flask-moment.readthedocs.io/en/latest/
from flask_wtf.csrf import CSRFProtect          # https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
from flask_session import Session               # https://flask-session.readthedocs.io/en/latest/
from flask_seeder import FlaskSeeder            # https://github.com/diddi-/flask-seeder
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()
marshmallow = Marshmallow()
moment = Moment()
csrf = CSRFProtect()
session = Session()
seeder = FlaskSeeder()
