from flask import render_template
from flask_login import login_required, current_user
from app.home import bp


@bp.route('/')
@login_required
def index():
    return render_template('index.html.j2', username=current_user.username)
