from datetime import datetime

class Address(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    city=db.Column(db.String(50))
    postal_code=db.Column(db.String(7))
    street=db.Column(db.String(50))
    country=db.Column(db.String(50))
    home_nr=db.Column(db.Integer)
    local_nr=db.Column(db.Integer)
    users=db.relationship('Users', backref='address',lazy=True)
    suppliers=db.relationship('Suppliers', backref='address',lazy=True)

class Categories(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    items = db.relationship('Items', backref = 'categories', lazy = True)

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    picture = db.Column(db.Blob)
    description = db.Column(db.String(20))
    nr_phone = db.Column(db.Integer(15), unique=True)
    address_id=db.Column(db.Integer, db.ForeignKey('address.id'),nullable=False)
    items=db.relationship('Items', backref='users',lazy=True)
    
class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nr_phone = db.Column(db.Integer(15), unique=True)
    email = db.Column(db.String(50))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable = False)
    item=db.relationship('Items', backref='suppliers',lazy=True)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    status = db.Column(db.Boolean)
    picture = db.Column(db.Blob)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    modification_date = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
