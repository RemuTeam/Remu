import os

from kivy.event import EventDispatcher

from Constants.FileHandlingMode import OpenProject
from Constants.SupportedFileTypes import ProjectFileFormats
from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from GUI.PopUps.PopUps import ExceptionAlertPopUp
from Utils.FileHandler import read_file
from Domain.Project import Project


class ProjectOpenPopUp(FileHandlerPopUp, EventDispatcher):
    """
    A project selecting and opening popup
    """

    def __init__(self, master, project_path, test_mode=False):
        """
        Constructs a pop up that is used to open a single saved project file.
        The filechooser view is filtered and shows only files with the extension ".remu"
        :param master: the Master object to connect the opened Project to
        :param project_path: the default path for opening a project
        :param test_mode: if True, the popup is opened in test mode, False by default
        """
        super(ProjectOpenPopUp, self).__init__(title="Open project",
                                               default_path=project_path,
                                               callback=self.open_project,
                                               callback_button_text="Open",
                                               file_handling_mode=OpenProject,
                                               filters=ProjectFileFormats)
        self.project_path = project_path
        self.master = master
        self.test_mode = test_mode

    def open_project(self, path, selection, savefilename=None):
        """
        A callback method to be called when the file to open has been selected
        by the user.
        :param path: the path to open the project file from
        :param selection: a list, the selected file will be in the first index
        :return: None
        """
        json_str = read_file(os.path.join(path, selection[0]))
        try:
            project = Project()
            project.load_json(json_str)
            self.master.setup_project(project)
            self.master.layout.clear_presentations()
            self.master.load_project_to_gui()
        except Exception as ex:
            ExceptionAlertPopUp("Error while opening project", ex).open()