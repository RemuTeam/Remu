import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from Domain.Master import Master
from Domain.SlaveConnection import SlaveConnection
from GUI.GUIFactory import MasterGUILayout
from Domain.Command import Notification
from Networking.RemuTCP import RemuTCP

class MasterTest(unittest.TestCase):
    def setUp(self):
        self.layout = Mock(MasterGUILayout)
        self.master = Master(self.layout, False)
        #self.master.close_UDP_connection()
        self.mockMaster = Mock(Master(self.layout, False))

    def tearDown(self):
        if hasattr(self.master.slave_connections, 'connection'):
            self.master.close_TCP_connections()
        #self.master.close_UDP_connection()

    def test_add_slave_works(self):
        self.assertIsNotNone(self.master.slave_connections)
        self.master.add_slave("127.0.0.1")
        self.assertGreaterEqual(len(self.master.slave_connections.keys()), 1)



    def test_add_slave_connection_works(self):
        self.assertIsNotNone(self.master.slave_connections)
        self.master.add_slave_connection(SlaveConnection(None))
        self.assertGreaterEqual(len(self.master.slave_connections.keys()), 1)

    def test_request_next_works(self):
        with patch.object(self.master, 'request_next', return_value=None) as mock_method:
            self.master.request_next()

        mock_method.assert_called_once_with()

    def test_request_next_calls_slave_connections_show_next(self):
        with patch.object(SlaveConnection, 'show_next', return_value=None) as mock_method:
            slave_connection_mock = SlaveConnection(self.master)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.request_next()

        mock_method.assert_called_once_with()

    def test_update_presentation_status_to_layout_works(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.master)
            slave_connection_mock.set_connection(connection_mock)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.notify(Notification.PRESENTATION_UPDATE, "localhost:8000")

        mock_method.assert_called_once_with(Notification.PRESENTATION_UPDATE, "localhost:8000")

    def test_update_connection_works1(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.master)
            slave_connection_mock.set_connection(connection_mock)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.notify(Notification.CONNECTION_FAILED, "localhost:8000")

        mock_method.assert_called_once_with(Notification.CONNECTION_FAILED, "localhost:8000")

    def test_update_connection_works2(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.master)
            slave_connection_mock.set_connection(connection_mock)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.notify(Notification.CONNECTION_ESTABLISHED, "localhost:8000")

        mock_method.assert_called_once_with(Notification.CONNECTION_ESTABLISHED, "localhost:8000")

    def test_update_connection_works3(self):
        with patch.object(SlaveConnection, 'request_presentation', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.master)
            slave_connection_mock.set_connection(connection_mock)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.notify(Notification.CONNECTION_ESTABLISHED, "localhost:8000")

        mock_method.assert_called_once_with()

    def test_close_connections(self):
        with patch.object(RemuTCP, 'end_connection', return_value=None) as mock_method:
            connection_mock = RemuTCP(self.master, True, "")
            slave_connection_mock = SlaveConnection(self.master)
            slave_connection_mock.set_connection(connection_mock)
            self.master.add_slave_connection(slave_connection_mock)
            self.master.close_TCP_connections()

        mock_method.assert_called_once_with()