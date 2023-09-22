from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app import db

if TYPE_CHECKING:
    from app.models.customer import Customer


class Address(db.Model):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    zip: Mapped[int] = mapped_column(Integer)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))

    customer: Mapped["Customer"] = relationship("Customer", lazy="joined", back_populates="addresses")

    def __repr__(self):
        return (f"<Address id: {self.id!r},"
                f"street: {self.street!r}, "
                f"city: {self.city!r}, "
                f"state: {self.state!r}, "
                f"zip: {self.zip!r}, "
                f"customer_id: {self.customer_id!r}>")
