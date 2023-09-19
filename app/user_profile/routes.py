from app import db
from app.user_profile import bp
from app.models.user import User
from datetime import datetime
from flask import render_template
from flask_login import login_required, current_user


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/<username>/')
@login_required
def user(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    return render_template('user_profile.html.j2', user=user, username=current_user.username)
