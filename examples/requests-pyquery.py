## nodisplay
import json
## /nodisplay
from pyquery import PyQuery as pq
import requests

url = u"http://fr.wikipedia.org/wiki/Araignée"
resultat = requests.get(url)
document = pq(resultat.text).make_links_absolute(url)

# Sélectionner des éléments
json.dumps([a.attr.href for a in document("a").items()][:5], indent=2)
