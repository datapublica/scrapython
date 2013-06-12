# -*- coding: utf-8 -*-
## nodisplay
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule


## /nodisplay
class WikiAraignee(CrawlSpider):
    name = 'wiki1'
    # Domaines autorisés lors du parcours du site.
    # Les URLs sortant de ce domaines sont supprimées.
    allowed_domains = ['fr.wikipedia.org']
    start_urls = ['http://fr.wikipedia.org/wiki/Araignée']

    # Regles de suivi de lien
    rules = [
        Rule(SgmlLinkExtractor(),
             follow=False,
             ## nodisplay # Pour ne pas crawler plus de 10 liens
             process_links=lambda links: links[:5]
             ## /nodisplay
             )]
