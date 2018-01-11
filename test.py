'''
Unit tests for Docker app.
'''

import unittest
import os

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

'''
Test suite for setup and takedown.
'''
class AllTests(unittest.TestCase):

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

    # test user creation
    def test_user_setup(self):
        new_user = User("tylertarr", "tylertarr@huntington.com", "tylertarrhuntington")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert(t.name == 'tylertarr')
    
    # test that unregistered users can't log in
    def test_invalid_form_data(self):
        self.register("tylertarr", "tylertarr@huntington.com", "tylertarrhuntington", "tylertarrhuntington")
        response = self.login("wrongusername", "tylertarrhuntington")
        self.assertIn(b'Invalid username or password', response.data)

    # test that form is present on registration page
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register to access the task list", response.data)

    # test that users can register
    def test_users_can_register_and_login(self):

        # first check that registration works
        self.app.get("register/", follow_redirects=True)
        response = self.register(name="tylertarr",
                email="tylertarr@huntington.com",
                password="tylertarrhuntington",
                confirm="tylertarrhuntington")
        self.assertIn(b'Thanks for registering, please log in.', response.data)
        
        # now check that login works
        response = self.login("tylertarr", "tylertarrhuntington")
        self.assertIn(b"Welcome", response.data)

    # test that user registration error thrown when duplicate username used
    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register(name='tylertarr', email='tylertarr@huntington.com', 
                password='tylertarrhuntington', confirm='tylertarrhuntington')
        self.app.get('register/', follow_redirects=True)
        response = self.register(name='tylertarr', email='tylertarr@huntington.com', 
                password='tylertarrhuntington', confirm='tylertarrhuntington')
        self.assertIn(b'That username and/or email already exist', response.data)

    # test that logged in users can log out
    def test_logged_in_users_can_log_out(self):
        self.register("tylertarr", "tylertarr@huntington.com", 
                "tylertarrhuntington", "tylertarrhuntington")
        self.login(name="tylertarr", password="tylertarrhuntington")
        response = self.logout()
        self.assertIn(b"Successfully logged out", response.data)

    # test that non-logged in users can't logout
    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b"Successfully logged out", response.data)

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


        





if (__name__ == '__main__'): 
    unittest.main()
