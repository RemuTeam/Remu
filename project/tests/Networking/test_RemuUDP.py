import unittest
import time
from Networking.RemuUDP import MasterUDPListener
from Networking.RemuUDP import Beacon
from unittest.mock import Mock
from Domain.Master import Master

class TestRemuUDPMethods(unittest.TestCase):

    def setUp(self):
        self.beacon = Beacon()
        self.master_chef = MasterUDPListener(Mock(Master))

    def tearDown(self):
        self.beacon.stop_beaconing()
        self.master_chef.stop_listening_to_beacons()

    def test_init_slave(self):
        self.assertIsNone(self.beacon.transport)

    def test_slave_start_beaconing(self):
        self.beacon.start_beaconing()
        self.assertIsNotNone(self.beacon.transport)

    def test_init_master(self):
        self.assertIsNone(self.master_chef.transport)
        self.assertIsNone(self.master_chef.protocol)

    def test_master_starts_listening(self):
        self.master_chef.listen_for_beacons()
        self.assertIsNotNone(self.master_chef.transport)