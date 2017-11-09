import unittest
from unittest.mock import patch
from Networking.RemuFTP import *

class RemuFTPServerTest(unittest.TestCase):
    def setUp(self):
        self.s = RemuFTPServer('./', 8005)

    def test_default_port(self):
        server = RemuFTPServer()
        self.assertEqual(server.get_port(), 21)

    def test_default_path(self):
        server = RemuFTPServer()
        self.assertIsNone(server.get_path())

    def test_set_port(self):
        self.assertEqual(8005, self.s.get_port())
        self.s.set_port(1)
        self.assertEqual(1, self.s.get_port())

    def test_set_path(self):
        self.assertEqual('./', self.s.get_path())
        self.s.set_path("banaba")
        self.assertEqual('banaba', self.s.get_path())

    def test_no_path_raises_attribute_error_when_started(self):
        server = RemuFTPServer()
        with self.assertRaises(AttributeError):
            server.start()

class FileBufferingProtocolTest(unittest.TestCase):
    def setUp(self):
        self.buffer = FileBufferingProtocol()
        self.bufferSizeLimit = 50000000
        self.file = "ababa.bab"
        self.testData = bytearray("datatata", "utf-8")
        self.newBufferSizeLimit = len(self.testData) / 2

    def init_test_file(self, filename):
        with open(filename, "w") as f:
            f.truncate(0)

    def test_file_is_none_when_initialized(self):
        self.assertIsNone(self.buffer.get_file())

    def test_buffer_size_limit_is_default(self):
        self.assertEqual(self.buffer.get_buffersize_limit(), self.bufferSizeLimit)

    def test_buffer_size_can_be_set_at_init(self):
        b = FileBufferingProtocol(self.newBufferSizeLimit)
        self.assertEqual(self.newBufferSizeLimit, b.get_buffersize_limit())

    def test_buffer_size_can_be_set_later(self):
        self.buffer.set_buffersize_limit(self.newBufferSizeLimit)
        self.assertEqual(self.newBufferSizeLimit, self.buffer.get_buffersize_limit())

    def test_file_can_be_set_at_init(self):
        b = FileBufferingProtocol(file=self.file)
        self.assertEqual(self.file, b.get_file())

    def test_file_can_be_set_later(self):
        self.buffer.set_file(self.file)
        self.assertEqual(self.file, self.buffer.get_file())

    def test_buffer_is_written_to(self):
        b = FileBufferingProtocol(file=self.file)
        b.dataReceived(self.testData)
        self.assertEqual(self.testData, b.get_buffer_value())

    def test_buffersize_limit_checked(self):
        with patch.object(FileBufferingProtocol, 'buffersize_limit_reached', return_value=False) as mock_method:
            b = FileBufferingProtocol(file=self.file)
            b.dataReceived(self.testData)
        mock_method.assert_called_once_with()

    def test_buffersize_below_limit(self):
        self.buffer.dataReceived(self.testData)
        self.assertFalse(self.buffer.buffersize_limit_reached())

    def test_buffersize_limit_surpassed(self):
        self.buffer.dataReceived(self.testData)
        self.buffer.set_buffersize_limit(1)
        self.assertTrue(self.buffer.buffersize_limit_reached())

    def test_surpassing_buffersize_limit_writes_to_file(self):
        self.init_test_file(self.file)
        with patch.object(FileBufferingProtocol, 'write_buffer_to_file', return_value=None) as mock_method:
            b = FileBufferingProtocol(file=self.file)
            b.set_buffersize_limit(len(self.testData) / 2)
            b.dataReceived(self.testData)
        mock_method.assert_called_once_with()

    def test_surpassing_buffersize_limit_flushes_the_buffer(self):
        self.init_test_file(self.file)
        with patch.object(FileBufferingProtocol, 'flush_buffer', return_value=self.testData) as mock_method:
            b = FileBufferingProtocol(file=self.file)
            b.set_buffersize_limit(len(self.testData) / 2)
            b.dataReceived(self.testData)
        mock_method.assert_called_once_with()

    def test_flushing_buffer(self):
        self.buffer.dataReceived(self.testData)
        data = self.buffer.flush_buffer()
        self.assertEqual(self.testData, data)
        self.assertEqual(bytearray("", "utf-8"), self.buffer.get_buffer_value())