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

    """
    Handles requests for the presentation made by the master, returns the
    presentation with the response
    """
    def handle_request_presentation(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        response = Message()
        response.set_field("responseTo", Command.REQUEST_PRESENTATION.value)
        response.set_field("data", self.presentation.__dict__)
        return response

    """
    Handles requests to show the next picture in the presentation, 
    uses a callback (NYI) to tell the layout to update its view.
    Returns a confirmation to master
    """
    def handle_show_next(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        file = self.presentation.get_next()
        response = Message()
        response.set_field("responseTo", Command.SHOW_NEXT.value)
        return response

    """
    Handles invalid requests made by master, simply returns acknowledgement of 
    an invalid command without changing anything
    """
    def handle_invalid_command(self):
        response = Message()
        response.set_field("responseTo", Command.INVALID_COMMAND.value)
        return response

    # Messagehandler
    """
    Python's replacement for a switch-case: gives methods given 
    by the Command-enumerator, essentially just a dictionary that has function calls
    """
    messagehandler = {Command.REQUEST_PRESENTATION.value: handle_request_presentation,
                      Command.SHOW_NEXT.value: handle_show_next,
                      Command.INVALID_COMMAND.value: handle_invalid_command
                      }

    """
    Handles the responses to master's requests
    """
    def handle_message(self, msg):
        print("trying to parse")
        if "command" in msg.fields:
            print(str(msg.get_command()))
            return self.messagehandler[msg.get_command()](self)
        return self.handle_invalid_command()

    def connection_established(self, address):
        pass
