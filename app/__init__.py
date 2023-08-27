from app.extensions import db
from app.extensions import login_manager
from app.models.user import User
from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    ###################################################
    #### Login Manager
    ###################################################
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    ###################################################
    #### Register Blueprints
    ###################################################
    from app.routes.home_route import bp as home_bp
    app.register_blueprint(home_bp)

    from app.routes.customer_route import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')

    from app.routes.auth_route import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    
    return app