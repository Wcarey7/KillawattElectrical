from flask import session
import pytz


##############################################################################################################
#### Custom formatter for date fields
#### view and name args are for compatibility with Flask-Admin, empty strings can be passed in otherwise.
#### Example: user_last_seen = format_date_local('', user.last_seen, '')
##############################################################################################################
def format_date_local(view, value, name):
    print(value)
    if value is None:
        return ""

    if 'timezone' in session:
        local_tz = pytz.timezone(session['timezone'])
    else:
        # Default to UTC if timezone is not set
        local_tz = pytz.utc

    localized_dt = value.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return localized_dt.strftime('%m-%d-%Y %I:%M %p')
