from flask import current_app
from datetime import datetime
from app import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    addresses = db.relationship('Address', back_populates='customers')
    phoneNum = db.relationship('Telephone', back_populates='customers')
    email = db.relationship('Email', back_populates='customers')
    
    __mapper_args__ = {
        "polymorphic_identity": "customer",
    }
        
    def __repr__(self):
        return f'<id: {self.id!r}, name: {self.name!r}>'


class Telephone(db.Model):
    __tablename__ = 'telephone'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customers = db.relationship('Customer', back_populates='phoneNum')

    def __repr__(self):
        return f'<id: {self.id!r}, phoneNumber: {self.phoneNumber!r}, customer_id: {self.customer_id!r}>'


class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customers = db.relationship('Customer', back_populates='email')

    def __repr__(self):
        return f'<id: {self.id!r}, email: {self.email!r}, customer_id: {self.customer_id!r}>'
    