# Pytests to test the i18n.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/i18n")


def test_valid_i18n_object():
    ''' Tests an example of a valid i18n object '''

    valid_i18n = { "en" : "Fish", "fr" : "Poisson", "de": "Fisch" }
    VALIDATOR.validate(valid_i18n)


def test_invalid_i18n_object():
    ''' Tests an example of an invalid i18n object '''

    invalid_i18n = { "en" : { "de" : "Fisch" } }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(invalid_i18n)


def test_invalid_i18n_language_tag():
    ''' Tests an example of an invalid i18n language tag '''

    invalid_i18n = { "e" : "Fish" }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(invalid_i18n)
