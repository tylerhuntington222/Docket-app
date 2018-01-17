"""
db_create.py

A script to create the SQL database for Docket, a simple task
manager application.

Tyler Huntington, 2017
"""

# imports
from project import db

# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()

        
