import ipaddress
from Domain.SlaveConnection import SlaveConnection
from Domain.Command import Notification

class Master:

    """
    Constructor

    layout: the layout to be notified on changes
    """
    def __init__(self, layout):
        self.slave_connection = []
        self.layout = layout

    """
    Adds a slave connection by creating a new RemuTCP object
    and appending it to self.slave_connection
    
    address: an ip-string formatted as "ipa.ddr.es.s:port"
    """
    def add_slave(self, slave_address):
        slave_to_connect = SlaveConnection(self)
        slave_to_connect.connect_to_IP(slave_address)
        self.slave_connection.append(slave_to_connect)

    """
    Adds a pre-constructed SlaveConnection object to slave_connections
    
    slave_connection: SlaveConnection object
    """
    def add_slave_connection(self, slave_connection):
        self.slave_connection.append(slave_connection)

    """
    Asks the slaves to show their next visuals
    """
    def request_next(self):
        for i in range(0, len(self.slave_connection)):
            self.slave_connection[i].show_next()

    """
    Handles the received notification from a slave connection

    notification:   a Notification enum
    data:           an object
    """
    def notify(self, notification, data):
        return self.messagehandler[notification](self, notification, data)

    """
    Handles a presentation status update event
    
    notification:   a Notification enum object instance
    data:           an object instance
    """
    def update_presentation_status_to_layout(self, notification, data):
        self.layout.notify(notification, data)

    """
    Handles a connection update event
    
    notification:   a Notification enum object instance
    data:           an object instance
    """
    def update_connection(self, notification, data):
        self.layout.notify(notification, data)
        if notification == Notification.CONNECTION_ESTABLISHED:
            print("now asking for the presentation")
            for i in range(0, len(self.slave_connection)):
                self.slave_connection[i].request_presentation()

    """
    Informs the slave connection about the presentation ending
    """
    def end_presentation(self):
        if self.slave_connection is not None:
            for i in range(0, len(self.slave_connection)):
                self.slave_connection[i].end_presentation()

    """
    Closes all connections to slaves
    """
    def close_connections(self):
        if self.slave_connection is not None:
            for i in range(0, len(self.slave_connection)):
                self.slave_connection[i].connection.end_connection()

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: update_presentation_status_to_layout,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status_to_layout,
                      Notification.PRESENTATION_ENDED: end_presentation,
                      Notification.CONNECTION_FAILED: update_connection,
                      Notification.CONNECTION_ESTABLISHED: update_connection}
