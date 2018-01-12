'''
project/__init__.py

Main controller for integrating blueprints of Docket app.

Tyler Huntington, 2018
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config = config.from_pyfile('_config.py')
db = SQLAlchemy(app)

# import blueprints
from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)


