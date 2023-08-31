from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
marshmallow = Marshmallow()
bootstrap = Bootstrap()