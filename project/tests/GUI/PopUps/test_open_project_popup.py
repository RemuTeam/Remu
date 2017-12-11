import unittest
from GUI.PopUps.ProjectOpenPopUp import ProjectOpenPopUp
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout
from Constants.PathConstants import PathConstants
from Domain.Master import Master


class ProjectOpenPopUpTest(unittest.TestCase):
    def setUp(self):
        self.selection = ["test.remu"]
        self.master_gui_layout = MasterGUILayout()
        self.master = Master(self.master_gui_layout)
        self.path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
        self.popup = ProjectOpenPopUp(self.master, self.path, True)

    def test_open_project(self):
        self.assertIsNone(self.master.project)
        self.popup.open_project(self.path, self.selection)
        self.assertIsNotNone(self.master.project)