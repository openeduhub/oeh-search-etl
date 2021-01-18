import csv
import json
import logging
import os
import re
from typing import Generator, List
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from overrides import overrides
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider

import converter.env as env
import converter.items as items
from converter.constants import Constants
from converter.spiders.lom_base import LomBase

# TODO: Find suitable target field for channel/playlist information:
#   - Title (channel title included as organization in lifecycle-author)
#   - Description
#   - URL (channel url included as url in lifecycle-author)
#
# TODO: Find out whether `publishedAt` reflects modification
#   - Find another way to set `hash` if not
#
# Unhandled csv columns:
#   - typicalAgeRangeFrom
#   - typicalAgeRangeTo
#     TODO: Replace with educationalContext


class YoutubeSpider(Spider):
    """
    Parse a CSV file with Youtube channels and playlists and crawl them.

    The CSV file was manually exported from
    https://docs.google.com/spreadsheets/d/1VsGyb4mrbzq45qIGVt-j6_ut4_VGJPRA39oBhi5SxGk to
    `csv/youtube.csv`.
    """

    name = "youtube_spider"
    friendlyName = "Youtube"
    url = "https://www.youtube.com/"
    version = "0.2.0"

    @staticmethod
    def get_video_url(item: dict) -> str:
        assert item["kind"] == "youtube#video"
        return "https://www.youtube.com/watch?v={}".format(item["id"])

    @staticmethod
    def update_url_query(url: str, params: dict) -> str:
        """Take a url and update selected query parameters."""
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    @staticmethod
    def get_csv_rows(filename: str) -> Generator[dict, None, None]:
        csv_file_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "..", "csv", filename)
        )
        with open(csv_file_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                yield row

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lomLoader = YoutubeLomLoader(self.name, self.version, **kwargs)

    @overrides  # Spider
    def start_requests(self):
        if env.get("YOUTUBE_API_KEY", False) == "":
            logging.error("YOUTUBE_API_KEY is required for youtube_spider")
            return
        for row in YoutubeSpider.get_csv_rows("youtube.csv"):
            request = self.request_row(row)
            if request is not None:
                yield request

    def request_row(self, row: dict) -> Request:
        if row["url"].startswith("https://www.youtube.com"):
            url = urlparse(row["url"])
            if url.path == "/playlist":
                playlist_id = dict(parse_qsl(url.query))["list"]
                return self.request_playlist(playlist_id, meta={"row": row})
            elif url.path.startswith("/channel/"):
                channel_id = url.path.split("/")[2]
                return self.request_channel(channel_id, meta={"row": row})
            else:
                # Youtube offers custom URLs to popular channels of the form
                #   - https://www.youtube.com/c/<custom channel name>
                #   - https://www.youtube.com/<custom channel name>
                #   - https://www.youtube.com/user/<legacy user name>
                #   - https://www.youtube.com/<legacy user name>
                #
                # All of these lead to an ordinary channel, but we need to read its ID from the page
                # body.
                return Request(
                    row["url"], meta={"row": row}, callback=self.parse_custom_url,
                )

    def request_channel(self, channel_id: str, meta: dict) -> Request:
        part = ["snippet", "contentDetails", "statistics"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/channels"
            + "?part={}&id={}&key={}".format(
                "%2C".join(part), channel_id, env.get("YOUTUBE_API_KEY", False)
            )
        )
        return Request(url=request_url, meta=meta, callback=self.parse_channel)

    def parse_channel(self, response: Response) -> Request:
        body = json.loads(response.body)
        assert body["kind"] == "youtube#channelListResponse"
        assert "items" in body
        assert len(body["items"]) == 1
        playlist_id = body["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        response.meta["channel"] = body["items"][0]
        return self.request_playlist(playlist_id, response.meta)

    def request_playlist(self, playlist_id: str, meta: dict) -> Request:
        part = ["snippet"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/playlists"
            + "?part={}&id={}&key={}".format(
                "%2C".join(part), playlist_id, env.get("YOUTUBE_API_KEY"),
            )
        )
        return Request(request_url, meta=meta, callback=self.parse_playlist)

    def parse_playlist(self, response: Response):
        body = json.loads(response.body)
        assert body["kind"] == "youtube#playlistListResponse"
        assert body["pageInfo"]["totalResults"] == 1
        response.meta["playlist"] = body["items"][0]
        return self.request_playlist_items(body["items"][0]["id"], response.meta)

    def request_playlist_items(self, playlist_id: str, meta: dict) -> Request:
        part = ["snippet"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/playlistItems"
            + "?part={}&playlistId={}&key={}".format(
                "%2C".join(part), playlist_id, env.get("YOUTUBE_API_KEY"),
            )
        )
        return Request(request_url, meta=meta, callback=self.parse_playlist_items)

    def parse_playlist_items(self, response: Response):
        body = json.loads(response.body)
        assert body["kind"] == "youtube#playlistItemListResponse"
        ids = [item["snippet"]["resourceId"]["videoId"] for item in body["items"]]
        yield self.request_videos(ids, response.meta)
        if "nextPageToken" in body:
            request_url = YoutubeSpider.update_url_query(
                response.url, {"pageToken": body["nextPageToken"]}
            )
            yield response.follow(
                request_url, meta=response.meta, callback=self.parse_playlist_items
            )

    def request_videos(self, ids: List[str], meta: dict):
        part = ["snippet", "status", "contentDetails"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/videos"
            + "?part={}&id={}&key={}".format(
                "%2C".join(part), "%2C".join(ids), env.get("YOUTUBE_API_KEY"),
            )
        )
        return Request(request_url, meta=meta, callback=self.parse_videos)

    def parse_videos(self, response: Response):
        body = json.loads(response.body)
        assert body["kind"] == "youtube#videoListResponse"
        for item in body["items"]:
            response_copy = response.replace(url=self.get_video_url(item))
            response_copy.meta["item"] = item
            yield self.lomLoader.parse(response_copy)

    def parse_custom_url(self, response: Response) -> Request:
        match = re.search('<meta itemprop="channelId" content="(.+?)">', response.text)
        if match is not None:
            channel_id = match.group(1)
            return self.request_channel(channel_id, meta=response.meta)
        else:
            logging.warn("Could not extract channel id for {}".format(response.url))


class YoutubeLomLoader(LomBase):
    # The `response.meta` field is populated as follows:
    #   - `row`: The row of the CSV file containing the channel or playlist to be scraped with some
    #     additional information regarding all found videos.
    #   - `item`: Information about the video, obtained from the Youtube API.
    #   - `channel`: Information about the Youtube channel, obtained from the Youtuber API. Only
    #     populated if an entire channel was given in the CSV row.
    #   - `playlist`: Information about the Youtube playlist, obtained from the Youtuber API. These
    #     information are more relevant than the channel information when a specific playlist was
    #     given in the CSV row. However, when an entire channel was requested, we fall back to the
    #     `uploads` playlist, which provides only a generated title.

    @staticmethod
    def parse_csv_field(field: str) -> List[str]:
        """Parse semicolon-separated string."""
        values = [value.strip() for value in field.split(";") if value.strip()]
        if len(values):
            return values

    def __init__(self, name, version, **kwargs):
        self.name = name
        self.version = version
        super().__init__(**kwargs)

    @overrides  # LomBase
    def getId(self, response: Response) -> str:
        return YoutubeSpider.get_video_url(response.meta["item"])

    @overrides  # LomBase
    def getHash(self, response: Response) -> str:
        return self.version + response.meta["item"]["snippet"]["publishedAt"]

    @overrides  # LomBase
    def mapResponse(self, response) -> items.ResponseItemLoader:
        return LomBase.mapResponse(self, response, False)

    @overrides  # LomBase
    def getBase(self, response: Response) -> items.BaseItemLoader:
        base = LomBase.getBase(self, response)
        base.add_value("origin", response.meta["row"]["sourceTitle"].strip())
        base.add_value("lastModified", response.meta["item"]["snippet"]["publishedAt"])
        base.add_value("thumbnail", self.getThumbnailUrl(response))
        base.add_value("fulltext", self.getFulltext(response))
        return base

    def getThumbnailUrl(self, response: Response) -> str:
        thumbnails = response.meta["item"]["snippet"]["thumbnails"]
        thumbnail = (
            thumbnails["maxres"]
            if "maxres" in thumbnails
            else thumbnails["standard"]
            if "standard" in thumbnails
            else thumbnails["high"]
        )
        return thumbnail["url"]

    def getFulltext(self, response: Response) -> str:
        item = response.meta["item"]["snippet"]
        # If `channel` is populated, it has more relevant information than `playlist` (see comments
        # to `meta` field above).
        if "channel" in response.meta:
            channel = response.meta["channel"]["snippet"]
            fulltext = "\n\n".join(
                [channel["title"], channel["description"], item["title"]],
            )
        else:
            playlist = response.meta["playlist"]["snippet"]
            fulltext = "\n\n".join(
                [playlist["channelTitle"], playlist["title"], playlist["description"],],
            )
        return fulltext

    @overrides  # LomBase
    def getLOMGeneral(self, response: Response) -> items.LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"]["snippet"]["title"])
        general.add_value("description", self.getDescription(response))
        general.add_value(
            "keyword", self.parse_csv_field(response.meta["row"]["keyword"])
        )
        if "tags" in response.meta["item"]["snippet"]:
            general.add_value("keyword", response.meta["item"]["snippet"]["tags"])
        general.add_value(
            "language", self.parse_csv_field(response.meta["row"]["language"])
        )
        return general

    def getDescription(self, response: Response) -> str:
        return (
            response.meta["item"]["snippet"]["description"]
            # Fall back to playlist title when no description was given.
            or response.meta["playlist"]["snippet"]["title"]
        )

    @overrides  # LomBase
    def getLOMTechnical(self, response: Response) -> items.LomTechnicalItemLoader:
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value(
            "location", YoutubeSpider.get_video_url(response.meta["item"])
        )
        technical.add_value(
            "duration", response.meta["item"]["contentDetails"]["duration"]
        )
        return technical

    @overrides  # LomBase
    def getLOMLifecycle(self, response: Response) -> items.LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        lifecycle.add_value("role", "author")
        lifecycle.add_value(
            "organization", response.meta["item"]["snippet"]["channelTitle"]
        )
        lifecycle.add_value("url", self.getChannelUrl(response))
        return lifecycle

    def getChannelUrl(self, response: Response) -> str:
        channel_id = response.meta["item"]["snippet"]["channelId"]
        return "https://www.youtube.com/channel/{}".format(channel_id)

    @overrides  # LomBase
    def getLicense(self, response: Response) -> items.LicenseItemLoader:
        license = LomBase.getLicense(self, response)
        license.add_value("internal", response.meta["item"]["status"]["license"])
        # possible values: "youtube", "creativeCommon"
        if response.meta["item"]["status"]["license"] == "creativeCommon":
            license.add_value(
                "url", Constants.LICENSE_CC_BY_30
            )
        elif response.meta["item"]["status"]["license"] == "youtube":
            license.replace_value("internal", Constants.LICENSE_CUSTOM)
            license.add_value("description", "Youtube-Standardlizenz")
        return license

    @overrides  # LomBase
    def getValuespaces(self, response: Response) -> items.ValuespaceItemLoader:
        valuespaces = LomBase.getValuespaces(self, response)
        row = response.meta["row"]
        valuespaces.add_value(
            "learningResourceType", self.parse_csv_field(row["learningResourceType"]),
        )
        valuespaces.add_value("discipline", self.parse_csv_field(row["discipline"]))
        valuespaces.add_value(
            "intendedEndUserRole", self.parse_csv_field(row["intendedEndUserRole"]),
        )
        return valuespaces

