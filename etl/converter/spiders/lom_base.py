from converter.items import *
from pprint import pprint
import logging

class LomBase:
  friendlyName = 'LOM Based spider'
  ranking = 1
  def parse(self, response):
    main = self.getBase(response)
    main.add_value('lom', self.getLOM(response).load_item())
    logging.info(main.load_item())
    main.add_value('response', self.mapResponse(response).load_item())
    return main.load_item()

  def mapResponse(self, response):
    r = ResponseItemLoader()
    r.add_value('status',response.status)
    r.add_value('body',response.body.decode('utf-8'))
    r.add_value('headers',response.headers)
    r.add_value('url',response.url)
    return r

  def getLOM(self, response):
    lom = LomBaseItemloader()
    lom.add_value('general', self.getLOMGeneral(response).load_item())
    lom.add_value('lifecycle', self.getLOMLifecycle(response).load_item())
    lom.add_value('technical', self.getLOMTechnical(response).load_item())
    lom.add_value('educational', self.getLOMEducational(response).load_item())
    lom.add_value('rights', self.getLOMRights(response).load_item())
    lom.add_value('classification', self.getLOMClassification(response).load_item())
    return lom

  def getLOMGeneral(self, response = None):
    return LomGeneralItemloader()

  def getLOMLifecycle(self, response = None):
    return LomLifecycleItemloader()

  def getLOMTechnical(self, response = None):
    return LomTechnicalItemLoader()

  def getLOMEducational(self, response = None):
    return LomEducationalItemLoader()

  def getLOMRights(self, response = None):
    return LomRightsItemLoader()

  def getLOMClassification(self, response = None):
    return LomClassificationItemLoader()
