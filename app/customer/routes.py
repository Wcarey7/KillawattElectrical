from flask import render_template, current_app, request, g, flash, session, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timezone
from app import db
from app.customer import bp
from app.utilities.utilities import format_date_local
from app.models.customer import Customer, Telephone, Email, Memo
from app.models.address import Address
from app.models.user import User
from app.customer.forms import customerForm, addContactInfoForm, addMemoForm


##############################################################################################################
#### Table Index View of All Customers
##############################################################################################################
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Reset search query.
    session.pop('search_tag', default=None)
    session['thisRoutePrevPage'] = request.url

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


##############################################################################################################
#### Add Customer
##############################################################################################################
@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = customerForm()
    if form.validate_on_submit():
        new_customer = Customer(name=form.name.data,
                                related_username=current_user.username,
                                create_date=datetime.now(timezone.utc),
                                )
        new_address = Address(street=form.street.data,
                              city=form.city.data,
                              state=form.state.data,
                              zip=form.zip.data,
                              related_username=current_user.username,
                              )

        new_phone = Telephone(phone_number=form.phone_number.data,
                              related_username=current_user.username,
                              )
        new_email = Email(email=form.email.data,
                          related_username=current_user.username,
                          )

        new_customer.addresses.append(new_address)
        new_customer.phone_numbers.append(new_phone)
        new_customer.emails.append(new_email)

        db.session.add(new_customer)
        db.session.commit()
        flash('New Customer Added')
        return jsonify(status='200 OK', message='Customer add successful')

    return render_template('customer/new_customer.html.j2',
                           form=form,
                           Customer=Customer,
                           )


##############################################################################################################
#### Customer Summary View
##############################################################################################################
@bp.route('/<int:Id>/', methods=['POST', 'GET'])
@login_required
def detail(Id):
    form = customerForm()
    addContactForm = addContactInfoForm()
    createNewMemoForm = addMemoForm()
    customer = db.get_or_404(Customer, Id)

    memos = db.session.execute(db.select(Memo, User)
                               .join(Memo.user)
                               .where(Memo.customer_id == Id)
                               .order_by(Memo.create_date.desc())).all()

    thisRoutePrevPage = session.get('thisRoutePrevPage')

    if request.method == 'GET':
        # Pre-fill forms
        form.name.data = customer.name
        form.street.data = customer.addresses[0].street
        form.city.data = customer.addresses[0].city
        form.state.data = customer.addresses[0].state
        form.zip.data = customer.addresses[0].zip
        form.phone_number.data = customer.phone_numbers[0].phone_number
        form.email.data = customer.emails[0].email
        if (len(customer.phone_numbers) > 1):
            addContactForm.other_phone_number.data = customer.phone_numbers[1].phone_number
        if (len(customer.emails) > 1):
            addContactForm.other_email.data = customer.emails[1].email

        customer_create_date = format_date_local('', customer.create_date, '')

    return render_template('customer/customer_navbar.html.j2',
                           customer=customer,
                           form=form,
                           addContactForm=addContactForm,
                           createNewMemoForm=createNewMemoForm,
                           thisRoutePrevPage=thisRoutePrevPage,
                           customer_create_date=customer_create_date,
                           memos=memos,
                           format_date_local=format_date_local,
                           )


