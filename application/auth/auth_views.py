from __future__ import print_function
from flask import request, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from application import app, db
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

    #check if user with such password exists
    user = User.query.filter_by(username = login_form.username.data, password = login_form.password.data).first()

    if(not user):
        err = {'Error':['Username or password incorrect']}
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
    user = User(reg_form.username.data, reg_form.password.data)

    print(user)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth_login"))
