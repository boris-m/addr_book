import unittest
from run import Application
from run import Record


class AppTest(unittest.TestCase):
    def setUp(self):
        print "setup"
        self.app=Application()
        self.test_record=Record
        self.test_record.first_name   = "TestFirstName"
        self.test_record.last_name    = "TestLastName"
        self.test_record.birthday     = "1986-12-21"
        self.test_record.phone_number = "89500305009"


    def tearDown(self):
        print "teardown"
        #self.app.__del__()

    def test_db_connection_not_none(self):
        assert self.app.db_conection is not None

    def test_find_record_not_empty(self):
        assert self.app.__db.find_record("tmp") is not None

