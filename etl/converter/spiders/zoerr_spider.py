from converter.spiders.lrmi_base import LrmiBase

class ZoerrSpider(LrmiBase):
  name = 'zoerr_spider'
  sitemap_urls = ['https://uni-tuebingen.oerbw.de/edu-sharing/eduservlet/sitemap']