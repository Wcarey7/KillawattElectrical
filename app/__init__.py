from flask import Flask
from config import config
from logging.handlers import RotatingFileHandler
import logging
import os
from app.utilities.history_meta import versioned_session
from app.extensions import db
from app.extensions import login_manager
from app.extensions import migrate
from app.extensions import marshmallow
from app.extensions import moment
from app.extensions import csrf
from app.extensions import session
from app.extensions import seeder
from app.extensions import admin
from app.models.user import User


def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config[config_class])

    # Convert session lifetime to a number(milliseconds).
    @app.context_processor
    def add_session_config():
        return {
            'PERMANENT_SESSION_LIFETIME_MS': (
                app.permanent_session_lifetime.seconds * 1000),
        }

    ###################################################
    #### Init Extensions
    ###################################################
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    marshmallow.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    session.init_app(app)
    seeder.init_app(app, db)
    admin.init_app(app)

    versioned_session(db.session)
    ###################################################
    #### Login Manager
    ###################################################
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    ###################################################
    #### Register Blueprints
    ###################################################
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.customer import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user_profile import bp as user_profile_bp
    app.register_blueprint(user_profile_bp, url_prefix='/user')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    ###################################################
    #### Error Logging to File - For Production
    ###################################################
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/Killawatt.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Killawatt startup')

    return app
