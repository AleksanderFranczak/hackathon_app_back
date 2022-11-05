from flask import Flask, render_template, request, Response
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["DEVELOPMENT"] = True
app.config["DEBUG"] = True
# initialize the app with the extension
db.init_app(app)


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
    surrname = db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    # picture = db.Column(db.Blob)
    description = db.Column(db.String(20))
    nr_phone = db.Column(db.Integer, unique=True)
    address_id=db.Column(db.Integer, db.ForeignKey('address.id'),nullable=False)
    # items=db.relationship('Items', backref='users',lazy=True)
    
class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surrname = db.Column(db.String(50))
    nr_phone = db.Column(db.Integer, unique=True)
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
    picture = db.Column(db.BLOB)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    modification_date = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


with app.app_context():
    db.create_all()

def add_user_to_db(**kwargs):
    hash = sha256_crypt.encrypt(kwargs.get("password"))
    kwargs["password"] = hash
    try:
        user = Users(**kwargs)
        db.session.add(user)
        db.session.commit()
    except Exception:
        return 0
    return 1

#! Index route for testing purposes 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    
    # Getting data from front-end form
    data = request.form

    #Adding user to databse
    db_res = add_user_to_db(**data)
    if db_res == 1:
        data_dict = {"status": "registered"}
        return Response(response=json.dumps(data_dict), status=200, mimetype='application/json')
    elif db_res == 0:
        return Response(status=400)


#! route for login -> return json [status] = logged
@app.route("/login", methods=["POST"])
def login():
    data = request.form.get("email"), request.form.get("password")
    data_dict = {"email": data[0], "password": data[1]}
    
    try:
        if False:
            data_dict["status"] = "granted"
        else:
            data_dict["status"] = "denied"
    except Exception:
        return Response(status=400)
    
    return Response(response=json.dumps([data_dict]), status=200, mimetype='application/json')



if __name__ == "__main__":
    app.run()