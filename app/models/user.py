from flask_login import UserMixin
from flask import current_app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app import db


class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    security_permissions = db.Column(db.String, default="Admin") # TODO: make user types(i.e. Admin, Regular)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    
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
