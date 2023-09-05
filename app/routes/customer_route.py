from app import db
from app.models.customer import Customer
from app.models.address import Address
from app.customer.forms import AddCustomerForm
from flask import render_template, current_app, request, url_for, redirect, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import text

bp = Blueprint('customer', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #customer = db.session.execute(db.select(Customer)).scalars().all()
    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(db.select(Customer), page=page, per_page=current_app.config['CUSTOMERS_PER_PAGE'])
    customers = pagination.items
    
    return render_template('customer/index.html.j2', 
                            customers=customers,
                            pagination=pagination, 
                            Customer=Customer,
                            username=current_user.username) 


@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = AddCustomerForm()
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
        
    return render_template('customer/new_customer.html.j2', 
                            form=form, 
                            Customer=Customer,
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
        flash('Your changes have been saved.')
        return redirect(url_for('customer.detail', Id=customer.customer_id))

    return render_template('customer/customer_detail.html.j2', 
                           customer=customer, 
                           username=current_user.username)