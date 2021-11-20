# Pytests to test the referenceSystemConnection.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/referenceSystemConnection")


def test_valid_rsc():
    ''' Tests an example of a valid reference system connection object '''

    rsc = {
        "coordinates": ["y", "x", "z"],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    VALIDATOR.validate(rsc)


def test_missing_coordinates():
    ''' Invalid: missing coordinates '''

    rsc = {
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(rsc)


def test_empty_coordinates():
    ''' Invalid: empty coordinates array '''

    rsc = {
        "coordinates": [],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(rsc)


def test_invalid_coordinates_type():
    ''' Invalid: invalid contents of coordinates array '''

    rsc = {
        "coordinates": [ ["y", "x", "z"] ],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(rsc)


def test_missing_system():
    ''' Invalid: missing system '''

    rsc = {
        "coordinates": ["y", "x", "z"]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(rsc)


def test_invalid_system():
    ''' Invalid coordinate system object (missing type) '''

    rsc = {
        "coordinates": ["y", "x", "z"],
        "system": {
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(rsc)
