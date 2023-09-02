from app.extensions import db
from app.models.customer import Customer
from app.models.address import Address
from app.customer.forms import AddCustomerForm
from flask import render_template, request, url_for, redirect, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import text

bp = Blueprint('customer', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    customer = db.session.execute(db.select(Customer)).scalars()
    column_names = db.session.execute(text("SELECT * FROM Customer"))
    form = AddCustomerForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            new_customer = Customer(name=form.name.data)
            db.session.add(new_customer)
            db.session.commit()
            
            new_address = Address(street=form.street.data, 
                                    city=form.city.data,
                                    state=form.state.data,
                                    zip=form.zip.data,
                                    customer_id = new_customer.id)
                    
            db.session.add(new_address)
            db.session.commit()
            return redirect(url_for('customer.index'))
    
    return render_template('customer/index.html.j2', 
                            customer=customer, 
                            column_names=column_names,
                            form=form, 
                            username=current_user.username) 


@bp.route('/<int:Id>/')
@login_required
def detail(Id):
    form = AddCustomerForm()
    customer = db.get_or_404(Customer, Id)
    customer_address = db.one_or_404(db.select(Address).filter_by(customer_id=Id))
    column_names = db.session.execute(text("SELECT * FROM Address"))

    # pre-fill update form fields
    form.street.data = customer_address.street
    form.city.data = customer_address.city
    form.state.data = customer_address.state
    form.zip.data = customer_address.zip
    
    return render_template('customer/customer_detail.html.j2', 
                           customer=customer, 
                           customer_address=customer_address,
                           column_names=column_names,
                           form=form, 
                           username=current_user.username)


@bp.route('/<int:Id>/delete/', methods=["POST"])
@login_required
def delete_customer(Id):
    customerID = db.get_or_404(Customer, Id)
    db.session.delete(customerID)
    db.session.commit()
    return redirect(url_for('customer.index'))


@bp.route('/<int:Id>/edit/', methods=["POST", "GET"])
@login_required
def edit(Id):
    form = AddCustomerForm()
    customer = db.one_or_404(db.select(Address).filter_by(customer_id=Id))

    if form.validate_on_submit():
        customer.street = form.street.data
        customer.city = form.city.data
        customer.state = form.state.data
        customer.zip = form.zip.data

        db.session.add(customer)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('customer.detail', Id=customer.customer_id))
    
    # elif request.method == 'GET':
    #     form.street.data = customer.street
    #     form.city.data = customer.city
    #     form.state.data = customer.state
    #     form.zip.data = customer.zip

    return render_template('customer/customer_detail.html.j2', 
                           customer=customer,
                           form=form, 
                           username=current_user.username)