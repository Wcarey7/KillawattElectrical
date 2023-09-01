from app import db
from app.models.user import User
from app.auth.forms import LoginForm, RegistrationForm
from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():              
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_create_date()
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for("auth.login"))
    
    return render_template('auth/register.html.j2', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar()

        # check if the user actually exists
        # take the user-supplied password and compare it to the hashed password in the database
        if not user or not user.check_password(form.password.data):
            flash('Incorrect username or password, try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)

        # Next redirects user back to previous page.
        # .netloc for security to ensure redirect is within same domain
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    
    return render_template('auth/login.html.j2', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
