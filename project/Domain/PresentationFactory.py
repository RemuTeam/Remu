from Domain.TextPresentation import TextPresentation
from Domain.PicPresentation import PicPresentation
from Domain.ContentType import ContentType

"""
Creates predefined presentation objects that inherit
Presentation interface
"""
class PresentationFactory:
    """
    Creates a TextPresentation and returns it
    """
    @staticmethod
    def TextPresentation():
        presentation = TextPresentation()
        return presentation

    """
    Creates a PicPresentation and returns it
    """
    @staticmethod
    def PicPresentation():
        presentation = PicPresentation()
        return presentation

    """
    Creates a Presentation based on the PresentationType given.
    Uses the parameter entries to update the presentation contents.
    """
    @staticmethod
    def CreatePresentation(entries):
        presentation = PresentationFactory.PicPresentation()
        presentation.add_elements(entries)

        return presentation