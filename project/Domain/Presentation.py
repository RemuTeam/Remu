"""
DEFINES A UNIFIED INTERFACE
FOR ALL SPECIALIZED PRESENTATIONS
"""
class Presentation:

    """
    Requests for the next object in the presentation
    """
    def get_next(self):
        pass

    """
    Requests for a particular object in the presentation
    
    index:  an integer, the index of the object in the presentation
    """
    def get(self, index):
        pass

    """
    Resets the presentation, returning it to the beginning
    """
    def reset(self):
        pass

    """
    Loads the presentation's elements and resets the presentation
    """
    def load(self):
        pass

    """
    Requests the presentation to reload its elements without 
    """
    def reload(self):
        pass