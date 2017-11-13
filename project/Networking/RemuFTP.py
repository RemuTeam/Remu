from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor
from Domain.Command import Notification
import os

class RemuFTPServer:
    """
    A FILE TRANSFER PROTOCOL SERVER
    """
    def __init__(self, path=None, port=21):
        """
        Initializes the server to a given path and port
        :param path: a string, the root path of the FTP-server
        :param port: an integer, the port to listen, defaults to 21
        """
        self.__path = path
        self.__port = port
        self.__server = None

    def start(self):
        """
        Starts the server.
        :return: None
        """
        if self.__path is None:
            raise AttributeError("The server's root path cannot be None")

        p = Portal(FTPRealm(self.__path),
                   [AllowAnonymousAccess(), FilePasswordDB("pass.dat")])
        f = FTPFactory(p)
        self.__server = reactor.listenTCP(self.__port, f)
        print("started ftp server in path", self.get_path(), "listening for port", self.get_port())

    def stop(self):
        """
        Stops the server.
        :return: None
        """
        if self.__server is not None:
            self.__server.stopListening()
            print("ftp server stopped")

    def set_path(self, path):
        """
        Set the root path of the server

        Note! Does not change the path of a running server.
        The server must be stopped and started for the change of
        path to take effect.
        :param path: a string, the server's new root path
        :return: None
        """
        self.__path = path

    def set_port(self, new_port):
        """
        Set the port that the server listens to

        Note! Does not change the port of a running server.
        The server must be stopped and started for the change of
        port to take effect.

        new_port:   an integer, the server's new port to listen to
        """
        self.__port = new_port

    def get_path(self):
        """
        Returns the server's root path
        """
        return self.__path

    def get_port(self):
        """
        Returns the server's port
        """
        return self.__port


from twisted.internet.protocol import Protocol
from io import BytesIO


class FileBufferingProtocol(Protocol):
    """
    PROTOCOL FOR BUFFERING DATA RETRIEVED VIA AN FTP CONNECTION
    AND WRITING IT TO A DESIGNATED FILE
    """

    def __init__(self, buffersize_limit=50000000, file=None):
        """
        Initialize a new FileBufferingProtocol object.

        buffersize_limit:   an integer, the limit
                            of the buffer's size in bytes,
                            defaults to 50MB
        file:               the name of the file to write the
                            buffered data into
        """
        self.__buffer = BytesIO()
        self.__file = file
        self.__buffersize_limit = buffersize_limit

    def dataReceived(self, data):
        """
        En event called upon receiving data.

        data:   the received data
        """
        # print("data received!")
        self.__buffer.write(data)
        if self.__file is not None and self.buffersize_limit_reached():
            self.write_buffer_to_file()
            print("file written")

    def set_file(self, filename):
        """
        Set the name of the file to write buffer into

        filename:   a string, the name of the file
                    to write buffer into
        """
        self.__file = filename

    def get_file(self):
        """
        Returns the name of the file that the buffer
        writes into
        """
        return self.__file

    def buffersize_limit_reached(self):
        """
        A private function to check whether the buffer
        size limit has been reached.
        """
        # print("buffer:", self.__buffer.getbuffer().nbytes, "/", self.__buffersize_limit)
        return self.__buffer.getbuffer().nbytes >= self.__buffersize_limit

    def flush_buffer(self):
        """
        Resets the buffer and returns its content.
        """
        bufferContent = self.__buffer.getvalue()
        self.__buffer.truncate(0)
        self.__buffer.seek(0)
        return bufferContent

    def write_buffer_to_file(self):
        """
        Appends the buffer's content to the file
        and flushes the buffer.
        """
        print("attempting to write file")
        with open(self.__file, "ab+") as file:
            print("writing file")
            buffer_content = self.flush_buffer()
            file.write(buffer_content)
            print("file is written")

    def set_buffersize_limit(self, new_buffersize_limit):
        """
        Set new limit for the buffer's size

        :param new_buffersize_limit: an integer, the new limit
        :return: None
        """
        self.__buffersize_limit = new_buffersize_limit

    def get_buffersize_limit(self):
        """
        Get the set buffer's size limit

        :return: an integer, the buffer's size limit in bytes
        """
        return self.__buffersize_limit

    def get_buffer_value(self):
        """
        Get the BytesIO buffer object

        :return: a BytesIO, the buffer
        """
        return self.__buffer.getvalue()


from twisted.python import usage


