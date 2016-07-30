from test_utils import MockRequestResponse, TestPlatformClient


class TestMarkDeliveryReceipt(TestPlatformClient):

    def test_mark_delivery_receipt(self, layerclient, monkeypatch):
        def verify_request_args(method, url, headers, data):
            assert method == "POST"
            assert url == (
                "https://api.layer.com/apps/TEST_APP_UUID/"
                "messages/TEST_MESSAGE_UUID/receipts"
			)
            assert headers == {
                'Accept': 'application/vnd.layer+json; version=1.0',
                'Authorization': 'Bearer TEST_BEARER_TOKEN',
                'Content-Type': 'application/json',
             }
            json_data = json.loads(data)
            assert json_data == {
                'type': 'read',
            }

            return MockRequestResponse(True, {})

        monkeypatch.setattr("requests.request", verify_request_args)
        layerclient.mark_delivery_receipt_message('TEST_MESSAGE_UUID', 'read')


