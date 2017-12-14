from kivy.properties import StringProperty
from kivy.uix.popup import Popup

from GUI.PopUps.PopUps import ExceptionAlertPopUp
from Utils.FileHandler import *


class FileSavingDialogPopUp(Popup):
    """
    A popup functionality to confirm actions
    when saving a file that already exists.
    """
    destination = StringProperty('')
    new_filename = StringProperty('')
    original_destination_filename_only = StringProperty('')
    folder_name = StringProperty('')
    dismiss_button_text = StringProperty('')

    def __init__(self, source, destination, filename_list, listener, path,
                 folder_name, dismiss_button_text):
        """
        Constructs a popup
        :param source: the source to copy
        :param destination: the destinatio to copy the source to
        :param filename_list:
        :param listener:
        :param path:
        :param folder_name:
        :param dismiss_button_text:
        """
        super(FileSavingDialogPopUp, self).__init__()
        self.source = source
        self.destination_name = destination
        self.destination = destination
        self.path = path
        self.folder_name = folder_name
        self.dismiss_button_text = dismiss_button_text
        self.media_files = get_filenames_from_path(self.path)
        self.new_filename = prefilled_new_file_name(self.destination, self.path)
        self.original_destination_filename_only = get_filename_only(destination)
        self.ids.save_as.bind(text=self.on_text)
        self.filename_list = filename_list
        self.listener = listener

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

    def error(self, exception):
        ExceptionAlertPopUp("Error writing file", exception).open()