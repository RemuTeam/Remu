import os
import unittest
from shutil import copy, rmtree, move

from Constants.TestReturnValue import TestReturnValue

from Constants.PathConstants import PathConstants
from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from GUI.PopUps.ImportFilesPopUp import ImportFilesPopUp
from GUI.PopUps.BindPresentationToSlavePopUp import BindPresentationToSlavePopUp
from Domain.Slave import Slave
from Domain.Master import Master
from Domain.SlaveConnection import SlaveConnection
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout
from unittest.mock import Mock
from Domain.Presentation import Presentation
from kivy.uix.button import Button


class TestBindPresentationToSlavePopup(unittest.TestCase):

    def setUp(self):
        self.slave_name = "Slave"
        self.master = Master(Mock(MasterGUILayout))
        self.button = Button()
        self.bind_popup = BindPresentationToSlavePopUp([self.slave_name], None, self.master, self.button)

    def test_init_populates_presentation_list_properly(self):
        self.assertIsNone(self.bind_popup.presentation)
        self.assertEquals(self.bind_popup.listener, self.master)
        self.assertEquals(self.bind_popup.button, self.button)

    def test_checkbox_wont_select_if_no_boolean(self):
        self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, None)
        self.assertIsNone(self.bind_popup.selected_slave)

    def test_checkbox_selects(self):
        self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, True)
        self.assertEquals(self.bind_popup.selected_slave, self.slave_name)

    def test_confirm(self):
        self.bind_popup.confirm()
        self.assertEquals(self.button.text, '')

    #def test_confirm_just_works(self):
        # self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, True)
        # self.bind_popup.confirm()
        # self.assertEquals(self.button.text, self.slave_name)

