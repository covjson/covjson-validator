# pytest fixtures available in tests
from pathlib import Path
import json
from copy import deepcopy
import pytest
import jsonschema

import validator as validator_
from tools.bundle_schema import bundle_schema
from tools.downgrade_schema_to_draft07 import downgrade_schema_to_draft07


VALIDATOR_CACHE = {}
DOMAINS = {}
DOMAINS_BY_TYPE = {}


@pytest.fixture(scope="session")
def schema_store():
    return validator_.create_schema_store()


@pytest.fixture(params=["native", "draft-07-bundle"])
def validator(request, schema_store):
    mode = request.param
    schema_marker = request.node.get_closest_marker("schema")
    assert schema_marker is not None
    schema_id = schema_marker.args[0]
    validator = VALIDATOR_CACHE.get((mode, schema_id))
    if validator:
        return validator
    schema = schema_store[schema_id]
    if mode == "native":
        resolver = jsonschema.RefResolver(None, referrer=None, store=schema_store)
        validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    elif mode == "draft-07-bundle":
        schema = bundle_schema(schema_store, schema_id)
        schema = downgrade_schema_to_draft07(schema)
        validator = jsonschema.Draft7Validator(schema)
        # dump to disk for debugging purposes
        tmp_dir = Path("tmp")
        tmp_dir.mkdir(exist_ok=True)
        schema_name = schema_id.removeprefix("/schemas/")
        schema_file = tmp_dir / f"{schema_name}.draft07.json"
        with open(schema_file, "w") as f:
            json.dump(schema, f, indent=2)
    else:
        raise ValueError(f"Unknown mode {mode}")
    VALIDATOR_CACHE[(mode, schema_id)] = validator
    return validator


def load_domain_test_data():
    this_dir = Path(__file__).parent
    domain_dir = this_dir / 'test_data' / 'domains'
    for domain_type_dir in sorted(domain_dir.iterdir()):
        domain_type = domain_type_dir.name
        DOMAINS_BY_TYPE[domain_type] = {}
        for domain_file in sorted(domain_type_dir.glob('*.json')):
            with domain_file.open() as f:
                domain = json.load(f)
                name = domain_file.stem
                DOMAINS[name] = domain
                DOMAINS_BY_TYPE[domain_type][name] = domain

load_domain_test_data()


def pytest_addoption(parser):
    parser.addoption("--exhaustive", action="store_true",
                     help="run tests requesting a domain with all domains, " + \
                          "irrespective of 'exhaustive' marker")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "exhaustive: mark test to always run with all domains"
    )
    config.addinivalue_line(
        "markers", "schema(name): use the named schema for the 'validator' fixture"
    )


# Indirect parametrization fixtures, see pytest_generate_tests below.
# Necessary to always return a fresh copy of a domain that can
# be modified by the test.
@pytest.fixture
def domain(request):
    return deepcopy(DOMAINS[request.param])

for domain_type in DOMAINS_BY_TYPE.keys():
    fixture_name = f"{domain_type.lower()}_domain"
    globals()[fixture_name] = domain


def pytest_generate_tests(metafunc):
    exhaustive_cli = metafunc.config.getoption("exhaustive")
    exhaustive_mark = "exhaustive" in metafunc.definition.keywords
    single = not exhaustive_cli and not exhaustive_mark
    if 'domain' in metafunc.fixturenames:
        if single:
            metafunc.parametrize('domain',
                                 [next(iter(DOMAINS.keys()))],
                                 indirect=True)
        else:
            metafunc.parametrize('domain',
                                 DOMAINS.keys(),
                                 indirect=True)
    for domain_type in DOMAINS_BY_TYPE.keys():
        fixture_name = f"{domain_type.lower()}_domain"
        if fixture_name not in metafunc.fixturenames:
            continue
        if single:
            metafunc.parametrize(fixture_name,
                                 [next(iter(DOMAINS_BY_TYPE[domain_type].keys()))],
                                 indirect=True)
        else:
            metafunc.parametrize(fixture_name,
                                 DOMAINS_BY_TYPE[domain_type].keys(),
                                 indirect=True)


@pytest.fixture(scope='session')
def get_domain():
    def _get_domain(domain_name):
        return deepcopy(DOMAINS[domain_name])
    return _get_domain

