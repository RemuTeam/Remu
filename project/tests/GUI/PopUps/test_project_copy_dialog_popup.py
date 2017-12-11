import unittest
from unittest.mock import patch
from GUI.PopUps.ProjectCopyDialogPopUp import ProjectCopyDialogPopUp
from Constants.PathConstants import PathConstants


class TestProjectCopyDialogPopUp(unittest.TestCase):
    def test_replace_file(self):
        with patch.object(ProjectCopyDialogPopUp, 'save_source', return_value=None) as mock_method:
            popup_mock = ProjectCopyDialogPopUp("some_source", "destination", None, PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
            popup_mock.ids.save_as.text = "new_filename"
            popup_mock.replace_file()

        mock_method.assert_called_once_with("destination")

    def test_create_new_file(self):
        with patch.object(ProjectCopyDialogPopUp, 'save_source', return_value=None) as mock_method:
            popup_mock = ProjectCopyDialogPopUp("some_source", "destination", None, PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
            popup_mock.ids.save_as.text = "new_filename"
            popup_mock.create_new_file()

        mock_method.assert_called_once_with("new_filename")
