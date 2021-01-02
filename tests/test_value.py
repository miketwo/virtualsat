# -*- coding: utf-8 -*-
'''
Value Subsystem Testing
- Test basic functionality (adding/removing/clearing)
- Test that certain limitations exist wrt power
- Test that json commands work
'''
import pytest
from unittest.mock import Mock
from satellite import value


@pytest.fixture
def valuesub(static_power_subsystem):
    return value.ValueSubsystem(power_subsystem=static_power_subsystem)


@pytest.fixture
def valuesub_low_power(lower_power_subsystem):
    return value.ValueSubsystem(power_subsystem=lower_power_subsystem)


class TestTelemetry():
    def test_tlm_contains_everything(self, valuesub):
        tlm = valuesub.get_tlm()
        assert all(k in tlm['value'] for k in ("num", "names")), "Telemetry did not contain the expected keys"


class TestLimitations():
    def test_no_downloads_in_recharging_mode(self, valuesub):
        valuesub.pwr.mode = "recharge"
        with pytest.raises(SystemError, match=r'(?i).*mode.*'):
            valuesub.download()

    def test_no_value_in_recharging_mode(self, valuesub):
        valuesub.pwr.mode = "recharge"
        with pytest.raises(SystemError, match=r'(?i).*mode.*'):
            valuesub.create_value()


class TestExecutingCommands():
    def test_create_and_download_value(self, valuesub):
        valuesub.exec({"value": "create"})
        res = valuesub.exec({"value": "download"})

