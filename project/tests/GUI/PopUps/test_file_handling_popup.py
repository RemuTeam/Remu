import unittest
from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from Constants.FileHandlingMode import *

class TestFileHandlingPopUp(unittest.TestCase):
    def setUp(self):
        self.title = "test"
        self.callbackbuttontext = "button"
        self.path = "test_path"
        self.filters = ["*.jpg", "*.test"]
        self.imported_files = []
        self.selected_presentations = []
        self.presentation_names = ["test1", "test2"]
        self.open_project_layout = FileHandlerPopUp(title=self.title,
                                                   default_path=self.path,
                                                   callback=self.open_callback,
                                                   callback_button_text=self.callbackbuttontext,
                                                   file_handling_mode=OpenProject,
                                                   test_mode=True)
        self.import_multiple_layout = FileHandlerPopUp(title=self.title,
                                                       default_path=self.path,
                                                       callback=self.import_multiple_callback,
                                                       callback_button_text=self.callbackbuttontext,
                                                       file_handling_mode=ImportMultipleFiles,
                                                       imported_files=self.imported_files,
                                                       selected_presentations=self.selected_presentations,
                                                       presentation_names=self.presentation_names,
                                                       filters=self.filters,
                                                       test_mode=True)
        self.save_project_layout = FileHandlerPopUp(title=self.title,
                                                    default_path=self.path,
                                                    callback=self.save_callback,
                                                    callback_button_text=self.callbackbuttontext,
                                                    file_handling_mode=SaveProject,
                                                    test_mode=True)

    def open_callback(self, path, list, filename):
        pass

    def save_callback(self, path, list, filename):
        pass

    def import_multiple_callback(self, path, list, filename):
        pass

    def test_callback_button_on_open_project_popup_1(self):
        self.assertTrue(self.open_project_layout.ids.callback_button.disabled)

    def test_callback_button_on_open_project_popup_2(self):
        self.open_project_layout.ids.filechooser.selection.append("test")
        self.open_project_layout.check_selections(None, None)
        self.assertFalse(self.open_project_layout.ids.callback_button.disabled)

    def test_callback_button_on_import_multiple_popup_1(self):
        self.assertTrue(self.import_multiple_layout.ids.callback_button.disabled)

    def test_callback_button_on_import_multiple_popup_2(self):
        self.import_multiple_layout.ids.filechooser.selection.append("test")
        self.import_multiple_layout.check_selections(None, None)
        self.assertTrue(self.import_multiple_layout.ids.callback_button.disabled)

    def test_callback_button_on_import_multiple_popup_3(self):
        self.import_multiple_layout.selected_presentations.append("test")
        self.import_multiple_layout.check_selections(None, None)
        self.assertTrue(self.import_multiple_layout.ids.callback_button.disabled)

    def test_callback_button_on_import_multiple_popup_4(self):
        self.import_multiple_layout.ids.filechooser.selection.append("test")
        self.import_multiple_layout.selected_presentations.append("test")
        self.import_multiple_layout.check_selections(None, None)
        self.assertFalse(self.import_multiple_layout.ids.callback_button.disabled)

    def test_filename_input_with_valid_filename(self):
        self.assertTrue(self.save_project_layout.ids.callback_button.disabled)
        self.save_project_layout.check_filename(None, ".ekieki")
        self.assertFalse(self.save_project_layout.ids.callback_button.disabled)

    def test_filename_with_invalid_filename(self):
        self.assertTrue(self.save_project_layout.ids.callback_button.disabled)
        self.save_project_layout.check_filename(None, "\\ekieki")
        self.assertTrue(self.save_project_layout.ids.callback_button.disabled)

    def test_filename_with_empty_filename(self):
        self.assertTrue(self.save_project_layout.ids.callback_button.disabled)
        self.save_project_layout.check_filename(None, "")
        self.assertTrue(self.save_project_layout.ids.callback_button.disabled)