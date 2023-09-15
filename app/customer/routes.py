from flask import render_template, current_app, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.customer import bp
from app.models.customer import Customer, Telephone, Email
from app.models.address import Address
from app.customer.forms import AddCustomerForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    customers = db.paginate(db.select(Customer), 
                            page=page, 
                            per_page=current_app.config['CUSTOMERS_PER_PAGE'],
                            )

    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        customers = db.paginate(db.select(Customer).where(Customer.name.like(search)), 
                                page=page, 
                                per_page=current_app.config['CUSTOMERS_PER_PAGE'],
                                )
        
        return render_template('customer/index.html.j2', 
                               customers=customers, 
                               tag=tag, 
                               username=current_user.username,
                               )
    
    return render_template('customer/index.html.j2',
                            customers=customers,
                            username=current_user.username,
                            ) 


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
                              customer_id=new_customer.id,
                              )
        
        new_phone = Telephone(phoneNumber=form.phoneNum.data, 
                              customer_id=new_customer.id,
                              )
        
        new_email = Email(email=form.email.data, 
                          customer_id=new_customer.id,
                          )
        
        db.session.add_all([new_address, new_phone, new_email])
        db.session.commit()
        return redirect(url_for('customer.index'))
        
    return render_template('customer/new_customer.html.j2', 
                            form=form, 
                            Customer=Customer,
                            username=current_user.username,
                            ) 


# Customer detail view 
@bp.route('/<int:Id>/')
@login_required
def detail(Id):
    customer = db.get_or_404(Customer, Id)
  
    return render_template('customer/customer_detail.html.j2', 
                           customer=customer, 
                           username=current_user.username,
                           )


@bp.route('/<int:Id>/delete/', methods=['POST'])
@login_required
def delete_customer(Id):
    customerID = db.get_or_404(Customer, Id)
    db.session.delete(customerID)
    db.session.commit()
    flash('Customer deleted')
    return redirect(url_for('customer.index'))


# Edit route within the customer detail view
@bp.route('/<int:Id>/edit/', methods=['POST', 'GET'])
@login_required
def edit(Id):
    form = AddCustomerForm()
    customer = db.get_or_404(Customer, Id)
    
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.addresses[0].street = form.street.data
        customer.addresses[0].city = form.city.data
        customer.addresses[0].state = form.state.data
        customer.addresses[0].zip = form.zip.data
        customer.phoneNum[0].phoneNumber = form.phoneNum.data
        customer.email[0].email = form.email.data
        
        db.session.add(customer)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('customer.detail', Id=customer.id))
    
    elif request.method == 'GET':
        # Pre-fill forms
        form.name.data = customer.name
        form.street.data = customer.addresses[0].street
        form.city.data = customer.addresses[0].city
        form.state.data = customer.addresses[0].state
        form.zip.data = customer.addresses[0].zip
        form.phoneNum.data = customer.phoneNum[0].phoneNumber
        form.email.data = customer.email[0].email
        
    return render_template('customer/update_customer.html.j2',
                           form=form, 
                           customer=customer, 
                           username=current_user.username,
                           )
    