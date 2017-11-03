import os
from Domain.Presentation import Presentation
from Domain.PresentationType import PresentationType

"""
A PRESENTATION CLASS TO PRODUCE A PRESENTATION
CONTAINING TEXT OBJECTS
"""

class TextPresentation(Presentation):
    __PRESENTATION_TYPE = PresentationType.Text

    """
    Constructor

    initializes a list for text elements
    initializes the index to keep track of the element to show
    """
    def __init__(self):
        self.presentation_content = []
        self.index = 0

    """
    Populates the text element list from text file
    """
    def __populate_text_elements(self):
        if len(self.presentation_content) == 0:
            path = os.path.join(os.getcwd(), "texts")
            for filename in sorted(os.listdir(path)):
                relative_filename = "texts" + "/" + filename
                with open(relative_filename, "r") as file:
                    print(relative_filename)
                    self.__parse_text_file_to_list(file, self.presentation_content)

    """
    Parses a text file to a list.
    An empty line is used as a delimiter.
    
    file:               the file to read from
    list_to_populate:   the list to populate with strings
    """
    def __parse_text_file_to_list(self, file, list_to_populate):
        current_str = ""

        while True:
            line = file.readline()
            if not line:
                break
            current_str += line

        if current_str:
            list_to_populate.append(current_str)


    """
    Parses a delimited string to a list.
    The current_string is appended to if the line is not an empty string.
    If the line is an empty string, the current_string is appended to the list.
    
    current_str:        the current string to append to 
    line:               the line to append to the current_string
    list_to_populate:   the list to append the string to
    """
    @staticmethod
    def __parse_delimited_string_to_list(current_str, line, list_to_populate):
        if line == "\n":
            list_to_populate.append(current_str)
            return ""
        current_str += line
        return current_str

    """
    Requests for the next text element in the presentation
    
    returns:    a string
    """
    def get_next(self):
        return self.get(self.index)

    """
    Requests for a particular object in the presentation
    The next index is the next from the index that was requested

    index:      an integer, the index of the object in the presentation
    
    returns:    a string
    """
    def get(self, index):
        if -1 < index < len(self.presentation_content):
            next_element = self.presentation_content[index]
            self.index = index + 1
            return next_element
        else:
            return ""

    """
    Resets the presentation, returning it to the beginning
    """
    def reset(self):
        self.index = 0

    """
    Loads the presentation's elements and resets the presentation
    """
    def load(self):
        self.__populate_text_elements()
        self.reset()

    """
    Empties the list of text elements and reloads them again
    without resetting the presentation
    """
    def reload(self):
        del self.presentation_content[:]
        self.__populate_text_elements()

    """
    Sets the path and file name of the text file to open
    """
    def set_text_file_path_and_name(self, textfile):
        self.textfile = textfile

    """
    Request the type of the presentation

    returns the presentation's type
    """
    def get_presentation_type(self):
        return self.__PRESENTATION_TYPE

    """
    Request the content of the presentation
    """
    def get_presentation_content(self):
        return self.presentation_content