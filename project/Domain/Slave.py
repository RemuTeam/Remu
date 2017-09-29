from Domain.PicPresentation import PicPresentation

"""
CONTAINS SLAVE'S ADMINISTRATIVE AND PRESENTATIONAL DATA
"""
class Slave:

    """
    Constructor
    The master_connection is a RemuTCP object
    """
    def __init__(self, master_connection=None):
        self.presentation = self.create_presentation()
        self.master_connection = master_connection

    """
    Sets the slave's master_connection
    """
    def set_master_connection(self, master_connection):
        self.master_connection = master_connection

    """
    Creates slave's presentation
    """
    def create_presentation(self):
        return PicPresentation()