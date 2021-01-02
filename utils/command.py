#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from enum import Enum, EnumMeta

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) == EnumMeta:
            tmp = {str(s._name_): int(s._value_) for s in obj}
            return tmp
        return json.JSONEncoder.default(self, obj)

def as_enum(d):
    if d is None:
        return None
    if type(d) == dict:
        return Enum('DynamicEnum', d)
    return Enum('DynamicEnum', json.loads(d))


"""A Factory-style method that returns a Field class that can then be populated."""
def define_field(NAME, TYPE, DEFAULT=None, CHARLIMIT=None, RANGE=None, ENUM=None):
    assert TYPE in ["integer", "float", "enum", "string", "text", "datetime"], "{} is an Invalid type".format(TYPE)
    if TYPE == "enum":
        assert ENUM, "enum argument must be populated if type is enum"


    class Field():
        name = NAME
        type = TYPE
        default = DEFAULT
        characterLimit = CHARLIMIT
        range = RANGE
        enum = ENUM
        value = None

        def __init__(self, value=DEFAULT):
            super().__init__()
            self.validate(value)
            self.value = value

        def validate(self, value):
            # ToDo: Implement validation
            return True

        @classmethod
        def to_str(cls):
            return str([a for a in dir(cls) if not a.startswith('__') and not callable(getattr(cls, a))])

        def __str__(self):
            return "{},{},{}".format(self.name, self.type, self.value)

        def __eq__(self, other):
            retval = (isinstance(other, Field) and
                all([self.name == other.name,
                     self.type == other.type,
                     self.default == other.default,
                     self.characterLimit == other.characterLimit,
                     self.range == other.range,
                     self.enum == other.enum,
                     self.value == other.value]))
            print("CHECKING EQUALITY ---> {}".format(retval))
            return retval

        @classmethod
        def to_dict(self):
            if self.enum:
                enum_dict = {str(s._name_): int(s._value_) for s in self.enum}
            else:
                enum_dict = None
            tmp = {
                "name": self.name,
                "type": self.type,
                "default": self.default,
                "characterLimit": self.characterLimit,
                "range": self.range,
                "enum": enum_dict,
                "value": self.value
            }
            tmp = {k: v for (k, v) in tmp.items() if v is not None}
            return tmp

        @classmethod
        def to_definition(self):
            return json.dumps(self.to_dict())

    return Field


def define_field_from_dict(aDict):
    f = aDict
    enum = as_enum(f.get("enum", None))
    return define_field(f["name"], f["type"],
        f.get("default", None), f.get("charlimit", None),
        f.get("range", None), enum)


def define_command(DISPLAY_NAME, DESCRIPTION, FIELDS, TAGS=None):


    class Command():
        def __init__(self, *args):
            super().__init__()
            self.display_name = DISPLAY_NAME
            self.description = DESCRIPTION
            variable_fields = [f for f in FIELDS if not hasattr(f, 'value') or f.value is None]
            assert len(args) == len(variable_fields), "Incorrect number of arguments for fields to populate"
            combined = zip(args, variable_fields)
            self.fields = [field(arg) for (arg, field) in combined]
            self.tags = TAGS if TAGS is not None else []

        def to_definition(self):
            return json.dumps({
                "display_name": self.display_name,
                "description": self.description,
                "fields": [f.to_dict() for f in FIELDS],
                "tags": self.tags,
            }, cls=EnumEncoder)

        def __str__(self):
            return self.to_definition()


    return Command


def define_command_from_json(json_definition):
    d = json.loads(json_definition)
    fields = [define_field_from_dict(f) for f in d["fields"]]
    ret = define_command(
        DISPLAY_NAME=d["display_name"],
        DESCRIPTION=d["description"],
        FIELDS=fields,
        TAGS=d.get("tags", None))
    return ret