class Options(usage.Options):
    """
    Connection options used by the FTPClient class
    """

    optParameters = [['host', 'h', 'localhost'],
                     ['port', 'p', 8005],
                     ['username', 'u', 'anonymous'],
                     ['password', None, 'twisted@'],
                     ['passive', None, 0],
                     ['debug', 'd', 1],
                    ]


from twisted.internet.protocol import ClientCreator
from twisted.protocols.ftp import FTPClient, FTPFileListProtocol
from queue import Queue


class RemuFTPClient:
    """
    A FILE TRANSFER PROTOCOL CLIENT
    """
    def __init__(self, host, port, read_path, write_path, listener=None):
        """
        Initializes the client to a server

        :param host: an ip-formatted string, the server's address
        :param port: an integer, the port the host listens to
        :param read_path: a string, the host's path to read files from
        :param write_path: a string, the path to write into
        """
        self.host = host
        self.port = port
        self.client = None
        self.files = None
        self.fileCounter = 0
        self.read_path = read_path
        self.write_path = write_path
        self.bufferingProtocol = FileBufferingProtocol()
        self.configuration = Options()
        self.twisted_FTP_client = None
        self.file_queue = Queue()
        self.listener = listener

    def connect(self):
        """
        Connect the client
        """
        FTPClient.debug = self.configuration.opts['debug']
        creator = ClientCreator(reactor,
                                FTPClient,
                                self.configuration.opts['username'],
                                self.configuration.opts['password'],
                                passive=self.configuration.opts['passive'])
        self.client = creator.connectTCP(self.host,
                                         self.port).addCallback(self.connectionMade).addErrback(self.connectionFailed)

    def disconnect(self):
        """
        Disconnect the client
        """
        if self.client is not None:
            self.client.disconnect()

    def connectionFailed(self, f):
        """
        A callback function for a failed connection
        """
        print("Connection Failed:" + f)

    def connectionMade(self, ftpClient):
        """
        A callback function for a successful connection
        """

        # Get a detailed listing of the current directory
        self.twisted_FTP_client = ftpClient
        fileList = FTPFileListProtocol()
        d = ftpClient.list(self.read_path, fileList)
        d.addCallbacks(self.__getFiles, self.fail, callbackArgs=(fileList, ftpClient))

    def fail(self, error):
        """
        A callback function for a failed request
        """
        print('Failed.  Error was:')
        print(error)

    def __getFiles(self, result, fileListProtocol, ftpClient):
        """
        A callback function for handling a successful
        file listing retrieval from the server
        """
        print('Processed file listing')
        self.files = fileListProtocol.files
        for file in self.files:
            self.file_queue.put(file["filename"])
        self.printFiles()
        if self.files is not None:
            self.retrieveFiles()

    def writeFile(self, result):
        """
        A callback function that writes the buffer to its file
        """
        print("now writing file")
        self.bufferingProtocol.write_buffer_to_file()
        self.retrieveFiles()

    def retrieveFiles(self):
        """
        A function that attempts to retrieve all the
        files listed in the self.files object from the server
        """
        existing_files = self.get_existing_files(self.write_path)
        if self.fileCounter < len(self.files):
            print("-------------************----------------")
            print("retrieving file number: " + str(self.fileCounter + 1) + " out of " + str(len(self.files)))
            current_file = self.files[self.fileCounter]["filename"]
            self.fileCounter += 1
            if current_file in existing_files:
                print(current_file, "already exists, skipping...")
                self.retrieveFiles()
            else:
                self.bufferingProtocol.set_file(self.write_path + "/" + current_file)
                print("file set! ", self.bufferingProtocol.get_file())
                d = self.twisted_FTP_client.retrieveFile(current_file, self.bufferingProtocol)
                d.addCallbacks(self.writeFile, self.fail)
                print(self.fileCounter, len(self.files))
        elif self.fileCounter == len(self.files):
            self.listener.notify_file_transfer_completed()
            self.disconnect()
            self.fileCounter = 0

    def printFiles(self):
        """
        A debugging function to print the content of the
        retrieved file listing
        """
        if self.files is not None:
            for file in self.files:
                print('    %s: %d bytes, %s' \
                      % (file['filename'], file['size'], file['date']))
            print('Total: %d files' % (len(self.files)))

    def get_existing_files(self, path):
        filenames = []
        for filename in os.listdir(path):
            filenames.append(filename)
        return filenames
