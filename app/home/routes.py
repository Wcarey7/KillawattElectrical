from flask import render_template
from flask_login import current_user
from app.home import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        pass
    else:
        current_user.username = "Guest"

    return render_template('index.html.j2', username=current_user.username)
