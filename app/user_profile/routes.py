from datetime import datetime, timezone
from flask import render_template, request, session, jsonify
from flask_login import login_required, current_user
from app.user_profile import bp
from app.models.user import User
from app import db


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/<username>/')
@login_required
def user(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    return render_template('user_profile/user_profile.html.j2',
                           user=user,
                           )


@bp.route('/set_timezone/', methods=['POST', 'GET'])
def set_timezone():
    timezone = request.form['timezone']
    session['timezone'] = timezone
    session.modified = True
    return jsonify(status='200 OK')
