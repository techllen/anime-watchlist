from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import anime,thought,user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# this route redirect users to the register page
@app.route("/")
def home():
    # return render_template("register.html")
    return render_template("login.html")


# this route handles user registration
@app.route("/register", methods = ["POST"])
def register():
    # first thing first validate user inputs
    user_inputs = request.form
    if not user.User.validateRegister(user_inputs):
        # if any user input is invalid send the user to home page
        return redirect("/")
    else:
        #hashing passwords
        password_hash = bcrypt.generate_password_hash(request.form["password"])
        # print(password_hash)
        # dictionary to carry user input data
        user_data = {
            "username": request.form["username"],
            "email": request.form["email"],
            #assigning the password hash into the password dictionary key    
            "password": password_hash
        }
        # saving the data
        user_id = user.User.createOne(user_data)
        # assigning session to the user
        session["user_id"] = user_id
        # redirecting the user to the dashboard
        return render_template("dashboard.html")

# this route handles user login
@app.route("/login", methods = ["POST"])
def login():
    user_data = {
        "email": request.form["email"],
    }
    # validating the user
    found_user = user.User.validate_login(user_data)
    # when email is not found take the user back to the register page
    if not found_user:
        return redirect("/")
    else:
        # retrieve the user data
        user_in_db = user.User.getByEmail(user_data)
        # when password dont match take user back to the login page
        if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
            # getting the flash messages
            user.User.validate_login(user_data)
            return render_template("login.html")
        else:
            #assigning session to the user
            session["user_id"] = user_in_db.id
            # redirecting the user to the dashboard
            return render_template("dashboard.html")


# this route handles logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

