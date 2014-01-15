from database import init_db, db_session
from models import *
import datetime
import unittest


class TestCase(unittest.TestCase):

        def setUp(self):
            '''
            Need to modify the setup so that it points to  a testing database rather
            then the dev database
            '''
            init_db()

        def test_input_data(self):
            print db_session.bind
            u1 = User(name="Paul", email="paul.andy.young@gmail.com", 
                password="password")
            db_session.add(u1)
            db_session.commit()
            print "*****Data has been committed to DB*****"
        
        def test_query1(self):
            user1 = db_session.query(User).filter_by(name='Paul').first()
            print "User Name: ", user1.name, "User Email: ", user1.email

        def tearDown(self):
            db_session.remove()



if __name__ == '__main__':
    unittest.main()