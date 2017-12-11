import os

from kivy.event import EventDispatcher

from Constants.FileHandlingMode import SaveProject
from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from GUI.PopUps.ProjectCopyDialogPopUp import ProjectCopyDialogPopUp
from Utils.FileHandler import write_file, get_filename_with_extension


class ProjectSavePopUp(FileHandlerPopUp, EventDispatcher):
    """
    A Remu Project saving popup
    """

    def __init__(self, master, project_path, test_mode=False):
        """
        Contructor
        :param master: the Master object the Project is connected to
        :param project_path: the default project path
        :param test_mode: if True, the popup is opened in test mode, False by default
        """
        super(ProjectSavePopUp, self).__init__(title="Save project",
                                               default_path=project_path,
                                               callback=self.save_project,
                                               callback_button_text="Save",
                                               file_handling_mode=SaveProject)
        self.project_path = project_path
        self.master = master
        self.test_mode = test_mode

    def save_project(self, path, selection, savefilename):
        """
        A callback method to be called when a project is saved
        :param path: the path to save the project to
        :param selection: a selection of files, not used
        :param savefilename: the name of the project file to be saved
        :return: None
        """
        filename_with_extension = get_filename_with_extension(savefilename, "remu")
        destination = os.path.join(path, filename_with_extension)
        source = self.master.project.dump_json()
        if os.path.isfile(destination):
            ProjectCopyDialogPopUp(source, destination, self, path).open()
        else:
            write_file(path, filename_with_extension, source)
