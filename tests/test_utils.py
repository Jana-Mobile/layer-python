import pytest
from LayerClient import LayerClient


class MockRequestResponse(object):

    def __init__(self, ok, json):
        self.ok = ok
        self._json = json

    def json(self):
        return self._json


class TestPlatformClient(object):

    @pytest.yield_fixture
    def layerclient(self):
        client = LayerClient.PlatformClient(
            'TEST_APP_UUID',
            'TEST_BEARER_TOKEN',
        )
        yield client
