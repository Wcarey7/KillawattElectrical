from flask import Blueprint, session
from flask_login import current_user
from datetime import datetime
from flask import url_for, redirect, flash
from flask_admin.contrib.sqla import ModelView
from app.models.user import User
from app.admin.forms import adminUserForm
from app.utilities.utilities import format_date_local
from app import db
from app import admin

bp = Blueprint('adminDash', __name__)


class userAdminView(ModelView):
    list_template = 'admin/custom_list.html'
    create_template = 'admin/custom_create.html'
    edit_template = 'admin/custom_edit.html'

    can_create = True
    can_edit = True
    can_delete = True

    page_size = 10
    column_display_pk = True
    column_display_actions = True
    column_searchable_list = ('username', 'email')
    column_exclude_list = ('password')

    form = adminUserForm
    form_excluded_columns = ('create_date', 'last_seen', 'memos')

    def is_accessible(self):
        if current_user.security_permissions == 'Admin':
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash('Please login as admin to access this page')
        return redirect(url_for('auth.login'))

    # Override default formatters
    column_type_formatters = {
        datetime: format_date_local,
    }


admin.add_view(userAdminView(User, db.session, name='Users', endpoint='users'))
