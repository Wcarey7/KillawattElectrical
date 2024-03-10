from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, event, CheckConstraint
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    security_permissions: Mapped[str] = mapped_column(String(255), default="Admin")
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint(
            security_permissions.in_(["Admin", "Regular User"]),
            name='check_valid_security_permissions'
        ),
    )

    def __repr__(self):
        return (f"<User id: {self.id!r}, "
                f"username: {self.username!r}, "
                f"email: {self.email!r}, "
                f"security_permissions: {self.security_permissions}, "
                f"create_date: {self.create_date!r}>")

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Attribute event to trigger password hashing.
@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value
