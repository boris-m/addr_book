import unittest
from main import Application


class AppTest(unittest.TestCase):
    def setUp(self):
        print "setup"
        self.app=Application()

    def tearDown(self):
        print "teardown"
        self.app.__del__()

    def test_db_connection_not_none(self):
        assert self.app.db_conection is not None

