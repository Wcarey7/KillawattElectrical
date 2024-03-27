from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, event
from app import db

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.user import User


class Customer(db.Model):
    __tablename__ = "customer"
    use_mapper_versioning = True  # Creates a version_id column through the Versioned mixin.

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    related_username: Mapped[str] = mapped_column(String(255), default="System")
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    phone_numbers: Mapped[List["Telephone"]] = relationship("Telephone", back_populates="customer", cascade="all, delete-orphan")
    emails: Mapped[List["Email"]] = relationship("Email", back_populates="customer", cascade="all, delete-orphan")
    memos: Mapped[Optional[List["Memo"]]] = relationship("Memo", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<Customer id: {self.id!r}, "
                f"name: {self.name!r}>, "
                f"related_username: {self.related_username!r}>, "
                f"create_date: {self.create_date!r}> ")


class Telephone(db.Model):
    __tablename__ = "telephone"
    use_mapper_versioning = True  # Creates a version_id column through the Versioned mixin.

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(255))
    related_username: Mapped[str] = mapped_column(String(255), default="System")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="phone_numbers")

    def __repr__(self):
        return (f"<Telephone id: {self.id!r}, "
                f"phone_number: {self.phone_number!r}, "
                f"related_username: {self.related_username!r}>, "
                f"customer_id: {self.customer_id!r}>")


# Strip parentheses and dashes.
@event.listens_for(Telephone.phone_number, 'set', retval=True)
def format_phone_number(target, value, oldvalue, initiator):
    if value is not None:
        char_to_remove = ["(", ")", "-"]
        for char in char_to_remove:
            value = value.replace(char, "")
    return value


class Email(db.Model):
    __tablename__ = "email"
    use_mapper_versioning = True  # Creates a version_id column through the Versioned mixin.

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    related_username: Mapped[str] = mapped_column(String(255), default="System")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="emails")

    def __repr__(self):
        return (f"<Email id: {self.id!r}, "
                f"email: {self.email!r}, "
                f"related_username: {self.related_username!r}>, "
                f"customer_id: {self.customer_id!r}>")


class Memo(db.Model):
    __tablename__ = "memo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    memo_content: Mapped[str] = mapped_column(Text)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    related_username: Mapped[str] = mapped_column(String(255), default="System")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="memos")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="memos")

    def __repr__(self):
        return (f"<Memo id: {self.id!r}, "
                f"create_date: {self.create_date!r}, "
                f"related_username: {self.related_username!r}>, "
                f"customer_id: {self.customer_id!r}, "
                f"user_id: {self.user_id!r}, "
                f"memo_content: {self.memo_content!r}>")
