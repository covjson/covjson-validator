# pytest fixtures available in tests

from pathlib import Path
import json
import copy
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


@pytest.fixture(scope='session')
def get_domain():
    def _get_domain(domain_name):
        return copy.deepcopy(DOMAINS[domain_name])
    return _get_domain


@pytest.fixture(params=DOMAINS.values(),
                ids=DOMAINS.keys())
def domain(request):
    return copy.deepcopy(request.param)


@pytest.fixture(params=[next(iter(DOMAINS.values()))],
                ids=[next(iter(DOMAINS.keys()))])
def domain_1(request):
    return copy.deepcopy(request.param)


def generate_domain_type_fixture_all(domain_type):
    @pytest.fixture(params=DOMAINS_BY_TYPE[domain_type].values(),
                    ids=DOMAINS_BY_TYPE[domain_type].keys())
    def my_fixture(request):
        return copy.deepcopy(request.param)
    return my_fixture


for domain_type in DOMAINS_BY_TYPE.keys():
    globals()[f"{domain_type.lower()}_domain"] = \
        generate_domain_type_fixture_all(domain_type)


def generate_domain_type_fixture_single(domain_type):    
    @pytest.fixture(params=[next(iter(DOMAINS_BY_TYPE[domain_type].values()))],
                    ids=[next(iter(DOMAINS_BY_TYPE[domain_type].keys()))])
    def my_fixture(request):
        return copy.deepcopy(request.param)
    return my_fixture


for domain_type in DOMAINS_BY_TYPE.keys():
    globals()[f"{domain_type.lower()}_domain_1"] = \
        generate_domain_type_fixture_single(domain_type)

