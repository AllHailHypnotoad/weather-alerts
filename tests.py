from weather_app import db
from weather_app.models import *
import datetime
import unittest


class TestCase(unittest.TestCase):

        def setUp(self):
            '''
            Need to modify the setup so that it points to  a testing database rather
            then the dev database
            '''
            db.create_all()

        def test_input_data(self):
            u1 = User(name="Paul", email="paul.andy.young@gmail.com", 
                password="password", fs_access_token='asdfasdfasdwegdfg')
            db.session.add(u1)
            db.session.commit()
            print "*****Data has been committed to DB*****"
        
        def test_query1(self):
            user1 = User.query.filter_by(name='Paul').first()
            print "User Name: ", user1.name, "User Email: ", user1.email

        def tearDown(self):
            db.session.remove()



if __name__ == '__main__':
    unittest.main()
