# -*- coding: utf-8 -*-
'''

'''
import pytest
from enum import Enum
from unittest.mock import Mock
from utils import command
import json


class Subsystem(Enum):
    power = 1
    value = 2
    sched = 3


class PowerMode(Enum):
    normal   = 1
    recharge = 2


class TestDefinitialization():

    def test_enum_encoder(self):
        res = json.dumps(Subsystem, cls=command.EnumEncoder)
        expected = json.dumps({"power": 1, "value": 2, "sched": 3})
        assert expected == res

    def test_field_can_instantiate_from_json_definition(self):
        pass

    def test_field_can_produce_definition(self):
        SubsystemField = command.define_field("subsystem", "enum", ENUM=Subsystem)
        expected = json.dumps({"name": "subsystem", "type": "enum", "enum": {
                    "power": 1, "value": 2, "sched": 3}})
        result = SubsystemField.to_definition()
        assert(expected == result)

    def test_populated_field_can_produce_definition(self):
        SubsystemField = command.define_field("subsystem", "enum", ENUM=Subsystem)
        populated = SubsystemField(Subsystem.power)
        expected = json.dumps({"name": "subsystem", "type": "enum", "enum": {
                    "power": 1, "value": 2, "sched": 3}})
        result = populated.to_definition()
        assert(expected == result)

    def test_command_can_produce_definition(self):

        # Create the fields
        SubsystemField = command.define_field("subsystem", "enum", ENUM=Subsystem)
        PowerModeField = command.define_field("mode", "enum", ENUM=PowerMode)

        # Create the command
        PowerModeCommand = command.define_command(
            DISPLAY_NAME="Change Power Mode",
            DESCRIPTION="Sets the Power Mode",
            FIELDS=[SubsystemField(Subsystem.power), PowerModeField])

        # Instantiate the command
        recharge = PowerModeCommand(PowerMode.recharge)
        defin = recharge.to_definition()

        expected = json.dumps({
            "display_name": "Change Power Mode",
            "description": "Sets the Power Mode",
            "fields": [
                {"name": "subsystem", "type": "enum", "enum": {
                    "power": 1, "value": 2, "sched": 3}},
                {"name": "mode", "type": "enum", "enum": {
                    "normal": 1, "recharge": 2}},
                ],
            "tags": [],
            })

        assert(defin == expected)

    def test_field_from_dict(self):
        SubsystemField = command.define_field("subsystem", "enum", ENUM=Subsystem)
        ResultField = command.define_field_from_dict(SubsystemField.to_dict())

        # Instantiate for comparison
        sub = SubsystemField(Subsystem.power)
        res = ResultField(Subsystem.power)
        print(sub)
        print(res)
        # assert res == sub

    def test_command_from_json_definition(self):
        definition = json.dumps({
            "display_name": "Change Power Mode",
            "description": "Sets the Power Mode",
            "fields": [
                {"name": "subsystem", "type": "enum", "enum": {
                    "power": 1, "value": 2, "sched": 3}},
                {"name": "mode", "type": "enum", "enum": {
                    "normal": 1, "recharge": 2}},
                ],
            "tags": [],
            })

        CommandClass = command.define_command_from_json(definition)
        cmd = CommandClass(Subsystem.power, PowerMode.recharge)
        cmd = CommandClass(PowerMode.recharge, Subsystem.sched)

        print(cmd)
