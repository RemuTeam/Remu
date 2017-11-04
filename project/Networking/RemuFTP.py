from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor

"""
A FILE TRANSFER PROTOCOL SERVER
"""
class RemuFTPServer:
    """
    Initializes the server to a given path and port

    path:   the root path of the FTP-server
    port:   the port to listen, defaults to 21
    """
    def __init__(self, path=None, port=21):
        self.__path = path
        self.__port = port
        self.__server = None

    """
    Starts the server.
    """
    def start(self):
        if self.__path is None:
            raise AttributeError("The server's root path cannot be None")

        p = Portal(FTPRealm(self.__path),
                   [AllowAnonymousAccess(), FilePasswordDB("pass.dat")])
        f = FTPFactory(p)
        self.__server = reactor.listenTCP(self.__port, f)
        print("started ftp server in path", self.get_path(), "listening for port", self.get_port())

    """
    Stops the server.
    """
    def stop(self):
        if self.__server is not None:
            self.__server.stopListening()
            print("ftp server stopped")

    """
    Set the root path of the server
    
    Note! Does not change the path of a running server.
    The server must be stopped and started for the change of
    path to take effect.
    
    new_path:   a string, the server's new root path
    """
    def set_path(self, path):
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
        print("data received!")
        self.__buffer.write(data)
        if self.__file is not None and self.__buffersize_limit_reached():
            self.__write_buffer_to_file()

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
    def __buffersize_limit_reached(self):
        print("buffer:", self.__buffer.getbuffer().nbytes, "/", self.__buffersize_limit)
        return self.__buffer.getbuffer().nbytes >= self.__buffersize_limit

    """
    Resets the buffer and returns its content.
    """
    def __flush_buffer(self):
        bufferContent = self.__buffer.getvalue()
        self.__buffer.truncate(0)
        self.__buffer.seek(0)
        return bufferContent

    """
    Appends the buffer's content to the file 
    and flushes the buffer.
    """
    def __write_buffer_to_file(self):
        with open("copy_" + self.__file, "ab+") as file:
            buffer_content = self.__flush_buffer()
            file.write(buffer_content)


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


class RemuFTPClient:
    """
    A FILE TRANSFER PROTOCOL CLIENT
    """
    def __init__(self, host, port, read_path, write_path):
        """
        Initializes the client to a server

        :param host: an ip-formatted string, the server's address
        :param port: an integer, the port the host listens to
        :param read_path: a string, the host's path to read files from
        :param write_path: a string, the path to write into
        """
        self.host = host
        self.client = None
        self.files = None
        self.fileCounter = 0
        self.read_path = read_path
        self.write_path = write_path
        self.bufferingProtocol = FileBufferingProtocol()
        self.configuration = self.set_config(Options(), {'port': port, 'host': host})

    """
    Sets the connection's configuration
    
    options:            an Options object
    additional_options: a dictionary of options to add 
                        to the configuration
    """
    def set_config(self, options, additional_options):
        config = options
        config.parseOptions()

        for key, value in additional_options.items():
            config.opts[key] = value

        return config

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
        self.client = creator.connectTCP(self.configuration.opts['host'],
                                         self.configuration.opts['port']).addCallback(self.connectionMade).addErrback(self.connectionFailed)

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
        self.printFiles()
        if self.files is not None:
            self.retrieveFiles(ftpClient)

    """
    A function that attempts to retrieve all the 
    files listed in the self.files object from the server
    """
    def retrieveFiles(self, ftpClient):
        if self.fileCounter < len(self.files):
            print("-------------************----------------")
            print("retrieving file number: " + str(self.fileCounter) + " out of " + str(len(self.files)))
            current_file = self.files[self.fileCounter]["filename"]
            self.fileCounter += 1
            self.bufferingProtocol.set_file(self.write_path + "/" + current_file)
            print("file set! ", self.bufferingProtocol.get_file())
            d = ftpClient.retrieveFile(current_file, self.bufferingProtocol)
            d.addCallbacks(self.writeFile, self.fail, callbackArgs=(ftpClient))
            if self.fileCounter == len(self.files):
                self.disconnect()
                self.fileCounter = 0

    """
    A callback function that writes the buffer to its file
    """
    def writeFile(self, result, ftpClient):
        self.bufferingProtocol.write_buffer_to_file()
        print(self.bufferingProtocol.currentfile + " written out")
        self.retrieveFiles(ftpClient)

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
