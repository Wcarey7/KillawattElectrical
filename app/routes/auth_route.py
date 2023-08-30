from app.extensions import db
from app.models.user import User
from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Username is required.')
        elif not password:
            flash('Password is required.')
            
        user = db.session.execute(db.select(User)).first()
        if user:
            flash(f'The username, {username}, is already registered')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    
    return render_template('auth/register.html.j2')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Incorrect username or password, try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        # remember user after session expires
        login_user(user, remember=remember)
        return redirect(url_for('home.profile'))
    
    return render_template('auth/login.html.j2')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
