# Pytests to test the observedProperty.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/observedProperty")


def test_valid_minimal_observed_property():
    ''' Tests an example of a valid minimal i18n object '''

    op = { "label" : { "en" : "sea surface temperature" } }
    VALIDATOR.validate(op)


def test_continuous_observed_property():
    ''' Tests an observedProperty for continuous data '''

    op = {
        "id" : "http://vocab.nerc.ac.uk/standard_name/sea_surface_temperature/",
        "label" : { "en" : "Sea Surface Temperature" },
        "description" : { "en" : "The temperature of sea water near the surface" }
    }
    VALIDATOR.validate(op)


def test_categorical_observed_property():
    ''' Tests an observedProperty for categorical data '''

    op = {
        "id" : "http://example.com/land_cover",
        "label" : { "en" : "Land cover" },
        "description" : { "en" : "The material on the surface of the land" },
        "categories" : [
            {
                "id" : "http://example.com/urban",
                "label" : { "en" : "urban"},
                "description" : { "en": "Houses and stuff like that" }
            },
            {
                "id" : "http://example.com/forest",
                "label" : { "en" : "forest"}
            }
        ]
    }
    VALIDATOR.validate(op)


def test_invalid_label():
    ''' Invalid: label must be an i18n object '''

    op = { "label" : "sea surface temperature" }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(op)


def test_invalid_description():
    ''' Invalid: description must be an i18n object '''

    op = {
        "label" : { "en" : "sea surface temperature" },
        "description" : "This should be an i18n object"
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(op)


def test_missing_label():
    ''' Invalid: label must be present '''

    op = {
        "description" : { "en" : "The temperature of sea water near the surface" }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(op)


def test_empty_categories():
    ''' Invalid: categories array can't be empty if present '''

    op = {
        "label" : { "en" : "Land surface type" },
        "categories" : []
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(op)


def test_non_array_categories():
    ''' Invalid: categories must be an array '''

    op = {
        "label" : { "en" : "Land surface class" },
        "categories" : {
            "id" : "http://example.com/urban",
            "label" : { "en" : "urban"}
        }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(op)
