import unittest
from RemuApp import RemuApp
from unittest.mock import Mock
from Domain.Master import Master


class TestRemuAppMethods(unittest.TestCase):


    def setUp(self):
        self.app=RemuApp()

    def tearDown(self):
        if self.app.servicemode:
            self.app.servicemode.close_all_connections()
        self.app.close_connections()

    def test_setMaster(self):
        #self.assertFalse(self.app.isMaster)
        #self.app.set_master(Mock(Master))
        #self.assertEquals(self.app.isMaster, True)

        self.assertFalse(self.app.isMaster)
        self.app.set_servicemode(Mock(Master), True)
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


