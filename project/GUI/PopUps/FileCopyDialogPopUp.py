from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from Utils.FileHandler import copy_file_as
from os import path


class FileCopyDialogPopUp(FileSavingDialogPopUp):
    FOLDER_NAME = "media folder"
    DISMISS_BTN_TEXT = "Import existing"

    def __init__(self, source, destination, filename_list, listener, project_path):
        super(FileCopyDialogPopUp, self).__init__(source=source,
                                                  destination=destination,
                                                  filename_list=filename_list,
                                                  listener=listener,
                                                  path=project_path,
                                                  folder_name=self.FOLDER_NAME,
                                                  dismiss_button_text=self.DISMISS_BTN_TEXT)

    def replace_file(self):
        self.copy_source_file_as(self.destination)

    def create_new_file(self):
        filename = path.join(self.path, self.ids.save_as.text)
        self.copy_source_file_as(filename)

    def copy_source_file_as(self, filename):
        try:
            copy_file_as(self.source, filename, self.path)
            self.filename_list.append(filename)
            self.listener.notify_file_import()
        except Exception as ex:
            self.error(ex)
