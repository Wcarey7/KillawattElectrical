from flask_sqlalchemy import SQLAlchemy                 # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
from flask_login import LoginManager, current_user      # https://flask-login.readthedocs.io/en/latest/
from flask_migrate import Migrate                       # https://flask-migrate.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow               # https://flask-marshmallow.readthedocs.io/en/latest/
from flask_moment import Moment                         # https://flask-moment.readthedocs.io/en/latest/
from flask_wtf.csrf import CSRFProtect                  # https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
from flask_session import Session                       # https://flask-session.readthedocs.io/en/latest/
from flask_seeder import FlaskSeeder                    # https://github.com/diddi-/flask-seeder
from flask_admin import Admin, AdminIndexView           # https://flask-admin.readthedocs.io/en/latest/
from sqlalchemy.orm import DeclarativeBase
from flask import url_for, redirect, flash


class Base(DeclarativeBase):
    pass


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.security_permissions == "Admin":
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash('Please login as admin to access this page')
        return redirect(url_for('auth.login'))


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()
marshmallow = Marshmallow()
moment = Moment()
csrf = CSRFProtect()
session = Session()
seeder = FlaskSeeder()
admin = Admin(name='Killawatt Electrical',
              index_view=MyAdminIndexView(name='Dashboard Home'),
              base_template='admin/custom_layout.html',
              template_mode="bootstrap4",
              )
