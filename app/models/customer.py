from typing import TYPE_CHECKING
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app import db

if TYPE_CHECKING:
    from app.models.address import Address


class Customer(db.Model):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="customer", cascade="all, delete")
    phone_numbers: Mapped[List["Telephone"]] = relationship("Telephone", back_populates="customer", cascade="all, delete")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="customer", cascade="all, delete")
    
    def __repr__(self):
        return f"<Customer id: {self.id!r}, name: {self.name!r}>"


class Telephone(db.Model):
    __tablename__ = "telephone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[int] = mapped_column(Integer)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    
    customer: Mapped["Customer"] = relationship("Customer", back_populates="phone_numbers")

    def __repr__(self):
        return f"<Telephone id: {self.id!r}, phone_number: {self.phone_number!r}, customer_id: {self.customer_id!r}>"


class Email(db.Model):
    __tablename__ = "email"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    
    customer: Mapped["Customer"] = relationship("Customer", back_populates="emails")

    def __repr__(self):
        return f"<Email id: {self.id!r}, email: {self.email!r}, customer_id: {self.customer_id!r}>"
    