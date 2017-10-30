import ipaddress
from Networking.RemuTCP import RemuTCP
from Domain.Message import Message
from Domain.PicPresentation import PicPresentation
from Domain.Command import *
from Domain.MessageKeys import MessageKeys
from Domain.PresentationFactory import PresentationFactory
from functools import partial

"""
A class to handle one master-slave connection
"""
class SlaveConnection:

    """
    Constructor.

    Connection: a Networking object, if constructed beforehand
    """
    def __init__(self, master, connection=None):
        self.master = master
        self.set_connection(connection)
        self.presentation = None
        self.full_address = "localhost:8000"
        self.connected = self.connection is not None

    """
    Sets the connection to the slave
    """
    def set_connection(self, connection):
        self.connection = connection


    """
    Attempts to create a new Networking-connection with the provided IP address
    """
    def connect_to_IP(self, address):
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

    """
        Private function for sending commands
    """
    def __send_command(self, command, params=None):
        msg = Message()
        msg.set_field(MessageKeys.type_key, "command")
        msg.set_field(MessageKeys.command_key, command)
        msg.set_field(MessageKeys.params_key, params)
        self.connection.send_message(msg)


    """
        Requests the presentation-object from slave
    """
    def request_presentation(self):
        self.__send_command(Command.REQUEST_PRESENTATION.value)

    """
        Ask slave to show next item in presentation
    """
    def show_next(self):
        self.__send_command(Command.SHOW_NEXT.value)

    """
        Ask slave to reset the presentation and closes the connection to it.
    """
    def terminate_connection(self):
        self.__send_command(Command.DROP_CONNECTION.value)
        self.connection.end_connection()
        self.master.notify(Notification.CONNECTION_TERMINATED, self)

    """
        Called when slave responds to command "show_next"
        Advances presentation to next item
    """
    def response_next(self):
        self.currently_showing = self.presentation.get_next()

    """
        Sets the connection's presentation object
    """
    def set_presentation(self, presentation):
        self.presentation = presentation

    """
        Ends the current presentation
    """
    def end_presentation(self):
        self.__send_command(Command.END_PRESENTATION.value)

    """
    Creates a presentation based on the message received from master
    """
    def handle_presentation_response(self, data):
        presentation = None
        if MessageKeys.presentation_type_key in data and MessageKeys.presentation_content_key in data:
            presentation = PresentationFactory.CreatePresentation(data[MessageKeys.presentation_type_key], data[MessageKeys.presentation_content_key])
        self.set_presentation(presentation)
        self.master.notify(Notification.PRESENTATION_UPDATE, self)

    """
    Handles command to show next file
    """
    def handle_show_next_response(self, data=None):
        next_item = self.presentation.get_next()
        if next_item is None:
            self.presentation.reset()
        self.currently_showing = next_item
        self.master.notify(Notification.PRESENTATION_STATUS_CHANGE, next_item)

    """
    Resets the presentation on master's side, called when slave is told to 
    reset its presentation
    """
    def handle_ending_presentation(self, data=None):
        self.presentation.reset()

    """
    Invalid command handler, doesn't do anything useful except catch bad mistakes
    """
    def handle_invalid_command_response(self, data=None):
        print("Invalid command given")

    """
    Forwards the information of connection being established to master and its layout
    """
    def connection_established(self, full_address):
        self.connected = True
        self.master.notify(Notification.CONNECTION_ESTABLISHED, full_address)

    handle_responses = {Command.REQUEST_PRESENTATION.value: handle_presentation_response,
                        Command.SHOW_NEXT.value: handle_show_next_response,
                        Command.END_PRESENTATION.value: handle_ending_presentation,
                        Command.INVALID_COMMAND.value: handle_invalid_command_response
                        }

    """
        Handles incoming messages
    """
    def handle_message(self, msg):
        print(msg.fields)
        if MessageKeys.response_key in msg.fields:
            self.handle_responses[msg.get_response()](self, msg.fields)
                

    """
    Called from RemuTCP when the connection is lost; used to notify GUI of the status
    """
    def on_connection_lost(self):
        self.connected = False
        self.master.notify(Notification.CONNECTION_FAILED, self.full_address)
