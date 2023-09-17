from flask import render_template
from flask_login import login_required, current_user
from app.home import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        current_user.username = "Guest"
    return render_template('index.html.j2', username=current_user.username)
