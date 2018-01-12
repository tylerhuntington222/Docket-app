
# imports
import datetime
from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint

from .forms import AddTaskForm
from project import db
from project.models import Task

# config
tasks_blueprint = Blueprint('tasks', __name__)

# helper functions
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

"""
open_tasks()

Helper function for retrieving uncompleted tasks.
"""
def open_tasks():
    return db.session.query(Task).filter_by(
            status='1').order_by(Task.due_date.asc())

"""
closed_tasks()

Helper function for retrieving completed tasks.
"""
def closed_tasks():
    return db.session.query(Task).filter_by(
            status='0').order_by(Task.due_date.asc())


# routes
@tasks_blueprint.route("/tasks/", methods = ['GET', 'POST'])
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
@tasks_blueprint.route('/add/', methods = ['GET', 'POST'])
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
@tasks_blueprint.route('/complete/<int:task_id>/')
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
        return(redirect(url_for('tasks.tasks')))

    # handle case that user tries to complete a task they did not create
    else:
        flash("You can only update tasks that you created.")
        return(redirect(url_for('tasks.tasks')))


"""
delete(task_id)

Function for removing a task from the user's Docket.

Args:
    task_id: the unique ID of the task to be removed

Returns:
    redirects to user's task page
"""
@tasks_blueprint.route('/delete/<int:task_id>/', \
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
        return(redirect(url_for('tasks.tasks')))

    else:
        flash("You can only delete tasks that you created")
        return(redirect(url_for('tasks.tasks')))
        
