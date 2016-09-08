from LayerClient import LayerClient
from test_utils import MockRequestResponse, TestPlatformClient


class TestPrepareRichContent(TestPlatformClient):

    def test_prepare_rich_content(self, layerclient, monkeypatch):
        sender = LayerClient.Sender('alice', 'Alice')
        recipient = LayerClient.Sender('bob', 'Bob')

        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
            participants=[sender.id, recipient.id],
        )

        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/'
                'conversations/f3cc7b32-3c92-11e4-baad-164230d1df67/content'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
                'Upload-Content-Type': 'image/jpeg',
                'Upload-Content-Length': 23,
                # No support of the upload origin yet
                # 'Upload-Origin': 'http://mydomain.com'
            }
            assert data is None
            return MockRequestResponse(
                True,
                {
                    "id": "layer:///content/TEST_RICH_CONTENT_UUID",
                    "size": 23,
                    "upload_url": "someuploadurl",
                    "download_url": None,
                    "refresh_url": None,
                    "expiration": None
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.prepare_rich_content(
            conversation, 'image/jpeg', 23
        )

    def test_parse_response(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                True,
                {
                    "id": "layer:///content/TEST_RICH_CONTENT_UUID",
                    "size": 23,
                    "upload_url": "someuploadurl",
                    "download_url": None,
                    "refresh_url": None,
                    "expiration": None
                },
            )

        monkeypatch.setattr('requests.request', return_sample_response)
        sender = LayerClient.Sender('alice', 'Alice')
        recipient = LayerClient.Sender('bob', 'Bob')
        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
            participants=[sender.id, recipient.id],
        )
        rich_content = layerclient.prepare_rich_content(
            conversation, 'image/jpeg', 23
        )
        assert rich_content.id == 'layer:///content/TEST_RICH_CONTENT_UUID'
        assert rich_content.size == 23
        assert rich_content.upload_url == "someuploadurl"
