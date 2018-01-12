"""
views.py

Main controller for Docket, a simple task management web app.

Tyler Huntington, 2018
"""
# imports
import datetime
from forms import AddTaskForm, RegisterForm, LoginForm
from functools import wraps
from flask import Flask, flash, redirect, url_for, session, \
        request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# configuration
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User


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
            return(redirect(url_for('login')))

    return wrap

# route handlers
@app.route('/', methods = ['GET', 'POST'])
def login():
    
    # init error message var
    error = None
    
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                flash('Welcome, {}!'.format(user.name))
                return(redirect(url_for('tasks')))
            else:
                error = "Invalid username or password."
    return(render_template("login.html", form=form, error=error))

@app.route('/logout/')
@login_required
def logout():

    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash("Successfully logged out.")
    return redirect(url_for('login'))


@app.route("/tasks/", methods = ['GET', 'POST'])
@login_required
def tasks():

    return render_template(
            'tasks.html',
            form=AddTaskForm(request.form),
            open_tasks=open_tasks(),
            closed_tasks=closed_tasks(),
            )

"""
new_task()

Function for allowing user to manually add a new task to their
Docket.

"""
@app.route('/add/', methods = ['GET', 'POST'])
@login_required
def new_task():
    error = None
    
    # fetch the form data submitted with request
    form = AddTaskForm(request.form)

    if request.method=='POST':
        if form.validate_on_submit():
            new_task = Task(form.name.data, 
                    form.due_date.data,
                    form.priority.data,
                    datetime.datetime.utcnow(),
                    '1',
                    session['user_id']
            )
            db.session.add(new_task)
            db.session.commit()
            flash("New task successfully added to your Docket")

    # handler for GET request and invalid form entries
    return(render_template('tasks.html', 
        form=form, 
        error=error, 
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()))

    
"""
complete()

Function for marking a task as complete.

Args:
    task_id: the unique task_id of the task to be marked as \
            complete

Returns:
    redirects to user's task page

"""
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)

    # verify that user created the task they are attempting to mark complete
    if (session['user_id'] == task.first().user_id or 
            session['role'] == 'admin'):
        db.session.query(Task).filter_by(task_id=new_id) \
            .update({"status": "0"})
        db.session.commit()
        flash("Task successfully marked as complete!")
        return(redirect(url_for('tasks')))

    # handle case that user tries to complete a task they did not create
    else:
        flash("You can only update tasks that you created.")
        return(redirect(url_for('tasks')))


"""
delete(task_id)

Function for removing a task from the user's Docket.

Args:
    task_id: the unique ID of the task to be removed

Returns:
    redirects to user's task page
"""
@app.route('/delete/<int:task_id>/', \
        methods = ['GET', 'POST'])
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if (session["user_id"] == task.first().user_id or
            session['role'] == 'admin'):

        # find task to delete and remove it from table
        db.session.query(Task).filter_by(task_id=task_id) \
            .delete()
        db.session.commit()
        flash("Task successfully removed from your Docket")
        return(redirect(url_for('tasks')))

    else:
        flash("You can only delete tasks that you created")
        return(redirect(url_for('tasks')))
        

@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None

    # get the user registration form data
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                    form.name.data,
                    form.email.data,
                    form.password.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering, please log in.')

                return(redirect(url_for('login')))
            except(IntegrityError):
                error = "That username and/or email already exists."
                return(render_template('register.html', form=form, error=error))

    # if form entry not valid, redirect to registration page
    return render_template('register.html', 
            form=form,
            error=error)


# Error handling for form validation exceptions
def flash_errors(form):
    for field, error in form.errors.items():
        for error in errors:
            flash("uError in the {0}, field - {1}".format(
                getattr(form, field).label.text, error), 'error')

    


"""
open_tasks()

Helper function for retrieving open tasks.
"""
def open_tasks():
    return db.session.query(Task).filter_by(
            status='1').order_by(Task.due_date.asc())

"""
closed_tasks()

Helper function for retrieving closed tasks.
"""
def closed_tasks():
    return db.session.query(Task).filter_by(
            status='0').order_by(Task.due_date.asc())
