from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email
from app import db
from app.models.user import User


def select_field_choices():
    choices = [('Admin', 'Admin'),
               ('Regular User', 'Regular User'),
               ]
    return choices


class adminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    security_permissions = SelectField('Security Permissions', choices=select_field_choices(), validators=[DataRequired()])

    def validate_username(self, username):
        if self.username.object_data != username.data:
            user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()
            if user is not None:
                flash('Username already in use. Please choose a different username.')
                raise ValidationError('Username already in use. Please choose a different username.')

    def validate_email(self, email):
        if self.email.object_data != email.data:
            user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
            if user is not None:
                flash('Email already registered. Please use a different email.')
                raise ValidationError('Email already registered. Please use a different email.')
