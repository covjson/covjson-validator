# Pytests to test the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/domain")


def get_sample_grid_domain():
    ''' Returns a sample of a valid grid domain '''

    return {
        "type": "Domain",
        "domainType": "Grid",
        "axes": {
            "x": { "values": [1, 2, 3] },
            "y": { "values": [20, 21] },
            "z": { "values": [1] },
            "t": { "values": ["2008-01-01T04:00:00Z"] }
        },
        "referencing": [{
            "coordinates": ["t"],
            "system": {
                "type": "TemporalRS",
                "calendar": "Gregorian"
            }
        }, {
            "coordinates": ["y", "x", "z"],
            "system": {
                "type": "GeographicCRS",
                "id": "http://www.opengis.net/def/crs/EPSG/0/4979"
            }
        }]
    }


def get_sample_trajectory_domain():
    ''' Returns a sample of a valid trajectory domain '''

    return {
        "type": "Domain",
        "domainType": "Trajectory",
        "axes": {
            "composite": {
                "dataType": "tuple",
                "coordinates": ["t", "x", "y"],
                "values": [
                    ["2008-01-01T04:00:00Z", 1, 20],
                    ["2008-01-01T04:30:00Z", 2, 21]
                ]
            }
        },
        "referencing": [{
            "coordinates": ["t"],
            "system": {
                "type": "TemporalRS",
                "calendar": "Gregorian"
            }
        }, {
            "coordinates": ["x", "y"],
            "system": {
                "type": "GeographicCRS",
                "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        }]
    }


def test_valid_grid_domain():
    ''' Tests an example of a Grid domain '''

    domain = get_sample_grid_domain()
    VALIDATOR.validate(domain)


def test_valid_trajectory_domain():
    ''' Tests an example of a Trajectory domain '''

    domain = get_sample_trajectory_domain()
    VALIDATOR.validate(domain)


def test_valid_anonymous_domain():
    ''' Tests a domain with no domainType (valid, but not recommended) '''

    domain = get_sample_trajectory_domain()
    del domain["domainType"]
    VALIDATOR.validate(domain)


def test_missing_type():
    ''' Invalid: Grid domain with missing "type"  '''

    domain = get_sample_grid_domain()
    del domain["type"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_misspelled_type():
    ''' Invalid: Grid domain with misspelled "type"  '''

    domain = get_sample_grid_domain()
    domain["type"] = "Doman"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_missing_axes():
    ''' Invalid: Grid domain with missing "axes"  '''

    domain = get_sample_grid_domain()
    del domain["axes"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_wrong_domain_type():
    ''' Invalid: Grid domain with wrong type for "domainType"  '''

    domain = get_sample_grid_domain()
    domain["domainType"] = [ "Grid" ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_missing_x_axis():
    ''' Invalid: Grid domain with missing x axis  '''

    domain = get_sample_grid_domain()
    del domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_missing_y_axis():
    ''' Invalid: Grid domain with missing y axis  '''

    domain = get_sample_grid_domain()
    del domain["axes"]["y"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_extra_grid_axis():
    ''' Invalid: Grid domain with unrecognised extra axis  '''

    domain = get_sample_grid_domain()
    domain["axes"]["x2"] = domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


# TODO more tests for Trajectory (and perhaps refactor each set of domain type tests to separate folder)