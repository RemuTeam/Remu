from Domain.Presentation import Presentation
from Domain.Message import Message
from Domain.Command import Command
from Domain.MessageKeys import MessageKeys
from Networking.RemuUDP import Beacon
from Networking.RemuFTP import RemuFTPClient

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
        self.beacon = Beacon()
        self.beacon.start_beaconing()

    """
    Sets the slave's master_connection, it is a listening RemuTCP connection
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
    def handle_request_presentation(self, msg):
        self.beacon.stop_beaconing()
        self.load_presentation()
        metadata = {MessageKeys.response_key: Command.REQUEST_PRESENTATION.value,
                    MessageKeys.presentation_type_key: self.presentation.get_presentation_type().value,
                    MessageKeys.presentation_content_key: self.presentation.__dict__}
        return self.create_response(Command.REQUEST_PRESENTATION.value, metadata)

    """
    Handles requests to show the next picture in the presentation, 
    uses a callback to tell the layout to update its view.
    Returns a confirmation to master
    """
    def handle_show_next(self, msg):
        self.load_presentation()
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
    def handle_invalid_command(self, msg):
        return self.create_response(Command.INVALID_COMMAND.value)

    """
    Handles the ending of the presentation.
    """
    def handle_ending_presentation(self, msg):
        self.load_presentation()
        self.layout.reset_presentation()

        return self.create_response(Command.END_PRESENTATION.value)

    """
    Handles master closing its connection to the slave, doesn't close slave's 
    listening and doesn't reply to the message because the master doesn't have
    a connection to the slave anymore
    """
    def handle_closing_connection(self, msg):
        if self.presentation.get_presentation_content():
            self.presentation.reset()
        self.layout.reset_presentation()

    """
    Creates a instance of Message based on the given command
    """
    @staticmethod
    def create_response(command, metadata=None):
        resp = Message()
        resp.set_field(MessageKeys.response_key, command)
        if metadata is not None:
            for key, value in metadata.items():
                resp.set_field(key, value)
        return resp

    def retrieve_files_over_ftp(self, host, port, subpath):
        """
        Create a RemuFTPClient to retrieve files from a host

        :param host: the server's ip-address
        :param port: the server's port
        :param subpath: the subpath on the server to retrieve files from
        :return: doesn't return anything
        """
        client = RemuFTPClient(host, port, subpath, 'slave_presentation_path')
        client.connect()

    def handle_file_retrieval(self, msg):
        """
        Handles a command to retrieve files from a host

        :param msg: a Message object
        :return: a response to the received message
        """
        print("file retrieval")
        params = msg.get_field(MessageKeys.params_key)
        host = msg.get_field(MessageKeys.sender_key)
        port = params[MessageKeys.ftp_port_key]
        subpath = params[MessageKeys.ftp_subpath_key]
        self.retrieve_files_over_ftp(host, port, subpath)
        return self.create_response(msg.get_command())

    # Messagehandler
    """
    Python's replacement for a switch-case: gives methods given 
    by the Command-enumerator, essentially just a dictionary that has function calls
    """
    messagehandler = {Command.REQUEST_PRESENTATION.value: handle_request_presentation,
                      Command.SHOW_NEXT.value: handle_show_next,
                      Command.END_PRESENTATION.value: handle_ending_presentation,
                      Command.INVALID_COMMAND.value: handle_invalid_command,
                      Command.DROP_CONNECTION.value: handle_closing_connection,
                      Command.RETRIEVE_FILES.value: handle_file_retrieval
                      }

    """
    Handles the responses to master's requests
    """
    def handle_message(self, msg):
        print("trying to parse")
        if MessageKeys.command_key in msg.fields:
            print(str(msg.get_command()))
            return self.messagehandler[msg.get_command()](self, msg)
        return self.handle_invalid_command(msg)

    def connection_established(self, address):
        pass

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

    """
    Closes all networking protocols the slave uses
    """
    def close_all_connections(self):
        self.close_TCP_connections()
        self.close_UDP_connection()

    """
    Uses a RemuTCP method to close the listening connection
    """
    def close_TCP_connections(self):
        if self.master_connection is not None:
            self.master_connection.end_connection()

    """
    Uses a RemuUDP method to stop listening to the UDP connection
    """
    def close_UDP_connection(self):
        self.beacon.stop_beaconing()
