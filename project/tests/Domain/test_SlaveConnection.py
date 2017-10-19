import unittest
from Domain.SlaveConnection import SlaveConnection
from Networking.RemuTCP import RemuTCP
from unittest.mock import Mock
from unittest.mock import MagicMock
from Domain.PicPresentation import PicPresentation
from Domain.Slave import Slave
from Domain.Message import Message
from Domain.Master import Master
from Domain.Command import Command
from Domain.Command import Notification

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

        slavecon.handle_message(msg)
        self.assertEqual(slavecon.currently_showing, "images/b.jpg")

    def test_handle_invalid_command(self):
        msg = Message()
        msg.set_field("responseTo", "LET ME OUT LET ME OUT LET ME OUT")
        self.sc.handle_message(msg)

    def test_terminate_connection_sends_commands_and_closes_connections(self):
        self.sc.master = Mock(Master)
        self.sc.terminate_connection()
        self.sc.connection.send_message.assert_called_once()
        self.sc.connection.end_connection.assert_called_once()
        self.sc.master.notify.assert_called_once_with(Notification.CONNECTION_TERMINATED, self.sc)

    def test_end_presentation_sends_command(self):
        self.sc.end_presentation()
        self.sc.connection.send_message.assert_called_once()
        command_value =  self.sc.connection.mock_calls[0][1][0].fields["command"]
        self.assertEqual(command_value, Command.END_PRESENTATION.value)

    def test_presentation_resets_when_next_item_is_none(self):
        self.sc.master = Mock(Master)
        self.sc.presentation = Mock(PicPresentation)
        self.sc.presentation.get_next = MagicMock(return_value=None)
        self.sc.handle_show_next_response()
        self.sc.presentation.get_next.assert_called_once()
        self.sc.presentation.reset.assert_called_once()

    def test_connection_established_sets_connected_true(self):
        slavecon = SlaveConnection(Mock(Master))
        self.assertFalse(slavecon.connected)
        slavecon.connection_established("123.123.123.123:123123")
        self.assertTrue(slavecon.connected)

    def test_connection_established_notifies_master(self):
        slavecon = SlaveConnection(Mock(Master))
        slavecon.connection_established("123.123.123.123:123123")
        slavecon.master.notify.called_once_with(Notification.CONNECTION_ESTABLISHED, "123.123.123.123:123123")

    def test_on_connection_lost_sets_connected_false(self):
        self.sc.master = Mock(Master)
        self.assertTrue(self.sc.connected)
        self.sc.on_connection_lost()
        self.assertFalse(self.sc.connected)

    def test_on_connection_lost_notifies_master(self):
        slavecon = SlaveConnection(Mock(Master))
        slavecon.connection_established("123.123.123.123:123123")
        slavecon.on_connection_lost()
        slavecon.master.notify.called_once_with(Notification.CONNECTION_FAILED, "123.123.123.123:123123")


