from converter.spiders.oai_base import OAIBase

class OAISodis(OAIBase):
    verb="listIdentifiers"
    baseUrl = "https://sodis.de/cp/oai_pmh/oai.php"
    metadataPrefix = "oai_lom-de"
    set = "oer_mebis_activated"

    name="oai_sodis_spider"
    friendlyName='OAI Sodis'
    url = baseUrl
    version = '0.1'
