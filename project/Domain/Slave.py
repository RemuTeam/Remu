from Domain.PicPresentation import PicPresentation
from Domain.Message import Message
from Domain.Command import Command

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

    def handle_request_presentation(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        response = Message()
        response.set_field("responseTo", Command.REQUEST_PRESENTATION)
        response.set_field("data", self.presentation.__dict__)
        return response

    def handle_show_next(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        file = self.presentation.get_next()
        response = Message()
        response.set_field("responseTo", Command.SHOW_NEXT)
        return response

    def handle_invalid_command(self):
        response = Message()
        response.set_field("responseTo", Command.INVALID_COMMAND)
        return response

    # Messagehandler
    messagehandler = {Command.REQUEST_PRESENTATION: handle_request_presentation,
                      Command.SHOW_NEXT: handle_show_next,
                      Command.INVALID_COMMAND: handle_invalid_command
                      }

    """
    Handles the responses to master's requests
    """
    def handle_message(self, msg):
        if "command" in msg.fields:
            return self.messagehandler[msg.get_command()](self)
        return self.handle_invalid_command()


