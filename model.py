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

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    address_id=db.Column(db.Integer, db.ForeignKey('address.id'),nullable=False)
    items=db.relationship('Items', backref='users',lazy=True)
    