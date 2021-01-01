# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from satellite import power

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