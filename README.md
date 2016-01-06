# Layer Platform API Client

## About

This library provides a simple python wrapper around the Layer [Platform
API](https://developer.layer.com/docs/platform) for managing
conversations, messages and announcements.

The project is currently in Alpha, so please report any bugs or missing
features.

## Installation

Using `pip`:

`
$ pip install LayerClient
`

Or, download the source code and run

`
$ python setup.py install
`

There is a tox configuration to make testing and linting easier - the following
are supported:

    $ tox                    # Runs py27-test (unit tests under python 2.7) by default
    $ tox -e py3-test        # Runs tests under python3
    $ tox -e py27-coverage   # Run test coverage report
    $ tox -e lint            # Check for flake8 violations

## Usage

The interface is close to that of the HTTP API itself. Here is an example of a
sending a simple message:

    from LayerClient import LayerClient

    LAYER_APP_ID = 'your_app_uuid'
    LAYER_APP_TOKEN = 'bearer_token_from_layer_console'

    client = LayerClient.PlatformClient(
        LAYER_APP_ID,
        LAYER_APP_TOKEN,
    )

    sender = LayerClient.Sender(
        id='alice',
        name='Alice',
    )

    receiver = LayerClient.Sender(
        id='bob',
        name='Bob',
    )

    conversation = client.create_conversation(
        [
            sender.id,
            receiver.id,
        ],
        distinct=True,
        metadata={
            'background_color': '#3c3c3c',
            'title': 'A test conversaton',
        }
    )

    message_parts = [
        LayerClient.MessagePart(
            'Sure is nice to not talk about Crypto for a change!'
        ),
    ]

    notification = LayerClient.PushNotification(
        'You got a message from Alice!'
    )

    message_resp = client.send_message(
        conversation,
        sender,
        message_parts,
        notification=notification,
    )

