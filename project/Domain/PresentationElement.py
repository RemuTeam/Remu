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
                self.content = file.readlines()
        else:
            self.content = self.source_file

    def get_content(self):
        return self.content