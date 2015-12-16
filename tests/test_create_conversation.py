import json
from test_utils import MockRequestResponse, TestPlatformClient


class TestCreateConverstaion(TestPlatformClient):

    def test_create_conversation(self, layerclient, monkeypatch):
        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/conversations'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'participants': 'TEST_CONVERSATION_UUID',
                'metadata': None,
                'distinct': True,
            }

            return MockRequestResponse(
                True,
                {
                    'id': 'layer:///conversation/TEST_CONVERSATION_UUID',
                    'url': 'layer:///conversation/TEST_CONVERSATION_UUID',
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.create_conversation('TEST_CONVERSATION_UUID')

    def test_create_conversation_with_options(self, layerclient, monkeypatch):
        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/conversations'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'participants': 'TEST_CONVERSATION_UUID',
                'metadata': {
                    'Topic': 'A coffee conversation',
                    'Background': '#C0FFEE',
                },
                'distinct': False,
            }

            return MockRequestResponse(
                True,
                {
                    'id': 'layer:///conversation/TEST_CONVERSATION_UUID',
                    'url': 'layer:///conversation/TEST_CONVERSATION_UUID',
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.create_conversation(
            'TEST_CONVERSATION_UUID',
            False,
            {
                'Topic': 'A coffee conversation',
                'Background': '#C0FFEE',
            },
        )
