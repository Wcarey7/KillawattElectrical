from app.extensions import db
from app.models.customer import Customer
from app.models.address import Address
from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import select, text

bp = Blueprint('customer', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    customer = db.session.execute(db.select(Customer)).scalars()
    column_names = db.session.execute(text("SELECT * FROM Customer"))
    
    if request.method == 'POST':
        new_customer = Customer(name=request.form['input-name'])
        db.session.add(new_customer)
        db.session.commit()
        
        new_address = Address(street=request.form['input-street'], 
                                city=request.form['input-city'],
                                state=request.form['input-state'],
                                zip=request.form['input-zip'],
                                customer_id = new_customer.id)
                
        db.session.add(new_address)
        db.session.commit()
        return redirect(url_for('customer.index'))
    
    return render_template('customer/index.html.j2', 
                            customer=customer, 
                            column_names=column_names, 
                            username=current_user.username) 


@bp.route('/<int:Id>/')
@login_required
def detail(Id):
    customer = db.get_or_404(Customer, Id)
    customer_address = db.one_or_404(db.select(Address).filter_by(customer_id=Id))
    column_names = db.session.execute(text("SELECT * FROM Address"))
    return render_template('customer/customer_detail.html.j2', 
                           customer=customer, 
                           customer_address=customer_address,
                           column_names=column_names, 
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
    customer = db.one_or_404(db.select(Address).filter_by(customer_id=Id))
    
    if request.method == 'POST':
        street = request.form['input-update-street']
        city = request.form['input-update-city']
        state = request.form['input-update-state']
        zip = request.form['input-update-zip']

        customer.street = street
        customer.city = city
        customer.state = state
        customer.zip = zip

        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customer.detail', Id=customer.customer_id))

    return render_template('customer/customer_detail.html.j2', 
                           customer=customer, 
                           username=current_user.username)