# pytest fixtures available in tests

from pathlib import Path
import json
from copy import deepcopy
import pytest

DOMAINS = {}
DOMAINS_BY_TYPE = {}

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


def pytest_generate_tests(metafunc):
    exhaustive_cli = metafunc.config.getoption("exhaustive")
    exhaustive_mark = "exhaustive" in metafunc.definition.keywords
    single = not exhaustive_cli and not exhaustive_mark
    if 'domain' in metafunc.fixturenames:
        if single:
            metafunc.parametrize('domain',
                                 [deepcopy(next(iter(DOMAINS.values())))],
                                 ids=[next(iter(DOMAINS.keys()))])
        else:
            metafunc.parametrize('domain',
                                 map(deepcopy, DOMAINS.values()),
                                 ids=DOMAINS.keys())
    for domain_type in DOMAINS_BY_TYPE.keys():
        fixture_name = f"{domain_type.lower()}_domain"
        if fixture_name not in metafunc.fixturenames:
            continue
        if single:
            metafunc.parametrize(fixture_name,
                                 [deepcopy(next(iter(DOMAINS_BY_TYPE[domain_type].values())))],
                                 ids=[next(iter(DOMAINS_BY_TYPE[domain_type].keys()))])
        else:
            metafunc.parametrize(fixture_name,
                                 map(deepcopy, DOMAINS_BY_TYPE[domain_type].values()),
                                 ids=DOMAINS_BY_TYPE[domain_type].keys())


@pytest.fixture(scope='session')
def get_domain():
    def _get_domain(domain_name):
        return deepcopy(DOMAINS[domain_name])
    return _get_domain

