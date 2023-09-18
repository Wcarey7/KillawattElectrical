from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    security_permissions: Mapped[str] = mapped_column(String, default="Admin") # TODO: make user types(i.e. Admin, Regular)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    
    def __repr__(self):
        return (f"<User id: {self.id!r}, "
                f"username: {self.username!r}, "
                f"email: {self.email!r}, "
                f"security_permissions: {self.security_permissions}, "
                f"create_date: {self.create_date!r}>" )

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
