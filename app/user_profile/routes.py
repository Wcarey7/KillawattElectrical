from datetime import datetime, timezone
from flask import render_template, request, session, jsonify
from flask_login import login_required, current_user
from app.utilities.utilities import format_date_local
from app.user_profile import bp
from app.models.user import User
from app import db


@bp.before_app_request
def user_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/<username>/')
@login_required
def user(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    user_create_date = format_date_local('', user.create_date, '')
    user_last_seen = format_date_local('', user.last_seen, '')
    return render_template('user_profile/user_profile.html.j2',
                           user=user,
                           user_last_seen=user_last_seen,
                           user_create_date=user_create_date,
                           )


@bp.route('/set_timezone/', methods=['POST', 'GET'])
def set_timezone():
    timezone = request.form['timezone']
    session['timezone'] = timezone
    session.modified = True
    return jsonify(status='200 OK')
