import unittest
from Domain.SlaveConnection import SlaveConnection
from Networking.RemuTCP import RemuTCP
from unittest.mock import Mock
from Domain.PicPresentation import PicPresentation
from Domain.Slave import Slave
from Domain.Message import Message
from Domain.Master import Master
from Domain.Command import Command

class SlaveConnectionTest(unittest.TestCase):

    def setUp(self):
        self.connection_mock = Mock(RemuTCP)
        self.sc = SlaveConnection(None, self.connection_mock)

    def test_init_with_connection(self):
        self.assertEqual(self.connection_mock, self.sc.connection)

    def test_init_without_params(self):
        empty_slavecon = SlaveConnection(None)
        self.assertIsNone(empty_slavecon.connection)

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
        presentation = PicPresentation()
        presentation.pic_files.append("first")
        presentation.pic_files.append("second")
        self.sc.presentation = presentation
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, "first")
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, "second")

    def test_request_presentation_calls_send_message(self):
        self.sc.request_presentation()
        calls = self.connection_mock.method_calls
        name = calls[0][0]
        self.assertEqual(name, "send_message")

    def test_show_next_calls_send_message(self):
        self.sc.show_next()
        calls = self.connection_mock.method_calls
        name = calls[0][0]
        self.assertEqual(name, "send_message")

    def test_handle_picpresentation_response(self):
        slavecon = SlaveConnection(Mock(Master))
        slave = Slave()
        msg = slave.handle_request_presentation()
        slavecon.handle_message(msg)
        self.assertGreaterEqual(len(slavecon.presentation.pic_files), 2)


    def test_handle_show_next_response(self):
        slavecon = SlaveConnection(Mock(Master))
        slave = Slave()
        msg = slave.handle_request_presentation()
        slavecon.handle_message(msg)
        msg = Message()
        msg.set_field("responseTo", Command.SHOW_NEXT.value)
        slavecon.handle_message(msg)
        self.assertGreaterEqual(len(slavecon.presentation.pic_files), 2)
        self.assertEqual(slavecon.currently_showing, "images/a.jpg")

    def test_handle_invalid_command(self):
        msg = Message()
        msg.set_field("responseTo", "LET ME OUT LET ME OUT LET ME OUT")
        self.sc.handle_message(msg)