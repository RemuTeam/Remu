import unittest
from RemuApp import RemuApp


class TestRemuAppMethods(unittest.TestCase):


    def setUp(self):
        self.app=RemuApp()

    def tearDown(self):
        if self.app.master:
            self.app.master.stop_listening()

    def test_setMaster(self):

        self.assertFalse(self.app.isMaster)
        self.app.set_master()
        self.assertEquals(self.app.isMaster, True)

    """
    def test_setSlave(self):
        self.app.set_master()
        self.assertEquals(self.app.isMaster, True)
        self.app.set_slave()
        self.assertFalse(self.app.isMaster)
        #self.assertNotEquals(self.app.master,None)
        self.app.close_connections()
    """


