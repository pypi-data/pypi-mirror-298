# TikTokLiveWrapper

This project allows you to connect to TikTok livestreams and access available data using a creator's `@username`. It is designed to retrieve information from TikTok livestreams and cannot be used to post content or simulate interactions.

## Getting Started

1. Install the module:

   pip install TikTokLiveWrapper


## Create a connection to the chat:
    from TikTokLiveWrapper import TikTokLiveClient
    from TikTokLiveWrapper.events import ConnectEvent, CommentEvent

    client = TikTokLiveClient(unique_id="@username")

    @client.on(ConnectEvent)
    async def on_connect(event):
        print(f"Connected to @{event.unique_id}")

    async def on_comment(event):
        print(f"{event.user.nickname} -> {event.comment}")

    client.add_listener(CommentEvent, on_comment)

    client.run()


## Key Methods
- run: Connect to the livestream.
- add_listener: Add a listener for events.

## Events
Available events include: ConnectEvent, CommentEvent.

## License
MIT License. See the LICENSE file for details.