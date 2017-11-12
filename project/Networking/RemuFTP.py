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

    """
    Set the port that the server listens to

    Note! Does not change the port of a running server.
    The server must be stopped and started for the change of
    port to take effect.

    new_port:   an integer, the server's new port to listen to
    """
    def set_port(self, new_port):
        self.__port = new_port

    """
    Returns the server's root path
    """
    def get_path(self):
        return self.__path

    """
    Returns the server's port
    """
    def get_port(self):
        return self.__port


from twisted.internet.protocol import Protocol
from io import BytesIO

"""
PROTOCOL FOR BUFFERING DATA RETRIEVED VIA AN FTP CONNECTION
AND WRITING IT TO A DESIGNATED FILE
"""
class FileBufferingProtocol(Protocol):
    """
    Initialize a new FileBufferingProtocol object.

    buffersize_limit:   an integer, the limit
                        of the buffer's size in bytes,
                        defaults to 50MB
    file:               the name of the file to write the
                        buffered data into
    """
    def __init__(self, buffersize_limit=50000000, file=None):
        self.__buffer = BytesIO()
        self.__file = file
        self.__buffersize_limit = buffersize_limit

    """
    En event called upon receiving data.
    
    data:   the received data
    """
    def dataReceived(self, data):
        # print("data received!")
        self.__buffer.write(data)
        if self.__file is not None and self.buffersize_limit_reached():
            self.write_buffer_to_file()
            print("file written")

    """
    Set the name of the file to write buffer into
    
    filename:   a string, the name of the file 
                to write buffer into
    """
    def set_file(self, filename):
        self.__file = filename

    """
    Returns the name of the file that the buffer
    writes into
    """
    def get_file(self):
        return self.__file

    """
    A private function to check whether the buffer 
    size limit has been reached.
    """
    def buffersize_limit_reached(self):
        # print("buffer:", self.__buffer.getbuffer().nbytes, "/", self.__buffersize_limit)
        return self.__buffer.getbuffer().nbytes >= self.__buffersize_limit

    """
    Resets the buffer and returns its content.
    """
    def flush_buffer(self):
        bufferContent = self.__buffer.getvalue()
        self.__buffer.truncate(0)
        self.__buffer.seek(0)
        return bufferContent

    """
    Appends the buffer's content to the file 
    and flushes the buffer.
    """
    def write_buffer_to_file(self):
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


"""
Connection options used by the FTPClient class
"""
class Options(usage.Options):
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

    """
    Connect the client
    """
    def connect(self):
        FTPClient.debug = self.configuration.opts['debug']
        creator = ClientCreator(reactor,
                                FTPClient,
                                self.configuration.opts['username'],
                                self.configuration.opts['password'],
                                passive=self.configuration.opts['passive'])
        self.client = creator.connectTCP(self.host,
                                         self.port).addCallback(self.connectionMade).addErrback(self.connectionFailed)

    """
    Disconnect the client
    """
    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()

    """
    A callback function for a failed connection
    """
    def connectionFailed(self, f):
        print("Connection Failed:" + f)

    """
    A callback function for a successful connection
    """
    def connectionMade(self, ftpClient):
        # Get a detailed listing of the current directory
        self.twisted_FTP_client = ftpClient
        fileList = FTPFileListProtocol()
        d = ftpClient.list(self.read_path, fileList)
        d.addCallbacks(self.__getFiles, self.fail, callbackArgs=(fileList, ftpClient))

    """
    A callback function for a failed request
    """
    def fail(self, error):
        print('Failed.  Error was:')
        print(error)

    """
    A callback function for handling a successful 
    file listing retrieval from the server
    """
    def __getFiles(self, result, fileListProtocol, ftpClient):
        print('Processed file listing')
        self.files = fileListProtocol.files
        for file in self.files:
            self.file_queue.put(file["filename"])
        self.printFiles()
        if self.files is not None:
            self.retrieveFiles()

    """
    A callback function that writes the buffer to its file
    """
    def writeFile(self, result):
        print("now writing file")
        self.bufferingProtocol.write_buffer_to_file()
        self.retrieveFiles()

    """
    A function that attempts to retrieve all the 
    files listed in the self.files object from the server
    """
    def retrieveFiles(self):
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

    """
    A debugging function to print the content of the 
    retrieved file listing
    """
    def printFiles(self):
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
