from flask import request, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from application import app, db, bcrypt
from application.auth.auth_models import User
from application.auth.auth_forms import RegForm,LoginForm
import sys

#login screen and authentication
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    #if GET direct to login page
    if(request.method == "GET"):
        login_form = LoginForm()

        return render_template("auth/login.html",login_form = login_form)

    login_form = LoginForm(request.form)

    #validate that field imputs correct
    if(not login_form.validate()):
        err = login_form.errors
        return render_template("auth/login.html", login_form = login_form, err = err)

    #check if user with such username
    user = User.query.filter_by(username = login_form.username.data).first()

    if(not user):
        err = {'Error':['Username not found']}
        return render_template("auth/login.html", login_form = login_form, err = err)

    #check if password is correct
    if(not bcrypt.check_password_hash(user.password, login_form.password.data)):
        err = {'Error':['Incorrect password']}
        return render_template("auth/login.html", login_form = login_form, err = err)

    #if yes log user in
    login_user(user)

    return redirect(url_for("thread_index"))

#logout
@app.route("/auth/logout")
@login_required
def auth_logout():
    logout_user()

    return redirect(url_for("thread_index")) 

#registration screen and new user creation
@app.route("/auth/register", methods = ["GET","POST"])
def auth_reg():

    #if post return registration page
    if(request.method == "GET"):
        reg_form = RegForm()

        return render_template("auth/register.html", reg_form = reg_form)

    #else query registration form
    reg_form = RegForm(request.form)

    if(not reg_form.validate()):
        err = reg_form.errors

        return render_template("auth/register.html", reg_form = reg_form, err = err)

    #create user and commit to db
    user = User(reg_form.username.data, bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8'))

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth_login"))
