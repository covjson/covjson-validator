# Pytests to test the axis.json schema file
# TODO: factor out into specific tests for different axis types

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/anyAxis")


def test_valid_regular_axis(validator):
    ''' Tests an example of a valid regular axis '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360 }
    validator.validate(axis)


def test_axis_with_number_array(validator):
    ''' Tests a minimal example of a valid axis made of an array of values '''

    axis = { "values" : [1, 2, 3, 4, 5] }
    validator.validate(axis)


def test_time_axis(validator):
    ''' Tests a minimal example of a valid axis made of an array of time values '''

    axis = { "values" : ["2001-01-01T00:00:00Z", "2001-01-02T00:00:00Z", "2001-01-03T00:00:00Z"] }
    validator.validate(axis)


def test_axis_with_bounds(validator):
    ''' Tests an axis that has a bounds array '''

    axis = {
        "values": [20, 21],
        "bounds": [19.5, 20.5, 20.5, 21.5]
    }
    validator.validate(axis)


def test_time_axis_with_bounds(validator):
    ''' Tests a minimal example of a valid axis made of an array of time values,
        with a bounds array '''

    axis = {
        "values" : ["2001-01-01T12:00:00Z", "2001-01-02T12:00:00Z"],
        "bounds" : ["2001-01-01T00:00:00Z", "2001-01-02T00:00:00Z",
                    "2001-01-02T00:00:00Z", "2001-01-03T00:00:00Z"]
    }
    validator.validate(axis)


def test_primitive_axis_with_data_type(validator):
    ''' Tests a minimal example of a valid axis made of an array of values,
        with declaration of primitive data type '''

    axis = { "values" : [1, 2, 3, 4, 5] }
    validator.validate(axis)


def test_axis_with_string_array(validator):
    ''' Tests a minimal example of a valid axis made of an array of strings (e.g. times) '''

    axis = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T04:30:00Z"] }
    validator.validate(axis)


def test_axis_with_tuples_array(validator):
    ''' Tests an axis whose values are tuples '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    validator.validate(axis)


def test_axis_with_polygons_array(validator):
    ''' Tests an axis whose values are polygons '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ]
        ]
    }
    validator.validate(axis)


def test_missing_start(validator):
    ''' Invalid: missing "start" property '''

    axis = { "stop" : 180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_missing_stop(validator):
    ''' Invalid: missing "stop" property '''

    axis = { "start" : -180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_missing_num(validator):
    ''' Invalid: missing "num" property '''

    axis = { "start" : -180.0, "stop" : 180.0 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_invalid_start(validator):
    ''' Invalid: "start" has wrong type '''

    axis = { "start" : "-180.0", "stop" : 180.0, "num" : 360 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_invalid_stop(validator):
    ''' Invalid: "stop" has wrong type '''

    axis = { "start" : -180.0, "stop" : "180.0", "num" : 360 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_invalid_num(validator):
    ''' Invalid: "num" has wrong type '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360.1 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_negative_num(validator):
    ''' Invalid: "num" cannot be negative '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : -360 }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_values_in_regular_axis(validator):
    ''' Invalid: "values" can't be present in a regular axis '''

    axis = { "start" : -180.0, "stop" : 180.0, "num" : 360, "values" : [ -180.0, -179.0, -178.0 ] }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_empty_values_array(validator):
    ''' Invalid: axis values are empty '''

    axis = { "values" : []}
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_nonunique_numeric_array(validator):
    ''' Invalid: axis values are not unique '''

    axis = { "values" : [1, 2, 3, 4, 5, 5]}
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_nonunique_times_array(validator):
    ''' Invalid: time values are not unique '''

    axis = { "values" : ["2001-01-01T00:00:00Z", "2001-01-02T00:00:00Z", "2001-01-02T00:00:00Z"] }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_axis_with_inconsistent_bounds_type(validator):
    ''' Tests an axis that has a bounds array but of the wrong type '''

    axis = {
        "values": [20, 21],
        "bounds": ["19.5", "20.5", "20.5", "21.5"]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_empty_tuples_array(validator):
    ''' Invalid: tuples array is empty '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": []
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_invalid_tuples_axis(validator):
    ''' Invalid: type of values inconsistent with dataType (tuple) '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [1, 2, 3, 4, 5]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_empty_tuple(validator):
    ''' Invalid: one of the tuples is empty '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            [],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_tuples_axis_missing_coordinates(validator):
    ''' Invalid tuples axis: "coordinates" is missing '''

    axis = {
        "dataType": "tuple",
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_tuples_axis_empty_coordinates(validator):
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
        validator.validate(axis)


def test_invalid_tuple_value(validator):
    ''' Invalid: one of the tuple values isn't a number or string '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", [2], 21]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_duplicate_tuple_value(validator):
    ''' Invalid: tuple values are duplicated '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_missing_value_in_tuple(validator):
    ''' Invalid: one of the tuples only has one value (not a tuple) '''

    axis = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            [20]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_empty_polygon_array(validator):
    ''' Invalid: polygon array is empty '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": []
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_invalid_polygons_axis(validator):
    ''' Invalid: type of values inconsistent with dataType (polygon) '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [1, 2, 3, 4, 5]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_duplicate_polygon_value(validator):
    ''' Invalid: polygon is duplicated '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ],
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_nearly_duplicate_polygon_value(validator):
    ''' Valid: polygon is nearly duplicated, but not quite '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ],
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.1, 1.0], [100.0, 0.0] ] ]
        ]
    }
    validator.validate(axis)


def test_polygon_axis_missing_coordinates_array(validator):
    ''' Invalid polygon axis: "coordinates" is missing '''

    axis = {
        "dataType": "polygon",
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_polygon_axis_empty_coordinates(validator):
    ''' Invalid polygon axis: "coordinates" is empty '''

    axis = {
        "dataType": "polygon",
        "coordinates": [ ],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_polygon_axis_with_invalid_coordinate_pair(validator):
    ''' Invalid: one of the coordinates is missing '''

    axis = {
        "dataType": "polygon",
        "coordinates": ["x", "y"],
        "values": [
            [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0], [100.0, 0.0] ]  ]
        ]
    }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_axis_with_mixed_type_values(validator):
    ''' Invalid: axis values can't be of mixed type '''

    axis = { "values" : [1, 2, 3, "4", 5] }
    with pytest.raises(ValidationError):
        validator.validate(axis)


def test_tuple_axis_with_mistyped_data_type(validator):
    ''' Valid: dataType is mistyped but valid as custom type '''

    axis = {
        "dataType": "tple",
        "coordinates": ["x", "y"],
        "values": [ [1, 20], [2, 21] ]
    }
    validator.validate(axis)
