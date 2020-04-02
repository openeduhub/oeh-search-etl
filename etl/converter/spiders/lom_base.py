from converter.items import *

class LomBase:

  def parse(self, response):
    self.pre_parse(response)
    main = self.getBase(response)
    main.add_value('lom', self.getLOM(response).load_item())
    return main.load_item()
    
  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.json['identifier'])
    base.add_value('hash', self.json['version'])
    base.add_value('fulltext', self.json['description'])
    return base

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
    return LomLifecycleItemloader()

  def getLOMEducational(self, response = None):
    return LomEducationalItemLoader()

  def getLOMRights(self, response = None):
    return LomRightsItemLoader()

  def getLOMClassification(self, response = None):
    return LomClassificationItemLoader()
