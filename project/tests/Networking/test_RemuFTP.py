import unittest
from Networking.RemuFTP import RemuFTPServer

class RemuFTPTest(unittest.TestCase):
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