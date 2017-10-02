import ipaddress
from RemuTCP.RemuTCP import RemuTCP
from Domain.Message import Message
from Domain.PicPresentation import PicPresentation

"""
A class to handle one master-slave connection
"""
class SlaveConnection:

    """
    Constructor.

    Address: a string in format ip.add.res.s:port
    Connection: a RemuTCP object, if constructed beforehand
    """
    def __init__(self, address, connection=None):
        self.set_connection(address, connection)
        self.presentation = None

    """
    Sets up the connection to the slave
    """
    def set_connection(self, address, connection):
        if connection:
            self.connection = connection
        else:
            try:
                self.create_new_tcp_connection(address, connection)
                print("Slave added")
            except ValueError as e:
                self.slaves = None
                print("Invalid IP-address or port")
                print(e)

    """
    Attempts to create a new RemuTCP-connection
    """
    def create_new_tcp_connection(self, address, connection):
        slave_address_parts = address.split(":")
        ip_address = slave_address_parts[0] if len(slave_address_parts) > 0 else None
        port = slave_address_parts[1] if len(slave_address_parts) > 1 else None
        ipaddress.ip_address(ip_address)
        self.connection = RemuTCP(self, True, ip_address, port)

    """
        Private function for sending commands
    """
    def __send_command(self, command, params=None):
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", command)
        msg.set_field("params", params)
        self.connection.send_message(msg)

    """
        Requests the presentation-object from slave
    """
    def request_presentation(self):
        self.__send_command("request_presentation")

    """
        Ask slave to show next item in presentation
    """
    def show_next(self):
        self.__send_command("show_next")

    """
        Called when slave responds to command "show_next"
        Advances presentation to next item
    """
    def response_next(self):
        currently_showing = self.presentation.get_next()

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
        Handles incoming messages
    """
    def handle_message(self, msg):
        print(msg.fields)
        response = None
        if self.__isPresentationResponse(msg):
            presentation = PicPresentation()
            presentation_fields = msg.fields["data"]
            presentation.pic_index = presentation_fields["pic_index"]
            presentation.pic_files = presentation_fields["pic_files"]
            self.set_presentation(presentation)
        return response
