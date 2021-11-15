# Pytests to test the i18n.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/axis")


def test_valid_regular_axis():
    ''' Tests an example of a valid regular axis '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360 }
    VALIDATOR.validate(axis)


def test_axis_with_number_array():
    ''' Tests a minimal example of a valid axis made of an array of values '''

    axis = { "values" : [1, 2, 3, 4, 5] }
    VALIDATOR.validate(axis)


def test_axis_with_string_array():
    ''' Tests a minimal example of a valid axis made of an array of strings (e.g. times) '''

    axis = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T04:30:00Z"] }
    VALIDATOR.validate(axis)


def test_axis_with_tuples_array():
    ''' Tests an axis whose values are tuples '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    VALIDATOR.validate(axis)


def test_missing_start():
    ''' Invalid: missing "start" property '''

    axis = { "stop" : 180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_missing_stop():
    ''' Invalid: missing "stop" property '''

    axis = { "start" : -180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_missing_num():
    ''' Invalid: missing "num" property '''

    axis = { "start" : -180.0, "stop" : 180.0 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_invalid_start():
    ''' Invalid: "start" has wrong type '''

    axis = { "start" : "-180.0", "stop" : 180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_invalid_stop():
    ''' Invalid: "stop" has wrong type '''

    axis = { "start" : -180.0, "stop" : "180.0", "num" : 360 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_invalid_num():
    ''' Invalid: "num" has wrong type '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360.1 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_negative_num():
    ''' Invalid: "num" cannot be negative '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : -360 }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_values_in_regular_axis():
    ''' Invalid: "values" can't be present in a regular axis '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360, "values" : [ -180.0, -179.0, -178.0 ] }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_empty_values_array():
    ''' Invalid: axis values are empty '''

    axis = { "values" : []}
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_nonunique_values_array():
    ''' Invalid: axis values are not unique '''

    axis = { "values" : [1, 2, 3, 4, 5, 5]}
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_invalid_tuples_axis():
    ''' Invalid: type of values inconsistent with dataType (tuple) '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [1, 2, 3, 4, 5]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_axis_with_mixed_type_values():
    ''' Invalid: axis values can't be of mixed type '''

    axis = { "values" : [1, 2, 3, "4", 5] }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)
