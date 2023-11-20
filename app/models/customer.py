import os
from typing import TYPE_CHECKING
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Index
from app import db

if TYPE_CHECKING:
    from app.models.address import Address


class Customer(db.Model):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="customer", cascade="all, delete")
    phone_numbers: Mapped[List["Telephone"]] = relationship("Telephone", back_populates="customer", cascade="all, delete")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="customer", cascade="all, delete")

    db_uri = os.environ.get('DATABASE_URI')
    if db_uri is not None and "mysql" in db_uri.lower():
        Index('ix_name', name, mysql_prefix = 'FULLTEXT')

    def __repr__(self):
        return f"<Customer id: {self.id!r}, name: {self.name!r}>"


class Telephone(db.Model):
    __tablename__ = "telephone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(255))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="phone_numbers")

    def __repr__(self):
        return f"<Telephone id: {self.id!r}, phone_number: {self.phone_number!r}, customer_id: {self.customer_id!r}>"

    # Strip paranthesis and dashes.
    def format_set_phone_number(self, phone_num):
        char_to_remove = ["(", ")", "-"]
        for char in char_to_remove:
            phone_num = phone_num.replace(char, "")
        self.phone_number = phone_num


class Email(db.Model):
    __tablename__ = "email"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="emails")

    db_uri = os.environ.get('DATABASE_URI')
    if db_uri is not None and "mysql" in db_uri.lower():
        Index('ix_email', email, mysql_prefix = 'FULLTEXT')

    def __repr__(self):
        return f"<Email id: {self.id!r}, email: {self.email!r}, customer_id: {self.customer_id!r}>"
