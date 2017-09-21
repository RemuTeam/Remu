import unittest
from RemuApp import RemuApp


class TestRemuAppMethods(unittest.TestCase):


    def setUp(self):
        self.app=RemuApp()

    def test_setMaster(self):

        self.assertFalse(self.app.isMaster)
        self.app.set_master()
        self.assertEquals(self.app.isMaster, True)

    def test_setSlave(self):
        self.app.set_master()
        self.assertEquals(self.app.isMaster, True)
        self.app.set_slave()
        self.assertFalse(self.app.isMaster)
        self.assertNotEquals(self.app.master,None)


    def test_addSlave(self):

        self.assertEquals(self.app.slaves, None)
        self.app.add_slave('127.0.0.1')
        self.assertNotEquals(self.app.slaves, None)

