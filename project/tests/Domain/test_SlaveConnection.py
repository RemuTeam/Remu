import unittest
from unittest.mock import Mock, MagicMock
from unittest.mock import patch

from Constants.Command import Command
from Constants.Command import Notification

from Constants.MessageKeys import MessageKeys
from Domain.Master import Master
from Domain.Message import Message
from Domain.SlaveConnection import SlaveConnection
from Domain.Presentation import Presentation
from Networking.RemuTCP import RemuTCP


class SlaveConnectionTest(unittest.TestCase):

    def setUp(self):
        self.connection_mock = Mock(RemuTCP)
        self.sc = SlaveConnection(None, None, self.connection_mock)

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

    """
    def test_show_next(self):
        presentation = Presentation()
        presentation.set_files(["first", "second"])
        presentation.load()
        self.sc.presentation = presentation
        self.assertEqual(self.sc.currently_showing, -1)
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, -1)
        self.sc.response_next()
        self.assertEqual(self.sc.currently_showing, "second")
    """

    def test_show_next_calls_send_message(self):
        self.sc.show_next()
        calls = self.connection_mock.method_calls
        name = calls[0][0]
        self.assertEqual(name, "send_message")

    def test_handle_invalid_command(self):
        msg = Message()
        msg.set_field(MessageKeys.response_key, "LET ME OUT LET ME OUT LET ME OUT")
        self.sc.handle_message(msg)

    def test_terminate_connection_sends_commands_and_closes_connections(self):
        self.sc.master = Mock(Master)
        self.sc.terminate_connection()
        self.sc.connection.end_connection.assert_called_once_with()
        self.sc.master.notify.assert_called_once_with(Notification.CONNECTION_TERMINATED, self.sc)

    def test_end_presentation_sends_command(self):
        self.sc.end_presentation()
        command_value = self.sc.connection.mock_calls[0][1][0].fields["command"]
        self.assertEqual(command_value, Command.END_PRESENTATION.value)

    """
    def test_presentation_resets_when_next_item_is_none(self):
        self.sc.master = Mock(Master)
        self.sc.presentation = Mock(Presentation)
        self.sc.presentation.get_next = Mock(return_value=None)
        self.sc.handle_show_next_response()
        self.sc.presentation.get_next.assert_called_once_with()
        self.sc.presentation.reset.assert_called_once_with()
    """

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

    def test_send_presentation(self):
        with patch.object(SlaveConnection, 'send_command', return_value=None) as mock_method:
            self.sc.send_presentation(["a.jpg", "b.jpg"])
        mock_method.assert_called_once_with(Command.SEND_PRESENTATION.value, {'presentation_content': ['a.jpg', 'b.jpg']})

    def test_handle_show_next_response(self):
        self.sc.master = MagicMock(Master)
        self.sc.presentation = Presentation()
        self.sc.handle_show_next_response({MessageKeys.index_key: 1})
        self.sc.master.notify.assert_called_once_with(Notification.PRESENTATION_STATUS_CHANGE, 1)
