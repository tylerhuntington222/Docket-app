'''
Unit tests for task-related functionality of Docket app. Tests pertain to 
the `tasks` blueprint.
'''

import unittest
import os

from project import app, db
from project._config import basedir
from project.models import User, Task

TEST_DB = 'test.db'

'''
Test suite for setup and takedown.
'''
class TasksTests(unittest.TestCase):

    #-------------------------------------------------------------------------#
    '''
    HELPER METHODS FOR TESTS
    '''
    #-------------------------------------------------------------------------#
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(
                basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # helper method to attempt login
    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), 
                follow_redirects=True)

    # helper method to register a user
    def register(self, name, email, password, confirm):
        return self.app.post('register/', 
                data=dict(name=name,
                    email=email,
                    password=password,
                    confirm=confirm),
                follow_redirects=True)

    # helper method to perform logout
    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    # helper method to create a user
    def create_user(self, name, email, password):
        new_user=User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    # helper function to create a new task
    def create_task(self):
        return self.app.post('add/', 
                data=dict(name="Go to the bank",
                    due_date="1/23/2018",
                    priority='4',
                    status='1'),
                follow_redirects=True)

        
    #-------------------------------------------------------------------------#
    '''
    TESTS
    '''
    #-------------------------------------------------------------------------#
    # test that logged in users can view tasks
    def test_logged_in_users_can_view_tasks(self):
        self.register("tylertarr", "tyler@tarr.com",
                "tylerhuntington", "tylerhuntington")
        response = self.login("tylertarr", "tylerhuntington")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a new task:", response.data)

    # test that not logged in users cannot access tasks page
    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b"You need to log in first", response.data)

    # test that users can add tasks
    def test_users_can_add_tasks(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New task successfully added to your Docket',
                response.data)

    # test that users cannot add tasks when there is an error
    def test_users_cannot_add_tasks_when_error(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name="Go to the grocery store",
            due_date=' ',
            priority='4',
            status='1'),
            follow_redirects=True)
        self.assertIn(b'This field is required', response.data)

    # test that users can complete tasks
    def test_users_can_complete_tasks(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'Task successfully marked as complete', response.data)

    # test that users can delete tasks
    def test_users_can_delete_tasks(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b"Task successfully removed", response.data)

    # test that users cannot complete tasks that they did not create
    def test_users_cannot_complete_tasks_they_did_not_create(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user("tessajo", "tessa@jo.com", "tessasternberg")    
        self.login("tessajo", "tessasternberg")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'Task successfully marked as complete', 
                response.data)
        self.assertIn(b"You can only update tasks that you created", 
            response.data)

   # test that users cannot delete tasks that they did not create
    def test_users_cannot_delete_tasks_they_did_not_create(self):
        self.create_user("tylertarr", "tyler@tarr.com", "tylerhuntington")    
        self.login("tylertarr", "tylerhuntington")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user("tessajo", "tessa@jo.com", "tessasternberg")    
        self.login("tessajo", "tessasternberg")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'Task successfully removed', 
                response.data)


        





        

        


        





if (__name__ == '__main__'): 
    unittest.main()
