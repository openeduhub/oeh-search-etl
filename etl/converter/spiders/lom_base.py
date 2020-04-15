from converter.items import *
from pprint import pprint
import logging
from converter.db_connector import Database
class LomBase:
  friendlyName = 'LOM Based spider'
  ranking = 1


  # override to improve performance and automatically handling id
  def getId(self, response = None):
    return None
  # override to improve performance and automatically handling hash
  def getHash(self, response = None):
    return None

  def hasChanged(self, response = None):
    db = Database().findItem(self.getId(response),self)
    changed = db == None or db[1] != self.getHash(response)
    if not changed:
      logging.info('Item ' + db[0] + ' has not changed')
    return changed

  def parse(self, response):
    if self.getId(response) != None and self.getHash(response) != None:
      db = Database().findItem(self.getId(response),self)
      if not self.hasChanged(response):
        return None
  
    main = self.getBase(response)
    main.add_value('lom', self.getLOM(response).load_item())
    main.add_value('valuespaces', self.getValuespaces(response).load_item())
    logging.debug(main.load_item())
    main.add_value('response', self.mapResponse(response).load_item())
    return main.load_item()

  def mapResponse(self, response):
    r = ResponseItemLoader()
    r.add_value('status',response.status)
    r.add_value('body',response.body.decode('utf-8'))
    r.add_value('headers',response.headers)
    r.add_value('url',response.url)
    return r

  def getValuespaces(self, response):
    return ValuespaceItemLoader()

  def getLOM(self, response):
    lom = LomBaseItemloader()
    lom.add_value('general', self.getLOMGeneral(response).load_item())
    lom.add_value('lifecycle', self.getLOMLifecycle(response).load_item())
    lom.add_value('technical', self.getLOMTechnical(response).load_item())
    lom.add_value('educational', self.getLOMEducational(response).load_item())
    lom.add_value('rights', self.getLOMRights(response).load_item())
    lom.add_value('classification', self.getLOMClassification(response).load_item())
    return lom

  def getBase(self, response = None):
    base = BaseItemLoader()
    base.add_value('sourceId', self.getId(response))
    base.add_value('hash', self.getHash(response))
    return base

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
