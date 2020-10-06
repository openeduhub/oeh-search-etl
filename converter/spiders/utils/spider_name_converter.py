import logging

spider_to_friendly_name = None


def load_friendly_spider_names():
    """
    Returns a dictionary which maps the Spider's name to its "friendly" name.

    e.g., merlin_spider --> Merlin, br_rss_spider --> Bayerischer Rundfunk

    Based on https://stackoverflow.com/questions/46871133/get-all-spiders-class-name-in-scrapy

    Author: Ioannis Koumarelas, ioannis.koumarelas@hpi.de, Schul-Cloud, Content team.
    """
    from scrapy.utils import project
    from scrapy import spiderloader

    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    spider_names = spider_loader.list()
    spider_classes = [spider_loader.load(name) for name in spider_names]

    spider_name_to_friendly_name = {}
    for spider in spider_classes:
        spider_name_to_friendly_name[spider.name] = spider.friendlyName

    return spider_name_to_friendly_name


def get_spider_friendly_name(spider_name):
    """
    Given the spider's name, returns its friendly name.
    """

    global spider_to_friendly_name
    if spider_to_friendly_name is None:
        spider_to_friendly_name = load_friendly_spider_names()

    if spider_name in spider_to_friendly_name:
        return spider_to_friendly_name[spider_name]
    else:
        if spider_name is not None:
            logging.info("Friendly name for spider " + spider_name + " has not been found.")
        return spider_name


if __name__ == '__main__':
    load_friendly_spider_names()