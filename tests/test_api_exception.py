import pytest
from LayerClient import LayerClient
from test_utils import MockRequestResponse, TestPlatformClient


class TestApiException(TestPlatformClient):

    def test_json_exception(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                False,
                json={
                    'message': 'Operation not supported',
                    'code': 40,
                    'id': 23,
                },
                status_code=401,
            )

        monkeypatch.setattr('requests.request', return_sample_response)

        with pytest.raises(LayerClient.LayerPlatformException) as e:
            layerclient.get_conversation('some_uuid')

        assert e.value.message == 'Operation not supported'
        assert e.value.http_code == 401
        assert e.value.code == 40
        assert e.value.error_id == 23

    def test_raw_exception(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                False,
                text='Internal server error',
                status_code=500,
            )

        monkeypatch.setattr('requests.request', return_sample_response)

        with pytest.raises(LayerClient.LayerPlatformException) as e:
            layerclient.get_conversation('some_uuid')

        assert e.value.message == 'Internal server error'
        assert e.value.http_code == 500
