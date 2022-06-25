from flask_app import app
from flask import render_template,redirect,session,request
# from flask_app.models import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# this route redirect users to the index/home page
@app.route("/")
def home():
    # return render_template("registration.html")
    pass