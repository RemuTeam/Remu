import unittest
from Networking.RemuTCP import RemuTCP
from Networking.RemuTCP import RemuProtocol
from Networking.RemuTCP import RemuProtocolFactory
from Domain.Message import Message

from unittest.mock import patch

class MockClass:

    def write(self, *largs):
        pass

    def getPeer(self, *largs):
        return self

    def handle_message(self, *largs):
        pass

    host = "jee"

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

    def test_data_received(self):
        with patch.object(MockClass, 'write', return_value=None) and\
                patch.object(MockClass, 'handle_message', return_value=Message()):
            remuprotocol = RemuProtocol()
            remuprotocol.transport = MockClass()
            tcp = RemuTCP(None, False, None, 8003)
            tcp.connection = MockClass()
            tcp.parent = MockClass()
            remuprotocol.factory = RemuProtocolFactory(tcp)
            remuprotocol.dataReceived(b'{"name": "test", "last": "case"}')



