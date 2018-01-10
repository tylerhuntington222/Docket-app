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

    # test user creation
    def test_user_setup(self):
        new_user = User("michael", "michael@herman.com", "michaelherman")
        db.session.add(new_user)
        db.session.commit()

        test = db.session.query(User).all()
        for t in test:
            t.name
        assert(t.name == 'michael')



if (__name__ == '__main__'): 
    unittest.main()
