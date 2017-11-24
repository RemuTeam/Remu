import unittest
from GUI.GUIFactory import ImportFilesPopUp
from GUI.GUIFactory import FileSavingDialogPopUp
from kivy.properties import ListProperty
from Domain.PathConstants import PathConstants
from Domain.TestReturnValue import TestReturnValue
import os
from shutil import copy, rmtree, move

class TestImportFilesPopup(unittest.TestCase):
    def setUp(self):
        self.copy_files = ["b.jpg", "test_text2.txt"]
        self.movable_file = "test_text.txt"
        self.temp_dir = os.path.join(os.getcwd(), "test_media_temp")
        self.popup = ImportFilesPopUp(MasterGUIImpl(), [], ["a", "b"], [],
                                      PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER,
                                      True)

    def tearDown(self):
        self.delete_temp_dir()

    def create_temp_dir(self):
        self.delete_temp_dir()
        os.mkdir(self.temp_dir)
        for filename in self.copy_files:
            source = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, filename)
            destination = os.path.join(self.temp_dir, filename)
            copy(source, destination)
        move(os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.movable_file),
             os.path.join(self.temp_dir, self.movable_file))

    def delete_temp_dir(self):
        if (os.path.isdir(self.temp_dir)):
            move(os.path.join(self.temp_dir, self.movable_file),
                 os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.movable_file))
            rmtree(self.temp_dir, True)

    def test_import_button(self):
        self.assertTrue(self.popup.ids.import_button.disabled)

    def test_import_button_2(self):
        self.popup.ids.filechooser.selection.append("test")
        self.popup.check_selections(None, None)
        self.assertTrue(self.popup.ids.import_button.disabled)

    def test_import_button_3(self):
        self.popup.selected_presentations.append("test")
        self.popup.check_selections(None, None)
        self.assertTrue(self.popup.ids.import_button.disabled)

    def test_import_button_4(self):
        self.popup.ids.filechooser.selection.append("test")
        self.popup.selected_presentations.append("test")
        self.popup.check_selections(None, None)
        self.assertFalse(self.popup.ids.import_button.disabled)

    def test_init_populates_presentation_list_properly(self):
        self.assertEqual(len(self.popup.ids.presentation_list.children), 2)

    def test_selected_presentations_is_empty_at_first(self):
        self.assertEqual(len(self.popup.selected_presentations), 0)

    def test_checbox_active_adds_and_removes_properly(self):
        checkbox = self.popup.ids.presentation_list.children[0].ids.checker
        label = checkbox.label
        self.popup.on_checkbox_active(checkbox, True)
        self.assertEqual(self.popup.selected_presentations[0], label)
        self.assertEqual(self.popup.local_presentation_selection[0], label)
        self.popup.on_checkbox_active(checkbox, False)
        self.assertEqual(len(self.popup.selected_presentations), 0)
        self.assertEqual(len(self.popup.local_presentation_selection), 0)

    def test_start_import(self):
        self.popup.import_files_for_presentation(None, self.copy_files)
        self.assertEqual(self.popup.listener.counter, 2)

    def test_import_from_media_dir(self):
        self.create_temp_dir()
        counter = self.popup.listener.counter
        media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
        filename = os.path.join(media_path, self.copy_files[0])
        filename_list = []
        self.popup.copy_file(media_path, filename, filename, filename_list, self.popup.listener)
        self.assertEqual(filename_list[0], filename)
        self.assertEqual(self.popup.listener.counter, counter - 1)

    def test_import_with_existing_filename(self):
        self.create_temp_dir()
        media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
        filename = self.copy_files[0]
        source = os.path.join(self.temp_dir, filename)
        destination = os.path.join(media_path, filename)
        retval = self.popup.copy_file(self.temp_dir, source, destination, [], self.popup.listener)
        self.assertEqual(retval, TestReturnValue.FileSavingDialogPopUp)

    def test_import_with_new_filename(self):
        self.create_temp_dir()
        media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
        filename = self.movable_file
        self.assertFalse(os.path.isfile(os.path.join(media_path, filename)))
        source = os.path.join(self.temp_dir, filename)
        destination = os.path.join(media_path, filename)
        filename_list = []
        self.popup.copy_file(self.temp_dir, source, destination, filename_list, self.popup.listener)
        self.assertTrue(os.path.isfile(os.path.join(media_path, filename)))
        self.assertEqual(filename_list[0], destination)

class TestFileSavingDialogPopUp(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(os.getcwd(), "test_media_temp")
        self.filename_1 = "b.jpg"
        self.alleged_new_filename_1 = "b_copy.jpg"
        self.filename_2 = "a.jpg"
        self.alleged_new_filename_2 = "a_copy_copy.jpg"
        self.source = os.path.join(self.temp_dir, self.filename_1)
        self.destination = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.filename_1)
        self.popup = FileSavingDialogPopUp(self.source, self.destination, [], MasterGUIImpl(),
                                           PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)

    def test_copy_filename_is_correct(self):
        self.assertEqual(self.popup.new_filename, self.alleged_new_filename_1)

    def test_copy_filename_is_correct_2(self):
        suorce = os.path.join(self.temp_dir, self.filename_2)
        distenation = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.filename_2)
        pupop = FileSavingDialogPopUp(suorce, distenation, [], MasterGUIImpl(),
                                      PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
        self.assertEqual(pupop.new_filename, self.alleged_new_filename_2)

    def test_copy_button_is_enabled_at_first(self):
        self.assertFalse(self.popup.ids.copy_file_button.disabled)

    def test_copy_button_disables_if_filename_exists(self):
        self.popup.on_text(None, "b.jpg")
        self.assertTrue(self.popup.ids.copy_file_button.disabled)

    def test_copy_button_disables_if_filename_empty(self):
        self.popup.on_text(None, "")
        self.assertTrue(self.popup.ids.copy_file_button.disabled)

    def test_copy_button_disables_if_save_as_contains_illegal_char(self):
        self.popup.on_text(None, self.alleged_new_filename_1 + "%")
        self.assertTrue(self.popup.ids.copy_file_button.disabled)
        self.popup.on_text(None, self.alleged_new_filename_1)
        self.assertFalse(self.popup.ids.copy_file_button.disabled)

class MasterGUIImpl():
    def __init__(self):
        self.counter = -1

    def notify_file_import(self):
        self.counter -= 1

    def import_started(self, value):
        self.counter = value