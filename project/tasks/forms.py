"""
project/tasks/forms.py

A module containing class definition for the AddTaskForm() class 
which creates a form for adding new tasks to a user's Docket.

Tyler Huntington, 2018
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, \
        SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddTaskForm(Form):
    task_id = IntegerField()
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateField('Due Date (mm/dd/yyyy)', \
            validators=[DataRequired()], format='%m/%d/%Y')
    priority = SelectField(
            'Priority',
            validators=[DataRequired()],
            choices=[('1', '1'), ('2', '2'), ('3', '3'),
                ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                ('8', '8'), ('9', '9'), ('10', '10')
            ]
    )
    status = IntegerField('Status')


        


