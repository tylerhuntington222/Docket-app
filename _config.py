import os

# get the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

# configure app vars
DATABASE = 'docket.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'myprecious'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# define the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
