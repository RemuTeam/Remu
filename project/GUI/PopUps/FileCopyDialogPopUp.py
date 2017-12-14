from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from Utils.FileHandler import copy_file_as
from os import path


class FileCopyDialogPopUp(FileSavingDialogPopUp):
    """
    A class to handle copying a imported file to the media folder, if the file already
    exists in the media folder
    """
    FOLDER_NAME = "media folder"
    DISMISS_BTN_TEXT = "Import existing"

    def __init__(self, source, destination, filename_list, listener, project_path):
        """
        Constructs a popup that can be used to save a copy of the selected file
        or to replace the destination file
        :param source: the source file
        :param destination: the destination file
        :param filename_list: a list to append the imported file name to after saving
        :param listener: the listener to notify when file is imported
        :param project_path: the path to save the file to
        """
        super(FileCopyDialogPopUp, self).__init__(source=source,
                                                  destination=destination,
                                                  filename_list=filename_list,
                                                  listener=listener,
                                                  path=project_path,
                                                  folder_name=self.FOLDER_NAME,
                                                  dismiss_button_text=self.DISMISS_BTN_TEXT)

    def replace_file(self):
        """
        Replaces the destination file with the source file
        :return: None
        """
        self.copy_source_file_as(self.destination)

    def create_new_file(self):
        """
        Creates a new file from the source file
        :return:
        """
        filename = path.join(self.path, self.ids.save_as.text)
        self.copy_source_file_as(filename)

    def copy_source_file_as(self, filename):
        """
        Copies the source file as selected file
        :param filename: the filename to copy the source as
        :return: None
        """
        try:
            copy_file_as(self.source, filename)
            self.filename_list.append(filename)
            self.listener.notify_file_import()
        except Exception as ex:
            self.error(ex)
