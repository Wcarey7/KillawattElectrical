from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, event
from app import db

if TYPE_CHECKING:
    from app.models.address import Address


class Customer(db.Model):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    phone_numbers: Mapped[List["Telephone"]] = relationship("Telephone", back_populates="customer", cascade="all, delete-orphan")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer id: {self.id!r}, name: {self.name!r}>"


class Telephone(db.Model):
    __tablename__ = "telephone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(255))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="phone_numbers")

    def __repr__(self):
        return f"<Telephone id: {self.id!r}, phone_number: {self.phone_number!r}, customer_id: {self.customer_id!r}>"


class Email(db.Model):
    __tablename__ = "email"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="emails")

    def __repr__(self):
        return f"<Email id: {self.id!r}, email: {self.email!r}, customer_id: {self.customer_id!r}>"


# Strip paranthesis and dashes.
@event.listens_for(Telephone.phone_number, 'set', retval=True)
def format_phone_number(target, value, oldvalue, initiator):
    if value is not None:
        char_to_remove = ["(", ")", "-"]
        for char in char_to_remove:
            value = value.replace(char, "")
    return value
