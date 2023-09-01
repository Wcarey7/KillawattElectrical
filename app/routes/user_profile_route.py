from app.extensions import db
from app.models.user import User
from datetime import datetime
from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import login_required, current_user


bp = Blueprint('user_profile', __name__)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/<username>/')
@login_required
def user(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    return render_template('user_profile.html.j2', user=user)