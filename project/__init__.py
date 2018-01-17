'''
project/__init__.py

Main controller for integrating blueprints of Docket app.

Tyler Huntington, 2018
'''

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# import blueprints
from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)

# error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
