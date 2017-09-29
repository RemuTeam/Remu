from RemuTCP.RemuTCP import RemuTCP
from Domain.Message import Message

class SlaveConnection:

    def __init__(self, ip_address, port, connection=None):
        if connection:
            self.connection = connection
        else:
            self.connection = RemuTCP(self, True, ip_address, port)
        self.presentation = None

    def request_presentation(self):
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", "request_presentation")
