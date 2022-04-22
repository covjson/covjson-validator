# Pytests to test the Grid domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_grid_domain(validator, grid_domain):
    ''' Tests an example of a Grid domain '''

    validator.validate(grid_domain)


def test_missing_x_axis(validator, grid_domain):
    ''' Invalid: Grid domain with missing x axis '''

    del grid_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_missing_y_axis(validator, grid_domain):
    ''' Invalid: Grid domain with missing y axis '''

    del grid_domain["axes"]["y"]
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_empty_x_axis(validator, grid_domain):
    ''' Invalid: Grid domain with empty 'x' axis '''

    grid_domain["axes"]["x"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_empty_y_axis(validator, grid_domain):
    ''' Invalid: Grid domain with empty 'y' axis '''

    grid_domain["axes"]["y"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_empty_z_axis(validator, grid_domain):
    ''' Invalid: Grid domain with empty 'z' axis '''

    grid_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_empty_t_axis(validator, grid_domain):
    ''' Invalid: Grid domain with empty 't' axis '''

    grid_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


def test_extra_multi_coordinate_axis(validator, grid_domain):
    ''' Invalid: Grid domain with unrecognised multi-coordinate axis '''

    grid_domain["axes"]["x2"] = grid_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(grid_domain)


# TODO the schema forbids this currently, but the spec allows it
# def test_extra_single_coordinate_axis(validator, grid_domain):
#     ''' Valid: Grid domain with unrecognised single-coordinate axis '''

#     grid_domain["axes"]["x2"] = { "values": [1] }
#     grid_domain["referencing"].append({
#         "coordinates": ["x2"],
#         "system": {
#             "type": "GeographicCRS",
#             "id": "http://foo"
#         }
#     })
#     validator.validate(grid_domain)


def test_wrong_x_axis_type_with_no_domain_type(validator, grid_domain):
    ''' Grid domain with a tuple axis instead of a primitive one, but
        there is no domainType so it will validate '''

    grid_domain["axes"]["x"] = {
        "dataType": "tuple",
        "coordinates": ["t", "x", "y"],
        "values": [
            ["2008-01-01T04:00:00Z", 1, 20],
            ["2008-01-01T04:30:00Z", 2, 21]
        ]
    }
    del grid_domain["domainType"]
    validator.validate(grid_domain)
