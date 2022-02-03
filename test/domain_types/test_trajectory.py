# Pytests to test the Trajectory domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")

@pytest.mark.exhaustive
def test_valid_trajectory_domain(validator, trajectory_domain):
    ''' Tests an example of a Trajectory domain '''

    validator.validate(trajectory_domain)


def test_missing_composite_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with missing 'composite' axis '''

    del trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_wrong_composite_axis_type(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with primitive instead of tuple axis '''

    trajectory_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_extra_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with unrecognised extra axis '''

    trajectory_domain["axes"]["composite2"] = \
        trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


# TODO test optional 'z' axis has single coordinate only
# TODO test coordinate identifiers of 'composite' axis
#      to be "t","x","y","z" or "t","x","y"
# TODO test there cannot be both 'z' in 'composite' and a 'z' axis
