# Pytests to test the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator
from domain_generator import get_random_domain_of_type

VALIDATOR = validator.create_custom_validator("/schemas/domain")


def get_random_trajectory_domain():
    domain = get_random_domain_of_type('Trajectory')
    assert domain['domainType'] == 'Trajectory'
    return domain


def test_valid_trajectory_domain():
    ''' Tests an example of a Trajectory domain '''

    domain = get_random_trajectory_domain()
    VALIDATOR.validate(domain)


def test_missing_composite_axis():
    ''' Invalid: Trajectory domain with missing 'composite' axis '''

    domain = get_random_trajectory_domain()
    del domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_wrong_composite_axis_type():
    ''' Invalid: Trajectory domain with primitive instead of tuple axis '''

    domain = get_random_trajectory_domain()
    domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


def test_extra_axis():
    ''' Invalid: Trajectory domain with unrecognised extra axis '''

    domain = get_random_trajectory_domain()
    domain["axes"]["composite2"] = domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(domain)


# TODO test optional 'z' axis has single coordinate only
# TODO test coordinate identifiers of 'composite' axis
#      to be "t","x","y","z" or "t","x","y"
# TODO test there cannot be both 'z' in 'composite' and a 'z' axis
