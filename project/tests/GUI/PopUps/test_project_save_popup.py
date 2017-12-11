import unittest
from GUI.PopUps.ProjectSavePopUp import ProjectSavePopUp
from Constants.PathConstants import PathConstants
from Domain.Master import Master
from Domain.Project import Project
import os

class ProjectSavePopUpTest(unittest.TestCase):
    def setUp(self):
        self.project = Project()
        self.master = Master(None)
        self.master.project = self.project
        self.path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
        self.test_file = "project_test_file"
        self.test_file_with_extension = self.test_file + ".remu"
        self.test_file_with_path = os.path.join(self.path, self.test_file_with_extension)
        self.popup = ProjectSavePopUp(self.master, self.path, True)

    def tearDown(self):
        os.remove(self.test_file_with_path) if os.path.isfile(self.test_file_with_path) else None

    def test_save_project(self):
        self.assertFalse(os.path.isfile(self.test_file_with_path))
        self.popup.save_project(self.path, [], self.test_file)
        self.assertTrue(os.path.isfile(self.test_file_with_path))