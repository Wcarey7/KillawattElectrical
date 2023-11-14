from faker import Faker  # https://faker.readthedocs.io/en/master/
from flask_seeder import Seeder, Faker as FlaskFaker, generator
from app import db
from app.models.customer import Customer, Email, Telephone
from app.models.address import Address


# Faker doesnt need access to the db, okay to init here.
fake = Faker()


def fake_state():
    return fake.state_abbr(include_territories=False, include_freely_associated_states=False)


# flask-seeder Generator subclass to return Faker methods.
class FakerGenerator(generator.Generator):
    def __init__(self, method, **kwargs):
        super().__init__(**kwargs)
        self._method = method

    def generate(self):
        return self._method()


class CustomerSeeder(Seeder):

    def run(self):
        """ To seed: flask seed run
        flask-seeder cannot append relationships to its instantiated classes.
        So the 'customer_id' is manually set on the many to one relationships.
        """

        # Delete all existing customers in database before seeding
        customers = db.session.execute(db.select(Customer)).scalars().all()
        for customer in customers:
            db.session.delete(customer)
        db.session.commit()
        print(fake.state_abbr(include_territories=False))
        print(fake.state_abbr())
        customer_faker = FlaskFaker(
            cls=Customer,
            init={
                "id": generator.Sequence(),
                "name": FakerGenerator(fake.name),
            }
        )

        address_faker = FlaskFaker(
            cls=Address,
            init={
                "street": FakerGenerator(fake.street_address),
                "city": FakerGenerator(fake.city),
                "state": FakerGenerator(fake_state),
                "zip": FakerGenerator(fake.postcode),
                "customer_id": generator.Sequence(),
            }
        )

        email_faker = FlaskFaker(
            cls=Email,
            init={
                "email": FakerGenerator(fake.free_email),
                "customer_id": generator.Sequence()
            }
        )

        telephone_faker = FlaskFaker(
            cls=Telephone,
            init={
                "phone_number": FakerGenerator(fake.basic_phone_number),
                "customer_id": generator.Sequence()
            }
        )

        num_to_create = 22

        # Create Customer
        for customer in customer_faker.create(num_to_create):
            print("Adding customer: %s" % customer)
            self.db.session.add(customer)

        # Create Address
        for address in address_faker.create(num_to_create):
            print("Adding address: %s" % address)
            self.db.session.add(address)

        # Create Email
        for email in email_faker.create(num_to_create):
            print("Adding email: %s" % email)
            self.db.session.add(email)

        # Create Telephone
        char_to_remove = ["(", ")", "-"]
        for telephone in telephone_faker.create(num_to_create):
            for char in char_to_remove:
                telephone.phone_number = telephone.phone_number.replace(char, "")
            print("Adding telephone: %s" % telephone)
            self.db.session.add(telephone)
