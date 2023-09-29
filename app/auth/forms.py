from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
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
    email = StringField('Email', validators=[DataRequired()])           # Email() validator removed, was raising an error during Unit Tests
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
        if user is not None:
            raise ValidationError('Please use a different email address.')
