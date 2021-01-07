# -*- coding: utf-8 -*-
import pytest
from datetime import datetime, timedelta
from groundstation.track import TrackingSystem


satname = "STARLINK-24"
line1 = "1 44238U 19029D   20366.78684316  .00004289  00000-0  24662-3 0  9998"
line2 = "2 44238  52.9975  32.3246 0001305  89.7284 270.3857 15.14479195 87325"

dt = datetime.utcfromtimestamp(1609817765.0)  # 7 seconds before a pass


@pytest.fixture
def track():
    GS_LATITUDE = 38.6270
    GS_LONGITUDE = -90.1994
    track = TrackingSystem(GS_LATITUDE, GS_LONGITUDE)
    track._DT_FOR_TEST = dt
    return track


def test_tracking(track):
    assert track.tracking() is False
    assert track.in_pass() is False
    assert track.target_in_view() is False
    assert track.elevation == 0
    assert track.get_passes() == []


def test_postconditions_before_pass(track):
    track.set_target(satname, line1, line2)

    # print(track.info())
    assert track.tracking() is True
    assert track.in_pass() is False
    assert track.target_in_view() is False
    assert track.elevation == 0
    assert len(track.get_passes()) > 0


def test_postconditions_during_pass(track):
    track._DT_FOR_TEST += timedelta(seconds=30)
    track.set_target(satname, line1, line2)

    # print(track.info())
    assert track.tracking() is True
    assert track.in_pass() is True
    assert track.target_in_view() is True
    assert track.elevation > 0
    assert len(track.get_passes()) > 0


def test_info_changing(track):
    track.set_target(satname, line1, line2)
    prev = track.info()
    for i in range(1, 20):
        track._DT_FOR_TEST = dt + timedelta(seconds=i)
        track._recalc_pointing()
        assert track.info() != prev
        prev = track.info()
