# Pytests to test the axis.json schema file
# TODO: factor out into specific tests for different axis types

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/anyAxis")


def test_valid_regular_axis():
    ''' Tests an example of a valid regular axis '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360 }
    VALIDATOR.validate(axis)


def test_axis_with_number_array():
    ''' Tests a minimal example of a valid axis made of an array of values '''

    axis = { "values" : [1, 2, 3, 4, 5] }
    VALIDATOR.validate(axis)


def test_time_axis():
    ''' Tests a minimal example of a valid axis made of an array of time values '''

    axis = { "values" : ["2001-01-01T00:00:00Z", "2001-01-02T00:00:00Z", "2001-01-03T00:00:00Z"] }
    VALIDATOR.validate(axis)


def test_axis_with_bounds():
    ''' Tests an axis that has a bounds array '''

    axis = {
        "values": [20, 21],
        "bounds": [19.5, 20.5, 20.5, 21.5]
    }
    VALIDATOR.validate(axis)


def test_time_axis_with_bounds():
    ''' Tests a minimal example of a valid axis made of an array of time values,
        with a bounds array '''

    axis = {
        "values" : ["2001-01-01T12:00:00Z", "2001-01-02T12:00:00Z"],
        "bounds" : ["2001-01-01T00:00:00Z", "2001-01-02T00:00:00Z",
                    "2001-01-02T00:00:00Z", "2001-01-03T00:00:00Z"]
    }
    VALIDATOR.validate(axis)


def test_primitive_axis_with_data_type():
    ''' Tests a minimal example of a valid axis made of an array of values,
        with declaration of primitive data type '''

    axis = { "dataType" : "primitive", "values" : [1, 2, 3, 4, 5] }
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


def test_axis_with_polygons_array():
    ''' Tests an axis whose values are polygons '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ]
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


def test_axis_with_inconsistent_bounds_type():
    ''' Tests an axis that has a bounds array but of the wrong type '''

    axis = {
        "values": [20, 21],
        "bounds": ["19.5", "20.5", "20.5", "21.5"]
    }
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


def test_tuples_axis_missing_coordinates():
    ''' Invalid tuples axis: "coordinates" is missing '''

    axis = {
        "dataType": "tuple",
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_tuples_axis_empty_coordinates():
    ''' Invalid tuples axis: "coordinates" is empty '''

    axis = {
        "dataType": "tuple",
        "coordinates": [],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_invalid_polygons_axis():
    ''' Invalid: type of values inconsistent with dataType (polygon) '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [1, 2, 3, 4, 5]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_polygon_axis_missing_coordinates():
    ''' Invalid polygon axis: "coordinates" is missing '''

    axis = {
        "dataType": "polygon",
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ]
        ]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_axis_with_mixed_type_values():
    ''' Invalid: axis values can't be of mixed type '''

    axis = { "values" : [1, 2, 3, "4", 5] }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)


def test_primitive_axis_with_mistyped_data_type():
    ''' Tests a minimal example of a valid axis made of an array of values,
        with declaration of primitive data type (mistyped) '''

    axis = { "dataType" : "primtive", "values" : [1, 2, 3, 4, 5] }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(axis)
