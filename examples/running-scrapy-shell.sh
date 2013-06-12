scrapy shell xpath.html # Accepte un fichier ou une URL

[...]
# hxs est une variable contenant le fichier ou l'URL téléchargée)
# elle permet de faire des requêtes XPath sur ce contenu
>>> hxs.select("/html/body//li")
[<HtmlXPathSelector xpath='/html/body//li' data=u'<li class="c1">Premier […]
