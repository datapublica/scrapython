# créer un projet scrapy
# Un projet scrapy peut contenir plusieurs araignées
scrapy startproject mon_projet

cd mon_projet

# créer une araignée
scrapy genspider -t basic my_spider mon.domaine.com

# lancer l'araignée
scrapy runspider mon_projet/spiders/my_spider.py
