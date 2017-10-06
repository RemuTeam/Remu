import ipaddress
from Domain.SlaveConnection import SlaveConnection
from Domain.Command import Notification

class Master:

    def __init__(self, layout):
        self.slave_connection = None
        self.layout = layout

    """
        You can add slaves to master by using REMUTCP.py 
    """

    def add_slave(self, slave_address):
        self.slave_connection = SlaveConnection(self)
        self.slave_connection.connect_to_IP(slave_address)

    def request_next(self):
        if self.slave_connection is not None:
            self.slave_connection.show_next()

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
            self.slave_connection.request_presentation()

    def close_connections(self):
        self.slave_connection.connection.end_connection()

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: update_presentation_status_to_layout,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status_to_layout,
                      Notification.CONNECTION_FAILED: update_connection,
                      Notification.CONNECTION_ESTABLISHED: update_connection}
