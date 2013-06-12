# -*- coding: utf-8 -*-
## nodisplay
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field


## /nodisplay
class WikiItem(Item):
    title = Field()


class WikiAraignee(CrawlSpider):
    name = 'wiki2'
    allowed_domains = ['fr.wikipedia.org']
    start_urls = ['http://fr.wikipedia.org/wiki/Araignée']

    rules = [
        Rule(SgmlLinkExtractor(),
             callback='parse_page',
             ## nodisplay # Pour ne pas crawler plus de 10 liens
             follow=False,
             process_links=lambda links: links[:5],
             ## /nodisplay
             )]

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//title/text()').extract()
        return WikiItem(title=title)
