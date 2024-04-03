from flask import session
import pytz


##############################################################################################################
#### Custom formatter for date fields
#### view and name args are for compatibility with Flask-Admin, empty strings can be passed in otherwise.
#### Example: user_last_seen = format_date_local('', user.last_seen, '')
##############################################################################################################
def format_date_local(view, value, name):
    if value is None:
        return ""

    if 'timezone' in session:
        local_tz = pytz.timezone(session['timezone'])
    else:
        # Default to UTC if timezone is not set
        local_tz = pytz.utc

    localized_dt = value.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return localized_dt.strftime('%m-%d-%Y %I:%M %p')


##############################################################################################################
#### Custom formatter for phone number as (XXX)XXX-XXXX
##############################################################################################################
def format_phone_number(phone_number):
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, phone_number))

    # Format the number as (XXX)XXX-XXXX
    formatted_number = f"({digits[0:3]}){digits[3:6]}-{digits[6:]}"

    return formatted_number