##############################################################################################################
#### Edit Customer - Also handles deletion of other contact info (otherPhone, otherEmail).
##############################################################################################################
@bp.route('/<int:Id>/edit/', methods=['POST'])
@login_required
def edit(Id):
    form = customerForm()
    addContactForm = addContactInfoForm()
    customer = db.get_or_404(Customer, Id)
    username = current_user.username

    if form.validate_on_submit():
        if customer.name != form.name.data:
            customer.name = form.name.data
            customer.related_username = username
        if customer.addresses[0].street != form.street.data:
            customer.addresses[0].street = form.street.data
            customer.addresses[0].related_username = username
        if customer.addresses[0].city != form.city.data:
            customer.addresses[0].city = form.city.data
            customer.addresses[0].related_username = username
        if customer.addresses[0].state != form.state.data:
            customer.addresses[0].state = form.state.data
            customer.addresses[0].related_username = username
        if customer.addresses[0].zip != form.zip.data:
            customer.addresses[0].zip = form.zip.data
            customer.addresses[0].related_username = username
        if customer.phone_numbers[0].phone_number != form.phone_number.data:
            customer.phone_numbers[0].phone_number = form.phone_number.data
            customer.phone_numbers[0].related_username = username
        if customer.emails[0].email != form.email.data:
            customer.emails[0].email = form.email.data
            customer.emails[0].related_username = username

        # Add/edit other_phone.
        if (len(customer.phone_numbers) <= 1 and request.form.get('other_phone_number')):
            addOtherPhone = Telephone(phone_number=request.form.get('other_phone_number'),
                                      related_username=current_user.username,
                                      )
            customer.phone_numbers.append(addOtherPhone)

        if (len(customer.phone_numbers) > 1):
            if customer.phone_numbers[1].phone_number != addContactForm.other_phone_number.data:
                customer.phone_numbers[1].phone_number = addContactForm.other_phone_number.data
                customer.phone_numbers[1].related_username = username

        # Add/edit other_email.
        if (len(customer.emails) <= 1 and request.form.get('other_email')):
            addOtherEmail = Email(email=request.form.get('other_email'),
                                  related_username=current_user.username,
                                  )
            customer.emails.append(addOtherEmail)

        if (len(customer.emails) > 1):
            if customer.emails[1].email != addContactForm.other_email.data:
                customer.emails[1].email = addContactForm.other_email.data
                customer.emails[1].related_username = username

        # Handle deletion of other contact info
        if 'deleteOtherContactInfo' in request.form and request.form['deleteOtherContactInfo'] == 'true':
            # Delete otherPhone or otherEmail.
            if 'otherPhone' in request.form and len(customer.phone_numbers) > 1:
                other_phone_to_delete = db.session.get(Telephone, customer.phone_numbers[1].id)
                if other_phone_to_delete:
                    db.session.delete(other_phone_to_delete)

            if 'otherEmail' in request.form and len(customer.emails) > 1:
                other_email_to_delete = db.session.get(Email, customer.emails[1].id)
                if other_email_to_delete:
                    db.session.delete(other_email_to_delete)

        db.session.add(customer)
        db.session.commit()
        flash('Your changes have been saved.')
        return jsonify(status='200 OK', message='Customer edit successful')

    # If form did not validate, return an error response
    flash('Form validation failed. Your changes were not saved.')
    return jsonify(status='400 Bad Request', error='Form validation failed')


##############################################################################################################
#### Delete Customer
##############################################################################################################
@bp.route('/<int:Id>/delete/', methods=['POST'])
@login_required
def delete_customer(Id):
    customerID = db.get_or_404(Customer, Id)
    if customerID:
        db.session.delete(customerID)
        db.session.commit()
        flash('Customer deleted')
        return jsonify(status='200 OK', message='Customer deletion successful')

    flash('Customer does not exist.')
    return jsonify(status='400 Bad Request', message='Customer does not exist.')


##############################################################################################################
#### Search Customer
##############################################################################################################
@bp.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    session['thisRoutePrevPage'] = request.url
    thisRoutePrevPage = session.get('thisRoutePrevPage')

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
                           thisRoutePrevPage=thisRoutePrevPage,
                           )


##############################################################################################################
#### Create new memo
##############################################################################################################
@bp.route('/<int:Id>/create_new_memo/', methods=['POST'])
@login_required
def create_new_memo(Id):
    createNewMemoForm = addMemoForm()

    if request.method == 'POST':
        new_memo = Memo(memo_content=createNewMemoForm.memo_content.data,
                        create_date=datetime.now(timezone.utc),
                        related_username=current_user.username,
                        customer_id=Id,
                        user_id=current_user.id,
                        )

        db.session.add(new_memo)
        db.session.commit()
        flash('Memo added successfully')
        return jsonify(status='200 OK', message='Memo added successfully')

    flash('Memo creation failed')
    return jsonify(status='400 Bad Request', message='Memo creation failed')
