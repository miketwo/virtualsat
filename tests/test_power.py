# -*- coding: utf-8 -*-
import pytest
from unittest.mock import Mock
from satellite import power

@pytest.fixture
def pwrsub():
    mock_scheduler = Mock()
    return power.PowerSubsystem(scheduler=mock_scheduler)

class TestTelemetry():
    def test_tlm_contains_power_mode_and_reboots(self, pwrsub):
        tlm = pwrsub.get_tlm()
        assert all(k in tlm for k in ("power","mode","reboots"))

class TestUpdatingState():
    def test_power_drains(self, pwrsub):
        starting = {"power":100, "mode":"normal"}
        pwrsub.configure(starting)
        ending = pwrsub.update()
        assert starting["mode"] == ending["mode"]
        assert starting["power"] > ending["power"]

    def test_power_recharges(self, pwrsub):
        starting = {"power":50, "mode":"recharge"}
        pwrsub.configure(starting)
        ending = pwrsub.update()
        assert starting["mode"] == ending["mode"]
        assert starting["power"] < ending["power"]

    def test_at_zero_power_reboot_counter_increments(self, pwrsub):
        starting = {"power":1, "mode":"normal", "reboots": 0}
        pwrsub.configure(starting)
        ending = pwrsub.update()
        assert starting["reboots"] < ending["reboots"]

    def test_at_zero_power_mode_changes(self, pwrsub):
        starting = {"power":1, "mode":"normal", "reboots": 0}
        pwrsub.configure(starting)
        ending = pwrsub.update()
        assert starting["mode"] != ending["mode"]

    def test_at_zero_power_power_is_not_negative(self, pwrsub):
        starting = {"power":1, "mode":"normal", "reboots": 0}
        pwrsub.configure(starting)
        ending = pwrsub.update()
        assert 0 == ending["power"]

class TestTakingActions:

    @pytest.mark.parametrize("action", [
        ("picture"),
        ("download"),
    ])
    def test_actions_reduce_power(self, pwrsub, action):
        starting = {"power":50}
        pwrsub.configure(starting)
        ending = pwrsub.take_action(action)
        assert ending["power"] < starting["power"]

    def test_no_power_fails_action_and_doesnt_change_power(self, pwrsub):
        starting = {"power":1}
        pwrsub.configure(starting)
        with pytest.raises(SystemError):
            pwrsub.take_action('picture')
        assert pwrsub.power == starting['power']

    def test_bad_action_throws(self, pwrsub):
        with pytest.raises(SystemError):
            pwrsub.take_action("doesnt exist")

class TestExecutingCommands():

    @pytest.mark.parametrize("starting_mode, command, ending_mode", [
        ("recharge", {"mode": "normal"}, "normal"),
        ("normal", {"mode": "recharge"}, "recharge"),
    ])
    def test_mode_changes(self, pwrsub, starting_mode, command, ending_mode):
        starting = {"power":50, "mode":starting_mode}
        pwrsub.configure(starting)
        ending = pwrsub.exec(command)
        assert(ending["mode"] == ending_mode)