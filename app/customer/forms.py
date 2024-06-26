from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField, SelectField, EmailField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length


def select_field_choices_state():
    choices = [("", ""), ("AL", "AL"), ("AK", "AK"), ("AZ", "AZ"), ("AR", "AR"), ("CA", "CA"),
               ("CO", "CO"), ("CT", "CT"), ("DE", "DE"), ("DC", "DC"), ("FL", "FL"), ("GA", "GA"), ("HI", "HI"),
               ("ID", "ID"), ("IL", "IL"), ("IN", "IN"), ("IA", "IA"), ("KS", "KS"), ("KY", "KY"), ("LA", "LA"),
               ("ME", "ME"), ("MD", "MD"), ("MA", "MA"), ("MI", "MI"), ("MN", "MN"), ("MS", "MS"), ("MO", "MO"),
               ("MT", "MT"), ("NE", "NE"), ("NV", "NV"), ("NH", "NH"), ("NJ", "NJ"), ("NM", "NM"), ("NY", "NY"),
               ("NC", "NC"), ("ND", "ND"), ("OH", "OH"), ("OK", "OK"), ("OR", "OR"), ("PA", "PA"), ("RI", "RI"),
               ("SC", "SC"), ("SD", "SD"), ("TN", "TN"), ("TX", "TX"), ("UT", "UT"), ("VT", "VT"), ("VA", "VA"),
               ("WA", "WA"), ("WV", "WV"), ("WI", "WI"), ("WY", "WY")]
    return choices


def select_to_add_contact_choices():
    choices = [("", ""),
               ("otherPhone", "Other Phone"),
               ("otherEmail", "Other Email")]
    return choices


class customerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', choices=select_field_choices_state(), validators=[DataRequired()])
    zip = IntegerField('Zip', validators=[DataRequired()])
    phone_number = TelField('Phone Number', id='phoneNumber', name='Phone Number', validators=[DataRequired(), Length(min=13, max=13)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit', id='customerFormButton')


class addContactInfoForm(FlaskForm):
    select_to_add = SelectField('Create Contact', choices=select_to_add_contact_choices())
    other_phone_number = TelField('Other Phone', id='otherPhone', validators=[DataRequired(), Length(max=13)])
    other_email = EmailField('Other Email', id="otherEmail", validators=[DataRequired(), Email()])


class addMemoForm(FlaskForm):
    memo_content = TextAreaField('Memo Content', id='memoContent', validators=[DataRequired(), Length(min=1)])
