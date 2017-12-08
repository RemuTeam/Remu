from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from GUI.PopUps.PopUps import ExceptionAlertPopUp
from Constants.FileHandler import *
from Services.FileCopyService import copy_file_as, prefilled_new_file_name, get_filenames_from_path, save_source_as

import os


class FileSavingDialogPopUp(Popup):
    """
    A popup functionality to confirm actions
    when copying a file that already exists.
    """
    destination = StringProperty('')
    new_filename = StringProperty('')
    original_destination_filename_only = StringProperty('')

    def __init__(self, source, destination, filename_list, listener, media_path, source_is_file=True):
        """
        The source and destination files are passed as arguments
        :param source: a string, the source file with path
        :param destination: a string, the destination file with path
        :param filename_list: the list to append the created filename
        """
        super(FileSavingDialogPopUp, self).__init__()
        self.source = source
        self.destination_name = destination
        self.destination = destination
        self.path = media_path
        self.media_files = get_filenames_from_path(self.path)
        self.new_filename = prefilled_new_file_name(self.destination, self.path)
        self.original_destination_filename_only = self.__parse_filename_only(destination)
        self.ids.save_as.bind(text=self.on_text)
        self.filename_list = filename_list
        self.listener = listener
        self.source_is_file = source_is_file

    def on_text(self, instance, filename):
        """
        This function is called every time the bound widget's text-property changes
        :param instance: the instance of the Widget
        :param filename: the value in the text property
        :return:
        """
        copy_file_btn = self.ids.copy_file_button
        if filename in self.media_files or not check_filename(filename):
            copy_file_btn.disabled = True
        else:
            copy_file_btn.disabled = False

    def __parse_filename_only(self, filepath):
        """
        A private helper method to return the file name from a
        "path1/path2/path3/filename.ext" string.
        :param filepath: a string, the pathpathpathfile-thingy
        :return: a string the file name only
        """
        paths_and_file_list = filepath.split(os.sep)
        return paths_and_file_list[len(paths_and_file_list) - 1]

    def replace_file(self):
        self.copy_source_file_as(self.destination) if self.source_is_file else self.save_source_as(self.destination)

    def create_new_file(self):
        filename = os.path.join(self.path, self.ids.save_as.text)
        self.copy_source_file_as(filename) if self.source_is_file else self.save_source_as(filename)

    def copy_source_file_as(self, filename):
        try:
            print(self.source, filename)
            copy_file_as(self.source, filename, self.path)
            self.filename_list.append(filename)
            self.listener.notify_file_import()
        except Exception as ex:
            self.error(ex)

    def save_source_as(self, filename):
        try:
            save_source_as(self.source, filename, self.path)
        except Exception as ex:
            self.error(ex)

    def error(self, exception):
        ExceptionAlertPopUp("Error writing file", exception).open()