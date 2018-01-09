"""
forms.py

A module containing class definition for the AddTaskForm() class 
which creates a form for adding new tasks to a user's Docket.

Tyler Huntington, 2018
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, \
        SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

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

class RegisterForm(Form):
    name = StringField(
            'Username',
            validators=[DataRequired()]
    )
    
    password = PasswordField(
            'Password',
            validators=[DataRequired(), Length(min=6, max=40)]
    )
    
    confirm = PasswordField(
            'Confirm Password',
            validators=[DataRequired(), EqualTo('password', 
                message='Passwords must match')]
    )

    email = StringField(
            'Email',
            validators=[DataRequired()]
    )

class LoginForm(Form):
    name = StringField('Username', validators=[DataRequired()])
    password = StringField('Password',
            validators=[DataRequired()])



        


