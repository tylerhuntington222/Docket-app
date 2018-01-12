'''
Unit tests for user-related functionality of Docket app. Tests pertain to 
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
class UsersTests(unittest.TestCase):

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

    def create_admin(self, name, email, password):
        new_admin = User(name=name, email=email, password=password,
            role = "admin")
        db.session.add(new_admin)
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
    # test user registration
    def test_users_can_register(self):
        new_user = User("tylertarr", "tylertarr@huntington.com", 
                "tylertarrhuntington")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert(t.name == 'tylertarr')

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b"Please sign in to access your task list",
        response.data) 

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b"Invalid username or password", response.data)

    # test that users can register
    def test_users_can_login(self):

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


    # test that unregistered users can't log in
    def test_invalid_form_data(self):
        self.register("tylertarr", "tylertarr@huntington.com", 
                "tylertarrhuntington", "tylertarrhuntington")
        response = self.login("wrongusername", "tylertarrhuntington")
        self.assertIn(b'Invalid username or password', response.data)

    # test that form is present on registration page
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please register to access the task list", response.data)

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

    def test_user_login_field_errors(self):
        response = self.app.post('/',
            data = dict(name='', password='tylerhuntington'),
            follow_redirects=True)
        self.assertIn(b"This field is required", response.data)

    def test_user_default_role(self):
        db.session.add(
            User(
                "johnny",
                "johnny@appleseed.com",
                "appleseed"
            )
        )
        db.session.commit()
        users = db.session.query(User).all()
        for u in users:
            self.assertEquals(u.role, 'user')

    def test_admin_users_can_complete_tasks_they_did_not_create(self):
        self.create_user("averagejoe", "average@joe.com", "averagejoe")
        self.login("averagejoe", "averagejoe")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin("superman", "super@man.com", "superman")
        self.login("superman", "superman")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'Task successfully marked as complete', response.data)

    def test_admin_users_can_delete_tasks_they_did_not_create(self):
        self.create_user("averagejoe", "average@joe.com", "averagejoe")
        self.login("averagejoe", "averagejoe")
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin("superman", "super@man.com", "superman")
        self.login("superman", "superman")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'Task successfully removed from your Docket', 
            response.data)

    def test_task_template_displays_logged_in_user_name(self):
        self.register('william', 'william@shakespeare.com',
            'william', 'william')
        self.login('william', 'william')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b"william", response.data)























if __name__ == "__main__":
    unittest.main()
