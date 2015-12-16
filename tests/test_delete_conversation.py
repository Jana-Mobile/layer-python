from test_utils import MockRequestResponse, TestPlatformClient


class TestDeleteConverstaion(TestPlatformClient):

    def test_delete_conversation(self, layerclient, monkeypatch):
        def verify_request_args(method, url, headers, data):
            assert method == "DELETE"
            assert url == (
                "https://api.layer.com/apps/TEST_APP_UUID/"
                "conversations/TEST_CONVERSATION_UUID"
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            assert data is None

            return MockRequestResponse(True, {})

        monkeypatch.setattr("requests.request", verify_request_args)
        layerclient.delete_conversation('TEST_CONVERSATION_UUID')
