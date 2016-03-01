import datetime
from dateutil.tz import tzutc
import json
from LayerClient import LayerClient
from test_utils import MockRequestResponse, TestPlatformClient


class TestSendMessage(TestPlatformClient):

    def test_send_message(self, layerclient, monkeypatch):
        sender = LayerClient.Sender('alice', 'Alice')
        recipient = LayerClient.Sender('bob', 'Bob')

        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
            participants=[sender.id, recipient.id],
        )

        message_parts = [
            LayerClient.MessagePart(
                'Top secret message',
                'text/confidential',
            ),
        ]

        notification = LayerClient.PushNotification(
            'You have a new message!',
            sound='foo.wav',
            recipients={
                'bob': LayerClient.PushNotification('Message for Bob!'),
            },
        )

        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/conversations'
                '/f3cc7b32-3c92-11e4-baad-164230d1df67/messages'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'parts': [
                    {
                        'body': 'Top secret message',
                        'mime_type': 'text/confidential',
                    },
                ],
                'sender': {
                    'user_id': 'alice',
                },
                'notification': {
                    'text': 'You have a new message!',
                    'sound': 'foo.wav',
                    'recipients': {
                        'bob': {
                            'sound': None,
                            'text': 'Message for Bob!',
                        },
                    },
                },
            }

            return MockRequestResponse(
                True,
                {
                    'id': 'layer:///messages/TEST_MESSAGE_UUID',
                    'url': 'layer:///messages/TEST_MESSAGE_UUID',
                    'conversation': conversation.as_dict(),
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.send_message(
            conversation,
            sender,
            message_parts,
            notification=notification,
        )

    def test_parse_response(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                True,
                {
                    'id': (
                        'layer:///messages/'
                        '940de862-3c96-11e4-baad-164230d1df67'
                    ),
                    'url': (
                        'https://api.layer.com/apps/'
                        '24f43c32-4d95-11e4-b3a2-0fd00000020d/messages/'
                        '940de862-3c96-11e4-baad-164230d1df67'
                    ),
                    'conversation': {
                        'id': (
                            'layer:///conversations/'
                            'f3cc7b32-3c92-11e4-baad-164230d1df67'
                        ),
                        'url': (
                            'https://api.layer.com/apps/'
                            '24f43c32-4d95-11e4-b3a2-0fd00000020d'
                            '/conversations/'
                            'f3cc7b32-3c92-11e4-baad-164230d1df67'
                        ),
                    },
                    'parts': [
                        {
                            'body': 'Hello, World!',
                            'mime_type': 'text/plain'
                        },
                        {
                            'body': 'YW55IGNhcm5hbCBwbGVhc3VyZQ==',
                            'mime_type': 'image/jpeg',
                            'encoding': 'base64'
                        }
                    ],
                    'sent_at': '2014-09-09T04:44:47+00:00',
                    'sender': {
                        'name': 't-bone',
                        'user_id': None
                    },
                    'recipient_status': {
                        '777': 'sent',
                        '999': 'sent',
                        '111': 'sent'
                    }
                },
            )

        monkeypatch.setattr('requests.request', return_sample_response)
        sender = LayerClient.Sender('alice', 'Alice')
        messagepart = LayerClient.MessagePart('Hi!')
        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
        )
        response = layerclient.send_message(
            conversation,
            sender,
            [messagepart]
        )
        assert response.uuid() == '940de862-3c96-11e4-baad-164230d1df67'
        assert response.sent_at == datetime.datetime(
            2014, 9, 9, 4, 44, 47, tzinfo=tzutc()
        )
        assert response.sender.id is None
        assert response.sender.name == 't-bone'

        assert response.conversation.uuid() == (
            'f3cc7b32-3c92-11e4-baad-164230d1df67'
        )

        assert response.parts[0].body == 'Hello, World!'
        assert response.parts[1].mime_type == 'image/jpeg'
        assert response.parts[1].encoding == 'base64'

        assert response.recipient_status == {
            '777': 'sent',
            '999': 'sent',
            '111': 'sent'
        }

    def test_send_message_with_rich_content(self, layerclient, monkeypatch):
        sender = LayerClient.Sender('alice', 'Alice')
        recipient = LayerClient.Sender('bob', 'Bob')

        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
            participants=[sender.id, recipient.id],
        )

        message_parts = [
            LayerClient.MessagePart(
                None,
                mime='image/jpeg',
                content={
                    'id': 'layer:///content/TEST_CONTENT_UUID',
                    'size': 23,
                }
            ),
        ]

        def verify_request_args(method, url, headers, data):
            assert method == 'POST'
            assert url == (
                'https://api.layer.com/apps/TEST_APP_UUID/conversations'
                '/f3cc7b32-3c92-11e4-baad-164230d1df67/messages'
            )
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'parts': [
                    {
                        'mime_type': 'image/jpeg',
                        'content': {
                            'id': 'layer:///content/TEST_CONTENT_UUID',
                            'size': 23,
                        }
                    },
                ],
                'sender': {
                    'user_id': 'alice',
                }
            }

            return MockRequestResponse(
                True,
                {
                    'id': 'layer:///messages/TEST_MESSAGE_UUID',
                    'url': 'layer:///messages/TEST_MESSAGE_UUID',
                    'conversation': conversation.as_dict(),
                },
            )

        monkeypatch.setattr('requests.request', verify_request_args)
        layerclient.send_message(
            conversation,
            sender,
            message_parts
        )

    def test_parse_response_with_rich_content(self, layerclient, monkeypatch):
        def return_sample_response(method, url, headers, data):
            return MockRequestResponse(
                True,
                {
                    'id': (
                        'layer:///messages/'
                        '940de862-3c96-11e4-baad-164230d1df67'
                    ),
                    'url': (
                        'https://api.layer.com/apps/'
                        '24f43c32-4d95-11e4-b3a2-0fd00000020d/messages/'
                        '940de862-3c96-11e4-baad-164230d1df67'
                    ),
                    'conversation': {
                        'id': (
                            'layer:///conversations/'
                            'f3cc7b32-3c92-11e4-baad-164230d1df67'
                        ),
                        'url': (
                            'https://api.layer.com/apps/'
                            '24f43c32-4d95-11e4-b3a2-0fd00000020d'
                            '/conversations/'
                            'f3cc7b32-3c92-11e4-baad-164230d1df67'
                        ),
                    },
                    'parts': [
                        {
                            'mime_type': 'image/jpeg',
                            'content': {
                                'id': 'layer:///content/TEST_CONTENT_UUID',
                                'size': 23,
                                'download_url': 'some download url',
                                'refresh_url': 'some refresh url',
                                'expiration': '2014-09-10T04:44:47+00:00'
                            }
                        }
                    ],
                    'sent_at': '2014-09-09T04:44:47+00:00',
                    'sender': {
                        'name': 't-bone',
                        'user_id': None
                    },
                    'recipient_status': {
                        '777': 'sent',
                        '999': 'sent',
                        '111': 'sent'
                    }
                },
            )

        monkeypatch.setattr('requests.request', return_sample_response)
        sender = LayerClient.Sender('alice', 'Alice')
        messagepart = LayerClient.MessagePart(
            None,
            mime='image/jpeg',
            content={
                'id': 'layer:///content/TEST_CONTENT_UUID',
                'size': 23,
            }
        )
        conversation = LayerClient.Conversation(
            'layer:///conversations/f3cc7b32-3c92-11e4-baad-164230d1df67',
            'some_conversation_url',
        )
        response = layerclient.send_message(
            conversation,
            sender,
            [messagepart]
        )
        assert response.uuid() == '940de862-3c96-11e4-baad-164230d1df67'
        assert response.sent_at == datetime.datetime(
            2014, 9, 9, 4, 44, 47, tzinfo=tzutc()
        )
        assert response.sender.id is None
        assert response.sender.name == 't-bone'

        assert response.conversation.uuid() == (
            'f3cc7b32-3c92-11e4-baad-164230d1df67'
        )

        assert response.parts[0].body == None
        assert response.parts[0].mime_type == 'image/jpeg'
        assert response.parts[0].encoding == None
        assert isinstance(response.parts[0].content, dict)
        assert response.parts[0].content.get('id') == 'layer:///content/TEST_CONTENT_UUID'
        assert response.parts[0].content.get('size') == 23

        assert response.recipient_status == {
            '777': 'sent',
            '999': 'sent',
            '111': 'sent'
        }
