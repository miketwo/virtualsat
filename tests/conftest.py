# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from datetime import datetime
from satellite import power
from groundstation.core import Groundstation


@pytest.fixture
def static_power_subsystem():
    mock_scheduler = Mock()
    sub = power.PowerSubsystem(scheduler=mock_scheduler)
    return sub


@pytest.fixture
def lower_power_subsystem():
    mock_scheduler = Mock()
    sub = power.PowerSubsystem(scheduler=mock_scheduler)
    sub.configure({"power":1, "mode":"normal", "reboots": 0})
    return sub


@pytest.fixture
def StlGroundstation():
    GS_LATITUDE = 38.6270
    GS_LONGITUDE = -90.1994
    return Groundstation("Stl", GS_LATITUDE, GS_LONGITUDE)


@pytest.fixture
def TrackingStlGroundstation(StlGroundstation):
    ''' A station tracking a satellite with time set to just before a pass '''
    dt = datetime.utcfromtimestamp(1609817765.0)  # 7 seconds before a pass
    StlGroundstation.tracking_system._DT_FOR_TEST = dt
    satname = "STARLINK-24"
    line1 = "1 44238U 19029D   20366.78684316  .00004289  00000-0  24662-3 0  9998"
    line2 = "2 44238  52.9975  32.3246 0001305  89.7284 270.3857 15.14479195 87325"
    StlGroundstation.set_target(satname, line1, line2)
    return StlGroundstation


@pytest.fixture
def command_defs():
    return {
        "satellite": {
            "power": {
                "r": {
                    "subsystem": "power",
                    "mode": "recharge"
                },
                "n": {
                    "subsystem": "power",
                    "mode": "normal"
                },
            },
            "value": {
                "c": {
                    "subsystem": "value",
                    "value": "create"
                },
                "d": {
                    "subsystem": "value",
                    "value": "download"
                },
            },
            "sched": {
                "subsystem": "sched",
            }
        },
        "groundstation": {
            "track": {}
        }
    }
