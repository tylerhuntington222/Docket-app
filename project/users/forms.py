"""
forms.py

A module containing class definitions for the RegisterForm 
and LoginForm classes used in the Docket app.

Tyler Huntington, 2018
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, \
        SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm(Form):
    name = StringField(
            'Username',
            validators=[DataRequired(), Length(min=6, max=25)]
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
            validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )

class LoginForm(Form):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
            validators=[DataRequired()])



        


