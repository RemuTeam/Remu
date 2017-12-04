from kivy.event import EventDispatcher

from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from Constants.FileHandlingMode import OpenProject
from Constants.FileHandler import read_file
import os


class ProjectOpenPopUp(FileHandlerPopUp, EventDispatcher):
    """
    A file selection and opening popup
    """

    def __init__(self, master, project_path, test_mode=False):
        """
        Constructor

        :param master: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ProjectOpenPopUp, self).__init__(title="Open project",
                                               default_path=project_path,
                                               callback=self.open_project,
                                               callback_button_text="Open",
                                               file_handling_mode=OpenProject)
        self.project_path = project_path
        self.master = master
        self.test_mode = test_mode

    def open_project(self, path, selection, savefilename=None):
        """
        IMPLEMENT ME ASAP!
        :param path:
        :param selection:
        :return:
        """
        json_str = read_file(os.path.join(path, selection[0]))
        self.master.project.load_json(json_str)
        self.master.layout.clear_presentations()
        self.master.load_project_to_gui()