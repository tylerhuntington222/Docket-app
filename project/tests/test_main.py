'''
project/test_main.py

A testing suite for app error handling functions.

Tyler Huntington, 2018
'''

import os
import unittest

from project import app, db
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'


class MainTests(unittest.TestCase):

    #------SETUP AND TEARDOWN------#

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #------HELPER METHODS------#
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name,password=password),
            follow_redirects=True)

    #------TESTS------#
    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exist/')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Sorry, there\'s nothing here.", response.data)

    def test_500_error(self):
        bad_user = User(
                name='tylertarr',
                email='tyler@tarr.com',
                password='huntington'
        )
        db.session.add(bad_user)
        db.session.commit()
        
        try:
            response = self.login('tylertarr', 'huntington')
            self.assertEquals(response.status_code, 500)
            self.assertNotIn(b"ValueError: Invalid salt", response.data)
            self.assertIn(b"Something went terribly wrong.", response.data)
        except(ValueError):
            pass


    if __name__ == "__main__":
        unittest.main()
