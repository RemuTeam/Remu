import unittest
from Domain.SlaveConnection import SlaveConnection
from RemuTCP.RemuTCP import RemuTCP
from unittest.mock import Mock
from Domain.PicPresentation import PicPresentation

class SlaveConnectionTest(unittest.TestCase):
    sc = None

    def setUp(self):
        mock = Mock(RemuTCP)
        self.sc = SlaveConnection(None, mock)

    def test_init_with_connection(self):
        mock = Mock(RemuTCP)
        slavecon = SlaveConnection(None, mock)
        self.assertEqual(mock, slavecon.connection)

    def test_init_without_params(self):
        slavecon = SlaveConnection(None)
        self.assertIsNone(slavecon.connection)

    def test_invalid_ip_address1(self):
        self.sc.connect_to_IP("192.168.asd.1")
        self.assertIsNone(self.sc.connection)

    def test_invalid_ip_address2(self):
        self.sc.connect_to_IP("192.168:7000")
        self.assertIsNone(self.sc.connection)

    def test_invalid_ip_address3(self):
        self.sc.connect_to_IP("192.168.1234.1")
        self.assertIsNone(self.sc.connection)

    def test_invalid_port1(self):
        self.sc.connect_to_IP("192.168.1.2:1111asd")
        self.assertIsNone(self.sc.connection)

    def test_invalid_port2(self):
        self.sc.connect_to_IP("192.168.1.2:")
        self.assertIsNone(self.sc.connection)

    def test_show_next(self):
        self.sc.connection = Mock(RemuTCP)
        presentation = PicPresentation()
        presentation.pic_files.append("first")
        presentation.pic_files.append("second")
        self.sc.presentation = presentation
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, "first")
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, "second")

    def test_request_presentation_calls_send_message(self):
        mocktcp = Mock(RemuTCP)
        self.sc.connection = mocktcp
        self.sc.request_presentation()
        calls = mocktcp.method_calls
        name = calls[0][0]
        self.assertEqual(name, "send_message")

    def test_show_next_calls_send_message(self):
        mocktcp = Mock(RemuTCP)
        self.sc.connection = mocktcp
        self.sc.show_next()
        calls = mocktcp.method_calls
        name = calls[0][0]
        self.assertEqual(name, "send_message")
