import os

from kivy.event import EventDispatcher

from Constants.FileHandlingMode import SaveProject
from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from Utils.FileHandler import write_file, get_filename_with_extension


class ProjectSavePopUp(FileHandlerPopUp, EventDispatcher):
    """
    A file selection and opening popup
    """

    def __init__(self, listener, project_path, test_mode=False):
        """
        Constructor

        :param listener: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ProjectSavePopUp, self).__init__(title="Save project",
                                               default_path=project_path,
                                               callback=self.save_project,
                                               callback_button_text="Save",
                                               file_handling_mode=SaveProject)
        self.project_path = project_path
        self.listener = listener
        self.test_mode = test_mode

    def save_project(self, path, dont_use_this_list, savefilename):
        """
        PLEASE IMPLEMENT ASAP!
        :param path:
        :param savefilename:
        :return:
        """
        filename_with_extension = get_filename_with_extension(savefilename, "remu")
        destination = os.path.join(path, filename_with_extension)
        source = self.listener.project.dump_json()
        if os.path.isfile(destination):
            FileSavingDialogPopUp(source, destination, None, self, path, source_is_file=False).open()
        else:
            write_file(path, filename_with_extension, source)
