# Pytests to test the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/domain")


def test_valid_grid_domain(grid_domain):
    ''' Tests an example of a Grid domain '''

    VALIDATOR.validate(grid_domain)


def test_missing_x_axis(grid_domain_1):
    ''' Invalid: Grid domain with missing x axis '''

    domain = grid_domain_1
    del domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_missing_y_axis(grid_domain_1):
    ''' Invalid: Grid domain with missing y axis '''

    domain = grid_domain_1
    del domain["axes"]["y"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_extra_multi_coordinate_axis(grid_domain_1):
    ''' Invalid: Grid domain with unrecognised multi-coordinate axis '''

    domain = grid_domain_1
    domain["axes"]["x2"] = domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


# TODO the schema forbids this currently, but the spec allows it
# def test_extra_single_coordinate_axis(grid_domain_1):
#     ''' Valid: Grid domain with unrecognised single-coordinate axis '''

#     domain = grid_domain_1
#     domain["axes"]["x2"] = { "values": [1] }
#     domain["referencing"].append({
#         "coordinates": ["x2"],
#         "system": {
#             "type": "GeographicCRS",
#             "id": "http://foo"
#         }
#     })
#     VALIDATOR.validate(domain)



def test_wrong_x_axis_type_with_no_domain_type(grid_domain_1):
    ''' Grid domain with a tuple axis instead of a primitive one, but
        there is no domainType so it will validate '''

    domain = grid_domain_1
    domain["axes"]["x"] = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    del domain["domainType"]
    VALIDATOR.validate(domain)

