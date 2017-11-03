from Domain.ContentType import ContentType

class PresentationElement():

    def __init__(self, type, source):
        self.type = type
        self.source_file = source
        self.content = None
        self.prepare_content()

    def prepare_content(self):
        if self.type == ContentType.Text:
            with open(self.source_file) as file:
                self.content = file.read()
        else:
            self.content = self.source_file

    def get_content(self):
        return self.content

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.type != other.type:
            return False
        if self.source_file is not other.source_file:
            return False
        return True
