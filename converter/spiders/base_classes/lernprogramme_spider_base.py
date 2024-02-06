import csv
import hashlib
from abc import ABCMeta, abstractmethod
from io import StringIO
from typing import List

import converter.items as items
from .lom_base import LomBase
from overrides import overrides
from scrapy.http import Request, Response
from scrapy.http.response.text import TextResponse


class LernprogrammeSpiderBase(metaclass=ABCMeta):
    version = "0.1.0"

    @classmethod
    @property
    @abstractmethod
    def name(cls) -> str:
        return ""

    @property
    @abstractmethod
    def friendlyName(self):
        pass

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    @abstractmethod
    def static_values(self):
        pass

    @property
    @abstractmethod
    def start_urls(self):
        pass

    @property
    @abstractmethod
    def exercises(self):
        pass

    def map_row(self, row: dict) -> dict:
        return row

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loader = LernprogrammeLomLoader(
            self.name, self.version, self.url, self.static_values, **kwargs
        )
        self.exercise_loader = (
            LernprogrammeLomLoader(
                self.name,
                self.version,
                self.url,
                merge(self.static_values, self.exercises["static_value_overrides"]),
                **kwargs
            )
            if self.exercises is not None
            else None
        )

    async def parse(self, response):
        reader = csv.DictReader(
            StringIO(response.text),  # DictReader expects a file handle
            ["title", "description", "keywords", "thumbnail", "url", "width", "height"],
            delimiter=";",
        )
        next(reader)  # Skip header row
        for row in reader:
            row = self.map_row(row)
            response_copy = response.replace(url=row["url"])
            response_copy.meta["row"] = row
            yield await self.loader.parse(response_copy)
            if self.exercise_loader is not None:
                yield self.request_exercise(row)

    def request_exercise(self, row: dict):
        url = self.exercises["get_url"](row)
        row_overrides = self.exercises["get_row_overrides"](row)
        merged_row = {**row, **row_overrides, "url": url}
        return Request(
            url,
            meta={"row": merged_row},
            callback=self.parse_exercise,
        )

    def parse_exercise(self, response: Response):
        # `ItemLoader` will only accept (subclasses of) `TextResponse`, so we forge a
        # `TextResponse` with everything of the actual response except `body`.
        response_copy = TextResponse(
            url=response.url,
            status=response.status,
            headers=response.headers,
            flags=response.flags,
            request=response.request,
        )
        return self.exercise_loader.parse(response_copy)


class LernprogrammeLomLoader(LomBase):
    @staticmethod
    def parse_csv_field(field: str) -> List[str]:
        """Parse comma-separated string."""
        values = [value.strip() for value in field.split(",") if value.strip()]
        if len(values):
            return values

    def __init__(self, name, version, url, static_values, **kwargs):
        self.name = name
        self.version = version
        self.url = url
        self.static_values = static_values
        super().__init__(**kwargs)

    @overrides  # LomBase
    def getId(self, response: Response) -> str:
        return response.meta["row"]["url"]

    @overrides  # LomBase
    def getHash(self, response: Response) -> str:
        hash_string = self.version + str(response.meta["row"].items())
        return hashlib.sha1(hash_string.encode("utf8")).hexdigest()

    @overrides  # LomBase
    def getBase(self, response: Response) -> items.BaseItemLoader:
        base = LomBase.getBase(self, response)
        if response.meta["row"]["thumbnail"] is not None:
            base.add_value("thumbnail", response.meta["row"]["thumbnail"])
        return base

    @overrides  # LomBase
    def getLOMGeneral(self, response: Response) -> items.LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["row"]["title"])
        general.add_value("description", response.meta["row"]["description"])
        general.add_value(
            "keyword", self.parse_csv_field(response.meta["row"]["keywords"])
        )
        general.add_value("language", self.static_values["language"])
        return general

    @overrides  # LomBase
    def getLOMTechnical(self, response: Response) -> items.LomTechnicalItemLoader:
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", self.static_values["format"])
        technical.add_value("location", response.meta["row"]["url"])
        return technical

    @overrides  # LomBase
    def getLOMLifecycle(self, response: Response) -> items.LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        lifecycle.add_value("role", "author")
        lifecycle.add_value("firstName", self.static_values["author"]["first_name"])
        lifecycle.add_value("lastName", self.static_values["author"]["last_name"])
        lifecycle.add_value("url", self.url)
        return lifecycle

    @overrides  # LomBase
    def getLicense(self, response: Response) -> items.LicenseItemLoader:
        license = LomBase.getLicense(self, response)
        license.add_value("url", self.static_values["licence_url"])
        return license

    @overrides  # LomBase
    def getValuespaces(self, response: Response) -> items.ValuespaceItemLoader:
        valuespaces = LomBase.getValuespaces(self, response)
        skos = self.static_values["skos"]
        valuespaces.replace_value("new_lrt", skos["new_lrt"])
        valuespaces.add_value(
            "learningResourceType",
            skos["learningResourceType"],
        )
        valuespaces.add_value("discipline", skos["discipline"])
        valuespaces.add_value("intendedEndUserRole", skos["intendedEndUserRole"])
        valuespaces.add_value("educationalContext", skos["educationalContext"])
        valuespaces.add_value("toolCategory", skos["toolCategory"])
        return valuespaces


def merge(source: dict, overrides: dict) -> dict:
    """
    Deep-merge `overrides` onto `source`.

    Only fields already present in `source` will be overridden.
    """
    result = {}
    for key, value in source.items():
        if isinstance(value, dict):
            result[key] = merge(source[key], overrides[key] if key in overrides else {})
        elif key in overrides:
            result[key] = overrides[key]
        else:
            result[key] = value
    return result