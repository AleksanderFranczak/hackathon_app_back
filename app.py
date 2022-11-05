from flask import Flask, render_template, request, Response
from db import init_databse, user_in_db, add_user_to_db
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# app = Flask(__name__)
# app.config.from_object('config.DevelopmentConfig')
# db = SQLAlchemy()

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
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
    email=db.Column(db.String(50))
    password=db.Column(db.String(50))
    address_id=db.Column(db.Integer, db.ForeignKey('address.id'),nullable=False)
    items=db.relationship('Items', backref='users',lazy=True)
    
class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
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
    # picture = db.Column(db.Blob)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    modification_date = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


with app.app_context():
    db.create_all()

# try:
#     res = init_databse()
#     if res:
#         raise Exception("Database is not created properly")
# except Exception:
#     raise Exception("Database is not created properly")


#! Index route for testing purposes 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    
    # Getting data from front-end form
    data = request.form.get("email"), request.form.get("password")

    #Adding user to databse
    try:
        add_user_to_db(*data)
    except Exception:
        return Response(status=400)
    
    data_dict = {"email": data[0], "password": data[1], "status": "registered"}
    return Response(response=json.dumps(data_dict), status=200, mimetype='application/json')




#! route for login -> return json [status] = logged
@app.route("/login", methods=["POST"])
def login():
    data = request.form.get("email"), request.form.get("password")
    data_dict = {"email": data[0], "password": data[1]}
    
    try:
        if user_in_db(*data):
            data_dict["status"] = "granted"
        else:
            data_dict["status"] = "denied"
    except Exception:
        return Response(status=400)
    
    return Response(response=json.dumps([data_dict]), status=200, mimetype='application/json')



if __name__ == "__main__":
    app.run()