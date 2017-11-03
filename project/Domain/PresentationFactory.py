from Domain.TextPresentation import TextPresentation
from Domain.PicPresentation import PicPresentation
from Domain.PresentationType import PresentationType

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
    def CreatePresentation(type, entries):
        presentation = None
        if type == PresentationType.Image.value:
            presentation = PresentationFactory.PicPresentation()
        elif type == PresentationType.Text.value:
            presentation = PresentationFactory.TextPresentation()
        if presentation:
            presentation.__dict__.update(entries)
        return presentation