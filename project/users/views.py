"""
views.py

Controller for users blueprint of Docket app. Manages 
control flow for all user-related functionality of the app.

Tyler Huntington, 2018
"""
# imports
import datetime
from .forms import RegisterForm, LoginForm
from functools import wraps
from flask import Flask, flash, redirect, url_for, session, \
        request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from project import db, bcrypt
from project.models import User

# configuration
users_blueprint = Blueprint('users', __name__)


# helper functions

"""
login_required(test)

A wrapper function for checking whether the user is logged in
to their account.

Args:
    test: function that should only be called if the
    user is logged in.

Returns:
    if user is logged in, returns 'test' function passed as
    an argument.

    if user is not logged in, redirects to login page
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):

        if ('logged_in' in session):
            return(test(*args, **kwargs))

        else:
            flash("You need to log in first")
            return(redirect(url_for('users.login')))

    return wrap


# route handlers
@users_blueprint.route('/', methods = ['GET', 'POST'])
def login():
    
    # init error message var
    error = None

    # init logged_in variable for this session
    session["logged_in"] = None
    
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if (user is not None and bcrypt.check_password_hash(
                user.password, request.form['password'])):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash('Welcome, {}!'.format(user.name))
                return(redirect(url_for('tasks.tasks')))
            else:
                error = "Invalid username or password."

    # log out user if previously logged in
    if session['logged_in']:
        session.pop('logged_in', None)
   
    return(render_template("login.html", form=form, error=error))

@users_blueprint.route('/logout/')
@login_required
def logout():

    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    flash("Successfully logged out.")
    return redirect(url_for('users.login'))


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None

    # get the user registration form data
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                    form.name.data,
                    form.email.data,
                    bcrypt.generate_password_hash(form.password.data)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering, please log in.')

                return(redirect(url_for('users.login')))
            except(IntegrityError):
                error = "That username and/or email already exists."
                return(render_template('register.html', form=form, error=error))

    # if form entry not valid, redirect to registration page
    return render_template('register.html', 
            form=form,
            error=error)





