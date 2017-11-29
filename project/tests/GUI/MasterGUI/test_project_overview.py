import unittest
from unittest.mock import Mock
from GUI.MasterGUI.ProjectOverview import ProjectOverview
from Domain.Master import Master
from Domain.SlaveConnection import SlaveConnection
from Domain.Presentation import Presentation


class ProjectOverviewTest(unittest.TestCase):

    def setUp(self):
        self.slave_overview = ProjectOverview()
        self.slave_connection_mock = SlaveConnection(Mock(Master))
        presentation = Presentation()
        presentation.set_files(["a.jpg", "b.jpg", "g.mp4", "test_text.txt", "test_text2.txt"])
        self.slave_connection_mock.set_presentation(presentation)

    def test_update_slave_to_overview(self):
        self.slave_overview.update_slave_to_overview(self.slave_connection_mock)
        self.assertIsNotNone(self.slave_overview.slave_buttons[self.slave_connection_mock.full_address])
        self.assertIsNotNone(self.slave_overview.slave_presentations[self.slave_connection_mock.full_address])

    def test_remove_slave_from_overview(self):
        self.slave_overview.update_slave_to_overview(self.slave_connection_mock)
        self.slave_overview.remove_slave_from_overview(self.slave_connection_mock.full_address)
        self.assertNotIn(self.slave_connection_mock.full_address, self.slave_overview.slave_buttons)
        self.assertNotIn(self.slave_connection_mock.full_address, self.slave_overview.slave_presentations)