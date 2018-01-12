
from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

#with sqlite3.connect(DATABASE_PATH) as con:
#
#    # get cursor from db
#    c = con.cursor()
#
#    # temporarily change the name of tasks table
#    c.execute("""ALTER TABLE tasks RENAME TO old_tasks""")
#
#    # re-create a new tasks table with new schema
#    db.create_all()
#
#    # retrieve data from old tasks table
#    c.execute("""SELECT name, due_date, priority, status FROM old_tasks \
#            ORDER BY task_id ASC""")
#
#    # save all rows as a list of tuples; set posted date to current time and user_id to 1
#    data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]
#
#    # insert data into tasks folder
#    c.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, \
#            user_id) VALUES(?, ?, ?, ?, ?, ?)""", data)
#
#    # delete old tasks table
#    c.execute("""DROP TABLE old_tasks""")
#

with sqlite3.connect(DATABASE_PATH) as con:

    # get cursor
    c = con.cursor()

    # temporarily change the name of the users table
    c.execute("""ALTER TABLE users RENAME TO old_users""")

    # re-create new users table with updated schema
    db.create_all()

    # retrieve data from old users table
    c.execute("""SELECT name, email, password FROM old_users \
            ORDER BY id ASC""")

    # save all rows as a list of tuples and set role to user
    data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

    # insert data into users table
    c.executemany("""INSERT INTO users (name, email, password, role) \
            VALUES(?, ?, ?, ?)""", data)

    # delete old users table
    c.execute("""DROP TABLE old_users""")

















