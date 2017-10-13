import unittest
import time
from RemuTCP.RemuTCP import RemuTCP

class TestRemuTCPMethods(unittest.TestCase):

    def test_init_slave(self):
        tcp = RemuTCP(None, False, None, 8001)
        self.assertIsNone(tcp.address)
        self.assertIsNotNone(tcp.listener)
        tcp.stop_listening()

    def test_init_master(self):
        tcp = RemuTCP(None, True, "127.0.0.1", 8002)
        self.assertEqual("127.0.0.1", tcp.address)
        self.assertIsNone(tcp.listener)




