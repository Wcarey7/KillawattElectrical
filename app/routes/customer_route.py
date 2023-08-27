from app.extensions import db
from app.models.customer import Customer
from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import login_required, current_user


bp = Blueprint('customer', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    customers = Customer.query.all()

    if request.method == 'POST':
        new_customer = Customer(name=request.form['input-name'], address=request.form['input-address'])
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('customer.index'))
    
    return render_template('customer/index.html.j2', customers=customers, username=current_user.username) 