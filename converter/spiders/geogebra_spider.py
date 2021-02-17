import json
import logging
import jmespath

import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from .base_classes import LomBase, JSONBase

log = logging.getLogger(__name__)

jmes_id = jmespath.compile('id')
jmes_language = jmespath.compile('language')
jmes_mod_date = jmespath.compile('date_modified')
jmes_thumb_url = jmespath.compile('thumbUrl')
jmes_title = jmespath.compile('title')
jmes_keywords = jmespath.compile('keywords')
jmes_description = jmespath.compile('description')
jmes_topic = jmespath.compile('topic')
jmes_type = jmespath.compile('type')
jmes_categories = jmespath.compile('categories')
jmes_file_format = jmespath.compile('fileFormat')
jmes_content_size = jmespath.compile('ContentSize')
learningResourceTypeMap = {
    'game': 'educational_game',
    'practice': 'drill_and_practice',
}


class GeoGebraSpider(CrawlSpider, LomBase, JSONBase):
    """
    The spider that will crawl geogebra.org

    .. todo::

       Further improvements on geogebra might be:

       * adding `creator.displayname` information as author name, falling back on username.
       * using `deleted` to ignore the resource if set to True
       * using `type` == 'book' to include the chapters
    """

    name = "geogebra_spider"
    friendlyName = "GeoGebra"
    url = "https://www.geogebra.org"
    version = "0.1"
    start_urls = [
        "https://www.geogebra.org/m-sitemap-1.xml",
        "https://www.geogebra.org/m-sitemap-2.xml",
        "https://www.geogebra.org/m-sitemap-3.xml",
        "https://www.geogebra.org/m-sitemap-4.xml",
        "https://www.geogebra.org/m-sitemap-5.xml",
        "https://www.geogebra.org/m-sitemap-6.xml",
        "https://www.geogebra.org/m-sitemap-7.xml",
        "https://www.geogebra.org/m-sitemap-8.xml",
        "https://www.geogebra.org/m-sitemap-9.xml",
        "https://www.geogebra.org/m-sitemap-10.xml",
        "https://www.geogebra.org/m-sitemap-11.xml",
    ]

    apiUrl = "https://api.geogebra.org/v1.0/materials/%id?scope=extended&embed=creator,tags,topics"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def parse(self, response, **kwargs):
        """
        parse the sitemaps and generate requests to the api

        sitemaps look like this::

           <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
               <url>
                   <loc>https://www.geogebra.org/m/eyEPBSCr</loc>
               </url>
               <url>...</url>

        :param response:
        :param kwargs:
        :return:
        """
        for url in response.xpath('//*[name()="url"]/*[name()="loc"]//text()').getall():
            # url example: https://www.geogebra.org/m/eyEPBSCr
            split = url.split("/")
            _id = split[-1]  # example: eyEPBSCr
            api_url = f'https://api.geogebra.org/v1.0/materials/{_id}?scope=extended&embed=creator,tags,topics'
            yield scrapy.Request(url=api_url, callback=self.parse_entry, meta={"url": url})

    def parse_entry(self, response: scrapy.http.Response):
        """
        parse a json response from the materials api
        """
        response.meta['item'] = json.loads(response.body)
        language = jmes_language.search(response.meta['item'])
        if 'de' == language:
            return LomBase.parse(self, response)
        log.info(f'Skpping entry with language {language}')
        return None

    def getId(self, response=None):
        return jmes_id.search(response.meta['item'])

    def getHash(self, response=None):
        return self.version + jmes_mod_date.search(response.meta['item'])

    def getBase(self, response=None):
        """
        thumbnails are delivered from the api like:
        https://www.geogebra.org/resource/pug8qwmb/aSZtgWaSBFA8AOIL/material-pug8qwmb-thumb$1.png

        `$1` is a placeholder that can be replaced with '' to get a smaller thumbnail, `@l` to get a larger

        other possible values might be `@xs` `@xl`

        https://www.geogebra.org/resource/pug8qwmb/aSZtgWaSBFA8AOIL/material-pug8qwmb-thumb.png
        """
        base = super().getBase(response)
        # 'thumbUrl': 'https://www.geogebra.org/resource/eyEPBSCr/X8yK3pCN8pvUYZUZ/material-eyEPBSCr-thumb$1.png',
        thumb = jmes_thumb_url.search(response.meta['item']).replace('$1', '@l')
        base.add_value('thumbnail', thumb)
        base.add_value('lastModified', jmes_mod_date.search(response.meta['item']))
        return base

    def getLOMGeneral(self, response=None):
        general = super().getLOMGeneral(response)
        data = response.meta['item']
        general.add_value('identifier', jmes_id.search(data))
        general.add_value('title', jmes_title.search(data))
        general.add_value('keyword', jmes_keywords.search(data))
        general.add_value('language', jmes_language.search(data))
        general.add_value('description', jmes_description.search(data))
        return general

    def getValuespaces(self, response):
        valuespaces = super().getValuespaces(response)
        data = response.meta['item']
        valuespaces.add_value("discipline", jmes_topic.search(data))
        resource_type = jmes_type.search(data)
        if resource_type == 'ws':
            valuespaces.add_value('learningResourceType', 'worksheet')
        elif resource_type == 'book':
            valuespaces.add_value('learningResourceType', 'text')
        else:
            log.warning(f'unknown learningResourceType {resource_type}')
        for category in jmes_categories.search(data):
            if category not in learningResourceTypeMap:
                log.warning(f'unmapped learningResourceType: {category}')
                continue
            valuespaces.add_value('learningResourceType', learningResourceTypeMap[category])
        return valuespaces

    def getLOMEducational(self, response=None):
        educational = super().getLOMEducational(response)
        # educational.add_value('typicalLearningTime', data['timeRequired'])
        return educational

    def getLicense(self, response=None):
        license = super().getLicense(response)
        license.add_value("url", Constants.LICENSE_CC_BY_SA_30)
        return license

    def getLOMTechnical(self, response=None):
        technical = super().getLOMTechnical(response)
        data = response.meta['item']
        technical.add_value("format", jmes_file_format.search(data))
        technical.add_value("size", jmes_file_format.search(data))
        technical.add_value("location", response.meta["url"])
        return technical


