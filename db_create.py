"""
db_create.py

A script to create the SQL database for Docket, a simple task
manager application.

Tyler Huntington, 2017
"""
from views import db
from models import Task
from datetime import date

# init the database schema
db.create_all()

## insert sample data
#db.session.add(Task("Make doctor's appointment", 
#    date(2018, 1, 19), 8, 1))
#db.session.add(Task("Book train ticket to New York",
#    date(2018, 1, 15), 6, 1))

# commit the change
db.session.commit()

        
