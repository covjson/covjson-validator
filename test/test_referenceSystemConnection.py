# Pytests to test the referenceSystemConnection.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/referenceSystemConnection")

def test_valid_rsc(validator):
    ''' Tests an example of a valid reference system connection object '''

    rsc = {
        "coordinates": ["y", "x", "z"],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    validator.validate(rsc)


def test_missing_coordinates(validator):
    ''' Invalid: missing coordinates '''

    rsc = {
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(rsc)


def test_empty_coordinates(validator):
    ''' Invalid: empty coordinates array '''

    rsc = {
        "coordinates": [],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(rsc)


def test_invalid_coordinates_type(validator):
    ''' Invalid: invalid contents of coordinates array '''

    rsc = {
        "coordinates": [ ["y", "x", "z"] ],
        "system": {
            "type": "GeographicCRS",
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(rsc)


def test_missing_system(validator):
    ''' Invalid: missing system '''

    rsc = {
        "coordinates": ["y", "x", "z"]
    }
    with pytest.raises(ValidationError):
        validator.validate(rsc)


def test_invalid_system(validator):
    ''' Invalid coordinate system object (missing type) '''

    rsc = {
        "coordinates": ["y", "x", "z"],
        "system": {
            "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(rsc)
