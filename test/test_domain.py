# Pytests to test the domain.json schema file
# See domain_types/ for tests specific to each domain type

import random
import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


def test_valid_anonymous_domain(validator, domain):
    ''' Tests a domain with no domainType (valid, but not recommended) '''

    del domain["domainType"]
    validator.validate(domain)


def test_valid_custom_domain(validator, domain):
    ''' Tests a domain with a custom domainType (valid, but not recommended) '''

    domain["domainType"] = "https://foo/custom"
    validator.validate(domain)


def test_missing_type(validator, domain):
    ''' Invalid: Domain with missing "type" '''

    del domain["type"]
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_misspelled_type(validator, domain):
    ''' Invalid: Domain with misspelled "type" '''

    domain["type"] = "Doman"
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_wrong_domain_type(validator, domain):
    ''' Invalid: Domain with wrong type for "domainType" '''

    domain["domainType"] = [ "Grid" ]
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_missing_axes(validator, domain):
    ''' Invalid: Domain with missing "axes" '''

    del domain["axes"]
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_wrong_axes_type(validator, domain):
    ''' Invalid: Domain with wrong type for "axes" '''

    domain["axes"] = "xyz"
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_missing_referencing(validator, domain):
    ''' Invalid: Domain with missing "referencing" '''

    del domain["referencing"]
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_wrong_referencing_type(validator, domain):
    ''' Invalid: Domain with wrong type for "referencing" '''

    domain["referencing"] = "WGS84 and UTC"
    with pytest.raises(ValidationError):
        validator.validate(domain)


def test_additional_property(validator, domain):
    ''' Valid: Domain with additional property '''

    domain["ex:comment"] = "This is a comment"
    validator.validate(domain)


def test_wrong_axis_type(validator, domain):
    ''' Invalid: Domain with common domain type with mismatching axis data type '''

    axes = domain["axes"]

    # pick a random axis and change its data type
    name = list(axes.keys())[random.randint(0, len(axes) - 1)]
    if name in ['x', 'y', 'z', 't']:
        axes[name] = {
            "dataType": "tuple",
            "coordinates": ["t", "x", "y"],
            "values": [
                ["2008-01-01T04:00:00Z", 1, 20],
                ["2008-01-01T04:30:00Z", 2, 21]
            ]
        }
    elif name == 'composite':
        axes[name] = { "values": [1] }

    with pytest.raises(ValidationError):
        validator.validate(domain)

# TODO test that coordinates without matching reference system are rejected
#      The spec doesn't reject it, but probably should.

# For all common domain types:
# TODO test that 't', if existing, must be connected to a TemporalRS
# TODO test that 'x', 'y', 'z', if existing, must be connected
#      to GeographicCRS / ProjectedCRS
# NOTE: this may need stricter text in the spec, currently:
# "The axis and coordinate identifiers "x" and "y" MUST refer
#  to horizontal spatial coordinates, "z" to vertical spatial
#  coordinates, and all of "x", "y", and "z" MUST be referenced
#  by a spatial coordinate reference system."
