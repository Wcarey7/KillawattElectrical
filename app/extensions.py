from flask_sqlalchemy import SQLAlchemy         # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
from flask_login import LoginManager            # https://flask-login.readthedocs.io/en/latest/
from flask_migrate import Migrate               # https://flask-migrate.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow       # https://flask-marshmallow.readthedocs.io/en/latest/
from flask_bootstrap import Bootstrap5          # https://bootstrap-flask.readthedocs.io/en/stable/
from flask_moment import Moment                 # https://flask-moment.readthedocs.io/en/latest/
from flask_wtf.csrf import CSRFProtect          # https://flask-wtf.readthedocs.io/en/0.15.x/csrf/


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
marshmallow = Marshmallow()
bootstrap = Bootstrap5()
moment = Moment()
csrf = CSRFProtect()