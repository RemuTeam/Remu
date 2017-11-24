import ipaddress
from Networking.RemuTCP import RemuTCP
from Domain.Message import Message
from Domain.Command import *
from Domain.MessageKeys import MessageKeys
from Domain.Presentation import Presentation
from functools import partial


class SlaveConnection:
    """
    A class to handle one master-slave connection
    """

    def __init__(self, master, slave_name=None, connection=None):
        """
        Constructor.

        Connection: a Networking object, if constructed beforehand
        """
        self.master = master
        self.set_connection(connection)
        self.presentation = None
        self.full_address = "localhost:8000"
        self.slave_name = slave_name
        self.connected = self.connection is not None
        self.currently_showing = -1

    def set_connection(self, connection):
        """
        Sets the connection to the slave
        """
        self.connection = connection

    def connect_to_IP(self, address):
        """
        Attempts to create a new Networking-connection with the provided IP address
        """
        try:
            slave_address_parts = address.split(":")
            ip_address = slave_address_parts[0] if len(slave_address_parts) > 0 else None
            port = slave_address_parts[1] if len(slave_address_parts) > 1 else 8000
            ipaddress.ip_address(ip_address)
            self.full_address = ip_address + ":" + str(port)
            self.connection = RemuTCP(self, True, ip_address, int(port))
            print("Slave added")
        except ValueError as e:
            self.connection = None
            print("Invalid IP-address or port")
            print(e)

    def __send_command(self, command, params=None):
        """
        Private function for sending commands
        """
        if self.connection:
            msg = Message()
            print(params)
            msg.set_field(MessageKeys.type_key, "command")
            msg.set_field(MessageKeys.command_key, command)
            msg.set_field(MessageKeys.params_key, params)
            self.connection.send_message(msg)

    def request_presentation(self):
        """
        Requests the presentation-object from slave
        """
        self.__send_command(Command.REQUEST_PRESENTATION.value)

    def show_next(self):
        """
        Ask slave to show next item in presentation
        """
        self.__send_command(Command.SHOW_NEXT.value)

    def terminate_connection(self):
        """
        Ask slave to reset the presentation and closes the connection to it.
        """
        self.__send_command(Command.DROP_CONNECTION.value)
        self.connection.end_connection() if self.connection else None
        self.master.notify(Notification.CONNECTION_TERMINATED, self)

    def set_presentation(self, presentation):
        """
        Sets the connection's presentation object
        """
        self.presentation = presentation

    def send_presentation(self, presentation_filenames):
        self.set_presentation(presentation_filenames)
        params = {}
        params[MessageKeys.presentation_content_key] = presentation_filenames

        self.__send_command(Command.SEND_PRESENTATION.value, params)

    def end_presentation(self):
        """
        Ends the current presentation
        """
        self.__send_command(Command.END_PRESENTATION.value)

    def retrieve_presentation_files(self, port, subpath, filenames):
        self.presentation = filenames
        params = {MessageKeys.ftp_port_key: port,
                  MessageKeys.ftp_subpath_key: subpath,
                  MessageKeys.presentation_content_key: filenames}
        self.__send_command(Command.RETRIEVE_FILES.value, params)

    def handle_presentation_response(self, data):
        """
        Creates a presentation based on the message received from master
        """
        presentation = None
        if MessageKeys.presentation_content_key in data:
            presentation = Presentation.CreatePresentation(data[MessageKeys.presentation_content_key])
        self.set_presentation(presentation)
        self.master.notify(Notification.PRESENTATION_UPDATE, self)

    def handle_show_next_response(self, response=None):
        """
        Handles command to show next file
        """
        self.currently_showing = response[MessageKeys.index_key]
        self.master.notify(Notification.PRESENTATION_STATUS_CHANGE, self.currently_showing)

    def handle_ending_presentation(self, data=None):
        """
        Resets the presentation on master's side, called when slave is told to
        reset its presentation
        """
        self.currently_showing = -1


    def handle_invalid_command_response(self, data=None):
        """
        Invalid command handler, doesn't do anything useful except catch bad mistakes
        """
        print("Invalid command given")

    def handle_retrieve_files_response(self, fields):
        print("Slave", fields["sender"], "retrieved files, yay!")

    def connection_established(self, full_address):
        """
        Forwards the information of connection being established to master and its layout
        """
        self.connected = True
        self.master.notify(Notification.CONNECTION_ESTABLISHED, full_address)

    handle_responses = {Command.REQUEST_PRESENTATION.value: handle_presentation_response,
                        Command.SHOW_NEXT.value: handle_show_next_response,
                        Command.END_PRESENTATION.value: handle_ending_presentation,
                        Command.INVALID_COMMAND.value: handle_invalid_command_response,
                        Command.RETRIEVE_FILES.value: handle_retrieve_files_response
                        }

    def handle_message(self, msg):
        """
        Handles incoming messages
        """
        print(msg.fields)
        if MessageKeys.response_key in msg.fields:
            self.handle_responses[msg.get_response()](self, msg.fields)

    def on_connection_lost(self):
        """
        Called from RemuTCP when the connection is lost; used to notify GUI of the status
        """
        self.connected = False
        self.master.notify(Notification.CONNECTION_FAILED, self.full_address)
