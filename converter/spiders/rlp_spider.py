from .base_classes import OAIBase


class RLPSpider(OAIBase):
    name = "rlp_spider"
    friendlyName = "Schulcampus RLP"
    # sitemap_urls = ['https://cloud.schulcampus-rlp.de/edu-sharing/eduservlet/sitemap']
    url = "https://cloud.schulcampus-rlp.de"
    baseUrl = "https://cloud.schulcampus-rlp.de/edu-sharing/eduservlet/oai/provider"
    set = "default"
    metadataPrefix = "lom"
    version = "0.1.0"

    def __init__(self, **kwargs):
        OAIBase.__init__(self, **kwargs)

    def shouldImport(self, response):
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")
        rightsDescriptions = record.xpath(
            "metadata/lom/rights/description/string//text()"
        ).get()
        if not rightsDescriptions:
            return False
        return (
            rightsDescriptions.startswith("https://creativecommons.org/licenses/pdm")
            or rightsDescriptions.startswith(
                "https://creativecommons.org/publicdomain/zero"
            )
            or rightsDescriptions.startswith("https://creativecommons.org/licenses/by")
            or rightsDescriptions.startswith(
                "https://creativecommons.org/licenses/by-sa"
            )
        )
