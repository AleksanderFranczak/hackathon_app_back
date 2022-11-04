from flask import Flask, render_template, request, jsonify, Response
from db import init_databse, user_in_db, add_user_to_db
import json

def init():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    try:
        res = init_databse()
        if res:
            raise Exception("Database is not created properly")
    except Exception:
        raise Exception("Database is not created properly")
    return app

app = init()

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