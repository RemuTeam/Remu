from kivy.event import EventDispatcher

from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp
from Constants.FileHandlingMode import OpenProject


class ProjectOpenPopUp(FileHandlerPopUp, EventDispatcher):
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
        super(ProjectOpenPopUp, self).__init__(title="Open project",
                                               default_path=project_path,
                                               callback=self.open_project,
                                               callback_button_text="Open",
                                               file_handling_mode=OpenProject)
        self.project_path = project_path
        self.listener = listener
        self.test_mode = test_mode

    def open_project(self, path, selection, savefilename=None):
        """
        IMPLEMENT ME ASAP!
        :param path:
        :param selection:
        :return:
        """
        print("PLEASE IMPLEMENT ME!")