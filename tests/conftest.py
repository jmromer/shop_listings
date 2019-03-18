"""Test configuration"""

import os
import sys

import pytest

LIB_DIR = os.path.join('lib', os.path.dirname('.'))
sys.path.insert(0, os.path.abspath(LIB_DIR))

os.environ['ETSY_API_KEY'] = 'DUMMY_API_KEY'


@pytest.fixture(scope='module')
def vcr_cassette_dir():
    return os.path.join('tests', 'cassettes', os.path.dirname('.'))


@pytest.fixture
def app():
    from web.routes import app
    return app
