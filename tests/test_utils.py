import pytest
from LayerClient import LayerClient


class MockRequestResponse(object):

    def __init__(self, ok, json=None, text=None, status_code=200):
        self.ok = ok
        self._json = json
        self.text = text
        self.status_code = status_code

    def json(self):
        if self._json is None:
            raise ValueError
        return self._json


class TestPlatformClient(object):

    @pytest.yield_fixture
    def layerclient(self):
        client = LayerClient.PlatformClient(
            'TEST_APP_UUID',
            'TEST_BEARER_TOKEN',
        )
        yield client
