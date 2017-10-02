import ipaddress
from RemuTCP.RemuTCP import RemuTCP
from Domain.Message import Message
from Domain.PicPresentation import PicPresentation
from Domain.Command import Command

class SlaveConnection:

    def __init__(self, address, connection=None):
        if connection:
            self.connection = connection
        else:
            try:
                slave_address_parts = address.split(":")
                ipaddress.ip_address(slave_address_parts[0])
                if len(slave_address_parts) == 2:
                    self.connection = RemuTCP(self, True, slave_address_parts[0], int(slave_address_parts[1]))
                else:
                    self.connection = RemuTCP(self, True, slave_address_parts[0])
                print("Slave added")
            except ValueError as e:
                self.slaves = None
                print("Invalid IP-address or port")
                print(e)
        self.presentation = None

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
        self.__send_command(Command.REQUEST_PRESENTATION)

    """
        Ask slave to show next item in presentation
    """
    def show_next(self):
        self.__send_command(Command.SHOW_NEXT)

    """
        Called when slave responds to command "show_next"
        Advances presentation to next item
    """
    def response_next(self):
        self.currently_showing = self.presentation.get_next()

    def set_presentation(self, presentation):
        self.presentation = presentation

    def __isPresentationResponse(self, msg):
        if "response" in msg.fields and "responseTo" in msg.fields:
            response_command = msg.fields["responseTo"]
            return response_command == "request_presentation"
        return False


    def handle_presentation_response(self, data):
        presentation = PicPresentation()
        presentation.pic_index = data["pic_index"]
        presentation.pic_files = data["pic_files"]
        self.set_presentation(presentation)

    def handle_show_next_response(self, data):
        self.currently_showing = self.presentation.get_next()

    def handle_invalid_command_response(self, data):
        print("Invalid command given")

    handle_responses = {Command.REQUEST_PRESENTATION: handle_presentation_response,
                        Command.SHOW_NEXT: handle_show_next_response,
                        Command.INVALID_COMMAND: handle_invalid_command_response
                        }

    """
        Handles incoming messages
    """
    def handle_message(self, msg):
        print(msg.fields)
        if "responseTo" in msg.fields:
            if "data" in msg.fields:
                self.handle_responses[msg.get_command()](msg.get_data())
        #if self.__isPresentationResponse(msg):
        #    presentation = PicPresentation()
        #    presentation_fields = msg.fields["data"]
        #    presentation.pic_index = presentation_fields["pic_index"]
        #    presentation.pic_files = presentation_fields["pic_files"]
        #    self.set_presentation(presentation)
        #return response
