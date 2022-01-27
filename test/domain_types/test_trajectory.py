# Pytests to test the Trajectory domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/domain")

@pytest.mark.exhaustive
def test_valid_trajectory_domain(trajectory_domain):
    ''' Tests an example of a Trajectory domain '''

    VALIDATOR.validate(trajectory_domain)


def test_missing_composite_axis(trajectory_domain):
    ''' Invalid: Trajectory domain with missing 'composite' axis '''

    del trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(trajectory_domain)


def test_wrong_composite_axis_type(trajectory_domain):
    ''' Invalid: Trajectory domain with primitive instead of tuple axis '''

    trajectory_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(trajectory_domain)


def test_extra_axis(trajectory_domain):
    ''' Invalid: Trajectory domain with unrecognised extra axis '''

    trajectory_domain["axes"]["composite2"] = \
        trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(trajectory_domain)


# TODO test optional 'z' axis has single coordinate only
# TODO test coordinate identifiers of 'composite' axis
#      to be "t","x","y","z" or "t","x","y"
# TODO test there cannot be both 'z' in 'composite' and a 'z' axis
