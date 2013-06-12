# -*- coding: utf-8 -*-
## nodisplay
import re
import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.item import Item, Field


## /nodisplay
class People(Item):
    name = Field()


class QuiFaitQuoi(BaseSpider):
    name = 'amiando2'
    allowed_domains = ['fr.amiando.com']
    start_urls = ['http://fr.amiando.com/scrapathon.html?page=961570']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        ## nodisplay
        # Extract next link
        links = hxs.select("//span[@class='pagerBlock'][1]//a")
        links = [a.select("@onclick")[0].extract()
                 for a in links
                 if "Suivant" in a.extract()]
        if len(links) > 0:
            next_link = re.search("'(.*?)'", links[0])
            next_link = next_link.group(1)
            next_link = urlparse.urljoin(response.url, next_link)
            yield Request(next_link)
        ## /nodisplay
        for p in hxs.select("//ul[@class='eventPageGuestListContainer']/"
                            "li//strong/text()"):
            yield People(name=p.extract())
