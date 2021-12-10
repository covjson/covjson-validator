# Pytests to test the parameterGroup.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/parameterGroup")

def get_example_parameter_group():
    return {
        "type": "ParameterGroup",
        "label": {
            "en": "Daily sea surface temperature with uncertainty information"
        },
        "description": {
            "en": "Long description..."
        },
        "observedProperty": {
            "id": "http://vocab.nerc.ac.uk/standard_name/sea_surface_temperature/",
            "label": {
                "en": "Sea surface temperature"
            }
        },
        "members": ["SST_mean", "SST_stddev"]
    }


def test_valid_parameter_group():
    ''' Tests an example of a valid parameter group '''

    group = get_example_parameter_group()
    VALIDATOR.validate(group)


def test_no_type():
    ''' Invalid: parameter group with no "type" '''

    group = get_example_parameter_group()
    del group["type"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_wrong_type():
    ''' Invalid: parameter group with mistyped "type" '''

    group = get_example_parameter_group()
    group["type"] = "ParametreGroup"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_id_with_wrong_type():
    ''' Invalid: parameter group with incorrect "id" type '''

    group = get_example_parameter_group()
    group["id"] = { "href": "http://foo" }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_label_with_incorrect_type():
    ''' Invalid: parameter group with incorrect "label" type '''

    group = get_example_parameter_group()
    group["label"] = "Not an i18n object"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_description_with_incorrect_type():
    ''' Invalid: parameter group with incorrect "description" type '''

    group = get_example_parameter_group()
    group["description"] = "Not an i18n object"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_observed_property_with_wrong_type():
    ''' Invalid: parameter group with incorrect "observedProperty" type '''

    group = get_example_parameter_group()
    group["observedProperty"] = "Wind velocity"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_missing_label_and_observed_property():
    ''' Invalid: parameter group with both "label" & "observedProperty" missing '''

    group = get_example_parameter_group()
    del group["label"]
    del group["observedProperty"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_missing_members():
    ''' Invalid: parameter group with "members" missing '''

    group = get_example_parameter_group()
    del group["members"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_empty_members():
    ''' Invalid: parameter group with empty "members" '''

    group = get_example_parameter_group()
    group["members"] = []
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


def test_members_with_incorrect_item_type():
    ''' Invalid: parameter group with "members" containing non-string items '''

    group = get_example_parameter_group()
    group["members"] = ["SST_mean", 1]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(group)


# TODO the spec says observedProperty is the same as for Parameter
#      but it wouldn't make sense to have "categories" in there
