# Pytests to test the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator
from domain_generator import get_random_domain_of_type

VALIDATOR = validator.create_custom_validator("/schemas/domain")


def get_random_grid_domain():
    domain = get_random_domain_of_type('Grid')
    assert domain['domainType'] == 'Grid'
    return domain


def test_valid_grid_domain():
    ''' Tests an example of a Grid domain '''

    domain = get_random_grid_domain()
    VALIDATOR.validate(domain)


def test_missing_x_axis():
    ''' Invalid: Grid domain with missing x axis '''

    domain = get_random_grid_domain()
    del domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_missing_y_axis():
    ''' Invalid: Grid domain with missing y axis '''

    domain = get_random_grid_domain()
    del domain["axes"]["y"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_extra_multi_coordinate_axis():
    ''' Invalid: Grid domain with unrecognised multi-coordinate axis '''

    domain = get_random_grid_domain()
    domain["axes"]["x2"] = domain["axes"]["x"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


# TODO the schema forbids this currently, but the spec allows it
# def test_extra_single_coordinate_axis():
#     ''' Valid: Grid domain with unrecognised single-coordinate axis '''

#     domain = get_random_grid_domain()
#     domain["axes"]["x2"] = { "values": [1] }
#     domain["referencing"].append({
#         "coordinates": ["x2"],
#         "system": {
#             "type": "GeographicCRS",
#             "id": "http://foo"
#         }
#     })
#     VALIDATOR.validate(domain)



def test_wrong_x_axis_type_with_no_domain_type():
    ''' Grid domain with a tuple axis instead of a primitive one, but
        there is no domainType so it will validate '''

    domain = get_random_grid_domain()
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

