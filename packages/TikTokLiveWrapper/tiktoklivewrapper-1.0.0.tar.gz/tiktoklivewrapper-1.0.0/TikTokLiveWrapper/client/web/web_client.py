from TikTokLiveWrapper.client.web.routes import FetchIsLiveRoute
from TikTokLiveWrapper.client.web.routes.room_id_api import RoomIdAPIRoute
from TikTokLiveWrapper.client.web.routes.download_video import VideoFetchRoute
from TikTokLiveWrapper.client.web.routes.gift_list import GiftListRoute
from TikTokLiveWrapper.client.web.routes.image_download import ImageFetchRoute
from TikTokLiveWrapper.client.web.routes.room_id_live_html import RoomIdLiveHTMLRoute
from TikTokLiveWrapper.client.web.routes.room_info import FetchRoomInfoRoomIdRoute
from TikTokLiveWrapper.client.web.routes.sign_fetch import SignFetchRoute
from TikTokLiveWrapper.client.web.web_base import TikTokHTTPClient


class TikTokWebClient(TikTokHTTPClient):
    """
    Wrapper for the HTTP client to add web routes

    """

    def __init__(self, **kwargs):
        """
        Create a web client with registered TikTok routes

        :param kwargs: Arguments to pass to the super-class

        """

        super().__init__(**kwargs)

        self.fetch_room_id_from_html: RoomIdLiveHTMLRoute = RoomIdLiveHTMLRoute(self)
        self.fetch_room_id_from_api: RoomIdAPIRoute = RoomIdAPIRoute(self)
        self.fetch_room_info: FetchRoomInfoRoomIdRoute = FetchRoomInfoRoomIdRoute(self)
        self.fetch_gift_list: GiftListRoute = GiftListRoute(self)
        self.fetch_image: ImageFetchRoute = ImageFetchRoute(self)
        self.fetch_video: VideoFetchRoute = VideoFetchRoute(self)
        self.fetch_is_live: FetchIsLiveRoute = FetchIsLiveRoute(self)
        self.fetch_sign_fetch: SignFetchRoute = SignFetchRoute(self, self._sign_api_key)
