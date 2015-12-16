import datetime
from dateutil.tz import tzutc
import json
from LayerClient import LayerClient
from test_utils import MockRequestResponse, TestPlatformClient


class TestSendAnnouncement(TestPlatformClient):

    def test_send_announcement(self, layerclient, monkeypatch):
        sender = LayerClient.Sender('alice', 'Alice')
        recipients = ['bob', 'charlie']

        message_parts = [
            LayerClient.MessagePart(
                'Top secret message',
                'text/confidential',
            ),
        ]

        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/announcements'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'recipients': recipients,
                'parts': [{
                    'body': 'Top secret message',
                    'mime_type': 'text/confidential',
                }],
                'sender': {
                    'name': 'Alice',
                }
            }

            return MockRequestResponse(
                True,
                {
                    'id': 'layer:///messages/TEST_MESSAGE_UUID',
                    'url': 'layer:///messages/TEST_MESSAGE_UUID',
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.send_announcement(
            sender,
            recipients,
            message_parts,
        )

    def test_parse_response(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                True,
                {
                    'id': (
                        'layer:///announcements/'
                        'f3cc7b32-3c92-11e4-baad-164230d1df67'
                    ),
                    'url': (
                        'https://api.layer.com/apps/'
                        '24f43c32-4d95-11e4-b3a2-0fd00000020d/announcements'
                        '/f3cc7b32-3c92-11e4-baad-164230d1df67'
                    ),
                    'sent_at': '2014-09-15T04:44:47+00:00',
                    'recipients': ['bob', 'charlie'],
                    'sender': {
                        'name': 'Alice',
                        'user_id': None
                    },
                    'parts': [
                        {
                            'body': 'Hello, World!',
                            'mime_type': 'text/plain'
                        }
                    ]
                },
            )

        monkeypatch.setattr('requests.request', return_sample_response)
        sender = LayerClient.Sender('alice', 'Alice')
        recipients = ['bob', 'charlie']
        message_parts = [
            LayerClient.MessagePart(
                'Top secret message',
            ),
        ]
        announcement = layerclient.send_announcement(
            sender,
            recipients,
            message_parts,
        )
        assert announcement.uuid() == 'f3cc7b32-3c92-11e4-baad-164230d1df67'
        assert announcement.sent_at == datetime.datetime(
            2014, 9, 15, 4, 44, 47, tzinfo=tzutc()
        )
        assert announcement.recipients == ['bob', 'charlie']
        assert announcement.sender.as_dict() == {
            'name': 'Alice',
        }
        assert announcement.parts[0].body == 'Hello, World!'
        assert announcement.parts[0].mime_type == 'text/plain'
