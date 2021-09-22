from flask_app.models.user import User
from flask_app import app
from flask import  render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


##===============================
##  Render Login/Register Page
##================================
@app.route("/")
def login_page():
    return render_template("index.html")

##================
##  Register
##================
@app.route("/register", methods=["POST"] )
def register():
    #validate user!
    if not User.vlidate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.register_user(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

##================
##  Login
##================
@app.route("/login", methods=['POST'])
def login():
    data = { 
            "email" : request.form["email"] 
        }
    user = User.get_by_email(data)
    # user is not registered in the db

    validation_data = {
        "user" : user,
        "password" : request.form['password'],
    }

    if not User.validate_login(validation_data):
        return redirect("/")

    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    # never render on a post!!!
    return redirect("/dashboard")

##=========================
##  Dashboard/ Home Page
##=========================
@app.route("/dashboard")
def home_page():
    data = {
        "user_id" : session['user_id']
    }
    user = User.get_user_info(data)
    return render_template("dashboard.html", user = user)

##=========================
##  Logout Route
##=========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")