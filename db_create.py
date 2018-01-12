"""
db_create.py

A script to create the SQL database for Docket, a simple task
manager application.

Tyler Huntington, 2017
"""

# imports
from datetime import date

from project import db
from project.models import Task, User

# create the database and the db table
db.create_all()

# insert data
db.session.add(
        User("admin", "ad@min.com", "admin", "admin")
)
db.session.add(
        Task("Walk the dogs", date(2018, 1, 28), 10, 
            date(2018, 1, 12), 1, 1)
)
db.session.add(
        Task("Go grocery shopping", date(2018, 1, 20), 10,
            date(2018, 1, 12), 1, 1)
)

# commit the changes
db.session.commit()

        
