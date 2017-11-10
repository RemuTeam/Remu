from Domain.SlaveConnection import SlaveConnection
from Domain.Command import Notification
from Networking.RemuUDP import MasterUDPListener
from Networking.RemuFTP import RemuFTPServer

class Master:
    """
    A service mode class that contains the master device's functionality
    """

    def __init__(self, layout):
        """
        Constructor

        :param layout: the layout to be notified on changes
        """
        self.slave_connections = {}
        self.layout = layout
        self.FTPServer = None
        self.UDPListener = None

    def start_ftp_server(self, path, port):
        """
        Starts an FTP server in a designated path and port

        :param path: a string, the root path of the ftp server, e.g. './media'
        :param port: an integer, the port to listen to
        :return: None
        """
        self.FTPServer = RemuFTPServer(path, port)
        self.FTPServer.start()

    def start_udp_listening(self):
        """
        Starts listening for UDP broadcast

        :return: None
        """
        self.UDPListener = MasterUDPListener(self)
        self.UDPListener.listen_for_beacons()

    """
    Adds a slave connection by creating a new RemuTCP object
    and adding it to the dictionary self.slave_connections
    
    address: an ip-string formatted as "ipa.ddr.es.s:port"
    """
    def add_slave(self, slave_address):
        slave_to_connect = SlaveConnection(self)
        slave_to_connect.connect_to_IP(slave_address)
        self.slave_connections[slave_to_connect.full_address] = slave_to_connect

    """
    Adds a pre-constructed SlaveConnection object to slave_connections
    
    slave_connection: SlaveConnection object
    """
    def add_slave_connection(self, slave_connection):
        self.slave_connections[slave_connection.full_address] = slave_connection

    """
    Asks the slaves to show their next visuals
    """
    def request_next(self):
        for connection in self.slave_connections.values():
            connection.show_next()

    """
    Requests a slave to retrieve presentation files from the master
    
    connection: the SlaveConnection to make the request to
    subpath:    the path to the files under the root folder
    """
    def request_retrieve_presentation_files(self, connection, subpath="."):
        connection.retrieve_presentation_files(self.FTPServer.get_port(), subpath)

    """
    Asks a slave to show their next visual.
    Slave is chosen by its IP-address
    """
    def request_specific_next(self, address):
        if self.slave_connections[address]:
            self.slave_connections[address].show_next()
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
    def update_connection(self, notification, full_address):
        self.layout.notify(notification, full_address)
        if notification == Notification.CONNECTION_ESTABLISHED:
            print("Connection established")
            # print("now asking for the presentation")
            # self.slave_connections[full_address].request_presentation()
            #print("informing slave to retrieve media")
            #self.slave_connections[full_address].retrieve_presentation_files(8005, '.')

        if notification == Notification.CONNECTION_FAILED:
            self.layout.update_presentation_status(full_address)

    """
    Removes the knowledge of a slave from master and notifies GUI of the change
    """
    def remove_slave(self, notification, data):
        if data.full_address in self.slave_connections:
            self.slave_connections.pop(data.full_address, None)
        self.layout.notify(notification, data)

    def send_presentations_to_slaves(self):
        presentations = [["a.jpg", "b.jpg"], ["g.mp4", "a.jpg"]]
        i = 0
        for slavec in self.slave_connections.values():
            presentation = presentations[i%2]
            i += 1
            slavec.retrieve_presentation_files(8005, '.', presentation)


    """
    Informs the slave connection about the presentation ending
    """
    def end_presentation(self):
        for slave in self.slave_connections.values():
            slave.end_presentation()

    """
    Closes all connections to slaves
    """
    def close_all_connections(self):
        self.close_TCP_connections()
        self.close_UDP_connection()
        self.close_FTP_connection()

    """
    Closes all connections to slaves
    """
    def close_TCP_connections(self):
        for slave in self.slave_connections.values():
            slave.connection.end_connection()

    """
    Shuts down the FTP server
    """
    def close_FTP_connection(self):
        if self.FTPServer is not None:
            self.FTPServer.stop()

    """
    Closes the master's UDP protocol
    """
    def close_UDP_connection(self):
        if self.UDPListener is not None:
            self.UDPListener.stop_listening_to_beacons()

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: update_presentation_status_to_layout,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status_to_layout,
                      Notification.PRESENTATION_ENDED: end_presentation,
                      Notification.CONNECTION_FAILED: update_connection,
                      Notification.CONNECTION_ESTABLISHED: update_connection,
                      Notification.CONNECTION_TERMINATED: remove_slave}
