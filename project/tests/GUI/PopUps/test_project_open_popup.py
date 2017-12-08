import unittest
from unittest.mock import Mock
from Domain.Master import Master
from Constants.FileHandlingMode import OpenProject
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout
from GUI.PopUps.ProjectOpenPopUp import ProjectOpenPopUp

class TestProjectOpenPopUp(unittest.TestCase):
    def setUp(self):
        self.path = "testpath"
        self.layout = ProjectOpenPopUp(Mock(Master(MasterGUILayout())), self.path, True)

    def test_title_is_set(self):
        self.assertEqual(self.layout.title, "Open project")

    def test_default_path_is_set(self):
        self.assertEqual(self.layout.default_path, self.path)

    def test_callback_button_text_is_set(self):
        self.assertEqual(self.layout.ids.callback_button.text, "Open")

    def test_filehandling_mode_is_set(self):
        self.assertEqual(self.layout.file_handling_mode, OpenProject)