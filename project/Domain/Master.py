import ipaddress
from RemuTCP.RemuTCP import RemuTCP


class Master:

    def __init__(self):
        self.slave_connection = None

    """
        You can add slaves to master by using REMUTCP.py 
    """

    def add_slave(self, slave_address):
        slave_address_parts = slave_address.split(":")
        try:
            ipaddress.ip_address(slave_address_parts[0])
            if len(slave_address_parts) == 2:
                self.slaves = RemuTCP(self, True, slave_address_parts[0], int(slave_address_parts[1]))
            else:
                self.slaves = RemuTCP(self, True, slave_address_parts[0])
            print("Slave added")
        except ValueError as e:
            self.slaves = None
            print("Invalid IP-address or port")
            print(e)
