from kivy.app import App

from Constants.Command import Notification
from Domain.SlaveConnection import SlaveConnection
from Networking.RemuFTP import RemuFTPServer
from Networking.RemuUDP import MasterUDPListener
from kivy.logger import Logger
import Utils.FileHandler as fh
from Constants.PathConstants import PathConstants
import Constants.SupportedFileTypes as supp



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
        self.project = None
        self.FTPServer = None
        self.UDPListener = None

    def setup_project(self, project, media_path=PathConstants.ABSOLUTE_MEDIA_FOLDER):
        """
        Load a new project. Verifies that the project is valid and then loads it to the GUI
        :param project: The project to be loaded
        :return: Nothing
        """
        if self.verify_project(project, media_path):
            self.project = project
            self.layout.setup_project(project)
        else:
            Logger.error("Master: Invalid project")

    def verify_project(self, project, media_path=PathConstants.ABSOLUTE_MEDIA_FOLDER):
        """
        Verifies that all required files exist, filetypes are supported and filenames are valid.
        :param project: The project to be verified
        :return: True if valid, False otherwise
        """
        available_files = fh.get_filenames_from_path(media_path)
        for presentation in project.presentations:
            for filepath in presentation[1].presentation_filenames:
                filename = fh.get_filename_only(filepath)
                if fh.check_filename(filename) is False:
                    Logger.debug("Master: Invalid filename: %s ", filename)
                    return False
                if not filename in available_files:
                    Logger.debug("Master: File not found in media folder: %s", filename)
                    return False
                if not supp.extension_is_supported(fh.get_type_extension(filename)):
                    Logger.debug("Master: Invalid file type: %s", filename)
                    return False
        return True

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


    def bind_slave_to_presentation(self, presentation, slaveconnection_to_bind):

        self.slave_connections[slaveconnection_to_bind].presentation = presentation
        self.layout.notify(Notification.PRESENTING_DISABLED, False)
        Logger.debug("Master: bound presentation %s", self.slave_connections[slaveconnection_to_bind].presentation.presentation_filenames)

    def add_slave_connection(self, slave_connection):
        """
        Adds a pre-constructed SlaveConnection object to slave_connections

        slave_connection: SlaveConnection object
        """
        self.slave_connections[slave_connection.full_address] = slave_connection

    def load_project_to_gui(self):
        """
        Takes all tuples (named_presentation) from project class, which contain presentation's name and content, and
        requests master's layout to make gui widgets based on the project.
        :return: Nothing
        """
        for named_presentation in self.project.presentations:
            self.layout.create_new_presentation(named_presentation[0], named_presentation[1])

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
            slavec.retrieve_presentation_files(8005, '.')

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

    def handle_exception(self, message, exception):
        self.layout.error(message, exception)

"""
def load_project_to_gui()
    for named_presentation in self.project.presentations:
        self.layout.create_new_presentation(named_presentation[0], named_presentation[1])
"""