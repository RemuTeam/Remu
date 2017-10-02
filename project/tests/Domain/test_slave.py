from Domain.Slave import Slave
from RemuTCP.RemuTCP import RemuTCP
import unittest
from unittest.mock import Mock

class SlaveTest(unittest.TestCase):
    def test_init_with_no_connection(self):
        slave = Slave()
        self.assertIsNone(slave.master_connection)
        self.assertIsNotNone(slave.presentation)

    def test_init_with_connection(self):
        mock = Mock(RemuTCP)
        slave = Slave(mock)
        self.assertEqual(slave.master_connection, mock)

class RemuTCPMock(RemuTCP):
    def __init__(self):
        pass