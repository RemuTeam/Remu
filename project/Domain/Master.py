import ipaddress
from Domain.SlaveConnection import SlaveConnection


class Master:

    def __init__(self, layout):
        self.slave_connection = None
        self.layout = layout

    """
        You can add slaves to master by using REMUTCP.py 
    """

    def add_slave(self, slave_address):
        self.slave_connection = SlaveConnection(slave_address)


    """
    Informs the layout on changes in connection
    """
    def notify_layout(self):
        self.layout.notify()


    def request_next(self):
        if self.slave_connection is not None:
            self.slave_connection.show_next()
