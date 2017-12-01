from kivy.app import App

from Constants.Command import Notification
from Domain.SlaveConnection import SlaveConnection
from Networking.RemuFTP import RemuFTPServer
from Networking.RemuUDP import MasterUDPListener
from kivy.logger import Logger


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
        self.presentations = []
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
        config = App.get_running_app().config
        udp_port = config.getint('udp port')
        Logger.info("UDP port: %s", udp_port)
        self.UDPListener = MasterUDPListener(self)
        self.UDPListener.listen_for_beacons()

    def add_slave(self, slave_address, slave_name=None):
        """
        Adds a slave connection by creating a new RemuTCP object
        and adding it to the dictionary self.slave_connections

        address: an ip-string formatted as "ipa.ddr.es.s:port"
        """
        slave_to_connect = SlaveConnection(self, slave_name)
        slave_to_connect.connect_to_IP(slave_address)
        self.slave_connections[slave_name] = slave_to_connect

        #self.layout.notify(Notification.PRESENTATION_UPDATE, slave_to_connect)
        Logger.debug("Master: Slave length: %s", str(len(self.slave_connections)))
        Logger.debug("Master: Presentation length: %s", str(len(self.presentations)))

        if len(self.slave_connections) >= len(self.presentations) or True:
            self.layout.notify(Notification.PRESENTING_DISABLED, False)
        else:
            self.layout.notify(Notification.PRESENTING_DISABLED, True)

    def bind_slave_to_presentation(self, presentation, slaveconnection_to_bind):

        self.slave_connections[slaveconnection_to_bind].presentation = presentation
        #for slave_presentation in self.layout.ids.slave_overview.slave_presentations.values():
        #    self.presentations.append(slave_presentation.get_presentation_from_widgets())
        #presentation = self.presentations[0]
        #slave_to_bind.presentation = presentation

    def add_slave_connection(self, slave_connection):
        """
        Adds a pre-constructed SlaveConnection object to slave_connections

        slave_connection: SlaveConnection object
        """
        self.slave_connections[slave_connection.full_address] = slave_connection


    def request_next(self):
        """
        Asks the slaves to show their next visuals
        """
        for connection in self.slave_connections.values():
            connection.show_next()

    def request_retrieve_presentation_files(self, connection, subpath="."):
        """
        Requests a slave to retrieve presentation files from the master

        connection: the SlaveConnection to make the request to
        subpath:    the path to the files under the root folder
        """
        connection.retrieve_presentation_files(self.FTPServer.get_port(), subpath)

    def request_specific_next(self, address):
        """
        Asks a slave to show their next visual.
        Slave is chosen by its IP-address
        """
        if self.slave_connections[address]:
            self.slave_connections[address].visualize_next()

    def notify(self, notification, data):
        """
        Handles the received notification from a slave connection

        notification:   a Notification enum
        data:           an object
        """
        if notification == Notification.CONNECTION_ESTABLISHED:
            #self.layout.ids.slave_overview.slave_buttons['juuh'].on_release = self.slave_connections[data].show_next
            pass
        return self.messagehandler[notification](self, notification, data)

    def update_presentation_status_to_layout(self, notification, data):
        """
        Handles a presentation status update event

        notification:   a Notification enum object instance
        data:           an object instance
        """
        self.layout.notify(notification, data)

    def update_connection(self, notification, full_address):
        """
        Handles a connection update event

        notification:   a Notification enum object instance
        data:           an object instance
        """
        self.layout.notify(notification, full_address)
        if notification == Notification.CONNECTION_ESTABLISHED:
            Logger.info("Master: Connection established: %s", full_address)


        if notification == Notification.CONNECTION_FAILED:
            self.layout.update_presentation_status(full_address)

    def remove_slave(self, notification, data):
        """
        Removes the knowledge of a slave from master and notifies GUI of the change
        """
        if data.full_address in self.slave_connections:
            self.slave_connections.pop(data.full_address, None)
        self.layout.notify(notification, data)

    def send_presentations_to_slaves(self):
        i = 0
        for slavec in self.slave_connections.values():
            #presentation = self.presentations[i]
            i += 1
            slavec.retrieve_presentation_files(8005, '.', slavec.presentation)

    def end_presentation(self):
        """
        Informs the slave connection about the presentation ending
        """
        for slave in self.slave_connections.values():
            slave.end_presentation()

    def close_all_connections(self):
        """
        Closes all connections to slaves
        """
        self.close_TCP_connections()
        self.close_UDP_connection()
        self.close_FTP_connection()

    def close_TCP_connections(self):
        """
        Closes TCP connections to slaves
        """
        for slave in self.slave_connections.values():
            slave.connection.end_connection()

    def close_FTP_connection(self):
        """
        Shuts down the FTP server
        """
        if self.FTPServer is not None:
            self.FTPServer.stop()

    def close_UDP_connection(self):
        """
        Closes the master's UDP protocol
        """
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
                      Notification.CONNECTION_TERMINATED: remove_slave
                      }
