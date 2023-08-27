from app.extensions import db


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    def __repr__(self):
        return f'<id{self.id!r}, name {self.name!r}>'