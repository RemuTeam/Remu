import ipaddress
from Domain.SlaveConnection import SlaveConnection


class Master:

    def __init__(self):
        self.slave_connection = None

    """
        You can add slaves to master by using REMUTCP.py 
    """

    def add_slave(self, slave_address):
        self.slave_connection = SlaveConnection(slave_address)
