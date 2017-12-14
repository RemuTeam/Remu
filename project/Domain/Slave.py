import os

from Constants.Command import Command
from Constants.PathConstants import PathConstants
from kivy.app import App

from Constants.MessageKeys import MessageKeys
from Domain.Message import Message
from Domain.Presentation import Presentation
from Networking.RemuFTP import RemuFTPClient
from Networking.RemuUDP import Beacon
from kivy.logger import Logger


class Slave:
    """
    CONTAINS SLAVE'S ADMINISTRATIVE AND PRESENTATIONAL DATA
    """

    def __init__(self, layout=None):
        """
        Constructor
        The master_connection is a RemuTCP object
        """
        self.presentation_ended = False
        self.presentation = Presentation()
        self.layout = layout
        self.master_connection = None
        self.source = ''
        self.beacon = Beacon()
        self.beacon.start_beaconing()

    def set_master_connection(self, master_connection):
        """
        Sets the slave's master_connection, it is a listening RemuTCP connection
        """
        self.master_connection = master_connection
        self.master_connection.parent = self

    def set_layout(self, new_layout):
        self.layout = new_layout

    def reset_presentation(self):
        self.source = ''
        self.presentation.reset()

    def notify_file_transfer_completed(self):
        """
        Is used when the file transfer is ready to load the presentation
        :return: Nothing
        """
        self.presentation.load() if len(self.presentation.presentation_elements) == 0 else self.presentation.reload()

    def set_presentation(self, presentation):
        """
        Sets the slave's presentation
        """
        self.presentation = presentation

    def handle_show_next(self, msg):
        """
        Handles requests to show the next picture in the presentation,
        uses a callback to tell the layout to update its view.
        Returns a confirmation to master
        """
        if self.presentation_ended:
            return self.create_response(Command.SHOW_NEXT.value, {MessageKeys.index_key: -1})
        #self.load_presentation()
        current = self.presentation.get_next()
        if self.layout:
            if current is not None:
                self.layout.set_visible_widget(current)
            else:
                Logger.debug("Slave: Presentation ended")
                self.presentation_ended = True
                self.layout.reset_presentation()

        return self.create_response(Command.SHOW_NEXT.value, {MessageKeys.index_key: self.presentation.index})

    def handle_invalid_command(self, msg):
        """
        Handles invalid requests made by master, simply returns acknowledgement of
        an invalid command without changing anything
        """
        return self.create_response(Command.INVALID_COMMAND.value)

    def handle_ending_presentation(self, msg):
        """
        Handles the ending of the presentation.
        """
        app = App.get_running_app()

        self.load_presentation()
        self.layout.reset_presentation()
        if app.root is not None: #This is an ugly hack to make the tests work. Don't delete pls. Thank you.
            self.layout = app.root.get_current_layout()
        self.presentation_ended = True
        return self.create_response(Command.END_PRESENTATION.value)

    def handle_closing_connection(self, msg):
        """
        Handles master closing its connection to the slave, doesn't close slave's
        listening and doesn't reply to the message because the master doesn't have
        a connection to the slave anymore
        """
        if self.presentation.get_presentation_content():
            self.presentation.reset()
        self.layout.reset_presentation()

    @staticmethod
    def create_response(command, metadata=None):
        """
        Creates a instance of Message based on the given command
        """
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
        write_path = os.path.join(os.getcwd(), PathConstants.MEDIA_FOLDER)
        if not os.path.isdir(write_path):
            os.mkdir(write_path)
        client = RemuFTPClient(host, port, subpath, write_path, self)
        client.connect()

    def handle_file_retrieval(self, msg):
        """
        Handles a command to retrieve files from a host

        :param msg: a Message object
        :return: a response to the received message
        """
        Logger.info("Slave: Retrieving files")
        params = msg.get_field(MessageKeys.params_key)
        host = msg.get_field(MessageKeys.sender_key)
        port = params[MessageKeys.ftp_port_key]
        subpath = params[MessageKeys.ftp_subpath_key]
        self.presentation.set_files(params[MessageKeys.presentation_content_key])
        self.presentation.reset()
        self.layout.init_presentation()
        self.retrieve_files_over_ftp(host, port, subpath)
        self.presentation_ended = False
        return self.create_response(msg.get_command())

    def handle_received_presentation(self, msg):
        """Deprecated"""
        pass
        #print("Presentation received")
        #if MessageKeys.presentation_content_key in msg.fields:
        #    print("asd")

    # Messagehandler
    """
    Python's replacement for a switch-case: gives methods given 
    by the Command-enumerator, essentially just a dictionary that has function calls
    """
    messagehandler = {Command.SHOW_NEXT.value: handle_show_next,
                      Command.END_PRESENTATION.value: handle_ending_presentation,
                      Command.INVALID_COMMAND.value: handle_invalid_command,
                      Command.DROP_CONNECTION.value: handle_closing_connection,
                      Command.RETRIEVE_FILES.value: handle_file_retrieval,
                      #Command.SEND_PRESENTATION.value: handle_received_presentation
                      }

    def handle_message(self, msg):
        """
        Handles the responses to master's requests
        """
        Logger.debug("Slave: Trying to parse")
        if MessageKeys.command_key in msg.fields:
            Logger.info("Slave: Message command: %s", str(msg.get_command()))
            return self.messagehandler[msg.get_command()](self, msg)
        return self.handle_invalid_command(msg)

    def connection_established(self, address):
        pass

    def load_presentation(self):
        """
        Load the presentations content
        """
        if len(self.presentation.get_presentation_content()) == 0:
            self.presentation.load()

    def close_all_connections(self):
        """
        Closes all networking protocols the slave uses
        """
        self.close_TCP_connections()
        self.close_UDP_connection()

    def close_TCP_connections(self):
        """
        Uses a RemuTCP method to close the listening connection
        """
        if self.master_connection is not None:
            self.master_connection.end_connection()

    def close_UDP_connection(self):
        """
        Uses a RemuUDP method to stop listening to the UDP connection
        """
        self.beacon.stop_beaconing()

    def handle_exception(self, message, exception):
        self.layout.error(message, exception)
