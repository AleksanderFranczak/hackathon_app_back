from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')

#! Index route for testing purposes 
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    pass


#! route for login -> return json [status] = logged
@app.route("/login", methods=["POST"])
def login():
    data = request.form.get("email"), request.form.get("password")
    return jsonify(data)


if __name__ == "__main__":
    app.run()