from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.utilities.history_meta import Versioned
from app import db

if TYPE_CHECKING:
    from app.models.customer import Customer


class Address(Versioned, db.Model):
    __tablename__ = "address"
    use_mapper_versioning = True  # Creates a version_id column through the Versioned mixin.

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(255))
    zip: Mapped[int] = mapped_column(Integer)
    related_username: Mapped[str] = mapped_column(String(255), default="System")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"))

    customer: Mapped["Customer"] = relationship("Customer", lazy="joined", back_populates="addresses")

    def __repr__(self):
        return (f"<Address id: {self.id!r},"
                f"street: {self.street!r}, "
                f"city: {self.city!r}, "
                f"state: {self.state!r}, "
                f"zip: {self.zip!r}, "
                f"related_username: {self.related_username!r}>, "
                f"customer_id: {self.customer_id!r}>")
