from app import db
from flask import current_app

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    __mapper_args__ = {
        "polymorphic_identity": "address"
    }
    
    def __repr__(self):
        return {f"<id: {self.id!r},"
                f"street: {self.street!r}, "
                f"city: {self.city!r}, "
                f"state: {self.state!r}, "
                f"zip: {self.zip!r}, "
                f"customer_id: {self.customer_id!r}>"}
        