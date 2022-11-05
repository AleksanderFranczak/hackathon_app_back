from flask import Flask, render_template, request, Response, session
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt



# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.secret_key='supersecret9u32ujfwdnfn2iokey'

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
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    status = db.Column(db.Boolean)
    picture = db.Column(db.BLOB)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    modification_date = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)


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


def login_user(**kwargs):
    try:
        user=Users.query.limit(1).all()
        print(user is None)
    except Exception:
        return Response(status=400)
    if kwargs["password"] == user.password:
        return user
    else:
        return Response(status=400)

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
    email = request.form["email"]
    password= request.form["password"]
    data_dict = {"email": email, "password": password}
    
    db_res = login_user(**data_dict)
    session['user']=db_res
    """try:
        if False:
            data_dict["status"] = "granted"
        else:
            data_dict["status"] = "denied"
    except Exception:
        return Response(status=400)"""
    
    return Response(response=json.dumps([data_dict]), status=200, mimetype='application/json')


def add_product_to_db(json_data):
    print(json_data)
    try:
        if "supplier_id" not in json_data:
            json_data["supplier_id"] = "0"
        new_product = Items(**json_data)
        db.session.add(new_product)
        db.session.commit()
    except Exception as err:
        raise err
    return 1


@app.route("/add-item", methods=["POST"])
def add_item():
    data = request.get_json()
    # if "location" not in data:
    #     data["location"] = "Brak"
    db_res = add_product_to_db(data)
    if db_res == 1:
        return Response(status=200)
    elif not db_res == 0:
        return Response(status=400)


if __name__ == "__main__":
    app.run()