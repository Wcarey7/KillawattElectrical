from flask import render_template, current_app, request, url_for, redirect, flash, session, jsonify
from flask_login import login_required
from app import db
from app.customer import bp
from app.models.customer import Customer, Telephone, Email
from app.models.address import Address
from app.customer.forms import customerForm


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
                           )


@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = customerForm()
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
        flash('New Customer Added')
        return jsonify(status='200 OK')

    return render_template('customer/new_customer.html.j2',
                           form=form,
                           Customer=Customer,
                           )


# Customer detail view
@bp.route('/<int:Id>/', methods=['POST', 'GET'])
@login_required
def detail(Id):
    form = customerForm()
    customer = db.get_or_404(Customer, Id)

    if request.method == 'GET':
        # Pre-fill forms
        form.name.data = customer.name
        form.street.data = customer.addresses[0].street
        form.city.data = customer.addresses[0].city
        form.state.data = customer.addresses[0].state
        form.zip.data = customer.addresses[0].zip
        form.phone_number.data = customer.phone_numbers[0].phone_number
        form.email.data = customer.emails[0].email

    return render_template('customer/customer_navbar.html.j2',
                           customer=customer,
                           form=form,
                           )


@bp.route('/<int:Id>/delete/', methods=['POST'])
@login_required
def delete_customer(Id):
    customerID = db.get_or_404(Customer, Id)
    db.session.delete(customerID)
    db.session.commit()
    flash('Customer deleted')
    return jsonify(status='200 OK')


# Edit route within the customer detail view
@bp.route('/<int:Id>/edit/', methods=['POST'])
@login_required
def edit(Id):
    form = customerForm()
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
        return jsonify(status='200 OK')


@bp.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if 'search_tag' in session and request.method != 'POST':
        search_tag = session['search_tag']  # Perist search item across pagination.
    else:
        search_tag = request.form['search_tag']
        session['search_tag'] = search_tag

    page = request.args.get('page', 1, type=int)
    customers = db.paginate(db.select(Customer).where(Customer.name.like('%' + search_tag + '%')),
                            page=page,
                            per_page=current_app.config['CUSTOMERS_PER_PAGE'],
                            )

    # Pagination endpoint for macro
    endpoint = 'customer.search'

    return render_template('customer/index.html.j2',
                           customers=customers,
                           endpoint=endpoint,
                           )
