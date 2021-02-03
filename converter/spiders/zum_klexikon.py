from converter.spiders.zum_spider import ZUMSpider


class ZUMKlexikon(ZUMSpider):
    name = "zum_klexikon"
    friendlyName = "ZUM-Klexikon"
    url = "https://klexikon.zum.de/"
    version = "0.1.0"
    apiUrl = "https://klexikon.zum.de/api.php?action=query&format=json&list=allpages&apcontinue=%continue&aplimit=100"
    apiEntryUrl = (
        "https://klexikon.zum.de/api.php?action=parse&format=json&pageid=%pageid"
    )
    entryUrl = "https://klexikon.zum.de/wiki/%page"
    keywords = {}
