# -*- coding: utf-8 -*-
import pytest
from datetime import datetime, timedelta
from groundstation import track


def test_send_command_before_pass(TrackingStlGroundstation, command_defs):
    with pytest.raises(track.NoCurrentPassError):
        TrackingStlGroundstation.send_command(command_defs['satellite']['power']['r'])


# TBD: Figure out how to test this -- sends an http request.
# def test_send_command_during_pass(TrackingStlGroundstation, command_defs):
#     TrackingStlGroundstation.tracking_system._DT_FOR_TEST += timedelta(seconds=10)
#     TrackingStlGroundstation.send_command(command_defs['satellite']['power']['r'])
