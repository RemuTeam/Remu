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
        layout = Mock(MasterGUILayout)
        self.master = Master(layout)
        self.mockMaster = Mock(Master)

    def tearDown(self):
        if hasattr(self.master.slave_connection, 'connection'):
            self.master.close_connections()

    def test_add_slave_works(self):
        self.assertIsNone(self.master.slave_connection)
        self.master.add_slave("127.0.0.1")
        self.assertIsNotNone(self.master.slave_connection)

    def test_add_slave_connection_works(self):
        self.assertIsNone(self.master.slave_connection)
        self.master.add_slave_connection(Mock(SlaveConnection))
        self.assertIsNotNone(self.master.slave_connection)

    def test_request_next_works(self):
        with patch.object(Master, 'request_next', return_value=None) as mock_method:
            master_mock = Master(Mock(MasterGUILayout))
            master_mock.request_next()

        mock_method.assert_called_once_with()

    def test_request_next_calls_slave_connections_show_next(self):
        with patch.object(SlaveConnection, 'show_next', return_value=None) as mock_method:
            master_mock = Master(Mock(MasterGUILayout))
            slave_connection_mock = SlaveConnection(master_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.request_next()

        mock_method.assert_called_once_with()

    def test_update_presentation_status_to_layout_works(self):
        with patch.object(MasterGUILayout, 'notify', return_value=None) as mock_method:
            master_gui_mock = MasterGUILayout()
            master_mock = Master(master_gui_mock)
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(master_mock)
            slave_connection_mock.set_connection(connection_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.notify(Notification.PRESENTATION_UPDATE, "test_data")

        mock_method.assert_called_once_with(Notification.PRESENTATION_UPDATE, "test_data")

    def test_update_connection_works1(self):
        with patch.object(MasterGUILayout, 'notify', return_value=None) as mock_method:
            master_gui_mock = MasterGUILayout()
            master_mock = Master(master_gui_mock)
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(master_mock)
            slave_connection_mock.set_connection(connection_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.notify(Notification.CONNECTION_FAILED, "test_data")

        mock_method.assert_called_once_with(Notification.CONNECTION_FAILED, "test_data")

    def test_update_connection_works2(self):
        with patch.object(MasterGUILayout, 'notify', return_value=None) as mock_method:
            master_gui_mock = MasterGUILayout()
            master_mock = Master(master_gui_mock)
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(master_mock)
            slave_connection_mock.set_connection(connection_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.notify(Notification.CONNECTION_ESTABLISHED, "test_data")

        mock_method.assert_called_once_with(Notification.CONNECTION_ESTABLISHED, "test_data")

    def test_update_connection_works3(self):
        with patch.object(SlaveConnection, 'request_presentation', return_value=None) as mock_method:
            master_gui_mock = MasterGUILayout()
            master_mock = Master(master_gui_mock)
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(master_mock)
            slave_connection_mock.set_connection(connection_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.notify(Notification.CONNECTION_ESTABLISHED, "test_data")

        mock_method.assert_called_once_with()

    def test_close_connections(self):
        with patch.object(RemuTCP, 'end_connection', return_value=None) as mock_method:
            master_gui_mock = MasterGUILayout()
            master_mock = Master(master_gui_mock)
            connection_mock = RemuTCP(master_mock, True, "")
            slave_connection_mock = SlaveConnection(master_mock)
            slave_connection_mock.set_connection(connection_mock)
            master_mock.add_slave_connection(slave_connection_mock)
            master_mock.close_connections()

        mock_method.assert_called_once_with()