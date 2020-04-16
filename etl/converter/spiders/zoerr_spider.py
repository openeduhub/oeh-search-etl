from converter.spiders.lrmi_base import LrmiBase
from converter.spiders.oai_base import OAIBase

class ZoerrSpider(LrmiBase):
  name = 'zoerr_spider'
  friendlyName = 'OER-Repositorium Baden-Württemberg (ZOERR)'
  url = 'https://www.oerbw.de'
  baseUrl = 'https://www.oerbw.de/edu-sharing/eduservlet/oai/provider'
  set = 'default'
  metadataPrefix = 'lom'

  # only for LRMI
  sitemap_urls = ['https://www.oerbw.de/edu-sharing/eduservlet/sitemap']