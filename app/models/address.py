from app.extensions import db


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
        return f'<id: {self.id!r}, street: {self.street!r}, city: {self.city!r}, state: {self.state!r}, zip: {self.zip!r}, customer_id: {self.customer_id!r}>'