import unittest
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from Constants.Command import Notification
from Constants.PathConstants import PathConstants
from Domain.Master import Master
from Domain.SlaveConnection import SlaveConnection
from GUI.GUIFactory import MasterGUILayout
from Networking.RemuTCP import RemuTCP
from Domain.Project import Project
from Domain.Presentation import Presentation


class MasterTest(unittest.TestCase):
    def setUp(self):
        self.layout = Mock(MasterGUILayout)
        self.mock_master = Master(self.layout)

    def tearDown(self):
        if hasattr(self.mock_master.slave_connections, 'connection'):
            self.mock_master.close_TCP_connections()
        self.mock_master.close_UDP_connection()
        self.mock_master.close_FTP_connection()

    """
    def test_add_slave_works(self):
        self.assertIsNotNone(self.mock_master.slave_connections)
        self.mock_master.add_slave("127.0.0.1")
        self.assertGreaterEqual(len(self.mock_master.slave_connections.keys()), 1)
    """


    def test_add_slave_connection_works(self):
        self.assertIsNotNone(self.mock_master.slave_connections)
        self.mock_master.add_slave_connection(SlaveConnection(None))
        self.assertGreaterEqual(len(self.mock_master.slave_connections.keys()), 1)

    def test_add_multiples_of_slave_connection(self):
        self.assertIsNotNone(self.mock_master.slave_connections)
        self.mock_master.add_slave_connection(SlaveConnection(None))
        slavc = SlaveConnection(None)
        slavc.full_address = "192.168.100.1"
        self.mock_master.add_slave_connection(slavc)
        self.assertGreaterEqual(len(self.mock_master.slave_connections.keys()), 2)

    def test_request_next_works(self):
        with patch.object(self.mock_master, 'request_next', return_value=None) as mock_method:
            self.mock_master.request_next()

        mock_method.assert_called_once_with()

    def test_request_next_calls_slave_connections_show_next(self):
        with patch.object(SlaveConnection, 'show_next', return_value=None) as mock_method:
            slave_connection_mock = SlaveConnection(self.mock_master)
            self.mock_master.add_slave_connection(slave_connection_mock)
            self.mock_master.request_next()

        mock_method.assert_called_once_with()

    def test_request_next_calls_multiple_slave_connections_show_next(self):
        self.assertIsNotNone(self.mock_master.slave_connections)
        slavc = SlaveConnection(None)
        slavc.show_next = MagicMock(return_value=0)
        self.mock_master.add_slave_connection(slavc)
        slavc = SlaveConnection(None)
        slavc.full_address = "192.168.100.1"
        slavc.show_next = MagicMock(return_value=0)
        self.mock_master.add_slave_connection(slavc)
        self.mock_master.request_next()
        for slaveconnection in self.mock_master.slave_connections.values():
            slaveconnection.show_next.assert_called_once_with()

    def test_update_presentation_status_to_layout_works(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.mock_master)
            slave_connection_mock.set_connection(connection_mock)
            self.mock_master.add_slave_connection(slave_connection_mock)
            self.mock_master.notify(Notification.PRESENTATION_UPDATE, "localhost:8000")

        mock_method.assert_called_once_with(Notification.PRESENTATION_UPDATE, "localhost:8000")

    def test_update_connection_works1(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.mock_master)
            slave_connection_mock.set_connection(connection_mock)
            self.mock_master.add_slave_connection(slave_connection_mock)
            self.mock_master.notify(Notification.CONNECTION_FAILED, "localhost:8000")

        mock_method.assert_called_once_with(Notification.CONNECTION_FAILED, "localhost:8000")

    def test_update_connection_works2(self):
        with patch.object(self.layout, 'notify', return_value=None) as mock_method:
            connection_mock = Mock(RemuTCP)
            slave_connection_mock = SlaveConnection(self.mock_master)
            slave_connection_mock.set_connection(connection_mock)
            self.mock_master.add_slave_connection(slave_connection_mock)
            self.mock_master.notify(Notification.CONNECTION_ESTABLISHED, "localhost:8000")

        mock_method.assert_called_once_with(Notification.CONNECTION_ESTABLISHED, "localhost:8000")

    def test_close_connections(self):
        with patch.object(RemuTCP, 'end_connection', return_value=None) as mock_method:
            connection_mock = RemuTCP(self.mock_master, True, "")
            slave_connection_mock = SlaveConnection(self.mock_master)
            slave_connection_mock.set_connection(connection_mock)
            self.mock_master.add_slave_connection(slave_connection_mock)
            self.mock_master.close_TCP_connections()

        mock_method.assert_called_once_with()

    def test_setup_project_with_valid_project(self):
        project = Project()
        name1 = "test1"
        presentation1 = Presentation()
        presentation1.set_files(["a.jpg", "b.jpg"])

        name2 = "test2"
        presentation2 = Presentation()
        presentation2.set_files(["b.jpg", "a.jpg"])

        project.presentations.append((name1, presentation1))
        project.presentations.append((name2, presentation2))

        self.mock_master.setup_project(project, PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
        self.mock_master.layout.setup_project.assert_called_once_with(project)
        self.assertEqual(self.mock_master.project, project)

    def test_setup_project_with_unsupported_filetype(self):
        project = Project()
        name1 = "test1"
        presentation1 = Presentation()
        presentation1.set_files(["a.doc", "b.jpg"])

        project.presentations.append((name1, presentation1))

        self.mock_master.setup_project(project, PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
        self.mock_master.layout.setup_project.assert_not_called()
        self.assertNotEqual(self.mock_master.project, project)

    def test_setup_project_with_nonexistent_file(self):
        project = Project()
        name1 = "test1"
        presentation1 = Presentation()
        presentation1.set_files(["abadababababababbabababbababab.jpg", "b.jpg"])

        project.presentations.append((name1, presentation1))

        self.mock_master.setup_project(project, PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
        self.mock_master.layout.setup_project.assert_not_called()
        self.assertNotEqual(self.mock_master.project, project)

    def test_adding_slave(self):
        with patch.object(SlaveConnection, 'connect_to_IP', return_value=None):
            self.mock_master.add_slave("127.0.0.1", 'help')
            self.assertEqual(self.mock_master.slave_connections['help'].full_address, 'localhost:8000')

