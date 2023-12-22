from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import db
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()
        if user is not None:
            flash('Username already in use. Please choose a different username.')
            raise ValidationError('Username already in use. Please choose a different username.')

    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
        if user is not None:
            flash('Email already registered. Please use a different email.')
            raise ValidationError('Email already registered. Please use a different email.')

    def validate_password2(self, password2):
        if self.password.data != password2.data:
            flash('Passwords do not match')
            raise ValidationError('Passwords do not match')
