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
from converter.spiders.lom_base import LomBase

# Unhandled csv columns:
#   - sourceTitle
#     TODO: Find suitable target field
#
#   - typicalAgeRangeFrom
#   - typicalAgeRangeTo
#     TODO: Replace with educationalContext
#
# TODO: Find suitable target field for channel/playlist URL
#
# We could also consider adding information about the channel to videos.
#
# Example item:
# ```
# {
#   "kind": "youtube#playlistItem",
#   "etag": "q9_JO0nhU1k7HI7HuTUMsNOd6KM",
#   "id": "UExuX1JYWEUxZk1tUGRHbkVvYW00aGI0VDlJdjhNM2Joei4yODlGNEE0NkRGMEEzMEQy",
#   "snippet": {
#     "publishedAt": "2015-06-29T20:16:59Z",
#     "channelId": "UC_cCcxd8yUwIu1-rt5dpBdw",
#     "title": "BIOLOGIE NACHHILFE - Evolution & Entwicklung - die neue Serie | Evolution 1",
#     "description": "ALLE THEMEN AUS DIESEM VID[...]",
#     "thumbnails": {
#         [...]
#     },
#     "channelTitle": "Die Merkhilfe",
#     "playlistId": "PLn_RXXE1fMmPdGnEoam4hb4T9Iv8M3bhz",
#     "position": 0,
#     "resourceId": {
#       "kind": "youtube#video",
#       "videoId": "BF4st6XBViI"
#     }
#   },
#   "contentDetails": {
#     "videoId": "BF4st6XBViI",
#     "videoPublishedAt": "2015-07-05T13:00:01Z"
#   },
#   "status": {
#     "privacyStatus": "public"
#   }
# }
# ```


class YoutubeSpider(Spider, LomBase):
    name = "youtube_spider"
    friendlyName = "Youtube"
    url = "https://www.youtube.com/"
    version = "0.1.0"

    @overrides  # Spider
    def start_requests(self):
        for row in get_csv_rows("youtube.csv"):
            if (request := self._request_row(row)) is not None:
                yield request

    @overrides  # LomBase
    def getId(self, response: Response) -> str:
        return self._get_video_url(response.meta["item"])

    @overrides  # LomBase
    def getHash(self, response: Response) -> str:
        return self.version + response.meta["item"]["snippet"]["publishedAt"]

    @overrides  # LomBase
    def getBase(self, response: Response) -> items.BaseItemLoader:
        base = LomBase.getBase(self, response)
        thumbnails = response.meta["item"]["snippet"]["thumbnails"]
        thumbnail = (
            thumbnails["maxres"]
            if "maxres" in thumbnails
            else thumbnails["standard"]
            if "standard" in thumbnails
            else thumbnails["high"]
        )
        base.add_value("thumbnail", thumbnail["url"])
        return base

    @overrides  # LomBase
    def getLOMGeneral(self, response: Response) -> items.LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"]["snippet"]["title"])
        general.add_value(
            "description", response.meta["item"]["snippet"]["description"]
        )
        general.add_value("keyword", parse_csv_field(response.meta["row"]["keyword"]))
        general.add_value("language", parse_csv_field(response.meta["row"]["language"]))
        return general

    @overrides  # LomBase
    def getLOMTechnical(self, response: Response) -> items.LomTechnicalItemLoader:
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value("location", self._get_video_url(response.meta["item"]))
        return technical

    @overrides  # LomBase
    def getLicense(self, response: Response) -> items.LicenseItemLoader:
        license = LomBase.getLicense(self, response)
        license.add_value("internal", parse_csv_field(response.meta["row"]["license"]))
        return license

    @overrides  # LomBase
    def getValuespaces(self, response: Response) -> items.ValuespaceItemLoader:
        valuespaces = LomBase.getValuespaces(self, response)
        row = response.meta["row"]
        valuespaces.add_value(
            "learningResourceType", parse_csv_field(row["learningResourceType"])
        )
        valuespaces.add_value("discipline", parse_csv_field(row["discipline"]))
        valuespaces.add_value(
            "intendedEndUserRole", parse_csv_field(row["intendedEndUserRole"])
        )
        return valuespaces

    def _request_row(self, row: dict) -> Request:
        if row["url"].startswith("https://www.youtube.com"):
            url = urlparse(row["url"])
            if url.path == "/playlist":
                playlist_id = dict(parse_qsl(url.query))["list"]
                return self._request_playlist(playlist_id, meta={"row": row})
            elif url.path.startswith("/channel/"):
                channel_id = url.path.split("/")[2]
                return self._request_channel(channel_id, meta={"row": row})
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
                    row["url"], meta={"row": row}, callback=self._parse_custom_url,
                )

    def _request_channel(self, channel_id: str, meta: dict) -> Request:
        part = ["snippet", "contentDetails", "statistics"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/channels"
            + "?part={}&id={}&key={}".format(
                "%2C".join(part), channel_id, env.get("YOUTUBE_API_KEY")
            )
        )
        return Request(url=request_url, meta=meta, callback=self._parse_channel)

    def _parse_channel(self, response: Response) -> Request:
        body = json.loads(response.body)
        assert body["kind"] == "youtube#channelListResponse"
        assert body["pageInfo"]["totalResults"] == 1
        playlist_id = body["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        return self._request_playlist(playlist_id, response.meta)

    def _request_playlist(self, playlist_id: str, meta: dict) -> Request:
        part = ["snippet"]
        request_url = (
            "https://www.googleapis.com/youtube/v3/playlistItems"
            + "?part={}&playlistId={}&key={}".format(
                "%2C".join(part), playlist_id, env.get("YOUTUBE_API_KEY"),
            )
        )
        return Request(request_url, meta=meta, callback=self._parse_playlist_items)

    def _parse_playlist_items(self, response: Response):
        body = json.loads(response.body)
        assert body["kind"] == "youtube#playlistItemListResponse"
        body = json.loads(response.body)
        if "nextPageToken" in body:
            request_url = update_url_query(
                response.url, {"pageToken": body["nextPageToken"]}
            )
            yield response.follow(
                request_url, meta=response.meta, callback=self._parse_playlist_items
            )
        for item in body["items"]:
            response_copy = response.replace(url=self._get_video_url(item))
            response_copy.meta["item"] = item
            yield LomBase.parse(self, response_copy)

    def _parse_custom_url(self, response: Response) -> Request:
        if (
            match := re.search('"externalChannelId":"(.+?)"', response.text)
        ) is not None:
            channel_id = match.group(1)
            return self._request_channel(channel_id, meta=response.meta)
        logging.warn("Could not extract channel id for {}".format(response.url))

    def _get_video_url(self, item: dict) -> str:
        assert item["snippet"]["resourceId"]["kind"] == "youtube#video"
        return "https://www.youtube.com/watch?v={}".format(
            item["snippet"]["resourceId"]["videoId"]
        )


def update_url_query(url: str, params: dict) -> str:
    """Take a url and update selected query parameters."""
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def get_csv_rows(filename: str) -> Generator[dict, None, None]:
    csv_file_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "csv", filename)
    )
    with open(csv_file_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            yield row


def parse_csv_field(field: str) -> List[str]:
    """Parse semicolon-separated string."""
    values = [value.strip() for value in field.split(";") if value.strip()]
    if len(values):
        return values
