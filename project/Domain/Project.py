import json
from Domain.Presentation import Presentation
from kivy.logger import Logger

class Project:
    """
    A project is a collection of presentations that should be shown simultaneously.
    """

    def __init__(self):
        """
        Creates an empty project
        """
        self.presentations = [] #Lista tupleja, muodossa [(esityksenNimi, presentation), (toisenEsityksenNimi, toinenPresentation)]

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

    # POISTA JOSKUS JOOKO
    def create_test_presentation(self):
        Logger.warn("Project: create_test_presentation: PLEASE DELETE THIS AFTER EVERYTHING WORKS!")
        name1 = "bullshit"
        presentation1 = Presentation()
        presentation1.set_files(["a.jpg", "b.jpg"])

        name2 = "wtf"
        presentation2 = Presentation()
        presentation2.set_files(["b.jpg", "a.jpg"])

        self.presentations.append((name1, presentation1))
        self.presentations.append((name2, presentation2))