#     def test_checbox_active_adds_and_removes_properly(self):
#         checkbox = self.popup.ids.presentation_list.children[0].ids.checker
#         label = checkbox.label
#         self.popup.on_checkbox_active(checkbox, True)
#         self.assertEqual(self.popup.selected_presentations[0], label)
#         self.assertEqual(self.popup.local_presentation_selection[0], label)
#         self.popup.on_checkbox_active(checkbox, False)
#         self.assertEqual(len(self.popup.selected_presentations), 0)
#         self.assertEqual(len(self.popup.local_presentation_selection), 0)
#
#     def test_start_import(self):
#         self.popup.import_files_for_presentation(None, self.copy_files, None)
#         self.assertEqual(self.popup.listener.counter, 2)
#
#     def test_import_from_media_dir(self):
#         self.create_temp_dir()
#         counter = self.popup.listener.counter
#         media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
#         filename = os.path.join(media_path, self.copy_files[0])
#         filename_list = []
#         self.popup.copy_file(media_path, filename, filename, filename_list, self.popup.listener)
#         self.assertEqual(filename_list[0], filename)
#         self.assertEqual(self.popup.listener.counter, counter - 1)
#
#     def test_import_with_existing_filename(self):
#         self.create_temp_dir()
#         media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
#         filename = self.copy_files[0]
#         source = os.path.join(self.temp_dir, filename)
#         destination = os.path.join(media_path, filename)
#         retval = self.popup.copy_file(self.temp_dir, source, destination, [], self.popup.listener)
#         self.assertEqual(retval, TestReturnValue.FileSavingDialogPopUp)
#
#     def test_import_with_new_filename(self):
#         self.create_temp_dir()
#         media_path = PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER
#         filename = self.movable_file
#         self.assertFalse(os.path.isfile(os.path.join(media_path, filename)))
#         source = os.path.join(self.temp_dir, filename)
#         destination = os.path.join(media_path, filename)
#         filename_list = []
#         self.popup.copy_file(self.temp_dir, source, destination, filename_list, self.popup.listener)
#         self.assertTrue(os.path.isfile(os.path.join(media_path, filename)))
#         self.assertEqual(filename_list[0], destination)
#
# class TestFileSavingDialogPopUp(unittest.TestCase):
#     def setUp(self):
#         self.temp_dir = os.path.join(os.getcwd(), "test_media_temp")
#         self.copy_files = ["b.jpg", "test_text2.txt"]
#         self.filename_1 = "b.jpg"
#         self.filename_2 = "a.jpg"
#         self.filename_3 = "c"
#         self.new_filename = "newfile.jpg"
#         self.source = os.path.join(self.temp_dir, self.filename_1)
#         self.destination = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.filename_1)
#         self.popup = FileSavingDialogPopUp(self.source, self.destination, [], MasterGUIImpl(),
#                                            PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
#         ext = self.popup.COPY_EXTENSION
#         self.alleged_new_filename_1 = "b" + ext + ".jpg"
#         self.alleged_new_filename_2 = "a" + ext + ext + ".jpg"
#         self.alleged_new_filename_3 = "c" + ext
#
#     def tearDown(self):
#         self.delete_temp_dir()
#
#     def create_temp_dir(self):
#         self.delete_temp_dir()
#         os.mkdir(self.temp_dir)
#         for filename in self.copy_files:
#             source = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, filename)
#             destination = os.path.join(self.temp_dir, filename)
#             copy(source, destination)
#
#     def delete_temp_dir(self):
#         if (os.path.isdir(self.temp_dir)):
#             rmtree(self.temp_dir, True)
#
#     def test_copy_filename_is_correct(self):
#         self.assertEqual(self.popup.new_filename, self.alleged_new_filename_1)
#
#     def test_copy_filename_is_correct_2(self):
#         suorce = os.path.join(self.temp_dir, self.filename_2)
#         distenation = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.filename_2)
#         pupop = FileSavingDialogPopUp(suorce, distenation, [], MasterGUIImpl(),
#                                       PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
#         self.assertEqual(pupop.new_filename, self.alleged_new_filename_2)
#
#     def test_copy_filename_is_correct_3(self):
#         suorce = os.path.join(self.temp_dir, self.filename_3)
#         distenation = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.filename_3)
#         pupop = FileSavingDialogPopUp(suorce, distenation, [], MasterGUIImpl(),
#                                       PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER)
#         self.assertEqual(pupop.new_filename, self.alleged_new_filename_3)
#
#     def test_copy_button_is_enabled_at_first(self):
#         self.assertFalse(self.popup.ids.copy_file_button.disabled)
#
#     def test_copy_button_disables_if_filename_exists(self):
#         self.popup.on_text(None, self.filename_1)
#         self.assertTrue(self.popup.ids.copy_file_button.disabled)
#
#     def test_copy_button_disables_if_filename_empty(self):
#         self.popup.on_text(None, "")
#         self.assertTrue(self.popup.ids.copy_file_button.disabled)
#
#     def test_copy_button_disables_if_save_as_contains_illegal_char(self):
#         self.popup.on_text(None, self.alleged_new_filename_1 + "%")
#         self.assertTrue(self.popup.ids.copy_file_button.disabled)
#         self.popup.on_text(None, self.alleged_new_filename_1)
#         self.assertFalse(self.popup.ids.copy_file_button.disabled)
#
#     def test_replacing_works(self):
#         self.create_temp_dir()
#         pre_timestamp = os.path.getmtime(self.destination)
#         self.popup.replace_file()
#         post_timestamp = os.path.getmtime(self.destination)
#         self.assertTrue(pre_timestamp < post_timestamp)
#
#     def test_create_new_file(self):
#         self.create_temp_dir()
#         self.popup.ids.save_as.text = self.new_filename
#         self.popup.create_new_file()
#         new_file_path = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, self.new_filename)
#         new_file_created = os.path.isfile(new_file_path)
#         self.assertTrue(new_file_created)
#         if new_file_created:
#             os.remove(new_file_path)
#
# class MasterGUIImpl():
#     def __init__(self):
#         self.counter = -1
#
#     def notify_file_import(self):
#         self.counter -= 1
#
#     def import_started(self, value):
#         self.counter = value