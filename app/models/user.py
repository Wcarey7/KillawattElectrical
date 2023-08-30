from app.extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<id: {self.id!r}, username: {self.username!r}>'
