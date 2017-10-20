from Domain.Presentation import Presentation
from Domain.Message import Message
from Domain.Command import Command
from Domain.MessageKeys import MessageKeys

"""
CONTAINS SLAVE'S ADMINISTRATIVE AND PRESENTATIONAL DATA
"""
class Slave:

    """
    Constructor
    The master_connection is a RemuTCP object
    """
    def __init__(self, layout=None):
        self.presentation = Presentation()
        self.layout = layout
        self.master_connection = None
        self.source = ''

    """
    Sets the slave's master_connection
    """
    def set_master_connection(self, master_connection):
        self.master_connection = master_connection
        self.master_connection.parent = self

    def set_layout(self, new_layout):
        self.layout = new_layout

    def reset_presentation(self):
        self.source = ''
        self.presentation.reset()

    """
    Sets the slave's presentation
    """
    def set_presentation(self, presentation):
        self.presentation = presentation

    """
    Handles requests for the presentation made by the master, returns the
    presentation with the response
    """
    def handle_request_presentation(self):
        self.load_presentation()
        response = Message()
        response.set_field(MessageKeys.response_key, Command.REQUEST_PRESENTATION.value)
        response.set_field(MessageKeys.presentation_type_key, self.presentation.get_presentation_type().value)
        response.set_field(MessageKeys.presentation_content_key, self.presentation.__dict__)
        return response

    """
    Handles requests to show the next picture in the presentation, 
    uses a callback (NYI) to tell the layout to update its view.
    Returns a confirmation to master
    """
    def handle_show_next(self):
        self.load_presentation()
        current = self.presentation.get_next()
        self.layout.show(current)
        response = Message()
        response.set_field(MessageKeys.response_key, Command.SHOW_NEXT.value)
        return response

    """
    Handles invalid requests made by master, simply returns acknowledgement of 
    an invalid command without changing anything
    """
    def handle_invalid_command(self):
        response = Message()
        response.set_field(MessageKeys.response_key, Command.INVALID_COMMAND.value)
        return response

    """
    Handles the ending of the presentation.
    """
    def handle_ending_presentation(self):
        self.load_presentation()
        self.layout.reset_presentation()
        response = Message()
        response.set_field(MessageKeys.response_key, Command.END_PRESENTATION.value)
        return response

    # Messagehandler
    """
    Python's replacement for a switch-case: gives methods given 
    by the Command-enumerator, essentially just a dictionary that has function calls
    """
    messagehandler = {Command.REQUEST_PRESENTATION.value: handle_request_presentation,
                      Command.SHOW_NEXT.value: handle_show_next,
                      Command.END_PRESENTATION.value: handle_ending_presentation,
                      Command.INVALID_COMMAND.value: handle_invalid_command
                      }

    """
    Handles the responses to master's requests
    """
    def handle_message(self, msg):
        print("trying to parse")
        if MessageKeys.command_key in msg.fields:
            print(str(msg.get_command()))
            return self.messagehandler[msg.get_command()](self)
        return self.handle_invalid_command()

    def connection_established(self, address):
        pass

    def close_connections(self):
        self.master_connection.end_connection()

    """
    Returns the slave's presentation's PresentationType
    """
    def get_presentation_type(self):
        if self.presentation:
            return self.presentation.get_presentation_type()
        return None

    """
    Load the presentations content
    """
    def load_presentation(self):
        if not self.presentation.get_presentation_content():
            self.presentation.load()