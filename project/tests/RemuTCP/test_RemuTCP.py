import unittest
from RemuTCP.RemuTCP import RemuTCP

class TestRemuTCPMethods(unittest.TestCase):

    def test_init_no_params(self):
        tcp = RemuTCP(None)
        self.assertIsNone(tcp.address)
        self.assertIsNotNone(tcp.port)
        tcp.stop_listening()

    def test_init_master(self):
        tcp = RemuTCP(None, True, "127.0.0.1")
        self.assertEqual("127.0.0.1", tcp.address)
        self.assertIsNone(tcp.port)

    def test_connection_successful(self):
        slave = RemuTCP(None)
        master = RemuTCP(None, True, "127.0.0.1")
        self.assertIsNotNone(slave.connection)
        self.assertIsNotNone(master.connection)
        slave.stop_listening()






