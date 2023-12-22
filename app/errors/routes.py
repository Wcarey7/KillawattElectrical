from flask import render_template
from flask_login import current_user
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html.j2',
                           username=current_user.username,
                           ), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html.j2',
                           username=current_user.username,
                           ), 500
