from Domain.PicPresentation import PicPresentation
from Domain.Message import Message

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

    """
    Handles the responses to master's requests
    """
    def handle_message(self, msg):
        response = Message()
        if "command" in msg.fields:
            response.set_field("responseTo", msg.fields["command"])
            if msg.fields["command"] == "request_presentation":
                response.fields["data"] = self.presentation.__dict__
        return response

