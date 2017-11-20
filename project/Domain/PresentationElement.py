from Domain.ContentType import ContentType

class PresentationElement():
    """
    PresentationElement represents a single image, text or video element in a slave's presentation. It contains the
    the information about its type and source.

    If the element is a text file, the text is extracted into a string and referenced via self.content. Otherwise, the
    content refers to the path of the source file.
    """

    def __init__(self, element_type, source):
        self.element_type = element_type
        self.source_file = source
        self.content = None
        self.prepare_content()

    def prepare_content(self):
        """
        Prepares the content to be passed on to GUI. If the element is a text file, the text is extracted into a string
        and referenced via self.content. Otherwise, the content refers to the path of the source file.

        :return: Nothing
        """
        if self.element_type == ContentType.Text:
            with open(self.source_file) as file:
                self.content = file.read()
        else:
            self.content = self.source_file

    def get_content(self):
        return self.content

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.element_type != other.element_type:
            return False
        if self.source_file is not other.source_file:
            return False
        return True
