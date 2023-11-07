from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import ValidationError, DataRequired, Email, Length


class AddCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=13, max=13)])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
