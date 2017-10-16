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
    def __init__(self, layout=None):
        self.presentation = self.create_presentation()
        self.layout = layout
        self.master_connection = None
        self.source = ''

    """
    Sets the slave's master_connection, it is a listening RemuTCP connection
    """
    def set_master_connection(self, master_connection):
        self.master_connection = master_connection
        self.master_connection.parent = self

    def set_layout(self, new_layout):
        self.layout = new_layout

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
        return self.create_response(Command.REQUEST_PRESENTATION.value, self.presentation.__dict__)

    """
    Handles requests to show the next picture in the presentation, 
    uses a callback to tell the layout to update its view.
    Returns a confirmation to master
    """
    def handle_show_next(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        current = self.presentation.get_next()
        if self.layout:
            if current is not None:
                self.layout.show(current)
            else:
                self.layout.reset_presentation()

        return self.create_response(Command.SHOW_NEXT.value)


    """
    Handles invalid requests made by master, simply returns acknowledgement of 
    an invalid command without changing anything
    """
    def handle_invalid_command(self):
        return self.create_response(Command.INVALID_COMMAND.value)

    """
    Handles the ending of the presentation.
    """
    def handle_ending_presentation(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        self.layout.reset_presentation()

        return self.create_response(Command.END_PRESENTATION.value)

    """
    Handles master closing its connection to the slave, doesn't close slave's 
    listening and doesn't reply to the message because the master doesn't have
    a connection to the slave anymore
    """
    def handle_closing_connection(self):
        if not self.presentation.pic_files:
            self.presentation.get_filenames()
        self.layout.reset_presentation()

    """
    Creates a instance of Message based on the given command
    """
    def create_response(self, command, data=None):
        response = Message()
        response.set_field("responseTo", command)
        if data is not None:
            response.set_field("data", data)
        return response

    # Messagehandler
    """
    Python's replacement for a switch-case: gives methods given 
    by the Command-enumerator, essentially just a dictionary that has function calls
    """
    messagehandler = {Command.REQUEST_PRESENTATION.value: handle_request_presentation,
                      Command.SHOW_NEXT.value: handle_show_next,
                      Command.END_PRESENTATION.value: handle_ending_presentation,
                      Command.INVALID_COMMAND.value: handle_invalid_command,
                      Command.DROP_CONNECTION.value: handle_closing_connection
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


    """
    Uses a RemuTCP method to close the listening connection
    """
    def close_connections(self):
        self.master_connection.end_connection()
