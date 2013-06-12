# -*- coding: utf-8 -*-
## nodisplay
import re
import urlparse

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


## /nodisplay
class QuiFaitQuoi(BaseSpider):
    name = 'amiando'
    allowed_domains = ['fr.amiando.com']
    start_urls = ['http://fr.amiando.com/scrapathon.html?page=961570']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
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
