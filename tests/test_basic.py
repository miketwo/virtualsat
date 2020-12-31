# -*- coding: utf-8 -*-

import unittest
import satellite
import time
from datetime import datetime, timedelta

class BasicTestSuite(unittest.TestCase):

    def test_everything(self):
        sat = satellite.core.create_random_sat()
        lat, lon, _ = sat.current_position()
        look = sat.get_look(lat,lon)

        self.assertTrue(sat.is_visible_from(lat,lon))
        look = sat.get_look(lat,lon+180)
        self.assertFalse(sat.is_visible_from(lat,lon+180))
        
        now = datetime.now()
        sat.add_command("recharge", now + timedelta(seconds=5))
        sat.add_command("normal", now + timedelta(seconds=10))
        sat.add_command_scheduled_pics(now + timedelta(seconds=11), 15)
        sat.add_command("recharge", now + timedelta(seconds=11+15))
        sat.add_command("normal", now + timedelta(seconds=11+15+20))
        sat.add_command("downlink", now + timedelta(seconds=11+15+20+10))

        sat.print_commands()

        time.sleep(90)



if __name__ == '__main__':
    unittest.main()
