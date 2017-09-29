from Domain.Slave import Slave
from RemuTCP.RemuTCP import RemuTCP
import unittest

class SlaveTest(unittest.TestCase):
    def test_init_with_no_connection(self):
        slave = Slave()
        self.assertIsNone(slave.master_connection)
        self.assertIsNotNone(slave.presentation)

    def test_init_with_connection(self):
        slave = Slave({})
        self.assertIsNotNone(slave.master_connection)