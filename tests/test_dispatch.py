# -*- coding: utf-8 -*-

import unittest
from satellite import dispatch
import time
from datetime import datetime, timedelta

class DispatchSubsystemTestSuite(unittest.TestCase):

    def test_handling_unregistered_subsystems(self):
        d = dispatch.DispatchSubsystem()
        d.dispatch("nonexistent subsystem", {})


if __name__ == '__main__':
    unittest.main()
