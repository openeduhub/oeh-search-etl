import logging
import dateutil.parser
from scrapy.exceptions import DropItem

from converter.constants import Constants, OerType
from converter.pipelines.bases import BasicPipeline
log = logging.getLogger(__name__)


class LOMFillupPipeline(BasicPipeline):
    """
    fillup missing props by "guessing" or loading them if possible
    """
    def process_item(self, item, spider):
        if "fulltext" not in item and "text" in item["response"]:
            item["fulltext"] = item["response"]["text"]
        return item


class FilterSparsePipeline(BasicPipeline):
    def process_item(self, item, spider):
        try:
            if "location" not in item["lom"]["technical"]:
                raise DropItem(
                    "Entry "
                    + item["lom"]["general"]["title"]
                    + " has no technical location"
                )
        except KeyError:
            raise DropItem(f'Item {item} has no lom.technical.location')
        # pass through explicit uuid elements
        if "uuid" in item:
            return item
        try:
            # if it contains keywords, it's valid
            if _ := item["lom"]["general"]["keyword"]:
                return item
        except KeyError:
            pass
        try:
            # if it has a description, it's valid
            if _ := item["lom"]["general"]["description"]:
                return item
        except KeyError:
            pass
        try:
            # if it the valuespaces.learningResourceType is set, it is valid
            if _ := item["valuespaces"]["learningResourceType"]:
                return item
        except KeyError:
            pass
        # if none of the above matches drop the item

        try:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has neither keywords nor description"
            )
        except KeyError:
            raise DropItem(f'Item {item} was dropped for not providing enough metadata')


class NormLicensePipeline(BasicPipeline):
    def process_item(self, item, spider):
        if "url" in item["license"] and not item["license"]["url"] in Constants.VALID_LICENSE_URLS:
            for key in Constants.LICENSE_MAPPINGS:
                if item["license"]["url"].startswith(key):
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS[key]
                    break
        if "internal" in item["license"] and (
                "url" not in item["license"]
                or item["license"]["url"] not in Constants.VALID_LICENSE_URLS
        ):
            for key in Constants.LICENSE_MAPPINGS_INTERNAL:
                if item["license"]["internal"].casefold() == key.casefold():
                    # use the first entry
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS_INTERNAL[key][0]
                    break

        if "url" in item["license"] and "oer" not in item["license"]:
            if (
                    item["license"]["url"] == Constants.LICENSE_CC_BY_40
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_30
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_30
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_40
                    or item["license"]["url"] == Constants.LICENSE_CC_ZERO_10
            ):
                item["license"]["oer"] = OerType.ALL

        if "internal" in item["license"] and "oer" not in item["license"]:
            internal = item["license"]["internal"].lower()
            if "cc-by-sa" in internal or "cc-0" in internal or "pdm" in internal:
                item["license"]["oer"] = OerType.ALL
        return item


class ConvertTimePipeline(BasicPipeline):
    """
    convert typicalLearningTime into a integer representing seconds
    """
    def process_item(self, item, spider):
        # map lastModified
        if "lastModified" in item:
            try:
                item["lastModified"] = float(item["lastModified"])
            except:
                try:
                    date = dateutil.parser.parse(item["lastModified"])
                    item["lastModified"] = int(date.timestamp())
                except:
                    log.warning(
                        "Unable to parse given lastModified date "
                        + item["lastModified"]
                    )
                    del item["lastModified"]

        if "typicalLearningTime" in item["lom"]["educational"]:
            t = item["lom"]["educational"]["typicalLearningTime"]
            mapped = None
            splitted = t.split(":")
            if len(splitted) == 3:
                mapped = (
                        int(splitted[0]) * 60 * 60
                        + int(splitted[1]) * 60
                        + int(splitted[2])
                )
            if mapped is None:
                log.warning(
                    "Unable to map given typicalLearningTime "
                    + t
                    + " to numeric value"
                )
            item["lom"]["educational"]["typicalLearningTime"] = mapped
        return item
