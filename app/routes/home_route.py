from flask import render_template, Blueprint
from flask_login import login_required, current_user


bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html.j2', username=current_user.username)