example_data = """
{'type': 'ws',
 'date_created': 1385982105,
 'date_modified': 1536578023,
 'date_published': None,
 'visibility': 'O',
 'deleted': False,
 'thumbUrl': 'https://www.geogebra.org/resource/eyEPBSCr/X8yK3pCN8pvUYZUZ/material-eyEPBSCr-thumb$1.png',
 'qualityVerified': True,
 'language': 'en-GB',
 'description': 'This applet demonstrates how the [url=http://en.wikipedia.org/wiki/Method_of_exhaustion]method of exhaustion[/url] to calculate integrals can be implemented in GeoGebra.',
 'displayReason': None,
 'supportsLesson': True,
 'id': 'eyEPBSCr',
 'title': 'Method of Exhaustion',
 'creator': {'username': 'florian sonner',
  'profilemessage': '',
  'avatar': 'https://www.geogebra.org/user/1/tnne8CaF5lgRSofb/avatar@xs.png',
  'avatarXL': 'https://www.geogebra.org/user/1/tnne8CaF5lgRSofb/avatar@xl.png',
  'banner': False,
  'qualityVerified': True,
  'permissionGroup': None,
  'id': 1,
  'displayname': 'Florian Sonner',
  'profile': '/u/florian+sonner',
  'banned': False},
 'categories': [],
 'tags': ['calculus', 'exhaustion', 'integral', 'integral-calculus'],
 'topics': ['calculus', 'integral-calculus'],
 'elements': [{'id': 182873,
   'order': 0,
   'type': 'G',
   'title': '',
   'url': 'https://www.geogebra.org/resource/eyEPBSCr/X8yK3pCN8pvUYZUZ/material-eyEPBSCr.ggb',
   'thumbUrl': 'https://www.geogebra.org/resource/eyEPBSCr/X8yK3pCN8pvUYZUZ/material-eyEPBSCr-thumb$1.png',
   'previewUrl': 'https://www.geogebra.org/resource/eyEPBSCr/X8yK3pCN8pvUYZUZ/material-eyEPBSCr.png',
   'settings': {'enableUndoRedo': True,
    'showResetIcon': True,
    'enableShiftDragZoom': True,
    'enableRightClick': False,
    'enableLabelDrags': False,
    'showMenuBar': False,
    'showToolBar': False,
    'showAlgebraInput': False,
    'allowStyleBar': False,
    'showZoomButtons': False,
    'showToolBarHelp': False,
    'preferredAppletType': 'auto',
    'width': 800,
    'height': 600,
    'scale': 1,
    'fixApplet': False},
   'views': {'is3D': False,
    'AV': True,
    'SV': False,
    'CV': False,
    'EV2': False,
    'CP': False,
    'PC': False,
    'DA': False,
    'FI': False,
    'PV': False,
    'macro': False}}]}
"""
