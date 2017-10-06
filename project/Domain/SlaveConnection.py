import ipaddress
from RemuTCP.RemuTCP import RemuTCP
from Domain.Message import Message
from Domain.PicPresentation import PicPresentation
from Domain.Command import *
from functools import partial

"""
A class to handle one master-slave connection
"""
class SlaveConnection:

    """
    Constructor.

    Connection: a RemuTCP object, if constructed beforehand
    """
    def __init__(self, master, connection=None):
        self.master = master
        self.set_connection(connection)
        self.presentation = None

    """
    Sets the connection to the slave
    """
    def set_connection(self, connection):
        self.connection = connection

    """
    Attempts to create a new RemuTCP-connection with the provided IP address
    """
    def connect_to_IP(self, address):
        try:
            slave_address_parts = address.split(":")
            ip_address = slave_address_parts[0] if len(slave_address_parts) > 0 else None
            port = slave_address_parts[1] if len(slave_address_parts) > 1 else None
            ipaddress.ip_address(ip_address)
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
        msg.set_field("type", "command")
        msg.set_field("command", command)
        msg.set_field("params", params)
        self.connection.send_message(msg)

    def loseConnection(self):
        self.connection = None

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

    def __isPresentationResponse(self, msg):
        if "response" in msg.fields and "responseTo" in msg.fields:
            response_command = msg.fields["responseTo"]
            return response_command == "request_presentation"
        return False

    """
    Creates a presentation based on the message received from master
    """
    def handle_presentation_response(self, data):
        presentation = PicPresentation()
        presentation.pic_index = data["pic_index"]
        presentation.pic_files = data["pic_files"]
        self.set_presentation(presentation)
        self.master.notify(Notification.PRESENTATION_UPDATE, self.presentation)

    """
    Handles command to show next file
    """
    def handle_show_next_response(self, data=None):
        next_item = self.presentation.get_next()
        self.currently_showing = next_item
        self.master.notify(Notification.PRESENTATION_STATUS_CHANGE, next_item)

    def handle_invalid_command_response(self, data=None):
        print("Invalid command given")

    def connection_established(self, address):
        self.master.notify(Notification.CONNECTION_ESTABLISHED, address)

    handle_responses = {Command.REQUEST_PRESENTATION.value: partial(handle_presentation_response),
                        Command.SHOW_NEXT.value: partial(handle_show_next_response),
                        Command.INVALID_COMMAND.value: partial(handle_invalid_command_response)
                        }

    """
        Handles incoming messages
    """
    def handle_message(self, msg):
        print(msg.fields)
        if "responseTo" in msg.fields:
            if "data" in msg.fields:
                self.handle_responses[msg.get_field("responseTo")](self, msg.get_data())
        #if self.__isPresentationResponse(msg):
        #    presentation = PicPresentation()
        #    presentation_fields = msg.fields["data"]
        #    presentation.pic_index = presentation_fields["pic_index"]
        #    presentation.pic_files = presentation_fields["pic_files"]
        #    self.set_presentation(presentation)
        #return response
