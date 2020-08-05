import logging

from converter.spiders.edu_sharing_base import EduSharingBase

class OEHSpider(EduSharingBase):
  name = 'oeh_spider'
  friendlyName = 'Open Edu Hub'
  url = 'https://redaktion.openeduhub.net/edu-sharing/'
  apiUrl = 'https://redaktion.openeduhub.net/edu-sharing/rest/'
  version = '0.1.0'
  mdsId = 'mds_oeh'

  def __init__(self, **kwargs):
    EduSharingBase.__init__(self, **kwargs)

  def getBase(self, response):
    base = EduSharingBase.getBase(self, response)
    base.replace_value('type', self.getProperty('ccm:objecttype', response))
    return base

  def shouldImport(self, response = None):
    if 'ccm:collection_io_reference' in response.meta['item']['aspects']:
      logging.info('Skipping collection_io_reference with id ' + response.meta['item']['ref']['id'])
      return False
    return True
