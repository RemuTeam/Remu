import json
from Domain.Presentation import Presentation
from kivy.logger import Logger


class Project:
    """
    A project is a collection of presentations that should be shown simultaneously.
    """

    def __init__(self):
        """
        Creates an empty project, and initializes an empty list for presentations. Presentations are stored as a list of
        tuples, the first part of tuple being name of the presentation and the second part being an instance of
        presentation class.
        """
        self.presentations = []

    def remove_from_presentations(self, name):
        for presentation in self.presentations:
            if presentation[0] == name:
                self.presentations.remove(presentation)

    def dump_json(self):
        """
        Returns a json-formatted string representing the project.
        Presentation status is lost, only the presentation name and file contents are saved.
        This is intended to be used for saving the project as a file.
        :return: A json representation of the project.
        """
        # A list with presentation-objects replaced with the list of files in that project
        list_presentations = []
        for tuple in self.presentations:
            list_presentations.append((tuple[0], tuple[1].presentation_filenames))

        return json.dumps(list_presentations)

    def save_to_file(self, filename):
        """
        Writes the project to file as JSON.
        :param filename: file to be written
        :return: Nothing
        """
        json_string = self.dump_json()
        with open(filename, mode='w') as f:
            f.write(json_string)

    def load_from_file(self, filename):
        with open(filename, mode='r') as f:
            json_str = f.read()
            self.load_json(json_str)

    def load_json(self, json_str):
        """
        Load project from JSON.

        :param json_str: JSON-formatted string representing a project.
        :return: Nothing
        """

        # project_list elements are tuples containing presentation name and file contents
        # The format is ["presentationname", ["file1", "file2", ...]"]
        project_list = json.loads(json_str)

        # create the real presentations by replacing file list with Presentation objects
        presentation_list = []
        for presentation_tuple in project_list:
            name = presentation_tuple[0]
            files = presentation_tuple[1]
            pres = Presentation()
            pres.presentation_filenames = files
            presentation_list.append((name, pres))

        self.presentations = presentation_list
