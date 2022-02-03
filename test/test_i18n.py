# Pytests to test the i18n.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/i18n")


def test_valid_i18n_object(validator):
    ''' Tests an example of a valid i18n object '''

    valid_i18n = { "en" : "Fish", "fr" : "Poisson", "de": "Fisch" }
    validator.validate(valid_i18n)


def test_invalid_i18n_object(validator):
    ''' Tests an example of an invalid i18n object '''

    invalid_i18n = { "en" : { "de" : "Fisch" } }
    with pytest.raises(ValidationError):
        validator.validate(invalid_i18n)


# TODO: add test for invalid language strings?
