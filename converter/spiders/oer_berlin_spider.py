from converter.pipelines import LisumPipeline

from .base_classes import EduSharingBase


def _invert_mapping(forward_mapping: dict) -> dict[str, list[str]]:
    """
    Inverts one of the ``LisumPipeline`` forward mapping tables (OEH value -> Lisum value) into a
    reverse table (Lisum value -> list of OEH values).

    The forward tables use three value shapes, all of which are handled here:
    - scalar strings (e.g. ``"380": "C-MA"``)
    - lists of strings (e.g. ``"audiovisual_medium": ["audio", "video"]``)
    - empty strings (e.g. ``"open_activity": ""``), which carry no Lisum value and are skipped

    Since multiple OEH keys can map to the same Lisum value, every Lisum value inverts to the full
    list of OEH values that produced it ("map to all sources").
    """
    reverse_mapping: dict[str, list[str]] = {}
    for oeh_value, lisum_value in forward_mapping.items():
        lisum_values = lisum_value if isinstance(lisum_value, list) else [lisum_value]
        for single_lisum_value in lisum_values:
            if not single_lisum_value:
                # empty strings (e.g. "open_activity": "") don't correspond to a Lisum value
                continue
            reverse_mapping.setdefault(single_lisum_value, [])
            if oeh_value not in reverse_mapping[single_lisum_value]:
                reverse_mapping[single_lisum_value].append(oeh_value)
    return reverse_mapping


# reversed LisumPipeline mapping tables: Lisum value -> list of OEH values
LISUM_TO_OEH_DISCIPLINE = _invert_mapping(LisumPipeline.DISCIPLINE_TO_LISUM_SHORTHAND)
LISUM_TO_OEH_EDU_CONTEXT = _invert_mapping(LisumPipeline.EDUCATIONALCONTEXT_TO_LISUM)
LISUM_TO_OEH_LRT = _invert_mapping(LisumPipeline.LRT_OEH_TO_LISUM)


class OerBerlinSpider(EduSharingBase):
    """
    Imports content out of the LISUM / OER Berlin edu-sharing repository back into OEH.

    The repository stores Lisum-specific valuespace values (e.g. discipline "C-MA",
    educationalContext "primary school"). This spider reverses the ``LisumPipeline`` mapping tables
    so those values are translated back into OEH vocab keys, which the ``ProcessValuespacePipeline``
    then resolves against the OEH vocabularies.

    The ``importSearchId`` (saved-search uuid) is supplied at runtime via the
    ``EDU_SHARING_IMPORT_SEARCH_ID`` env var (handled by ``EduSharingBase``). Multiple comma-separated
    uuids are crawled one after another (OR-linked).
    """

    name = "oer_berlin_spider"
    friendlyName = "OER Berlin"
    url = "https://repository.oer-berlin.de/edu-sharing/"
    apiUrl = "https://repository.oer-berlin.de/edu-sharing/rest/"
    # saved-search uuid(s, comma-separated) to import from; can be overridden via EDU_SHARING_IMPORT_SEARCH_ID
    importSearchId = "c478568d-0945-4ef6-b856-8d0945eef679"
    mdsId = "-default-"
    version = "0.0.4"
    custom_settings = {
        "ROBOTSTXT_OBEY": False
    }

    @staticmethod
    def _reverse_map(valuespaces, field: str, raw_values, reverse_mapping: dict[str, list[str]]):
        """
        Replaces ``valuespaces[field]`` with the OEH values that correspond to the repository's raw
        Oer berlin values. Unknown values are passed through verbatim.
        """
        if not raw_values:
            return
        mapped_values: list[str] = []
        for raw_value in raw_values:
            if raw_value in reverse_mapping:
                for oeh_value in reverse_mapping[raw_value]:
                    if oeh_value not in mapped_values:
                        mapped_values.append(oeh_value)
            elif raw_value not in mapped_values:
                mapped_values.append(raw_value)
        valuespaces.replace_value(field, mapped_values)

    def getBase(self, response):
        base = EduSharingBase.getBase(self, response)
        # map the repository's educational description into the editorial notes ("ccm:notes")
        base.add_value("notes", self.getProperty("cclom:educational_description", response))
        return base

    def getLOMTechnical(self, response):
        technical = EduSharingBase.getLOMTechnical(self, response)
        # use the mimetype reported by the repository API instead of the hardcoded "text/html"
        cclom_format = self.getProperty("cclom:format", response)
        if cclom_format:
            technical.replace_value("format", cclom_format)
        return technical

    def getValuespaces(self, response):
        valuespaces = EduSharingBase.getValuespaces(self, response)
        self._reverse_map(
            valuespaces, "discipline",
            self.getProperty("ccm:taxonid", response), LISUM_TO_OEH_DISCIPLINE
        )
        self._reverse_map(
            valuespaces, "educationalContext",
            self.getProperty("ccm:educationalcontext", response), LISUM_TO_OEH_EDU_CONTEXT
        )
        self._reverse_map(
            valuespaces, "learningResourceType",
            self.getProperty("ccm:educationallearningresourcetype", response), LISUM_TO_OEH_LRT
        )
        return valuespaces
