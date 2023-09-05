from app import db
from flask import current_app
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.relationship('Address', backref='customer', cascade='all')

    __mapper_args__ = {
        "polymorphic_identity": "customer",
    }
        
    def __repr__(self):
        return f'<id: {self.id!r}, name: {self.name!r}>'