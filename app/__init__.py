from app.extensions import db
from app.extensions import login_manager
from app.extensions import migrate
from app.extensions import marshmallow
from app.extensions import bootstrap
from app.models.user import User
from flask import Flask
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    ###################################################
    #### Init Extensions
    ###################################################
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    bootstrap.init_app(app)
    
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
    from app.routes.home_route import bp as home_bp
    app.register_blueprint(home_bp)

    from app.errors.handlers import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.routes.customer_route import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')

    from app.routes.auth_route import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.user_profile_route import bp as user_profile_bp
    app.register_blueprint(user_profile_bp, url_prefix='/user')


    ###################################################
    #### Error Logging - For Production
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