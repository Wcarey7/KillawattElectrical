from flask import render_template, current_app, request, url_for, redirect, flash, session
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.customer import bp
from app.models.customer import Customer, Telephone, Email
from app.models.address import Address
from app.customer.forms import AddCustomerForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Reset search query.
    session.pop('search_tag', default=None)

    page = request.args.get('page', 1, type=int)
    customers = db.paginate(db.select(Customer),
                            page=page,
                            per_page=current_app.config['CUSTOMERS_PER_PAGE'],
                            )

    # Pagination endpoint for macro
    endpoint = 'customer.index'

    return render_template('customer/index.html.j2',
                           customers=customers,
                           endpoint=endpoint,
                           username=current_user.username,
                           )


@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = AddCustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(name=form.name.data)
        new_address = Address(street=form.street.data,
                              city=form.city.data,
                              state=form.state.data,
                              zip=form.zip.data,
                              )

        new_phone = Telephone()
        new_phone.format_set_phone_number(form.phone_number.data)
        new_email = Email(email=form.email.data)

        new_customer.addresses.append(new_address)
        new_customer.phone_numbers.append(new_phone)
        new_customer.emails.append(new_email)

        db.session.add(new_customer)
        db.session.commit()
        flash('New customer added')
        return redirect(url_for('customer.index'))

    return render_template('customer/new_customer.html.j2',
                           form=form,
                           Customer=Customer,
                           username=current_user.username,
                           )


# Customer detail view
@bp.route('/<int:Id>/', methods=['POST', 'GET'])
@login_required
def detail(Id):
    customer = db.get_or_404(Customer, Id)

    return render_template('customer/customer_navbar.html.j2',
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
        customer.phone_numbers[0].format_set_phone_number(form.phone_number.data)
        customer.emails[0].email = form.email.data

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
        form.phone_number.data = customer.phone_numbers[0].phone_number
        form.email.data = customer.emails[0].email

    return render_template('customer/edit_customer.html.j2',
                           form=form,
                           customer=customer,
                           username=current_user.username,
                           )


@bp.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if 'search_tag' in session:
        search_tag = session['search_tag']  # Perist search item across pagination.
    elif request.method == 'POST':
        search_tag = request.form['search_tag']
        session['search_tag'] = search_tag

    page = request.args.get('page', 1, type=int)
    #customers = db.paginate(db.select(Customer).where(Customer.name.like('%' + search_tag + '%')),
    customers = db.paginate(db.select(Customer, Email).where(or_(Customer.name.match(search_tag), Email.email.match(search_tag))), ## WORKS KIND OF
                            page=page,
                            per_page=current_app.config['CUSTOMERS_PER_PAGE'],
                            )

    # Pagination endpoint for macro
    endpoint = 'customer.search'

    return render_template('customer/index.html.j2',
                           customers=customers,
                           endpoint=endpoint,
                           username=current_user.username,
                           )
