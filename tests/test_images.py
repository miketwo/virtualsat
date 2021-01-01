# -*- coding: utf-8 -*-
'''
Image Subsystem Testing
- Test basic functionality (adding/removing/clearing pics)
- Test the circular buffer works
- Test that certain limitations exist when power is low
- Test that json commands work
- Future: Test that we can get an actual picture from Google's dataset
'''
import pytest
from unittest.mock import Mock
from satellite import images

@pytest.fixture
def imgsub(static_power_subsystem):
    return images.ImagingSubsystem(power_subsystem=static_power_subsystem)

@pytest.fixture
def imgsub_low_power(lower_power_subsystem):
    return images.ImagingSubsystem(power_subsystem=lower_power_subsystem)

class TestTelemetry():
    def test_tlm_contains_everything(self, imgsub):
        tlm = imgsub.get_tlm()
        assert all(k in tlm for k in ("num_pictures", "pictures")), "Telemetry did not contain the expected keys"

class TestLimitations():
    def test_no_downloads_in_recharging_mode(self, imgsub):
        imgsub.pwr.mode = "recharge"
        with pytest.raises(SystemError, match=r'(?i).*mode.*'):
            imgsub.download()

    def test_no_pics_in_recharging_mode(self, imgsub):
        imgsub.pwr.mode = "recharge"
        with pytest.raises(SystemError, match=r'(?i).*mode.*'):
            imgsub.take_pic()


class TestExecutingCommands():
    def test_create_and_download_image(self, imgsub):
        imgsub.exec({"image": "take"})
        res = imgsub.exec({"image": "download"})
