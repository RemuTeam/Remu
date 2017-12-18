from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from kivy.logger import Logger
from Utils.FileHandler import write_file, get_filename_only

class ProjectCopyDialogPopUp(FileSavingDialogPopUp):
    FOLDER_NAME = "project folder"
    DISMISS_BTN_TEXT = "Cancel"

    def __init__(self, source, destination, listener, project_path):
        super(ProjectCopyDialogPopUp, self).__init__(source=source,
                                                     destination=destination,
                                                     filename_list=None,
                                                     listener=listener,
                                                     path=project_path,
                                                     folder_name=self.FOLDER_NAME,
                                                     dismiss_button_text=self.DISMISS_BTN_TEXT)

    def replace_file(self):
        self.save_source(get_filename_only(self.destination))

    def create_new_file(self):
        self.save_source(self.ids.save_as.text)

    def save_source(self, filename):
        try:
            Logger.debug("PCDPopUp:Creating new file as " + filename)
            write_file(self.path, filename, self.source)
        except Exception as ex:
            self.error(ex)